"""Chequeos de equipos y ubicacion (calculo/equipos.py y calculo/figuras_plano.py).

Ejecutar desde la carpeta del proyecto:  python -m pytest calculo/tests -q
"""
import copy
import math

import pytest

from calculo import aire_humedo as ah
from calculo import edificio as ed
from calculo import equipos as eq
from calculo import estimacion as es
from calculo import supuestos

C = supuestos.defaults()
P = C["P"]
p = eq.parametros()
D = es.diseno(C)
R = eq.resumen_equipos(C)
A_ZONAS, A_COND = ed.superficies(C)


# ---------------------------------------------------------------- niveles
def test_superficies_por_nivel_suman_A_cond_y_A_cub():
    niv = R["niveles"]
    assert sum(n["clim"] for n in niv["niveles"]) == pytest.approx(A_COND, rel=1e-12)
    assert sum(n["bruta"] for n in niv["niveles"]) == pytest.approx(P["A_cub"], rel=1e-12)
    for n in niv["niveles"]:
        assert n["clim"] + n["no_clim"] == pytest.approx(n["bruta"], rel=1e-12)
        assert n["bruta"] == pytest.approx(P["A_cub"] / 3.0, rel=1e-12)
    assert niv["no_clim_total"] == pytest.approx(P["A_cub"] - A_COND, rel=1e-12)


def test_cada_zona_cierra_con_el_modelo_y_ninguna_es_negativa():
    niv = R["niveles"]
    for g, a_modelo in A_ZONAS.items():
        por_nivel = niv["por_zona"][g]
        assert all(a > 0.0 for a in por_nivel.values()), g
        assert sum(por_nivel.values()) == pytest.approx(a_modelo, rel=1e-12), g
    for n in niv["niveles"]:
        assert n["no_clim"] >= 0.0
        assert all(a >= 0.0 for _g, a, _t in n["zonas"])


def test_asignacion_de_zonas_a_niveles():
    """FA-08: guardia y diagnostico en el 1.er piso; quirofanos, areas criticas e internacion en el 2.º."""
    pz = R["niveles"]["por_zona"]
    assert set(pz["G1"]) == set(pz["G2"]) == set(pz["G3"]) == {2}
    assert set(pz["G4"]) == {1}
    assert set(pz["G5"]) == {1, 2, 3}
    cap = A_COND / 3.0
    por_nivel = {n["nivel"]: n["clim"] for n in R["niveles"]["niveles"]}
    assert por_nivel[1] == pytest.approx(cap, rel=1e-12)
    assert por_nivel[2] == pytest.approx(cap, rel=1e-12)
    assert por_nivel[3] <= cap * (1 + 1e-9)
    # numeros del enunciado: 4.620 m2 de G1 + G2 + G3 y 5.200 m2 climatizados por nivel
    assert A_ZONAS["G1"] + A_ZONAS["G2"] + A_ZONAS["G3"] == pytest.approx(4620.0)
    assert cap == pytest.approx(5200.0, abs=1.0)


@pytest.mark.parametrize("f_acond", [0.80, 0.85, 0.90, 0.95])
def test_niveles_cierran_para_otras_fracciones_climatizadas(f_acond):
    c = copy.deepcopy(C)
    c["P"]["f_acond"] = f_acond
    niv = eq.niveles(c)
    assert sum(n["clim"] for n in niv["niveles"]) == pytest.approx(f_acond * P["A_cub"], rel=1e-12)
    assert all(a > 0 for pz in niv["por_zona"].values() for a in pz.values())


def test_con_75_por_ciento_climatizado_los_criticos_no_entran_en_un_nivel():
    """Limite de la asignacion: con f_acond = 0,75 G1 + G2 + G3 (4.620 m2) superan un nivel climatizado (4.588 m2)."""
    c = copy.deepcopy(C)
    c["P"]["f_acond"] = 0.75
    with pytest.raises(ValueError):
        eq.niveles(c)


# ---------------------------------------------------------------- enfriadoras
def test_enfriadoras_dos_en_servicio_cubren_la_carga_o_se_declara_la_salida():
    e = R["enfriadoras"]
    assert e["Q_L"] == pytest.approx(D["Q_L"], rel=1e-12)
    assert e["cap_servicio"] == pytest.approx(2 * p["cap_enf"])
    assert e["n_total"] == 3
    if e["cumple"]:
        assert e["cap_servicio"] >= e["Q_L"]
        assert e["salida"] is None
    else:
        # no cumple: debe declararse con el faltante y la salida, y el faltante es chico
        assert e["cap_servicio"] < e["Q_L"]
        assert e["faltante_kW"] == pytest.approx(e["Q_L"] - 2 * p["cap_enf"])
        assert e["salida"] and "30XA 1102" in e["salida"]
        assert e["faltante_kW"] / e["Q_L"] < 0.02
    assert e["margen_kW"] == pytest.approx(e["cap_servicio"] - e["Q_L"])


def test_salida_con_mas_unidades_en_servicio_cubre_la_carga():
    e = R["enfriadoras"]
    assert e["n_serv_minimo_con_esta_unidad"] * p["cap_enf"] >= e["Q_L"]
    assert (e["n_serv_minimo_con_esta_unidad"] - 1) * p["cap_enf"] < e["Q_L"]
    # la capacidad requerida por unidad (2 en servicio) es la mitad de la carga
    assert e["req_unidad"] == pytest.approx(e["Q_L"] / 2.0)


def test_cop_de_catalogo_y_del_modelo():
    cp = R["cop"]
    assert cp["cop_catalogo"] == pytest.approx(988.0 / 288.2, rel=1e-12)
    assert cp["cop_modelo_34"] == pytest.approx(D["planta"]["COP"], rel=1e-12)
    assert cp["T_cond_modelo_34"] == pytest.approx(46.0)
    assert cp["cop_modelo_35"] < cp["cop_modelo_34"]                       # mas aire exterior, menos COP
    assert abs(cp["dif_rel_34"]) < 0.10                                    # mismo orden de magnitud
    assert 0.0 <= cp["fraccion_por_temperatura"] <= 1.0


# ---------------------------------------------------------------- calderas
def test_carga_de_diseno_de_la_caldera():
    cl = R["calderas"]
    assert cl["Q_invierno"] == pytest.approx(D["Q_caldera_invierno"], rel=1e-12)
    assert cl["Q_acs_punta"] == pytest.approx(p["f_punta_acs"] * D["acs"]["kW"], rel=1e-12)
    assert cl["Q_diseno"] == pytest.approx(cl["Q_invierno"] + cl["Q_acs_punta"], rel=1e-12)
    assert 0.0 < cl["Q_vapor"] < cl["Q_invierno"]                          # la humidificacion es una parte de la carga


def test_cascada_de_condensacion_con_una_unidad_parada_cubre_la_carga():
    cl, b = R["calderas"], R["calderas"]["opcion_b"]
    assert b["n_servicio"] == 3 and b["n_reserva"] == 1 and b["n"] == 4     # 3+1: cuatro unidades de 311 kW
    assert b["cap_una_parada"] == pytest.approx(3 * 311.0)
    assert b["cap_una_parada"] >= cl["Q_diseno"]
    assert b["cumple_con_una_parada"]
    # con solo 2 unidades en servicio no alcanza (ni la carga de invierno sola): por eso son 3 en servicio
    assert 2 * 311.0 < cl["Q_invierno"] < cl["Q_diseno"]
    assert not b["cumple_con_3_unidades"]                                   # 3 en total con una parada = 622 kW: no alcanza
    assert b["cap_3_unidades_una_parada"] == pytest.approx(622.0)


def test_caldera_2x100_y_gases():
    cl = R["calderas"]
    assert cl["opcion_a"]["n"] == 2
    assert cl["opcion_a"]["cap_con_una_parada"] >= cl["Q_diseno"]           # 2 x 100 %: una sola cubre toda la carga
    # el gas natural a plena carga: potencia del combustible = carga / rendimiento sobre PCI
    assert cl["E_comb_PCI_kW"] == pytest.approx(cl["Q_diseno"] / cl["eta_PCI_modelo"], rel=1e-12)
    assert cl["T_rocio_gases"] < P["T_gases"]
    assert 0.0 < cl["ahorro_gas_max"] < 0.3
    assert cl["DN_chimenea"] / 1000.0 >= cl["D_chimenea"]


# ---------------------------------------------------------------- UTAs
def test_utas_cantidad_y_caudal():
    u = R["utas"]
    por = u["por_zona"]
    assert por["G1"]["n"] == P["n_or"] == 6
    assert por["G2"]["n"] == 1
    for g in ("G3", "G4", "G5"):
        V = D["caudales"][g]["V_sup_m3h"]
        assert por[g]["n"] == math.ceil(V / 25000.0)
        assert por[g]["caudal_unidad"] <= 25000.0 + 1e-9
        assert por[g]["ubicacion"] == "cubierta"
    for g in ("G1", "G2"):
        assert por[g]["ubicacion"].startswith("cuarto técnico")
        assert por[g]["nivel"] == 2
        assert por[g]["hepa"]
    # el caudal repartido en las unidades suma el de la zona y el de todo el edificio
    for g in C["Z"]:
        assert por[g]["n"] * por[g]["caudal_unidad"] == pytest.approx(D["caudales"][g]["V_sup_m3h"], rel=1e-12)
    assert sum(x["caudal_m3h"] for x in u["lista"]) == pytest.approx(sum(c["V_sup_m3h"] for c in D["caudales"].values()), rel=1e-12)
    assert u["n_total"] == 18 and u["n_criticas"] == 7 and u["n_cubierta"] == 11


# ---------------------------------------------------------------- hidraulica
def test_agua_helada_caudal_y_diametro():
    h = R["hidraulica"]
    assert h["m_w"] * ah.CP_W * P["dT_aguahelada"] == pytest.approx(D["Q_L"], rel=1e-12)    # primera ley en el agua
    for tr in (h["principal"], h["ramal_enfriadora"]):
        assert tr["DN"] in p["serie_DN"]
        assert tr["DN"] % 50 == 0
        assert tr["v_real"] <= p["v_agua"]
        assert tr["DN"] / 1000.0 >= tr["D_calc_mm"] / 1000.0
        # es el menor DN de la serie que cumple: el anterior supera la velocidad maxima
        menores = [dn for dn in p["serie_DN"] if dn < tr["DN"]]
        if menores:
            v_menor = 4.0 * (tr["m_w"] / p["rho_agua"]) / (math.pi * (max(menores) / 1000.0) ** 2)
            assert v_menor > p["v_agua"]
    assert h["principal"]["DN"] == 250
    assert h["ramal_enfriadora"]["m_w"] == pytest.approx(h["m_w"] / 2.0)


# ---------------------------------------------------------------- shafts
def test_shafts_coherentes_con_los_caudales():
    sh = R["shafts"]
    for g, z in sh["por_zona"].items():
        cd = D["caudales"][g]
        assert z["A_imp"] * p["v_imp"] * 3600.0 == pytest.approx(cd["V_sup_m3h"], rel=1e-12)
        assert z["V_ret"] == pytest.approx(cd["V_sup_m3h"] - z["V_oa"] - p["exfiltracion"], rel=1e-12)
        assert z["A_ret"] * p["v_ret"] * 3600.0 == pytest.approx(z["V_ret"], rel=1e-12)
        assert z["V_oa"] == pytest.approx(cd["m_oa"] / P["rho_aire"] * 3600.0, rel=1e-12)
        assert z["A_imp"] > 0 and z["A_ret"] > 0
        assert 0.0 < z["A_vertical"] <= z["A_total"] + 1e-12
        assert z["n_shafts"] * p["area_shaft"] >= z["A_vertical"]
    assert sh["A_imp_total"] == pytest.approx(sum(z["A_imp"] for z in sh["por_zona"].values()))
    assert sh["A_ret_total"] == pytest.approx(sum(z["A_ret"] for z in sh["por_zona"].values()))
    assert sh["A_total"] == pytest.approx(sh["A_imp_total"] + sh["A_ret_total"])
    assert sh["n_shafts_por_area"] * p["area_shaft"] >= sh["A_vertical_total"]
    assert (sh["n_shafts_por_area"] - 1) * p["area_shaft"] < sh["A_vertical_total"]
    assert sh["n_shafts_por_area"] <= sh["n_shafts_agrupados"]               # agrupar por zona nunca baja la cantidad
    # las zonas criticas con UTA en el nivel solo suben aire exterior y extraccion
    for g in ("G1", "G2"):
        assert sh["por_zona"][g]["A_vertical"] < 0.5 * sh["por_zona"][g]["A_total"]


# ---------------------------------------------------------------- azotea
def test_carga_de_las_enfriadoras_sobre_la_azotea():
    a = R["azotea"]
    assert a["A_unidad"] == pytest.approx(14.0 * 3.5)
    assert a["peso_unidad_kN"] == pytest.approx(12.0 * 9.81)
    assert a["q_kN_m2"] == pytest.approx(12.0 * 9.81 / 49.0)
    assert a["peso_total_kN"] == pytest.approx(3 * a["peso_unidad_kN"])
    assert a["supera_ref"] == (a["q_kN_m2"] > p["q_ref_cubierta"])
    assert a["fraccion_cubierta"] < 0.05                                      # las enfriadoras ocupan una fraccion chica de la cubierta


# ---------------------------------------------------------------- matriz de decision y supuestos
def test_matriz_de_decision():
    m = R["matriz"]
    assert m["suma_pesos"] == pytest.approx(1.0)
    for _k, _crit, w, a, b, just in eq.MATRIZ_UBICACION:
        assert w > 0 and 1 <= a <= 5 and 1 <= b <= 5 and just
    assert m["ganador"] == "azotea"
    assert m["base"]["azotea"] > m["base"]["patio"]


def test_supuestos_nuevos_declarados():
    ids = [s["id"] for s in eq.SUPUESTOS.values()]
    assert len(ids) == len(set(ids))
    previos = {fila[0] for fila in supuestos.filas()}
    assert not (set(ids) & previos)                                           # no pisan los ids del modelo
    for k, s in eq.SUPUESTOS.items():
        assert s["estado"] in eq.ESTADOS, k
        assert s["justificacion"] and s["unidad"], k
    # los datos de catalogo son FUENTE SECUNDARIA, nunca DATO
    for k in ("modelo_enf", "cap_enf", "pot_enf", "cap_cond", "cap_cond_min", "eta_cond_PCS"):
        assert eq.SUPUESTOS[k]["estado"] == "FUENTE SECUNDARIA", k
    for k in ("huella_L", "huella_W", "peso_op_t", "f_punta_acs", "V_max_uta", "v_agua", "v_imp", "v_ret"):
        assert eq.SUPUESTOS[k]["estado"] == "SUPUESTO", k
    tabla = eq.tabla_supuestos_md()
    assert tabla.count("\n") == len(eq.SUPUESTOS) + 1


def test_la_figura_se_genera_sin_textos_superpuestos(tmp_path):
    from calculo import figuras_plano as fp
    ruta = fp.fig_plano(C, R, ruta=str(tmp_path / "plano.png"))
    assert (tmp_path / "plano.png").stat().st_size > 50_000
    assert ruta == str(tmp_path / "plano.png")
    assert fp.ULTIMOS_AVISOS == []
