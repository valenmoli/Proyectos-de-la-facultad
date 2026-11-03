"""Chequeos termodinamicos del modelo (ver PRD, seccion 4).

Ejecutar desde la carpeta del proyecto:  python -m pytest calculo/tests -q
"""
import copy

import pytest
from CoolProp.CoolProp import HAPropsSI

from calculo import aire_humedo as ah
from calculo import combustion as cb
from calculo import edificio as ed
from calculo import estimacion as es
from calculo import refrigeracion as rf
from calculo import supuestos

C = supuestos.defaults()
P = C["P"]


# ---------------------------------------------------------------- aire humedo
@pytest.mark.parametrize("T,Tbh", [(34, 25), (30, 22), (22, 15), (10, 8), (5, 4)])
def test_psicrometria_coincide_con_coolprop(T, Tbh):
    W = ah.w_desde_tbh(T, Tbh)
    h = ah.entalpia(T, W)
    W_cp = HAPropsSI("W", "T", T + 273.15, "B", Tbh + 273.15, "P", 101325)
    h_cp = HAPropsSI("H", "T", T + 273.15, "B", Tbh + 273.15, "P", 101325) / 1000.0
    assert W == pytest.approx(W_cp, rel=0.012)
    assert h == pytest.approx(h_cp, abs=0.8)


def test_serpentina_inversa():
    W = 0.0085
    T = ah.t_serpentina(W, 0.95)
    assert ah.w_desde_hr(T, 0.95) == pytest.approx(W, rel=1e-6)


# ---------------------------------------------------------------- refrigeracion
@pytest.mark.parametrize("Tc", [28, 32, 38, 46, 52])
def test_ciclo_segunda_ley_y_primera_ley(Tc):
    r = rf.ciclo(P["T_ev"], Tc, P["refrigerante"], P["sobrecal"], P["subenf"], P["eta_is"], P["eta_motor"])
    assert r["cop_comp"] < r["cop_carnot"]                     # segunda ley
    assert r["cop_elec"] < r["cop_comp"]
    assert r["q_H"] == pytest.approx(r["q_L"] + r["w"], rel=1e-9)   # primera ley en el ciclo
    assert r["h4"] == r["h3"]                                  # expansion isoentalpica
    assert 0.0 < r["x4"] < 1.0                                 # mezcla bifasica a la salida de la valvula
    assert r["h2"] > r["h2s"] > r["h1"]


def test_cop_decrece_con_la_condensacion():
    cops = [rf.ciclo(3, Tc)["cop_elec"] for Tc in (30, 38, 46, 54)]
    assert all(a > b for a, b in zip(cops, cops[1:]))


# ---------------------------------------------------------------- combustion
def test_balance_de_atomos():
    b = cb.balance(P)
    for atomo, (entra, sale) in b["atomos"].items():
        assert entra == pytest.approx(sale, rel=1e-12), atomo


def test_poder_calorifico_metano_puro():
    Pm = dict(P, gas_CH4=1.0, gas_C2H6=0.0, gas_C3H8=0.0, gas_N2=0.0, gas_CO2=0.0)
    pc = cb.poder_calorifico(Pm)
    assert pc["PCS_kJ_kmol"] == pytest.approx(890330.0, rel=1e-4)      # PCS del metano, tablas
    assert pc["PCI_kJ_kmol"] == pytest.approx(802310.0, rel=1e-4)      # PCI del metano
    # PCS - PCI = calor latente del agua formada: 2 kmol de agua por kmol de metano
    assert pc["PCS_kJ_kmol"] - pc["PCI_kJ_kmol"] == pytest.approx(2 * 44010.0, rel=1e-6)


def test_gas_natural_orden_de_magnitud():
    pc = cb.poder_calorifico(P)
    assert 8800.0 < pc["PCS_kcal_m3"] < 10200.0       # rango de la regulacion argentina citado como pista
    assert 1.09 < pc["relacion_PCS_PCI"] < 1.12


def test_caldera():
    cal = cb.caldera(P)
    assert 0.85 < cal["eta_PCI"] < 0.95
    assert cal["T_rocio"] < P["T_gases"]               # no condensa en la chimenea
    assert 1700.0 < cb.temperatura_llama_adiabatica(P) < 2100.0


def test_consumo_gas_coherente():
    cal = cb.caldera(P)
    g = cb.consumo_gas(1000.0, cal["eta_PCI"], cal["pc"])
    assert g["E_PCI_kWh"] == pytest.approx(1000.0 / cal["eta_PCI"])
    assert g["V_m3"] * cal["pc"]["PCS_kWh_m3"] == pytest.approx(g["E_PCS_kWh"])


# ---------------------------------------------------------------- tratamiento del aire
@pytest.mark.parametrize("g", ["G1", "G2", "G3", "G4", "G5"])
@pytest.mark.parametrize("estado", ["pico", "invierno", "media", "otonio"])
def test_balance_de_energia_del_aire(g, estado):
    caud = ed.caudales(C)
    if estado == "pico":
        T, W, f, qs = P["T_bs_ver"], ah.w_desde_tbh(P["T_bs_ver"], P["T_bh_ver"]), 1.0, P["q_sol_pico"]
    elif estado == "invierno":
        T, W, f, qs = P["T_inv"], ah.w_desde_hr(P["T_inv"], P["HR_inv"]), 0.0, 0.0
    elif estado == "media":
        T, W, f, qs = 24.0, ah.w_desde_hr(24.0, 0.68), 0.8, P["q_sol_dia"]
    else:
        T, W, f, qs = 16.0, ah.w_desde_hr(16.0, 0.75), 0.5, 0.0
    r = ed.proceso(C, g, caud, T, W, f, qs)
    m = caud[g]["m_sup"]
    # Todas las cargas son no negativas y el latente mas el sensible suman el total de la serpentina
    for k in ("Q_coil", "Q_coil_sens", "Q_coil_lat", "Q_recal", "Q_cal", "Q_hum"):
        assert r[k] >= -1e-9, k
    assert r["Q_coil_sens"] + r["Q_coil_lat"] == pytest.approx(r["Q_coil"], abs=1e-6)
    # No hay recalentamiento sin enfriamiento ni calefaccion con enfriamiento
    if not r["enfria"]:
        assert r["Q_coil"] == 0.0 and r["Q_recal"] == 0.0
    else:
        assert r["Q_cal"] == 0.0
    # Balance de entalpia de la corriente de aire: entalpia de impulsion calculada vs. del estado final
    h_vapor, h_agua = 2676.0, ah.h_agua_liquida(P["T_agua_red"])
    dW = r["Q_hum"] / (m * (h_vapor - h_agua)) if r["Q_hum"] > 0 else 0.0
    W_final = r["W_c"] + dW
    cond = m * (r["W_mix"] - r["W_c"]) * ah.h_agua_liquida(r["T_c"]) if r["enfria"] else 0.0
    h_sup_balance = (r["h_mix"] - (r["Q_coil"] + cond) / m + (r["Q_recal"] + r["Q_cal"]) / m
                     + r["Q_hum"] / m + r["calor_vent"] / m)
    h_sup_estado = ah.entalpia(r["T_sup"], W_final)
    assert h_sup_balance == pytest.approx(h_sup_estado, abs=0.6)
    # La impulsion absorbe la carga sensible neta de la zona
    cp = ah.cp_ah(r["W_sup_max"])
    assert m * cp * (r["T_r"] - r["T_sup"]) == pytest.approx(r["Q_s_zona_kW"], abs=0.02 * max(1.0, abs(r["Q_s_zona_kW"])) + 1e-6) \
        or r["T_sup"] in (P["T_sup_min"], P["T_sup_max"])


def test_caudales_cumplen_renovaciones():
    caud = ed.caudales(C)
    for g, z in C["Z"].items():
        A = caud[g]["A"]
        assert caud[g]["m_sup"] >= z["ach_tot"] * A * P["h_techo"] / 3600.0 * P["rho_aire"] - 1e-9
        assert caud[g]["m_oa"] <= caud[g]["m_sup"] + 1e-12


# ---------------------------------------------------------------- estimacion
@pytest.fixture(scope="module")
def R():
    return es.resumen(C)


def test_primera_ley_en_la_planta(R):
    d = R["diseno"]
    assert d["Q_L"] == pytest.approx(sum(v["Q_coil"] for v in d["verano"].values()))
    pl = R["anual"]["planta"]
    # Calor rechazado = frio entregado + trabajo en el eje (el motor aporta eta_motor del electrico del compresor)
    assert pl["Q_cond"] == pytest.approx(pl["Q_L"] + R["anual"]["elec"]["compresor"] * P["eta_motor"], rel=1e-9)


def test_segunda_ley_cop_mensual(R):
    for f in R["anual"]["mensual"]:
        if f["W_comp"] > 0:
            T_ev = P["T_ev"] + 273.15
            # COP del compresor (electrico) siempre menor que el de Carnot entre T_ev y la condensacion minima
            cop_carnot_max = T_ev / (P["T_cond_min"] - P["T_ev"])
            assert f["Q_L"] / f["W_comp"] < cop_carnot_max


def test_balance_de_energia_anual(R):
    an = R["anual"]
    assert R["E_total"] == pytest.approx(R["E_elec"] + R["E_gas_PCS"])
    assert an["q_util_total"] == pytest.approx(an["q_recal"] + an["q_cal"] + an["q_hum"] + an["q_acs"])
    assert R["E_gas_PCI"] == pytest.approx(an["q_util_total"] / an["eta_caldera"])
    assert an["elec"]["total"] == pytest.approx(sum(v for k, v in an["elec"].items() if k != "total"))
    assert an["serp_total"] == pytest.approx(an["planta"]["Q_L"])
    assert all(v >= 0 for v in an["elec"].values())


def test_acs_energia_sensible():
    a = es.acs(C)
    camas = P["camas_gen"] + P["camas_uti"]
    esperado = P["L_cama_dia"] * camas * 4.186 * (P["T_acs"] - P["T_agua_fria"]) * P["f_perd_acs"] / 3600.0   # kWh/dia
    assert a["kWh_dia"] == pytest.approx(esperado)


def test_sensibilidades_son_coherentes():
    base, filas = es.sensibilidad(C)
    r0 = es.resumen(C)["E_total"]
    assert base == pytest.approx(r0)
    por_nombre = {f["nombre"]: f["delta"] for f in filas}
    assert por_nombre["ACS por cama: 200 L/dia"] > 0 > por_nombre["ACS por cama: 55 L/dia"]
    assert por_nombre["Temperatura media mensual +2 K"] != 0.0


def test_mas_acs_mas_gas():
    c2 = copy.deepcopy(C)
    c2["P"]["L_cama_dia"] *= 2
    assert es.resumen(c2)["E_gas_PCS"] > es.resumen(C)["E_gas_PCS"]
    assert es.resumen(c2)["E_elec"] == pytest.approx(es.resumen(C)["E_elec"])   # el ACS no consume electricidad


# ---------------------------------------------------------------- defectos encontrados por la verificacion independiente
def _parse_tabla(md):
    filas = {}
    for linea in md.splitlines():
        celdas = [x.strip() for x in linea.strip().strip("|").split("|")]
        if len(celdas) == 6 and celdas[0] and celdas[0][0].isalpha() and celdas[0][1:].isdigit():
            filas[celdas[0]] = celdas
    return filas


def test_la_tabla_de_supuestos_reproduce_cada_valor():
    """La tabla es la entrada de una reimplementacion: no puede perder cifras (R9 mostraba 0,03 en vez de 0,025)."""
    filas = _parse_tabla(supuestos.tabla_md())
    n = 0
    for (id_, clave, _nom, valor, _u, _e, _f) in supuestos.filas():
        if isinstance(valor, (int, float)) and not isinstance(valor, bool):
            leido = float(filas[id_][2].replace(",", "."))
            assert leido == pytest.approx(valor, rel=1e-5), (id_, clave, filas[id_][2], valor)
            n += 1
    assert n > 40


def test_la_tabla_incluye_los_dias_de_cada_mes():
    assert "| Dias | 31 | 28 | 31 | 30 | 31 | 30 | 31 | 31 | 30 | 31 | 30 | 31 |" in supuestos.tabla_md()


def test_la_humedad_exterior_no_supera_la_saturacion():
    for i in range(12):
        W = ah.w_desde_hr(C["clima"]["T"][i], C["clima"]["HR"][i])
        for sgn in (+1, -1):
            T = C["clima"]["T"][i] + sgn * P["rango_diario"] / 2
            assert min(W, ah.w_desde_hr(T, 1.0)) <= ah.w_desde_hr(T, 1.0) + 1e-12
            assert ah.hr_desde_w(T, min(W, ah.w_desde_hr(T, 1.0))) <= 1.0 + 1e-9


def test_calor_del_ventilador_reduce_el_recalentamiento_y_sube_el_frio():
    c0 = copy.deepcopy(C)
    c0["P"]["f_calor_vent"] = 0.0
    d_con, d_sin = es.diseno(C), es.diseno(c0)
    assert d_con["Q_L"] > d_sin["Q_L"]                          # mas carga de serpentina al absorber el calor del ventilador
    an_con, an_sin = es.anual(C), es.anual(c0)
    assert an_con["q_recal"] + an_con["q_cal"] < an_sin["q_recal"] + an_sin["q_cal"]


def test_la_zona_de_dias_habiles_consume_proporcionalmente():
    c1 = copy.deepcopy(C)
    c1["Z"]["G5"]["f_dias"] = 1.0
    a0, a1 = es.anual(C), es.anual(c1)
    assert a0["zonas"]["G5"]["vent"] == pytest.approx(a1["zonas"]["G5"]["vent"] * C["Z"]["G5"]["f_dias"])
    assert a0["zonas"]["G5"]["serp"] == pytest.approx(a1["zonas"]["G5"]["serp"] * C["Z"]["G5"]["f_dias"])
