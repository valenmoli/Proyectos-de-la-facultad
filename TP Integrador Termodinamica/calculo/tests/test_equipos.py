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
def test_enfriadoras_tres_en_servicio_y_una_de_reserva_cumplen_con_una_parada():
    e = R["enfriadoras"]
    assert e["Q_L"] == pytest.approx(D["Q_L"], rel=1e-12)
    assert (e["n_serv"], e["n_res"], e["n_total"]) == (3, 1, 4)
    assert e["cap_servicio"] == pytest.approx(3 * p["cap_enf"])
    # con cualquiera de las cuatro unidades parada quedan 3 x 988 = 2.964 kW para 1.987 kW de diseno
    assert e["cap_una_parada"] == pytest.approx(3 * 988.0)
    assert e["cap_una_parada"] >= e["Q_L"]
    assert e["cumple"] and e["cumple_con_una_parada"]
    assert e["faltante_kW"] == 0.0
    assert e["margen_kW"] == pytest.approx(e["cap_servicio"] - e["Q_L"])
    assert e["margen_rel"] == pytest.approx(0.4915, abs=1e-3)                  # +49 %
    assert e["margen_una_parada_kW"] == pytest.approx(e["cap_una_parada"] - e["Q_L"])
    # cada unidad en servicio trabaja al 67 % de su capacidad nominal; con las cuatro en marcha, al 50 %
    assert e["carga_relativa_unidad"] == pytest.approx(e["Q_L"] / (3 * 988.0))
    assert 0.66 < e["carga_relativa_unidad"] < 0.68
    assert e["carga_relativa_todas"] == pytest.approx(e["Q_L"] / (4 * 988.0))
    assert e["req_unidad"] == pytest.approx(e["Q_L"] / 3.0)                    # cada unidad debe dar al menos un tercio de la carga
    # el margen cubre el calor de las bombas, que la carga de diseno no incluye
    assert e["calor_bombas_max_kW"] > 0.0
    assert e["cubre_con_bombas"]
    assert e["margen_con_bombas_kW"] == pytest.approx(e["cap_una_parada"] - e["Q_L"] - e["calor_bombas_max_kW"])


def test_salida_declara_la_sobredimension_y_la_alternativa_2_mas_1():
    e = R["enfriadoras"]
    txt = e["salida"]
    assert "sobredimensionada" in txt
    assert "2+1" in txt and "994" in txt
    assert "30XA 1102" in txt and "no está verificada" in txt
    assert "34" in txt and "35" in txt and "bombas" in txt


def test_alternativa_2_mas_1_con_la_misma_unidad_no_cumple_y_queda_documentada():
    e = R["enfriadoras"]
    alt = e["alt_2mas1"]
    assert (alt["n_serv"], alt["n_res"], alt["n_total"]) == (2, 1, 3)
    assert alt["cap_servicio"] == pytest.approx(2 * p["cap_enf"])
    assert not alt["cumple"]
    assert alt["faltante_kW"] == pytest.approx(e["Q_L"] - 2 * p["cap_enf"])
    assert alt["faltante_kW"] == pytest.approx(11.2, abs=0.05)
    assert alt["faltante_rel"] < 0.01                                          # 0,6 %
    # la unidad mas ajustada para 2+1 es de al menos 994 kW (la 30XA 1002 no llega a 988 + 6)
    assert alt["req_unidad"] == pytest.approx(e["Q_L"] / 2.0)
    assert alt["req_unidad_redondeada"] == 994
    assert alt["req_unidad"] > p["cap_enf"]
    assert alt["req_unidad_con_margen"] == pytest.approx(alt["req_unidad"] * 1.10)


def test_configuracion_2_mas_1_con_los_parametros_cambiados_no_cumple_y_da_la_salida():
    p2 = dict(p, n_serv=2, n_res=1)
    e2 = eq.enfriadoras(C, p2, D)
    assert not e2["cumple"] and not e2["cumple_con_una_parada"]
    assert e2["cap_servicio"] == pytest.approx(2 * 988.0)
    assert e2["faltante_kW"] == pytest.approx(D["Q_L"] - 1976.0)
    assert e2["salida"] and "30XA 1102" in e2["salida"] and "pasar a 3 unidades en servicio + 1 de reserva" in e2["salida"]
    assert e2["n_serv_minimo_con_esta_unidad"] == 3


def test_salida_con_mas_unidades_en_servicio_cubre_la_carga():
    e = R["enfriadoras"]
    assert e["n_serv_minimo_con_esta_unidad"] * p["cap_enf"] >= e["Q_L"]
    assert (e["n_serv_minimo_con_esta_unidad"] - 1) * p["cap_enf"] < e["Q_L"]
    assert e["n_serv_minimo_con_esta_unidad"] == e["n_serv"] == 3             # tres es la menor cantidad en servicio con esta unidad


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
    assert h["principal"]["v_real"] == pytest.approx(1.93, abs=0.01)
    # ramal por enfriadora en servicio: un tercio del caudal, DN 150 a 1,79 m/s con el criterio de 2,0 m/s
    assert h["ramal_enfriadora"]["m_w"] == pytest.approx(h["m_w"] / 3.0)
    assert h["ramal_enfriadora"]["DN"] == 150
    assert h["ramal_enfriadora"]["v_real"] == pytest.approx(1.79, abs=0.01)
    # si una unidad trabajara a su capacidad nominal (988 kW, 5 K) el ramal necesitaria DN 200
    assert h["ramal_a_capacidad_nominal"]["m_w"] == pytest.approx(988.0 / (ah.CP_W * P["dT_aguahelada"]))
    assert h["ramal_a_capacidad_nominal"]["DN"] == 200
    assert h["ramal_a_capacidad_nominal"]["v_real"] <= p["v_agua"]


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
    assert a["n_unidades"] == 4
    assert a["A_total"] == pytest.approx(4 * 49.0)                           # 196 m2
    assert a["peso_total_kN"] == pytest.approx(4 * a["peso_unidad_kN"])
    assert a["q_kN_m2"] == pytest.approx(2.40, abs=0.005)                    # la carga por unidad no cambia con la cantidad
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
    # supuestos de la configuracion 3+1 y de la planta tipo
    for k in ("n_serv", "n_res", "orientacion", "calle", "nucleo_planta", "distribucion_planta", "circulacion"):
        assert eq.SUPUESTOS[k]["estado"] == "SUPUESTO", k
    assert (eq.SUPUESTOS["n_serv"]["valor"], eq.SUPUESTOS["n_res"]["valor"]) == (3, 1)
    assert eq.SUPUESTOS["orientacion"]["valor"] == "norte arriba" and eq.SUPUESTOS["calle"]["valor"] == "sur"
    tabla = eq.tabla_supuestos_md()
    assert tabla.count("\n") == len(eq.SUPUESTOS) + 1


def test_justificacion_de_n_serv_y_n_res_cita_numeros_que_coinciden_con_el_calculo():
    """Las justificaciones son texto fijo: si cambia el modelo o el catalogo, este test avisa que hay que reescribirlas."""
    e = R["enfriadoras"]
    j10, j11 = eq.SUPUESTOS["n_serv"]["justificacion"], eq.SUPUESTOS["n_res"]["justificacion"]
    assert eq.coma(2 * p["cap_enf"]) in j10                                    # 1.976 kW
    assert eq.coma(e["Q_L"]) in j10 and eq.coma(e["Q_L"]) in j11               # 1.987 kW
    assert eq.coma(e["alt_2mas1"]["faltante_kW"], 1) in j10                    # 11,2 kW
    assert eq.coma(e["alt_2mas1"]["faltante_rel"] * 100, 1) in j10             # 0,6 %
    assert eq.coma(e["carga_relativa_unidad"] * 100) in j10                    # 67 %
    assert str(e["alt_2mas1"]["req_unidad_redondeada"]) in j10                 # 994 kW
    assert "1102" in j10 and "sobredimensionada" in j10
    assert eq.coma(e["cap_una_parada"]) in j11                                 # 2.964 kW
    assert eq.coma(e["margen_una_parada_rel"] * 100) in j11                    # 49 %
    assert "bombas" in j11 and "34" in j11 and "35" in j11


# ---------------------------------------------------------------- planta tipo
PL = R["planta"]


def _inter(a, b):
    return max(0.0, min(a[2], b[2]) - max(a[0], b[0])) * max(0.0, min(a[3], b[3]) - max(a[1], b[1]))


def _comparten_borde(a, b, tol=1e-9):
    """True si dos rectangulos se tocan a lo largo de un segmento de longitud positiva."""
    if abs(a[2] - b[0]) < tol or abs(b[2] - a[0]) < tol:
        if min(a[3], b[3]) - max(a[1], b[1]) > tol:
            return True
    if abs(a[3] - b[1]) < tol or abs(b[3] - a[1]) < tol:
        if min(a[2], b[2]) - max(a[0], b[0]) > tol:
            return True
    return False


def test_planta_tipo_es_un_rectangulo_4_a_3_con_la_superficie_bruta_de_un_nivel():
    assert PL["W"] * PL["H"] == pytest.approx(P["A_cub"] / 3.0, rel=1e-12)
    assert PL["W"] / PL["H"] == pytest.approx(4.0 / 3.0, rel=1e-12)
    assert PL["W"] == pytest.approx(90.3, abs=0.05) and PL["H"] == pytest.approx(67.7, abs=0.05)
    assert PL["A_nivel"] == pytest.approx(6117.3, abs=0.05)


@pytest.mark.parametrize("n", [1, 2])
def test_planta_tipo_las_zonas_llenan_el_nivel_sin_huecos_ni_solapes(n):
    nv = PL["niveles"][n]
    rects = [r for b in nv["bloques"] for r in b["rects"]]
    # la suma de las areas dibujadas coincide con la superficie bruta del nivel (tolerancia 0,5 %)
    total = sum(b["area_dibujada"] for b in nv["bloques"])
    assert total == pytest.approx(PL["A_nivel"], rel=5e-3)
    assert total == pytest.approx(PL["W"] * PL["H"], rel=1e-9)
    for i, r in enumerate(rects):
        assert -1e-9 <= r[0] < r[2] <= PL["W"] + 1e-9 and -1e-9 <= r[1] < r[3] <= PL["H"] + 1e-9
        for q in rects[i + 1:]:
            assert _inter(r, q) < 1e-6                                          # sin solapes
    # cada bloque mide los m2 del modelo (tolerancia 0,5 %)
    for b in nv["bloques"]:
        assert b["area_dibujada"] == pytest.approx(b["area_modelo"], rel=5e-3), b["id"]
    # cada zona suma sus m2 de niveles()
    por_zona = {}
    for b in nv["bloques"]:
        if b["zona"]:
            por_zona[b["zona"]] = por_zona.get(b["zona"], 0.0) + b["area_dibujada"]
    esperado = {g: a for g, a, _t in R["niveles"]["niveles"][n - 1]["zonas"]}
    assert set(por_zona) == set(esperado)
    for g, a in esperado.items():
        assert por_zona[g] == pytest.approx(a, rel=5e-3), g
    nuc = next(b for b in nv["bloques"] if b["id"] == "NUCLEO")
    assert nuc["area_dibujada"] == pytest.approx(R["niveles"]["niveles"][n - 1]["no_clim"], rel=5e-3)


def test_planta_tipo_nucleo_en_la_esquina_sudeste_del_lado_de_la_calle_y_mismo_lugar_en_los_dos_pisos():
    nucs = [next(b for b in PL["niveles"][n]["bloques"] if b["id"] == "NUCLEO")["rects"][0] for n in (1, 2)]
    assert nucs[0] == pytest.approx(nucs[1])
    x0, y0, x1, y1 = nucs[0]
    assert y0 == pytest.approx(0.0) and x1 == pytest.approx(PL["W"])           # toca el borde sur (calle) y el este
    assert (x1 - x0) * (y1 - y0) == pytest.approx(917.6, abs=0.05)
    nuc = PL["nucleo"]
    assert nuc["n_shafts"] == R["shafts"]["n_shafts_agrupados"] == 14
    assert nuc["area_shafts"] == pytest.approx(14 * p["area_shaft"])
    assert nuc["area_shafts"] < nuc["area"]                                     # los shafts caben en el nucleo


def test_planta_tipo_zonas_criticas_contiguas_al_nucleo_y_asignacion_por_piso():
    bl2 = {b["id"]: b for b in PL["niveles"][2]["bloques"]}
    nuc = bl2["NUCLEO"]["rects"][0]
    assert _comparten_borde(bl2["G1"]["rects"][0], nuc) and _comparten_borde(bl2["G2"]["rects"][0], nuc)
    assert _comparten_borde(bl2["G1"]["rects"][0], bl2["G2"]["rects"][0])
    assert {b["zona"] for b in PL["niveles"][2]["bloques"] if b["zona"]} == {"G1", "G2", "G3", "G5"}
    assert {b["zona"] for b in PL["niveles"][1]["bloques"] if b["zona"]} == {"G4", "G5"}
    # internacion en dos alas de igual superficie
    assert bl2["G3-sur"]["area_dibujada"] == pytest.approx(bl2["G3-norte"]["area_dibujada"]) == pytest.approx(A_ZONAS["G3"] / 2.0)
    assert PL["niveles"][2]["utas_criticas"] == {"G1": 6, "G2": 1}
    # 1.er piso: el ingreso cae sobre los consultorios y el acceso de guardia sobre G4, los dos sobre el borde sur
    bl1 = {b["id"]: b for b in PL["niveles"][1]["bloques"]}
    g5 = bl1["G5"]["rects"][0]
    assert g5[0] < PL["niveles"][1]["ingreso_x"] < g5[2]
    assert any(r[1] < 1e-9 and r[0] < PL["niveles"][1]["acceso_guardia_x"] < r[2] for r in bl1["G4"]["rects"])
    assert "3.er piso" in PL["nota_3er_piso"]


def test_planta_tipo_falla_con_claridad_si_las_superficies_no_entran():
    c = copy.deepcopy(C)
    c["P"]["f_acond"] = 0.75
    with pytest.raises(ValueError):
        eq.planta_tipo(c)


# ---------------------------------------------------------------- figuras
def test_la_figura_se_genera_sin_textos_superpuestos(tmp_path):
    from calculo import figuras_plano as fp
    ruta = fp.fig_plano(C, R, ruta=str(tmp_path / "plano.png"))
    assert (tmp_path / "plano.png").stat().st_size > 50_000
    assert ruta == str(tmp_path / "plano.png")
    assert fp.ULTIMOS_AVISOS == []


def test_la_figura_8_muestra_cuatro_enfriadoras_3_mas_1_con_huella_y_carga():
    from calculo import figuras_plano as fp
    import tempfile
    import os
    with tempfile.TemporaryDirectory() as d:
        fp.fig_plano(C, R, ruta=os.path.join(d, "plano.png"))
    textos = "\n".join(fp.ULTIMOS_TEXTOS)
    assert fp.ULTIMOS_AVISOS == []
    for n in ("C1", "C2", "C3", "C4"):
        assert n in fp.ULTIMOS_TEXTOS or any(t.startswith(n) for t in fp.ULTIMOS_TEXTOS), n
    assert "C4 (reserva)" in fp.ULTIMOS_TEXTOS and "C5" not in textos
    assert "3 en servicio" in textos and "+ 1 de reserva" in textos
    assert "4 unidades:" in textos
    assert "4 × 49 m² =" in textos and "196 m²" in textos
    assert "carga 2,4 kN/m²" in textos


def test_la_planta_tipo_se_genera_sin_textos_superpuestos_ni_fuera_de_la_figura(tmp_path):
    from calculo import figuras_plano as fp
    ruta = fp.fig_planta_tipo(C, R, ruta=str(tmp_path / "planta.png"))
    assert ruta == str(tmp_path / "planta.png")
    assert (tmp_path / "planta.png").stat().st_size > 50_000
    assert fp.ULTIMOS_AVISOS_PT == []                                          # ni superpuestos ni cortados
    textos = "\n".join(fp.ULTIMOS_TEXTOS_PT)
    for esperado in ("1.er piso", "2.º piso", "90,3 m", "67,7 m", "N", "Norte arriba", "20 m", "Escala gráfica", "Calle (supuesto)",
                     "Acceso de guardia", "Ingreso", "Núcleo técnico", "14 shafts", "G1 ×6", "G2 ×1", "3.er piso"):
        assert esperado in textos, esperado


def test_la_planta_tipo_dibuja_las_areas_proporcionales_a_los_m2(tmp_path):
    """Mide los rectangulos que realmente se dibujan: su superficie, en m2 a la escala del dibujo, coincide con la del nivel y con la de cada zona."""
    from calculo import figuras_plano as fp
    fp.fig_planta_tipo(C, R, ruta=str(tmp_path / "planta.png"))
    k = fp.ULTIMA_ESCALA_PT[0]
    assert k == pytest.approx(fp.PT_WP / PL["W"])
    for n in (1, 2):
        dib = {i: a for (nn, i, a) in fp.ULTIMAS_AREAS_PT if nn == n}
        assert sum(dib.values()) == pytest.approx(R["niveles"]["bruta_nivel"], rel=5e-3)
        for b in PL["niveles"][n]["bloques"]:
            assert dib[b["id"]] == pytest.approx(b["area_modelo"], rel=5e-3), (n, b["id"])
    # misma paleta que la figura 8
    assert fp.COLOR_ZONA["G1"] == "#c8aef4" and set(fp.COLOR_ZONA) == {"G1", "G2", "G3", "G4", "G5"}
