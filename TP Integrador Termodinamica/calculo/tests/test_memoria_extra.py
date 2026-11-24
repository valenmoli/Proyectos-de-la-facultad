"""Chequeos de las tablas y valores nuevos de la memoria de calculo (memoria_extra.py).

Fijan las cifras clave (cierres de balances, caso resuelto de G1, ciclo, combustion, calor rechazado anual), comprueban que las
cuentas impresas se reproducen a mano con los numeros impresos y que la memoria no usa las marcas viejas ni nombra archivos.
"""
import os
import re

import pytest

from calculo import combustion as cb
from calculo import construir_borrador as cbm
from calculo import edificio as ed
from calculo import equipos as eq
from calculo import estimacion as es
from calculo import memoria_extra as me
from calculo import mejoras as mj
from calculo import supuestos

C = supuestos.defaults()
P = C["P"]
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLANTILLA = os.path.join(RAIZ, "informe", "memoria_calculo.plantilla.md")


def num(s):
    """'1.987,2' -> 1987.2; acepta el signo menos tipografico."""
    return float(s.replace("−", "-").replace(".", "").replace(",", "."))


@pytest.fixture(scope="module")
def v():
    return me.valores_memoria(C, {}, {})


@pytest.fixture(scope="module")
def t():
    V, T = cbm.valores()
    return me.tablas_memoria(C, V, T), V, T


# ------------------------------------------------------------------ punto de diseno y caso resuelto de G1
def test_el_punto_de_diseno_declarado_es_el_que_usa_el_modelo():
    d = es.diseno(C)
    caud = ed.caudales(C)
    Tv, Wv = ed.estado_exterior_verano(C)
    for g in C["Z"]:
        r = ed.proceso(C, g, caud, Tv, Wv, me.F_ACT_DISENO, P["q_sol_pico"])
        assert r["Q_coil"] == pytest.approx(d["verano"][g]["Q_coil"], rel=1e-12)
        assert r["Q_recal"] == pytest.approx(d["verano"][g]["Q_recal"], rel=1e-12)
    assert me.F_ACT_DISENO == 1.0 and P["q_sol_pico"] == 20.0
    # el 0,8 de la tabla de actividad es del calculo anual (mitad diurna), no del diseno
    assert C["Z"]["G1"]["f_dia"] == 0.8 and C["Z"]["G1"]["f_env"] == 0.0 and P["q_sol_dia"] == 8.0


def test_caso_g1_cierra_con_el_modelo():
    g = me.caso_g1(C)
    d = es.diseno(C)["verano"]["G1"]
    assert g["Q_serp"] == pytest.approx(d["Q_coil"], rel=1e-12) and g["Q_rec"] == pytest.approx(d["Q_recal"], rel=1e-12)
    assert g["Q_sens"] + g["Q_lat"] == pytest.approx(g["Q_serp"], rel=1e-12)
    assert g["Qs"] == pytest.approx(g["r"]["Q_s_zona_kW"], rel=1e-12)           # f_env = 0: solo cuenta f_act
    assert g["m_a"] == pytest.approx(5.04) and g["V_m3h"] == pytest.approx(15120.0)
    assert g["W_vent"] == pytest.approx(12.6)
    assert g["m_a"] > g["m_sens"]                                              # manda la norma, no la carga
    # balance de energia de la serpentina: entalpia que sale del aire = calor al agua + entalpia del condensado
    assert g["m_a"] * (g["h_mix"] - g["h_c"]) == pytest.approx(g["Q_serp"] + g["m_cond"] * g["h_f"], rel=1e-9)


def test_cuentas_de_g1_se_reproducen_a_mano_con_los_numeros_impresos(v):
    k = lambda s: num(v["mx_g1_" + s])
    ma, vs = k("ma"), k("Vs")
    assert 1.2 * vs == pytest.approx(ma, abs=5e-3)
    assert k("xae") * k("hext") + k("xret") * k("hret") == pytest.approx(k("hmez"), abs=0.01)
    assert k("xae") * k("Wext") + k("xret") * k("Wr") == pytest.approx(k("Wmez"), abs=0.001)
    assert 252 * 60 / 1000.0 == pytest.approx(k("Qs"), abs=1e-9)
    assert k("Qs") / (ma * k("cpr")) == pytest.approx(22.0 - k("Timp"), abs=0.01)
    assert 22.0 - k("Qs") / (ma * k("cpr")) == pytest.approx(k("Timp3"), abs=0.005)
    assert vs * k("dp_kPa") / k("eta") == pytest.approx(k("Wvent"), abs=0.05)
    assert k("Wvent") / (ma * k("cpr")) == pytest.approx(k("dTvent"), abs=0.001)
    assert k("Timp3") - k("dTvent") == pytest.approx(k("Tobj"), abs=0.002)
    assert (k("Wr") - k("Ql") / (ma * 2501.0) * 1e3) == pytest.approx(k("Wc"), abs=0.001)
    assert 4.186 * k("Tc") == pytest.approx(k("hf"), abs=0.01)
    assert (k("Wmez") - k("Wc")) * 1e-3 == pytest.approx(k("dWk"), abs=1e-6)
    corchete = (k("hmez") - k("hc")) - k("dWk") * k("hf")
    assert corchete == pytest.approx(k("corchete"), abs=0.006)
    assert ma * k("corchete") == pytest.approx(k("Qserp"), abs=0.05)
    assert ma * k("dWk") * 2501.0 == pytest.approx(k("Qlat"), abs=0.05)
    assert k("Qserp") - k("Qlat") == pytest.approx(k("Qsens"), abs=0.051)
    assert 1.006 + 1.86 * k("Wc_k") == pytest.approx(k("cpc"), abs=1e-4)
    assert ma * k("cpc") * k("dTobj") == pytest.approx(k("Qrec"), abs=0.05)
    assert k("Tobj") - k("Tc") == pytest.approx(k("dTobj"), abs=0.002)
    # las cifras que antes no coincidian al calcularlas a mano
    assert v["mx_g1_Qserp"] == "79,5" and v["mx_g1_Qrec"] == "18,7"


def test_tabla_de_estados_del_aire_tiene_los_seis_estados_y_decimales_suficientes(t):
    tab = t[0]["tabla_psicro_m"]
    filas = [f for f in tab.splitlines() if re.match(r"\| [A-F] \|", f)]
    assert len(filas) == 6
    d = [num(x.strip()) for x in filas[3].split("|")[3:6]]                        # estado D: T, omega, h
    assert d == [pytest.approx(13.0, abs=0.01), pytest.approx(8.859, abs=0.001), pytest.approx(35.45, abs=0.01)]


# ------------------------------------------------------------------ cargas por zona
def test_cargas_por_zona_cierran_con_la_capacidad_frigorifica():
    cz = me.cargas_zona(C)
    assert sum(f["serp"] for f in cz["filas"]) == pytest.approx(cz["Q_L"], rel=1e-12)
    assert cz["Q_L"] == pytest.approx(1987.2, abs=0.05)
    for f in cz["filas"]:
        assert f["sens"] + f["lat"] == pytest.approx(f["serp"], rel=1e-9)
    assert cz["total"]["cal"] + cz["total"]["hum"] == pytest.approx(cz["Q_caldera_inv"], rel=1e-9)
    assert cz["total"]["rec"] == pytest.approx(es.diseno(C)["Q_recal_verano"], rel=1e-12)


def test_la_tabla_de_cargas_imprime_el_total_y_las_filas_suman_dentro_del_redondeo(t):
    filas = [f for f in t[0]["tabla_cargas"].splitlines() if re.match(r"\| G\d ", f)]
    assert len(filas) == 5
    serp = [num(f.split("|")[2].strip()) for f in filas]
    total = num(t[0]["tabla_cargas"].splitlines()[-1].split("|")[2].strip("* "))
    assert abs(sum(serp) - total) < 0.3 and total == pytest.approx(1987.2, abs=0.05)


# ------------------------------------------------------------------ refrigeracion
def test_ciclo_del_caso_resuelto_reproduce_la_tabla_y_el_modelo(v):
    cc = me.caso_ciclo(C)
    cic, d = cc["cic"], es.diseno(C)
    assert cc["W_comp"] == pytest.approx(d["planta"]["W_comp"], rel=1e-12)
    assert cc["Q_cond"] == pytest.approx(d["planta"]["Q_cond"], rel=1e-12)
    assert cc["Q_cond"] == pytest.approx(cc["m_ref"] * cic["q_H"], rel=1e-9)
    assert cic["q_L"] == pytest.approx(cic["h1"] - cic["h4"]) and cic["w"] == pytest.approx(cic["h2"] - cic["h1"])
    k = lambda s: num(v["mx_cic_" + s])
    assert k("h1") - k("h4") == pytest.approx(k("qL"), abs=0.011)
    assert k("h2") - k("h1") == pytest.approx(k("w"), abs=0.011)
    assert k("w") == pytest.approx(38.45, abs=0.005)                          # la figura rotula 38,5 (redondeo de 38,45)
    assert k("h1") + (k("h2s") - k("h1")) / 0.72 == pytest.approx(k("h2"), abs=0.011)
    assert k("h2") - k("h3") == pytest.approx(k("qH"), abs=0.011)
    assert k("qL") / k("w") == pytest.approx(k("copeje"), abs=0.001)
    assert k("copeje") * 0.94 == pytest.approx(k("copel"), abs=0.001)
    assert k("Tev_K") / (k("Tc_K") - k("Tev_K")) == pytest.approx(k("carnot"), abs=0.001)
    assert num(v["mx_QL"]) / k("copel") == pytest.approx(k("Wcomp"), abs=0.1)
    assert num(v["mx_QL"]) / k("qL") == pytest.approx(k("mref"), abs=0.001)
    assert num(v["mx_QL"]) + 0.94 * k("Wcomp") == pytest.approx(k("Qcond"), abs=0.1)
    assert k("mref") * k("qH") == pytest.approx(k("Qcond"), abs=0.1)
    assert 0.025 * k("Qcond") == pytest.approx(k("Wcond"), abs=0.05)
    assert k("mw") / 1000.0 * 250.0 / 0.60 == pytest.approx(k("Wbomba"), abs=0.05)
    assert k("copel") < k("carnot")                                           # segunda ley
    assert v["mx_cic_Wcomp"] == "558,7" and v["mx_QL"] == "1.987,2"


# ------------------------------------------------------------------ combustion
def test_pci_es_la_suma_ponderada_de_los_pci_de_cada_componente(v):
    cm = me.caso_comb(C)
    pc = cb.poder_calorifico(P)
    assert cm["pci_mezcla"] == pytest.approx(pc["PCI_kJ_kmol"], rel=1e-12)
    assert cm["pcs_mezcla"] == pytest.approx(pc["PCS_kJ_kmol"], rel=1e-12)
    assert sum(f["y"] * f["pci"] for f in cm["comp"]) + 0.0 == pytest.approx(821933.0, abs=0.5)
    assert cm["pci_mezcla"] / cm["v_molar"] / 3600.0 == pytest.approx(pc["PCI_kWh_m3"], rel=1e-12)
    assert cm["pci_mezcla"] / cm["v_molar"] / 3600.0 == pytest.approx(9.656, abs=5e-4)
    assert cm["pcs_mezcla"] / cm["v_molar"] / 4.1868 == pytest.approx(9196.0, abs=1.0)
    assert cm["comp"][0]["pci"] == pytest.approx(393520 + 2 * 241820 - 74850)
    # la suma impresa
    suma = sum(float(a.replace(",", ".")) * num(b) for a, b in re.findall(r"([\d,]+) \\cdot ([\d.]+)", v["mx_pci_suma"]))
    assert suma == pytest.approx(num(v["mx_pci"]), abs=1.0)


def test_perdida_de_gases_8_por_ciento_y_rendimiento(v):
    cm = me.caso_comb(C)
    cal = cb.caldera(P)
    assert cm["q_gases"] == pytest.approx(cal["q_gases"], rel=1e-12) and cm["eta"] == pytest.approx(cal["eta_PCI"], rel=1e-12)
    assert cm["q_gases"] == pytest.approx(0.0802, abs=5e-5) and cm["eta"] == pytest.approx(0.8998, abs=5e-5)
    assert num(v["mx_hprod"]) == pytest.approx(62631, abs=1) and num(v["mx_hreac"]) == pytest.approx(-3267, abs=1)
    assert (num(v["mx_hprod"]) - num(v["mx_hreac"])) / num(v["mx_pci"]) == pytest.approx(num(v["mx_qgases"]), abs=5e-5)
    assert 1 - num(v["mx_qgases"]) - 0.02 == pytest.approx(num(v["mx_eta"]), abs=5e-5)
    hr = 2.352 * num(v["mx_dho2"]) + num(v["mx_n2aire"]) * num(v["mx_dhn2"])
    assert hr == pytest.approx(num(v["mx_hreac"]), abs=2.0)


def test_consumo_de_gas_de_diseno_en_m3_por_hora(v):
    cm = me.caso_comb(C)
    ca = eq.calderas(C)
    assert cm["Q_dis"] == pytest.approx(ca["Q_diseno"], rel=1e-12) and cm["V_gas_h"] == pytest.approx(ca["V_gas_m3h"], rel=1e-12)
    assert cm["Q_inv"] + cm["Q_acs_punta"] == pytest.approx(cm["Q_dis"], rel=1e-12)
    assert v["mx_Qinv"] == "648,8" and v["mx_Qacs_punta"] == "85,6" and v["mx_Qdis"] == "734,4"          # 649 + 86 = 734 era redondeo
    assert num(v["mx_Qinv"]) + num(v["mx_f_punta"]) * num(v["mx_Qacs_med"]) == pytest.approx(num(v["mx_Qdis"]), abs=0.06)
    assert num(v["mx_Qdis"]) / num(v["mx_eta"]) == pytest.approx(num(v["mx_Epci"]), abs=0.1)
    assert num(v["mx_Epci"]) / 9.656 == pytest.approx(num(v["mx_Vgas_h"]), abs=0.05)
    assert 84.0 < cm["V_gas_h"] < 85.0


# ------------------------------------------------------------------ anual
def test_calor_rechazado_anual_es_frio_mas_trabajo_del_compresor(v):
    a = me.balance_anual(C)
    assert a["Q_cond"] == pytest.approx(a["frio"] + C["P"]["eta_motor"] * a["W_comp"], rel=1e-9)
    assert a["Q_cond"] / 1e3 == pytest.approx(4198, abs=0.5)
    assert num(v["mx_frio2"]) + 0.94 * num(v["mx_e_comp2"]) == pytest.approx(num(v["mx_Qcond2"]), abs=0.02)
    assert num(v["mx_frio2"]) / num(v["mx_e_comp2"]) == pytest.approx(num(v["mx_cop_comp"]), abs=0.005)
    assert num(v["mx_frio2"]) / (num(v["mx_e_comp2"]) + num(v["mx_e_cond2"]) + num(v["mx_e_bomb2"])) == pytest.approx(num(v["mx_cop_planta"]), abs=0.005)
    assert v["mx_cop_comp"] == "4,94" and v["mx_cop_planta"] == "3,96" and v["mx_Qcond"] == "4.198" and v["mx_cond_sobre_rec"] == "8,2"


def test_calor_util_gas_y_energia_final_se_reproducen_con_enteros(v):
    q = [num(v["mx_q_" + k]) for k in ("rec", "cal", "hum", "acs")]
    assert sum(q) == pytest.approx(num(v["mx_q_tot"]), abs=0.5) and v["mx_q_tot"] == "1.044" and v["mx_q_rec"] == "511"
    assert num(v["mx_q_tot"]) / num(v["mx_eta"]) * num(v["mx_pcs_pci"]) == pytest.approx(num(v["mx_Egas"]), abs=1.0)
    el = [num(v["mx_e_" + k]) for k in ("comp", "cond", "bomb", "vent")]
    assert sum(el) == pytest.approx(num(v["mx_Eelec"]), abs=1.0)
    assert num(v["mx_Eelec"]) + num(v["mx_Egas"]) == pytest.approx(num(v["mx_Etot"]), abs=1.0) and v["mx_Etot"] == "3.021"
    assert num(v["mx_Etot"]) * 1e3 / P["A_cub"] == pytest.approx(num(v["mx_Etot_i"]), abs=0.1)
    # ACS: 100 L x 158 camas x 4,186 x 43 K x 1,3 / 86.400
    assert 100 * 158 * 4.186 * 43 * 1.3 / 86400 == pytest.approx(num(v["mx_acs_kW"]), abs=0.05)


# ------------------------------------------------------------------ estados de las corrientes y propiedades
def test_estados_de_las_corrientes(t):
    k = me._ctx(C)["corr"]
    assert k["T_ah"] == (7.0, 12.0) and k["T_hw"] == (80.0, 60.0)
    assert k["m_ah"] == pytest.approx(es.diseno(C)["Q_L"] / (4.186 * 5.0), rel=1e-12)
    com = me.caso_comb(C)
    assert com["y_prod"]["H2O"] == pytest.approx(com["cal"]["y_H2O"], rel=1e-12)
    assert com["h_aire"] < 0 < com["h_gases"]
    tab = t[0]["tabla_estados_corrientes"]
    filas = [f for f in tab.splitlines()[2:]]
    assert len(filas) == 7
    for palabra in ("Gas natural", "Aire de combustión", "Gases de escape", "Agua helada", "Agua caliente", "ACS", "invierno"):
        assert any(palabra in f for f in filas), palabra
    assert "56,1" in tab and "16,4 % de agua" in tab


def test_r134a_coincide_con_dos_puntos_de_tabla_dentro_de_0_1_por_ciento():
    for f in me.contraste_r134a():
        assert abs(f["dp"]) < 1e-3 and abs(f["dh"]) < 1e-3
    assert {f["T"] for f in me.contraste_r134a()} == {0, 40}


def test_tabla_de_propiedades_cita_versiones(t):
    import importlib.metadata as md
    tab = t[0]["tabla_propiedades"]
    assert md.version("CoolProp") in tab and md.version("psychrolib") in tab


# ------------------------------------------------------------------ marcas, rutas y cobertura de parametros
def test_los_parametros_de_las_tablas_cubren_todo_el_modelo(t):
    assert sorted(me.ids_params_modelo()) == sorted(f[0] for f in supuestos.filas())
    assert sorted(me.ids_equipos()) == sorted(s["id"] for s in eq.SUPUESTOS.values())
    assert set(me._PM) == {f[0] for f in mj.PARAMETROS}
    tab = t[0]["tabla_parametros_m"]
    assert tab.count("\n") == 2 + len(me._params_modelo(dict(acond_txt="", est_txt="", fan_txt="", eta_txt=""))) - 1


PROHIBIDAS = ("RECORDADO", "recordad", "FUENTE SECUNDARIA", "SUPUESTO", "CONSTANTE", " DATO", "PROPIO", "cátedra", "catedra", "calculo/", "informe/", "datos/",
              ".py", "pytest", "python -m", "supuestos.md", "a confirmar", "no se pudo", "Borrador", "búsqueda web", "busqueda web", "via ")


def test_la_memoria_no_usa_marcas_viejas_ni_nombra_archivos(t, v):
    tablas, V, T = t
    texto = "\n".join([*tablas.values(), *v.values()])
    for p in PROHIBIDAS:
        assert p not in texto, p
    # los textos que vienen sin tildes del modelo no deben llegar a la memoria
    for mal in ("Parametro", "Justificacion", "canierias", "tamano", "obstaculos", "Temperatura minima", "diametro", "caida"):
        assert mal not in texto, mal
    propio = "\n".join([x for k, x in tablas.items() if k != "memoria_exergia"] + list(v.values()))    # la exergia trae sus propias etiquetas M14a, M15...
    assert not re.search(r"[Tt]abla M(?!14a|15|16|17)\d", propio)              # salvo las etiquetas de la exergia, las remisiones usan etiquetas semanticas


def test_marcas_nuevas_en_las_tablas_de_respaldo(t):
    for clave in ("tabla_parametros_m", "tabla_params_mejoras_m"):
        for f in t[0][clave].splitlines()[2:]:
            respaldo = f.split("|")[-2].strip()
            assert re.match(r"(\[\d+\](\\\*)?|supuesto|constante)", respaldo), respaldo
    # las fuentes numeradas coinciden con la lista unica
    assert "[1]" in t[0]["tabla_parametros_m"] and "[13]\\*" in t[0]["memoria_equipos"] and "[14]\\*" in t[0]["memoria_equipos"]


def test_valores_de_uso_corriente_pasan_a_supuesto(t):
    tab = t[0]["tabla_parametros_m"]
    for i in ("C1", "C2", "C3", "C4"):
        fila = [f for f in tab.splitlines() if f.startswith(f"| {i} ")][0]
        assert "supuesto (valor de uso corriente)" in fila
    assert "**supuesto** (valores de uso corriente)" in t[0]["memoria_exergia"]
    assert "supuesto (valor de uso corriente, entre 1 y 5 kN/m" in t[0]["memoria_equipos"]


def test_la_lista_de_referencias_de_la_memoria_numera_igual_que_la_lista_unica():
    from calculo import referencias
    lista = me.lista_referencias()
    for i, (cl, _txt, sec) in enumerate(referencias.REFERENCIAS, start=1):
        assert f"[{i}]{chr(92) + '*' if sec else ''} " in lista
        assert referencias.marca(cl) == f"[{i}]" + ("\\*" if sec else "")


# ------------------------------------------------------------------ sensibilidades y mejoras
def test_nota_de_superficies_verificada_contra_el_modelo(v):
    s = me.sens_superficies(C)
    esperado = {"gen": 1.6, "or": 1.2, "uti": 0.3, "acond": 8.0, "g4": 12.8}
    for k, x in esperado.items():
        assert abs(s[k][0]) * 100 == pytest.approx(x, abs=0.05), k
        assert abs(s[k][1]) * 100 == pytest.approx(x, abs=0.05), k
        assert s[k][0] * s[k][1] < 0                                           # un signo para cada lado
    nota = v["mx_nota_m2"]
    for x in ("±1,6 %", "±1,2 %", "±0,3 %", "±8,0 %", "±12,8 %"):
        assert x in nota


def test_lectura_de_mejoras(v):
    m = me.lectura_mejoras(C)
    assert m["ahorro_ind"] / 1e3 == pytest.approx(1520, abs=1) and m["ahorro_paq"] / 1e3 == pytest.approx(1500, abs=1)
    assert m["m1_con_b"] / 1e3 == pytest.approx(24, abs=1) and m["m1_solo"] / 1e3 == pytest.approx(94, abs=1)
    assert m["m4_con_b"] / 1e3 == pytest.approx(128, abs=1) and m["m4_solo"] / 1e3 == pytest.approx(77, abs=1)
    # M4: menos electricidad de ventiladores, mas gas, y el neto es el ahorro de la tabla
    m4 = m["m4"]
    assert m4["d_vent"] > 0 and m4["d_gas"] > 0
    assert m4["d_vent"] + m4["d_resto"] - m4["d_gas"] == pytest.approx(m4["d_E"], rel=1e-9)
    m6 = m["m6"]
    assert m6["d_vent"] > 0 and m6["d_vent"] == pytest.approx(0.875 * 12.6 * 12 * 365, rel=0.01)       # 1 - 0,5^3 de la potencia de G1 de noche
    assert m6["d_vent"] + m6["d_resto"] - m6["d_gas"] == pytest.approx(m6["d_E"], rel=1e-9)
    d_ua = me._sens_c(C, lambda c2: c2["P"].__setitem__("UA_m2", c2["P"]["UA_m2"] * 0.7))
    d_gi = me._sens_c(C, lambda c2: [(z.__setitem__("q_s", z["q_s"] * 0.7), z.__setitem__("q_l", z["q_l"] * 0.7)) for z in c2["Z"].values()])
    assert d_ua * 100 == pytest.approx(-2.5, abs=0.05) and d_gi * 100 == pytest.approx(0.7, abs=0.05)   # bajar las ganancias internas SUBE la energia
    assert "−2,5 %" in v["mx_lectura_mejoras"] and "+0,7 %" in v["mx_lectura_mejoras"]


def test_refrigerante():
    r = me.texto_refrigerante(C)
    assert "1.430" in r and "Kigali" in r and "R513A" in r and "A2L" in r and "35 %" in r and "3,55 contra 3,56" in r


def test_emisiones_del_caso_base_se_reproducen(v):
    assert num(v["mx_Epci_anual"]) * num(v["mx_co2_gas_kg4"]) == pytest.approx(num(v["mx_co2_gas_t"]), abs=0.5)
    assert num(v["mx_co2_gas_t"]) + num(v["mx_co2_elec_t"]) == pytest.approx(num(v["mx_co2_tot_t"]), abs=1.0)
    assert num(v["mx_Eelec"]) * 0.38 == pytest.approx(num(v["mx_co2_elec_t"]), abs=1.0)


def test_otras_variaciones():
    base, out = me.variaciones_extra(C)
    assert len(out) == 8
    assert max(abs(d) for _n, _e, d in out) < 0.2
    assert all(isinstance(e, float) for _n, e, _d in out)


# ------------------------------------------------------------------ exergia
@pytest.fixture(scope="module")
def exergia(t):
    return me.memoria_exergia(C, t[1], t[2])


def test_memoria_exergia_renumera_y_usa_las_marcas_nuevas(exergia):
    assert "## 9.1 " in exergia and "## 9.4 " in exergia and "## 8." not in exergia
    assert "cátedra" not in exergia and "recordad" not in exergia
    assert "Convención adoptada (supuesto)" in exergia
    assert exergia.index("Tabla Mexcal") < exergia.index("## 9.3 ")


def test_exergia_de_la_caldera_en_el_maximo_recalentamiento():
    x = me.exergia_caldera(C)
    # 300,0 kW (caldera) y 303,1 kW (caldera y ACS): 57,1 % y 57,7 % de lo destruido
    assert x["D_cal"] == pytest.approx(300.0, abs=0.05) and x["D_cal_acs"] == pytest.approx(303.1, abs=0.05)
    assert x["D_cal"] / x["D_total"] * 100 == pytest.approx(57.1, abs=0.05) and x["D_cal_acs"] / x["D_total"] * 100 == pytest.approx(57.7, abs=0.05)
    assert x["D_cal_acs"] / x["X_in"] * 100 == pytest.approx(55.1, abs=0.05)
    assert x["D_comb"] / x["X_comb"] * 100 == pytest.approx(30.2, abs=0.05) and x["D_transf"] / x["X_comb"] * 100 == pytest.approx(52.5, abs=0.05)
    assert x["D_comb"] + x["D_transf"] == pytest.approx(x["D_cal"], rel=1e-9)
    # balance de la caldera: combustible y aire = calor util + gases + radiacion + destruccion
    assert x["X_comb"] + x["X_aire"] == pytest.approx(x["X_calor"] + x["X_gas"] + x["X_rad"] + x["D_cal"], rel=1e-9)
    assert x["eta"] == pytest.approx(x["X_calor"] / x["X_comb"], rel=1e-12)


def test_exergia_de_la_enfriadora_y_cifras_del_informe():
    xe = me.exergia_resumen(C)
    assert xe["eta_enf"] * 100 == pytest.approx(30.8, abs=0.05) and xe["eta_planta"] * 100 == pytest.approx(26.1, abs=0.05)
    assert xe["D_a"] * 100 == pytest.approx(85.6, abs=0.05) and xe["X_in_a"] == pytest.approx(854.5, abs=0.05)
    assert (xe["comp_a"] + xe["cve_a"]) * 100 == pytest.approx(42.4, abs=0.05)


# ------------------------------------------------------------------ equipos
def test_shafts_14_con_g1_y_g2_compartiendo(t):
    sh = eq.resumen_equipos(C)["shafts"]
    assert sh["n_shafts_agrupados"] == 14
    por = [sh["por_zona"][g]["n_shafts"] for g in ("G1", "G2", "G3", "G4", "G5")]
    assert sum(por) == 15 and por[:2] == [1, 1]                                     # 1 + 1 + 3 + 5 + 5 = 15 si no se comparte
    assert sh["A_grupos"]["G1+G2"] < eq.parametros()["area_shaft"]                 # caben en un solo shaft
    texto = t[0]["memoria_equipos"]
    assert "1 (compartido con G2)" in texto and "1 + 3 + 5 + 5 = 14 y no 15" in texto


def test_textos_fijos_de_la_matriz_coinciden_con_el_modelo(t):
    r = eq.resumen_equipos(C)
    just = {m[0]: m[5] for m in eq.MATRIZ_UBICACION}
    assert f"{r['utas']['n_cubierta']} de las {r['utas']['n_total']} UTAs" in just["canerias"]
    assert "14 m y 12 t" in just["izaje"] and "Cuatro unidades" in just["izaje"]
    assert r["azotea"]["n_unidades"] == 4 and eq.parametros()["huella_L"] == 14.0 and eq.parametros()["peso_op_t"] == 12.0
    texto = t[0]["memoria_equipos"]
    assert "La decisión no es robusta" in texto and "3,25 contra 3,05" in texto and "3,38 contra 2,96" in texto
    assert "fig11_planta_tipo.png" in texto and "empatan" in texto


def test_equipos_con_decimales_donde_el_redondeo_confundia(t):
    texto = t[0]["memoria_equipos"]
    assert "648,8 + 85,6 = 734,4 kW" in texto and "649 + 86" not in texto


# ------------------------------------------------------------------ plantilla
def _plantilla():
    with open(PLANTILLA, encoding="utf-8") as f:
        return f.read()


def test_los_encabezados_de_la_plantilla_estan_numerados_en_orden():
    s = _plantilla()
    n1 = [int(m) for m in re.findall(r"(?m)^# (\d+)\. ", s)]
    assert n1 == list(range(1, 11))
    for sec in range(1, 10):
        sub = [int(m) for m in re.findall(rf"(?m)^## {sec}\.(\d+) ", s)]
        assert sub == list(range(1, len(sub) + 1)), sec
    assert "{#anexo-a" in s and s.count("{#sec-") == 10


def test_todas_las_claves_de_la_plantilla_estan_definidas(t, v):
    tablas, V, T = t
    s = _plantilla()
    claves = set(re.findall(r"\{\{(\w+)\}\}", s))
    fuentes = ""
    for nombre in ("construir_documentos.py", "construir_borrador.py", "texto_exergia.py", "texto_equipos.py", "referencias.py"):
        with open(os.path.join(RAIZ, "calculo", nombre), encoding="utf-8") as f:
            fuentes += f.read()
    from calculo import referencias
    refs = referencias.valores_ref()
    for k in sorted(claves):
        base = k[:-2] if k.endswith("_m") else k
        if k in tablas or k in v or base in v or k in V or base in V or k in refs:
            continue
        prefijo = base.split("_")[0] + "_"                                           # claves armadas en un bucle: V["dE_" + k]
        assert f'"{base}"' in fuentes or f'"{k}"' in fuentes or f'"{prefijo}" +' in fuentes, f"falta {k}"
    assert "<<" not in s


def test_remisiones_a_tablas_y_figuras_tienen_su_epigrafe(t, exergia):
    tablas, V, T = t
    s = _plantilla()
    cuerpo = "\n".join([s, tablas["memoria_equipos"], exergia, *[x for x in tablas.values()]])
    definidas = set(re.findall(r"(?m)^Table: Tabla M(\w+?)\.", cuerpo)) | set(re.findall(r"(?m)^!\[Figura M(\w+?)\.", cuerpo))
    usadas = set(re.findall(r"[Tt]abla M(\w+?)\b(?!\w)", cuerpo)) | set(re.findall(r"[Ff]igura M(\w+?)\b(?!\w)", cuerpo))
    assert usadas <= definidas, sorted(usadas - definidas)
    assert all(re.search(r"(?m)^Table: Tabla M" + re.escape(x) + r"\.", cuerpo) or re.search(r"Figura M" + re.escape(x) + r"\.", cuerpo) for x in definidas)


def test_la_memoria_generada_no_deja_marcadores_sin_reemplazar():
    md = os.path.join(RAIZ, "informe", "memoria_calculo.md")
    if not os.path.exists(md):
        pytest.skip("la memoria todavia no se generó")
    with open(md, encoding="utf-8") as f:
        s = f.read()
    sin_math = re.sub(r"\$\$.*?\$\$|\$[^$\n]*?\$", "", s, flags=re.S)
    assert "{{" not in sin_math and "<<" not in sin_math
    assert not re.search(r"\b[Tt]abla M[a-z]", s) and not re.search(r"\b[Ff]igura M[a-z]", s)
    for p in PROHIBIDAS:
        assert p not in s, p
