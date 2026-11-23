"""Tablas y valores propios de la version corta del informe (todo sale del modelo, nada se tipea).

Los llama construir_documentos.secciones_agentes. Las claves llevan el sufijo _inf para no chocar con las de la memoria.
"""
from . import aire_humedo as ah
from . import edificio as ed
from . import estimacion as es
from . import exergia as xg
from . import mejoras as mj
from . import refrigeracion as rf
from . import supuestos
from . import referencias as rfr
from .construir_borrador import n, tabla


def _c(c):
    P = c["P"]
    R = es.resumen(c)
    d = R["diseno"]
    return P, R, d


def valores_informe(c, V, T):
    P, R, d = _c(c)
    caud = d["caudales"]
    r = d["verano"]["G1"]
    m = caud["G1"]["m_sup"]
    h_C = r["h_mix"]
    h_D = ah.entalpia(r["T_c"], r["W_c"])
    h_f = 4.186 * r["T_c"]
    q_chequeo = m * ((h_C - h_D) - (r["W_mix"] - r["W_c"]) * h_f)
    assert abs(q_chequeo - r["Q_coil"]) < 0.05, "la ecuacion de la serpentina no reproduce el modelo"
    cic = rf.ciclo(P["T_ev"], d["planta"]["T_cond"], P["refrigerante"], P["sobrecal"], P["subenf"], P["eta_is"], P["eta_motor"])
    W = d["Q_L"] / cic["cop_elec"]
    Qc = d["Q_L"] + P["eta_motor"] * W
    sens = sum(v["Q_coil_sens"] for v in d["verano"].values())
    lat = sum(v["Q_coil_lat"] for v in d["verano"].values())
    an = es.anual(c)
    base, filas = mj.comparar(c)
    por = {f["clave"]: f for f in filas}
    B = por["B"]["detalle"]
    frio = an["serp_total"]
    v = {
        # serpentina del quirofano (zona G1)
        "inf_m": n(m, 2), "inf_hC": n(h_C, 2), "inf_hD": n(h_D, 2), "inf_wC": n(r["W_mix"], 5), "inf_wD": n(r["W_c"], 5),
        "inf_hf": n(h_f, 1), "inf_TD": n(r["T_c"], 1), "inf_dw_g": n((r["W_mix"] - r["W_c"]) * 1000, 2),
        # ciclo
        "inf_qL": n(cic["q_L"], 2), "inf_w": n(cic["w"], 2), "inf_W": n(W), "inf_Qc": n(Qc), "inf_COP": n(cic["cop_elec"], 3),
        "inf_Tev": n(P["T_ev"]), "inf_Tc": n(d["planta"]["T_cond"]),
        # necesidades
        "inf_sens": n(sens), "inf_lat": n(lat), "inf_lat_pct": n(lat / (sens + lat) * 100),
        "inf_cal_MWh": n(an["q_cal"] / 1e3), "inf_acs_MWh": n(an["q_acs"] / 1e3), "inf_acs_punta": n(2 * d["acs"]["kW"]),
        "inf_frio_MWh": n(frio / 1e3),
        # combustion
        "inf_q_util_MWh": n(an["q_util_total"] / 1e3),
        "inf_dw": n(r["W_mix"] - r["W_c"], 5),
        "inf_etaPCS": n(an["eta_caldera"] * es.cb.poder_calorifico(P)["PCI_kWh_m3"] / es.cb.poder_calorifico(P)["PCS_kWh_m3"], 4),
        # A contra B
        "inf_COP_B": n(frio / B["elec"]["compresor"], 2),
        "inf_Qcond_B": n(B["planta"]["Q_cond"] / 1e3),   # ya neto de lo que se recupera (4.198 + 0,94 x 81 - 499)
        "inf_m3_A": n(R["V_gas_m3"] / 1e3), "inf_m3_B": n(R["V_gas_m3"] * B["E_PCS"] / base["E_PCS"] / 1e3),
        "inf_E_B": n(B["E_total"] / 1e3), "inf_E_A": n(base["E_total"] / 1e3),
        "inf_iB": n(B["E_total"] / P["A_cub"]), "inf_iA": n(base["E_total"] / P["A_cub"]),
        "inf_elecB": n(B["E_elec"] / 1e3), "inf_gasB": n(B["E_PCS"] / 1e3), "inf_co2B": n(B["co2_t"]),
        "inf_gas_ahorro_pct": n((1 - B["E_PCS"] / base["E_PCS"]) * 100),
    }
    return v


def V_to_float(s):
    return float(s.replace(".", "").replace(",", "."))


def tablas_informe(c, V, T):
    P, R, d = _c(c)
    caud = d["caudales"]
    A = R["A"]
    Z = c["Z"]
    M = rfr.marca
    an = es.anual(c)
    base, filas = mj.comparar(c)
    por = {f["clave"]: f for f in filas}
    B = por["B"]["detalle"]
    t = {}

    # ---------------------------------------------------------------- los cuatro temas y como se conectan
    t["tabla_temas_inf"] = tabla(["Tema", "Qué resuelve en este sistema", "Qué recibe y qué entrega"], [
        ("Aire húmedo", "Cuánto frío y cuánto calor necesita el aire de cada zona: se enfría para quitarle vapor y se recalienta para impulsarlo",
         "Recibe el clima y las consignas; entrega la carga de la serpentina (frío) y del recalentador (calor)"),
        ("Refrigeración", "La enfriadora (ciclo de compresión de R134a) que vence la carga de las serpentinas",
         f"Recibe esa carga; entrega el trabajo del compresor, el COP y el calor que rechaza el condensador ({V['Q_cond_MWh']} MWh por año)"),
        ("Combustión", "La caldera de gas que entrega el calor de recalentamiento, calefacción y agua caliente",
         "Recibe ese calor útil; entrega el consumo de gas, los gases de escape y el CO₂"),
        ("Exergía", "Dónde se destruye capacidad de producir trabajo y por qué conviene aprovechar el calor del condensador",
         "Recibe los resultados de los tres temas; entrega la destrucción por equipo y la eficiencia exergética"),
    ], (13, 45, 42))

    # ---------------------------------------------------------------- datos del edificio
    t["tabla_datos_inf"] = tabla(["Dato", "Valor", "Cómo lo obtuvimos"], [
        ("Superficie cubierta", f"{V['A_cub']} m²", f"Cifra oficial de Presidencia {M('presidencia')} y la gacetilla {M('gacetilla')}; el intendente habló de «más de 20.000 m²» sin aclarar si es cubierta"),
        ("Camas", f"{V['camas_gen']} + {V['camas_uti']} = {V['camas_tot']}", f"La gacetilla {M('gacetilla')} las atribuye a cuidados progresivos y las tomamos como el total (Presidencia {M('presidencia')} prevé 160 de internación)"),
        ("Quirófanos", V["n_or"], f"Cifra de programa {M('presidencia')}"),
        ("Niveles", f"3 de {V['A_nivel']} m²", f"Presidencia {M('presidencia')} lista tres pisos (guardia y consultorios; internación y áreas críticas; administración); suponemos tres iguales (supuesto)"),
        ("Superficie climatizada", f"{V['f_acond']} % ({V['A_cond']} m²)", "Supuesto: se excluyen locales técnicos, morgue y depósitos"),
    ], (20, 17, 63))

    # ---------------------------------------------------------------- zonas: superficie, consigna y renovaciones
    def ach(g):
        return V_to_float(n(caud[g]["m_sup"] / P["rho_aire"] * 3600 / (A[g] * P["h_techo"]), 1))
    filas = [
        ("G1 Quirófanos", f"{n(A['G1'])} = {V['n_or']} × {V['a_or']}: la FGI {M('fgi')} exige al menos 37,2 m² libres; sumamos equipamiento fijo (supuesto)",
         f"{n(Z['G1']['t_ver'])} °C; {n(Z['G1']['hr_ver'] * 100)} %", f"{Z['G1']['ach_tot']} / {Z['G1']['ach_oa']}", f"ASHRAE 170 {M('ashrae170')}", "Continuo"),
        ("G2 Terapia intensiva", f"{n(A['G2'])} = {V['camas_uti']} camas × {V['a_uti']} m²: 9 m² por cama {M('res748')} × 2,7 por apoyo y circulación (supuesto)",
         f"{n(Z['G2']['t_ver'])} °C; {n(Z['G2']['hr_ver'] * 100)} %", f"{Z['G2']['ach_tot']} / {Z['G2']['ach_oa']}", f"ASHRAE 170 {M('ashrae170')}, a contrastar", "Continuo"),
        ("G3 Internación", f"{n(A['G3'])} = {V['camas_gen']} camas × {V['a_gen']} m² (supuesto: habitación con baño, office y circulaciones)",
         f"{n(Z['G3']['t_ver'])} °C; {n(Z['G3']['hr_ver'] * 100)} %", f"{Z['G3']['ach_tot']} / {Z['G3']['ach_oa']} (resulta {n(ach('G3'), 1)})", f"ASHRAE 170, habitación de pacientes {M('ashrae170')}", "Continuo"),
        ("G4 Guardia, imágenes, laboratorio", f"{n(A['G4'])} = {V['f_g4_pct']} % de las áreas generales (supuesto; la gacetilla {M('gacetilla')} da guardia 24 h)",
         f"{n(Z['G4']['t_ver'])} °C; {n(Z['G4']['hr_ver'] * 100)} %", f"{Z['G4']['ach_tot']} / {Z['G4']['ach_oa']}",
         "Promedio ponderado (supuesto): 0,25·12 espera y triage + 0,05·15 shock + 0,70·6 imágenes y laboratorio ≈ 8", "24 h"),
        ("G5 Consultorios y administración", f"{n(A['G5'])}: el resto de la superficie climatizada",
         f"{n(Z['G5']['t_ver'])} °C; {n(Z['G5']['hr_ver'] * 100)} %", f"{Z['G5']['ach_tot']} / {Z['G5']['ach_oa']} (resulta {n(ach('G5'), 1)})", "Supuesto, sin contrastar con la norma", "12 h, lunes a viernes"),
    ]
    t["tabla_zonas_inf"] = tabla(["Zona", "Superficie [m²] y cómo se obtiene", "Consigna de verano", "Renovaciones totales / de aire exterior [1/h]", "De dónde salen", "Horario"],
                                 filas, (13, 31, 10, 13, 22, 11))

    # ---------------------------------------------------------------- que tiene que dar el sistema
    inv_t = sorted({Z[g]["t_inv"] for g in Z})
    t["tabla_nec_inf"] = tabla(["Uso", "Condición que debe cumplir", "Potencia de diseño", "Energía anual"], [
        ("Frío (serpentinas)", f"Llevar el aire exterior ({V['T_ext_ver']} °C, {V['W_ext_ver']} g/kg) a las consignas de verano de la tabla de zonas",
         f"{V['Q_L_dis']} kW ({V['inf_sens']} sensibles y {V['inf_lat']} latentes, {V['inf_lat_pct']} % latente; {V['Q_L_dis_wm2']} W/m²)", f"{V['inf_frio_MWh']} MWh"),
        ("Recalentamiento", "Subir el aire que sale frío de la serpentina hasta la temperatura de impulsión", f"{V['Q_recal_ver']} kW en el diseño; hasta {n(xg.estados_de_analisis(c)['max_recalentamiento']['condiciones']['Q_recal_kW'])} kW en diciembre, de noche", f"{V['q_recal_MWh']} MWh"),
        ("Calefacción del aire", f"Consignas de invierno de {n(inv_t[0])} a {n(inv_t[-1])} °C con exterior a {n(P['T_inv'])} °C y {n(P['HR_inv'] * 100)} % de humedad",
         f"{V['Q_cal_inv_aire']} kW, más {V['Q_hum_inv']} kW de vapor para humidificar", f"{V['inf_cal_MWh']} MWh (la humidificación anual no se modela)"),
        ("Agua caliente sanitaria", f"Calentar el agua de red de {n(P['T_agua_red'])} a {n(P['T_acs'])} °C, {V['L_cama']} L por cama y día", f"{V['acs_kW']} kW medios ({V['inf_acs_punta']} de punta)", f"{V['inf_acs_MWh']} MWh"),
    ], (16, 36, 30, 18))

    # ---------------------------------------------------------------- A contra B
    t["tabla_ab_inf"] = tabla(["Indicador", "A (base)", "B (recupera el calor del condensador)"], [
        ("Energía final por año", f"{V['E_total_MWh']} MWh ({V['i_cub']} kWh/m²)", f"{V['inf_E_B']} MWh ({V['inf_iB']} kWh/m²): −{V['dE_B']} %"),
        ("Electricidad y gas (PCS)", f"{V['E_elec_MWh']} y {V['E_gas_MWh']} MWh", f"{V['inf_elecB']} y {V['inf_gasB']} MWh"),
        ("Gas natural", f"unos {V['inf_m3_A']} mil m³", f"unos {V['inf_m3_B']} mil m³ (−{V['inf_gas_ahorro_pct']} %)"),
        ("CO₂ por año", f"{V['co2_t']} t", f"{V['inf_co2B']} t: −{V['dC_B']} %"),
        ("COP anual del compresor", V["COP_est_comp"], V["inf_COP_B"]),
        ("Calor que se tira al ambiente", f"{V['Q_cond_MWh']} MWh", f"{V['inf_Qcond_B']} MWh"),
        ("Ventajas", "Simple y probada; es la referencia", "Usa un calor que hoy se tira y evita quemar gas; no agrega combustible ni equipos de combustión"),
        ("Limitaciones", f"Quema gas para recalentar mientras tira {V['Q_cond_MWh']} MWh de calor",
         f"El condensador trabaja más caliente ({V['T_cond_rec']} °C) y el compresor gasta {V['extra_elec_B']} MWh más; hay que coordinar calor y demanda ({V['dE_B75']} % si coinciden el 75 % del tiempo); necesita una enfriadora con recuperación"),
    ], (22, 30, 48))

    # ---------------------------------------------------------------- mejoras
    def fila_m(clave, nombre, principio):
        f = por[clave]
        return (nombre, principio, f"−{n(-f['d_E'] * 100, 1)} % ({n((base['E_total'] - f['E_total']) / 1e3)} MWh)", f"−{n(-f['d_co2'] * 100, 1)} % ({n(base['co2_t'] - f['co2_t'])} t)")

    t["tabla_mejoras_inf"] = tabla(["Medida", "Por qué mejora (principio termodinámico)", "Energía", "CO₂"], [
        fila_m("B", "B. Recuperar el calor del condensador",
               f"El calor que rechaza el condensador a {V['T_cond_min']}–{V['T_cond_anual_max']} °C vale poco como exergía y alcanza para agua a {V['T_agua_rec']} °C: sustituye gas que se quema con una llama teórica de {V['T_llama']} °C. Cuesta trabajo del compresor (condensa a {V['T_cond_rec']} °C)"),
        fila_m("M5", f"Fotovoltaica de {V['kWp']} kWp",
               f"Convierte radiación en electricidad (exergía pura) y desplaza la de la red: {V['fv_MWh']} MWh por año a {V['ef_elec']} t CO₂/MWh"),
        fila_m("M2", f"Solar térmico de {V['A_solar']} m² para el ACS",
               f"El agua a {n(P['T_acs'])} °C es calor de baja exergía: el sol lo entrega sin quemar gas y cubre el {V['solar_frac']} % de la demanda del ACS"),
        fila_m("M3", "Recuperador del aire de extracción",
               f"El aire que sale del edificio (unos 22 °C) precalienta o preenfría el aire exterior sin mezclarse (efectividad {V['eps_rec']}): baja la carga de la serpentina y del recalentador"),
        fila_m("M1", "Caldera de condensación",
               f"Con gases a {V['T_gases_cond']} °C, por debajo del rocío ({V['T_rocio']} °C), condensa el vapor de la combustión y recupera su calor latente: el rendimiento sobre PCS pasa de {V['eta_PCS_base']} a {V['eta_cond_PCS']} %"),
        ("M4 y M6. Ventiladores con 20 % menos de presión; quirófanos al 50 % del caudal de noche",
         "La potencia de un ventilador crece con el cubo del caudal: menos caudal sin actividad ahorra mucho más que lo que se pierde; detalle en la memoria",
         f"−{V['dE_M4']} % y −{V['dE_M6']} %", f"−{V['dC_M4']} % y −{V['dC_M6']} %"),
        fila_m("P", "Paquete B + M1 a M6", "No es la suma: el aporte de cada medida depende de las demás (con B, la caldera de condensación ahorra menos)"),
    ], (20, 52, 14, 14))
    return t
