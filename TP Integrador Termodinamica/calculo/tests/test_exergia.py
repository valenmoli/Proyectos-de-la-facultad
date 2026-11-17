"""Chequeos del analisis exergetico (calculo/exergia.py).

Ejecutar desde la carpeta del proyecto:  python -m pytest calculo/tests -q
"""
import math

import psychrolib as ps
import pytest

from calculo import aire_humedo as ah
from calculo import combustion as cb
from calculo import edificio as ed
from calculo import estimacion as es
from calculo import exergia as xg
from calculo import supuestos

K = 273.15
C = supuestos.defaults()
P = C["P"]


# ---------------------------------------------------------------- estados que se analizan
@pytest.fixture(scope="module")
def estados():
    return xg.estados_de_analisis(C)


@pytest.fixture(scope="module")
def invierno():
    Ti, Wi = ed.estado_exterior_invierno(C)
    return xg.analisis(C, Ti, Wi, {g: 0.0 for g in C["Z"]}, 0.0, f_dias_activos=False)


@pytest.fixture(scope="module")
def sens():
    return xg.sensibilidad_T0(C)


@pytest.fixture(scope="module")
def todos(estados, invierno, sens):
    """Todos los resultados de analisis() que se recorren en los chequeos generales."""
    out = [("verano pico", estados["verano_pico"]["resultado"]),
           ("max recalentamiento", estados["max_recalentamiento"]["resultado"]),
           ("invierno de diseno", invierno)]
    out += [(f"verano pico, T0 = {s['T0']}", s["resultado"]) for s in sens]
    return out


# ---------------------------------------------------------------- exergia del aire humedo
ESTADOS_MUERTOS = [(34.0, 0.0163), (18.9, 0.0117), (2.0, 0.0035), (17.5, 0.009)]


@pytest.mark.parametrize("T0,W0", ESTADOS_MUERTOS)
def test_exergia_del_aire_en_el_estado_muerto_es_cero(T0, W0):
    assert xg.ex_aire(T0, W0, T0, W0) == pytest.approx(0.0, abs=1e-12)


@pytest.mark.parametrize("T0,W0", ESTADOS_MUERTOS)
def test_exergia_del_aire_no_negativa(T0, W0):
    for T in range(-5, 46, 3):
        for W in (0.0005, 0.002, 0.005, 0.0085, 0.012, 0.0163, 0.025, 0.03):
            assert xg.ex_aire(T, W, T0, W0) >= -1e-12, (T, W, T0, W0)


def _ex_aire_por_potenciales_quimicos(T, W, T0, W0):
    """Forma independiente: suma sobre especies de m_i [(h_i - h_i0) - T0 (s_i - s_i0)] con presiones parciales."""
    t, t0 = T + K, T0 + K
    wt, wt0 = W / xg.MV_MA, W0 / xg.MV_MA
    pa, pv = 101325.0 / (1 + wt), 101325.0 * wt / (1 + wt)
    pa0, pv0 = 101325.0 / (1 + wt0), 101325.0 * wt0 / (1 + wt0)
    cp = ah.CP_A + W * ah.CP_V
    return (cp * ((t - t0) - t0 * math.log(t / t0)) + t0 * xg.R_A * math.log(pa / pa0)
            + W * t0 * xg.R_V * math.log(pv / pv0))


@pytest.mark.parametrize("T,W,T0,W0", [(12, 0.008, 34, 0.0163), (40, 0.02, 17.5, 0.009), (24, 0.0112, 34, 0.0163),
                                       (2, 0.0035, 2, 0.0035), (13, 0.0085, 18.9, 0.0117)])
def test_exergia_del_aire_coincide_con_la_forma_por_especies(T, W, T0, W0):
    assert xg.ex_aire(T, W, T0, W0) == pytest.approx(_ex_aire_por_potenciales_quimicos(T, W, T0, W0), rel=1e-10, abs=1e-12)


def test_exergia_del_liquido_es_coherente_con_la_del_aire():
    """En la saturacion a T0, d ex_aire / dW (por kg de vapor agregado) = exergia quimica del agua liquida a T0."""
    T0, W0 = 34.0, 0.0163
    Ws = ps.GetSatHumRatio(T0, 101325.0)
    d = 1e-6
    deriv = (xg.ex_aire(T0, Ws + d, T0, W0) - xg.ex_aire(T0, Ws - d, T0, W0)) / (2 * d)
    quim = xg.R_V * (T0 + K) * math.log(ps.GetSatVapPres(T0) / ps.GetVapPresFromHumRatio(W0, 101325.0))
    assert deriv == pytest.approx(quim, rel=1e-6)
    # el liquido a T0 y P0 tiene ademas el termino v (P0 - p_sat), de 0,1 kJ/kg
    assert xg.ex_agua_abierta(T0, T0, W0) == pytest.approx(quim + 0.0961, abs=0.01)
    assert xg.ex_agua_abierta(T0, T0, W0) > 90.0           # ~102 kJ/kg: no es despreciable frente a los ~1 kJ/kg termicos


def test_exergia_termica_del_agua():
    assert xg.ex_agua_termica(20.0, 20.0) == pytest.approx(0.0, abs=1e-12)
    for T in (5.0, 12.0, 60.0, 80.0):
        assert xg.ex_agua_termica(T, 20.0) > 0.0


# ---------------------------------------------------------------- exergia quimica del gas natural
@pytest.mark.parametrize("T0", [2.0, 18.9, 25.0, 34.0])
def test_exergia_quimica_del_gas_natural_cercana_al_PCI(T0):
    pc = cb.poder_calorifico(P)
    ex = xg.ex_quimica_gas_natural(P, T0)
    assert 0.95 < ex / pc["PCI_kJ_kmol"] < 1.10
    assert ex / pc["PCI_kJ_kmol"] == pytest.approx(1.037, abs=0.005)        # cociente tipico del gas natural


def test_exergia_quimica_del_metano_puro():
    Pm = dict(P, gas_CH4=1.0, gas_C2H6=0.0, gas_C3H8=0.0, gas_N2=0.0, gas_CO2=0.0)
    pc = cb.poder_calorifico(Pm)
    assert xg.ex_quimica_gas_natural(Pm, 25.0) == pytest.approx(831650.0)           # sin termino de mezcla
    assert xg.ex_quimica_gas_natural(Pm, 25.0) / pc["PCI_kJ_kmol"] == pytest.approx(1.0366, abs=1e-3)


def test_las_exergias_quimicas_estan_declaradas_como_recordadas(estados):
    assert "recordado" in xg.EX_QUIM_ESTADO
    for e in estados.values():
        assert "recordado" in e["resultado"]["caldera"]["estado_ex_quimicas"]


# ---------------------------------------------------------------- estados y condiciones
def test_estados_de_analisis(estados):
    ver, mr = estados["verano_pico"], estados["max_recalentamiento"]
    Tv, Wv = ed.estado_exterior_verano(C)
    assert ver["condiciones"]["T_out"] == Tv and ver["condiciones"]["W_out"] == Wv
    # estado muerto = estado exterior de cada estado
    for e in (ver, mr):
        est = e["resultado"]["estado"]
        assert est["T0"] == e["condiciones"]["T_out"] and est["W0"] == e["condiciones"]["W_out"]
        assert est["P0"] == 101325.0
    # el verano pico reproduce las magnitudes de estimacion.diseno
    d = es.diseno(C)
    assert ver["resultado"]["enfriadora"]["Q_L"] == pytest.approx(d["Q_L"], rel=1e-12)
    assert ver["resultado"]["enfriadora"]["W_comp"] == pytest.approx(d["planta"]["W_comp"], rel=1e-12)
    assert ver["resultado"]["caldera"]["Q_agua"] == pytest.approx(d["Q_recal_verano"] + d["acs"]["kW"], rel=1e-9)
    # el maximo recalentamiento es un estado (mes x mitad) del ano y recalienta mas que el verano pico
    T_m = dict(zip(C["clima"]["meses"], C["clima"]["T"]))[mr["condiciones"]["mes"]]
    assert mr["condiciones"]["T_out"] == pytest.approx(T_m + (P["rango_diario"] / 2 if mr["condiciones"]["mitad"] == "dia" else -P["rango_diario"] / 2))
    assert mr["condiciones"]["Q_recal_kW"] > d["Q_recal_verano"]


def test_el_aire_exterior_no_aporta_exergia_si_T0_es_el_estado_exterior(estados):
    for e in estados.values():
        for z in e["resultado"]["zonas"].values():
            assert z["x_oa"] == pytest.approx(0.0, abs=1e-9)


def test_la_potencia_electrica_de_entrada_es_la_del_modelo(estados):
    d = es.diseno(C)
    g = estados["verano_pico"]["resultado"]["global"]
    p = d["planta"]
    P_vent = sum(v["P_vent_kW"] for v in d["caudales"].values())
    assert g["X_elec"] == pytest.approx(p["W_comp"] + p["W_cond"] + p["W_bomba"] + P_vent, rel=1e-12)


# ---------------------------------------------------------------- segunda ley y cierre
def test_destrucciones_no_negativas(todos):
    for nombre, r in todos:
        for f in r["tabla"]:
            assert f["X_dest"] >= -1e-9, (nombre, f["clave"], f["X_dest"])
        for g, z in r["zonas"].items():
            for k, (F, Pr, L, D) in z["filas"].items():
                assert D >= -1e-9, (nombre, g, k, D)
        for k, v in r["perdidas"].items():
            assert v >= -1e-9, (nombre, k, v)


def test_cierre_del_balance_global(todos):
    for nombre, r in todos:
        g = r["global"]
        assert g["cierre_rel"] < 1e-6, (nombre, g["cierre_rel"])
        assert g["X_in"] == pytest.approx(g["X_elec"] + g["X_comb"])
        assert g["X_in"] == pytest.approx(g["P_total"] + g["L_total"] + g["D_total"], rel=1e-9)
        # cada equipo cumple F = P + L + D
        for f in r["tabla"]:
            assert f["X_in"] == pytest.approx(f["X_util"] + f["X_perdida"] + f["X_dest"], rel=1e-9, abs=1e-9), (nombre, f["clave"])
        if r["enfriadora"]["activa"]:
            assert r["verificaciones"]["cierre_enfriadora_rel"] < 1e-6


def test_participaciones_y_grupos_suman_la_destruccion_total(todos):
    for nombre, r in todos:
        assert sum(f["particip_dest"] for f in r["tabla"]) == pytest.approx(1.0, rel=1e-9)
        assert sum(r["destruccion_grupos"].values()) == pytest.approx(r["global"]["D_total"], rel=1e-9)


def test_eficiencias_entre_0_y_1(todos):
    for nombre, r in todos:
        for f in r["tabla"]:
            if f["eta_ex"] is not None:
                assert 0.0 < f["eta_ex"] < 1.0, (nombre, f["clave"], f["eta_ex"])
        if r["global"]["eta_global"] is not None:
            assert 0.0 < r["global"]["eta_global"] < 1.0
        assert 0.0 < r["caldera"]["eta_ex"] < 1.0
        if r["enfriadora"]["activa"]:
            assert 0.0 < r["enfriadora"]["eta_planta"] < r["enfriadora"]["eta_compresor_grupo"] < 1.0
        if r["acs"]["eta_cadena"] is not None:
            assert 0.0 < r["acs"]["eta_cadena"] < 1.0


def test_eficiencia_del_ventilador_es_su_rendimiento(estados):
    for e in estados.values():
        fila = next(f for f in e["resultado"]["tabla"] if f["clave"] == "ventilador")
        assert fila["eta_ex"] == pytest.approx(P["eta_vent"], rel=1e-12)


def test_motor_y_compresor(estados):
    r = estados["verano_pico"]["resultado"]
    t = {f["clave"]: f for f in r["tabla"]}
    W = r["enfriadora"]["W_comp"]
    assert t["motor"]["X_dest"] == pytest.approx((1 - P["eta_motor"]) * W, rel=1e-12)
    assert t["motor"]["eta_ex"] == pytest.approx(P["eta_motor"], rel=1e-12)
    # Gouy-Stodola: D = T0 m (s2 - s1) > 0 y el ciclo respeta la primera ley
    assert t["compresor"]["X_dest"] == pytest.approx(r["enfriadora"]["D_gs_compresor"], rel=1e-12)
    assert t["valvula"]["X_dest"] == pytest.approx(r["enfriadora"]["D_gs_valvula"], rel=1e-12)
    s1, s2, s3, s4 = r["enfriadora"]["s"]
    assert s2 > s1 and s4 > s3


# ---------------------------------------------------------------- enfriadora: COP y eficiencia exergetica
def test_eficiencia_exergetica_de_la_enfriadora_y_el_COP(estados):
    """eta_ex del compresor = X_frio / W_el = COP (T0/T_cw - 1) = COP / COP_reversible(T_cw, T0).

    T_cw es la temperatura media logaritmica del agua helada (con ella, Q_L (T0/T_cw - 1) es exactamente la variacion de
    exergia de la corriente de agua). COP_reversible(T_cw, T0) = T_cw / (T0 - T_cw) no es el COP de Carnot del ciclo
    T_ev / (T_cond - T_ev) que informa refrigeracion.ciclo: la razon entre ambos es la de las dos eficiencias,
        eta_ex = (COP / COP_Carnot_ciclo) * (COP_Carnot_ciclo / COP_reversible),
    el segundo factor mide cuanto del salto termico util se pierde en las transferencias de calor externas del evaporador
    (T_ev < T_cw) y del condensador (T_cond > T0).
    """
    for e in estados.values():
        r = e["resultado"]
        en = r["enfriadora"]
        T0 = r["estado"]["T0"]
        assert en["X_frio"] == pytest.approx(en["Q_L"] * ((T0 + K) / en["T_cw"] - 1.0), rel=1e-12)
        assert en["eta_compresor_grupo"] == pytest.approx(en["COP"] / en["cop_reversible_agua"], rel=1e-12)
        assert en["eta_compresor_grupo"] == pytest.approx(en["COP"] * en["T0_sobre_Tcw_menos_1"], rel=1e-12)
        eta_II_ciclo = en["COP"] / en["cop_carnot_ciclo"]                                           # COP electrico / COP de Carnot del ciclo
        assert en["eta_compresor_grupo"] == pytest.approx(eta_II_ciclo * en["cop_carnot_ciclo"] / en["cop_reversible_agua"], rel=1e-12)
        # el COP de Carnot de refrigeracion.ciclo es el reversible entre T_ev y T_cond
        assert xg.cop_reversible(P["T_ev"] + K, en["T_cond"] + K) == pytest.approx(en["cop_carnot_ciclo"], rel=1e-12)
        # regla de suma: la exergia electrica del compresor se reparte en frio + perdida + destrucciones de la enfriadora
        t = {f["clave"]: f for f in r["tabla"]}
        D_enf = sum(t[k]["X_dest"] for k in ("motor", "compresor", "condensador", "valvula", "evaporador"))
        assert en["W_comp"] == pytest.approx(en["X_frio"] + en["L_aire_condensador"] + D_enf, rel=1e-9)
        assert 1.0 == pytest.approx(en["eta_compresor_grupo"] + (en["L_aire_condensador"] + D_enf) / en["W_comp"], rel=1e-9)


def test_el_frio_tiene_menos_exergia_cuanto_menor_es_T0(sens):
    etas = [s["eta_enfriadora"] for s in sens]          # T0 = 34, 25, 17,5
    assert etas[0] > etas[1] > etas[2] > 0.0


# ---------------------------------------------------------------- caldera
def test_la_destruccion_de_la_caldera_es_la_mayor_parte_de_la_exergia_del_combustible(todos):
    for nombre, r in todos:
        c = r["caldera"]
        assert c["D_total"] / c["X_comb"] > 0.5, (nombre, c["D_total"] / c["X_comb"])
        assert c["D_total"] == pytest.approx(c["D_combustion"] + c["D_transferencia"], rel=1e-12)
        assert c["D_combustion"] > 0.0 and c["D_transferencia"] > 0.0
        assert c["T_llama"] == pytest.approx(1848.0, abs=1.0)
        # la caldera es un 80/60: su exergia util es solo una fraccion chica del calor util
        assert c["X_calor"] < 0.25 * c["Q_util"]


def test_caldera_balance_de_energia_y_exergia(estados):
    r = estados["max_recalentamiento"]["resultado"]
    c = r["caldera"]
    assert c["E_PCI"] == pytest.approx(c["Q_util"] / cb.caldera(P)["eta_PCI"], rel=1e-12)
    assert c["X_comb"] / c["E_PCI"] == pytest.approx(c["ex_comb_sobre_PCI"], rel=1e-9)
    # exergia del calor al agua 80/60: Q (1 - T0 ln(Ti/Tr)/(Ti - Tr))
    Ti, Tr, T0 = 80.0 + K, 60.0 + K, r["estado"]["T0"] + K
    assert c["X_calor"] == pytest.approx(c["Q_util"] * (1.0 - T0 * math.log(Ti / Tr) / (Ti - Tr)), rel=1e-9)
    fila = next(f for f in r["tabla"] if f["clave"] == "caldera")
    assert fila["X_in"] == pytest.approx(c["X_comb"], rel=1e-12)
    assert c["eta_ex"] == pytest.approx(c["X_calor"] / c["X_comb"], rel=1e-12)


def test_acs_se_trata_aparte(estados):
    r = estados["verano_pico"]["resultado"]
    a = r["acs"]
    assert a["Q_kW"] == pytest.approx(es.acs(C)["kW"], rel=1e-12)
    assert a["Q_util_kW"] == pytest.approx(a["Q_kW"] / P["f_perd_acs"], rel=1e-12)
    assert a["D_intercambiador"] > 0.0 and a["D_caldera_asignada"] > 0.0 and a["P"] > 0.0
    # cadena: exergia asignada del combustible = producto + perdidas + destrucciones
    assert a["X_comb_asignada"] == pytest.approx(a["P"] + a["L"] + a["L_caldera_asignada"] + a["D_intercambiador"] + a["D_caldera_asignada"], rel=1e-9)


# ---------------------------------------------------------------- invierno: humidificador y calefaccion
def test_invierno_humidificador_y_calefaccion(invierno):
    t = {f["clave"]: f for f in invierno["tabla"]}
    assert invierno["enfriadora"]["activa"] is False
    assert invierno["caldera"]["Q_vapor"] > 0.0
    assert t["humidificador"]["X_in"] > 0.0 and t["humidificador"]["X_dest"] > 0.0
    d = es.diseno(C)
    assert invierno["caldera"]["Q_util"] == pytest.approx(d["Q_caldera_invierno"] + d["acs"]["kW"], rel=1e-9)
    assert invierno["global"]["cierre_rel"] < 1e-6


# ---------------------------------------------------------------- Gouy-Stodola de la serpentina, con entropias de gas ideal
def test_destruccion_de_la_serpentina_igual_a_T0_por_la_generacion_de_entropia(estados):
    """D = T0 S_gen con la entropia del aire humedo como mezcla de gases ideales (calores especificos constantes),
    el condensado con cp constante y la referencia liquido-vapor en equilibrio a T0 (p_sat de psychrolib)."""
    r = estados["verano_pico"]["resultado"]
    T0 = r["estado"]["T0"]
    t0 = T0 + K
    hfg0 = 2501.0 + (ah.CP_V - ah.CP_W) * T0
    sv_ref = hfg0 / t0 - xg.R_V * math.log(101325.0 / ps.GetSatVapPres(T0))      # s_v(T0, P0) con s_liq(T0) = 0

    def s_aire(T, W):
        t = T + K
        wt = W / xg.MV_MA
        pa, pv = 101325.0 / (1 + wt), 101325.0 * wt / (1 + wt)
        return (ah.CP_A * math.log(t / t0) - xg.R_A * math.log(pa / 101325.0)
                + W * (ah.CP_V * math.log(t / t0) - xg.R_V * math.log(pv / 101325.0) + sv_ref))

    caud = ed.caudales(C)
    S = 0.0
    for g, z in r["zonas"].items():
        m = caud[g]["m_sup"]
        m_cw = z["Q_coil"] / (ah.CP_W * P["dT_aguahelada"])
        S += (m * (s_aire(z["T_c"], z["W_c"]) - s_aire(z["T_mix"], z["W_mix"]))
              + z["m_cond"] * ah.CP_W * math.log((z["T_c"] + K) / t0)
              + m_cw * ah.CP_W * math.log((7.0 + P["dT_aguahelada"] + K) / (7.0 + K)))
    D = next(f for f in r["tabla"] if f["clave"] == "serpentina")["X_dest"]
    assert t0 * S == pytest.approx(D, rel=0.005)


# ---------------------------------------------------------------- sensibilidad al estado muerto
def test_sensibilidad_al_estado_muerto(sens):
    assert [s["T0"] for s in sens] == [34.0, 25.0, 17.5]
    for s in sens:
        assert s["cierre_rel"] < 1e-6
        assert s["resultado"]["estado"]["T0"] == s["T0"]
        assert s["resultado"]["estado"]["T_out"] == 34.0        # el estado exterior no cambia: solo la referencia
    # la caldera mejora cuando T0 baja (el agua a 80/60 C tiene mas exergia respecto de un ambiente mas frio);
    # el frio empeora (el agua helada esta mas cerca de T0)
    assert sens[0]["eta_caldera"] < sens[1]["eta_caldera"] < sens[2]["eta_caldera"]
    assert sens[0]["eta_enfriadora"] > sens[1]["eta_enfriadora"] > sens[2]["eta_enfriadora"]
    # la destruccion total depende poco de T0 (D = T0 S_gen); el equipo que mas destruye no cambia
    D = [s["D_total"] for s in sens]
    assert max(D) / min(D) < 1.10
    mayor = [max(s["D_por_fila"], key=s["D_por_fila"].get) for s in sens]
    assert len(set(mayor)) == 1


def test_el_producto_del_aire_puede_dejar_de_estar_definido(sens):
    # con T0 = 17,5 C el aire impulsado (12 a 17 C) esta por debajo de T0 pero el exterior (34 C) esta por encima:
    # el aumento neto de exergia del aire es negativo y la eficiencia global no se define
    assert sens[2]["resultado"]["global"]["producto_aire_bien_definido"] is False
    assert sens[2]["eta_global"] is None
    assert sens[0]["eta_global"] is not None


def test_tabla_texto(estados):
    txt = xg.tabla_texto(estados["verano_pico"]["resultado"])
    assert "Caldera" in txt and "Compresor" in txt and "Estado muerto" in txt
