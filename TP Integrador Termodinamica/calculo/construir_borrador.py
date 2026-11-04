"""Construye el borrador del informe desde el modelo (ninguna cifra se copia a mano).

Uso (desde la carpeta del proyecto):  python -m calculo.construir_borrador [--sin-pdf]
Lee:   informe/borrador_proyecto.plantilla.md, informe/resultados_consumo.json, figuras/*.png
Escribe: informe/borrador_proyecto.md, .docx (ecuaciones nativas de Word) y .pdf (HTML con MathML impreso con Chromium)

La plantilla usa {{nombre}} para un valor ya formateado (coma decimal, punto de miles) y {{nombre_m}} para el
mismo valor dentro de una ecuacion LaTeX. Si falta un valor, el script se detiene.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

from . import aire_humedo as ah
from . import combustion as cb
from . import edificio as ed
from . import estimacion as es
from . import generar_resultados as gr
from . import refrigeracion as rf
from . import supuestos

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INFORME = os.path.join(RAIZ, "informe")
PLANTILLA = os.path.join(INFORME, "borrador_proyecto.plantilla.md")
MD = os.path.join(INFORME, "borrador_proyecto.md")
DOCX = os.path.join(INFORME, "borrador_proyecto.docx")
PDF = os.path.join(INFORME, "borrador_proyecto.pdf")
CSS = os.path.join(INFORME, "estilo_borrador.css")


def n(x, nd=0):
    return gr.n(x, nd)


# nombres de la sensibilidad con tildes (el modelo los escribe sin tildes)
NOMBRES_SENS = {
    "Humedad relativa de verano 5 puntos menos (todas las zonas)": "Humedad máxima de verano 5 puntos menor en todas las zonas",
    "Consultorios y administracion tambien funcionan 24 h": "Consultorios y administración funcionan también las 24 h",
    "Ventilador sin calor en el aire (sin calor de ventilador)": "Sin calor del ventilador en el aire",
    "ACS por cama: 200 L/dia": "ACS de 200 L por cama y día (en vez de 100)",
    "ACS por cama: 55 L/dia": "ACS de 55 L por cama y día",
    "Temperatura media mensual +2 K": "Temperatura media mensual +2 K",
    "Temperatura media mensual -2 K": "Temperatura media mensual −2 K",
    "Guardia, diagnostico y laboratorio: 50 % de las areas generales": "Guardia, diagnóstico y laboratorio: 50 % de las áreas generales",
    "Guardia, diagnostico y laboratorio: 20 % de las areas generales": "Guardia, diagnóstico y laboratorio: 20 % de las áreas generales",
    "Humedad relativa media -8 puntos": "Humedad relativa media del clima −8 puntos",
    "Superficie climatizada 95 %": "Superficie climatizada 95 % de la cubierta",
    "Superficie climatizada 75 %": "Superficie climatizada 75 % de la cubierta",
    "Humedad maxima de verano 60 % en quirofanos, terapia intensiva e internacion": "Humedad máxima de verano 60 % en quirófanos, terapia intensiva e internación",
}

# supuestos principales para el anexo: id -> (nombre con tildes, unidad con simbolos)
ANEXO = [
    ("E1", "Superficie cubierta total", "m²"), ("E2", "Fracción de la superficie cubierta que se climatiza", "–"),
    ("E3", "Camas de internación general", "camas"), ("E4", "Camas de terapia intensiva", "camas"),
    ("E5", "Cantidad de quirófanos", "–"), ("E10", "Conductancia de la envolvente por m² de piso expuesto", "W/(m² K)"),
    ("E14", "Fracción de las áreas generales que funciona las 24 h", "–"),
    ("C1", "Temperatura de bulbo seco de diseño, verano", "°C"), ("C2", "Temperatura de bulbo húmedo coincidente, verano", "°C"),
    ("C3", "Temperatura de bulbo seco de diseño, invierno", "°C"), ("C4", "Humedad relativa de diseño, invierno", "–"),
    ("C6", "Amplitud diaria de temperatura", "K"),
    ("A1", "Temperatura mínima del aire de impulsión", "°C"), ("A3", "Humedad relativa a la salida de la serpentina", "–"),
    ("A5", "Rendimiento total de los ventiladores", "–"), ("A8", "Fracción de la potencia del ventilador que se disipa como calor en el aire", "–"),
    ("R1", "Refrigerante", "–"), ("R2", "Temperatura de evaporación", "°C"), ("R5", "Rendimiento isentrópico del compresor", "–"),
    ("R6", "Rendimiento del motor del compresor", "–"), ("R7", "Diferencia entre condensación y temperatura exterior", "K"),
    ("R8", "Temperatura mínima de condensación", "°C"),
    ("B1", "Gas natural: metano (fracción molar)", "–"), ("B6", "Relación de aire (1 = estequiométrico)", "–"),
    ("B7", "Temperatura de los gases de escape", "°C"),
    ("S1", "Consumo de ACS por cama y día", "L/(cama día)"), ("S2", "Temperatura del ACS", "°C"),
    ("S3", "Temperatura del agua fría de entrada", "°C"), ("S4", "Factor por pérdidas de acumulación y recirculación", "–"),
]


def _fmt_valor(v):
    if isinstance(v, str):
        return v
    return supuestos._fmt(v)


def tabla(cab, filas, anchos):
    """Tabla de pipes con anchos relativos dados por la cantidad de guiones."""
    sep = "|" + "|".join("-" * a for a in anchos) + "|"
    out = ["| " + " | ".join(cab) + " |", sep]
    for f in filas:
        out.append("| " + " | ".join(str(x) for x in f) + " |")
    return "\n".join(out)


def valores():
    c = supuestos.defaults()
    P = c["P"]
    R = es.resumen(c)
    with open(os.path.join(INFORME, "resultados_consumo.json"), encoding="utf-8") as f:
        J = json.load(f)
    if abs(J["E_total_kWh"] - R["E_total"]) > 1e-6 * R["E_total"]:
        sys.exit("resultados_consumo.json no coincide con el modelo: correr python -m calculo.generar_resultados")
    d, an = R["diseno"], R["anual"]
    caud = d["caudales"]
    A = R["A"]
    V = {}
    T = {}

    # ---- edificio
    V["A_cub"] = n(P["A_cub"])
    V["A_cond"] = n(R["a_cond"])
    V["f_acond"] = n(P["f_acond"] * 100)
    V["camas_gen"] = n(P["camas_gen"])
    V["camas_uti"] = n(P["camas_uti"])
    V["camas_tot"] = n(P["camas_gen"] + P["camas_uti"])
    V["n_or"] = n(P["n_or"])

    # ---- zonas
    Z = c["Z"]
    operacion = {"G1": "Continuo; actividad de día", "G2": "Continuo", "G3": "Continuo", "G4": "24 h", "G5": "12 h, lunes a viernes"}
    nombres = {"G1": "G1 Quirófanos", "G2": "G2 Terapia intensiva", "G3": "G3 Internación general",
               "G4": "G4 Guardia, imágenes y laboratorio", "G5": "G5 Consultorios, administración y docencia"}
    filas = []
    for g in ("G1", "G2", "G3", "G4", "G5"):
        z = Z[g]
        m3h = caud[g]["m_sup"] / P["rho_aire"] * 3600
        m3h_oa = caud[g]["m_oa"] / P["rho_aire"] * 3600
        filas.append((nombres[g], n(A[g]), f"{n(z['t_ver'])} °C; {n(z['hr_ver'] * 100)} %", f"{n(z['ach_tot'])} / {n(z['ach_oa'])}",
                      n(m3h), n(m3h_oa), operacion[g]))
    T["tabla_zonas"] = tabla(["Zona", "Superficie [m²]", "Consigna de verano", "Renovaciones totales / de aire exterior [1/h]",
                              "Caudal de impulsión [m³/h]", "Aire exterior [m³/h]", "Funcionamiento"], filas, (22, 9, 12, 14, 11, 10, 18))
    V["m_sup_G1"] = n(caud["G1"]["m_sup"], 2)
    V["m3h_G1"] = n(caud["G1"]["m_sup"] / P["rho_aire"] * 3600)

    # ---- resultado principal
    V["E_total_MWh"] = n(R["E_total"] / 1e3)
    V["E_elec_MWh"] = n(R["E_elec"] / 1e3)
    V["E_gas_MWh"] = n(R["E_gas_PCS"] / 1e3)
    V["V_gas_mil"] = n(round(R["V_gas_m3"], -3))
    V["i_cub"] = n(R["i_total_cub"])
    V["i_cub1"] = n(R["i_total_cub"], 1)
    V["i_elec"] = n(R["i_elec_cub"])
    V["i_gas"] = n(R["i_gas_cub"])
    V["i_cond"] = n(R["i_total_cond"])
    V["frac_gas"] = n(R["frac_gas"] * 100)
    V["frac_elec"] = n((1 - R["frac_gas"]) * 100)
    V["Q_L_dis"] = n(d["Q_L"])
    V["Q_L_dis_wm2"] = n(d["Q_L"] * 1000 / P["A_cub"])
    V["W_comp_dis"] = n(d["planta"]["W_comp"])
    V["T_cond_dis"] = n(d["planta"]["T_cond"])
    V["Q_recal_ver"] = n(d["Q_recal_verano"])
    V["Q_cal_inv"] = n(d["Q_caldera_invierno"])
    V["acs_kW"] = n(d["acs"]["kW"])
    V["COP_est_comp"] = n(R["cop_estacional"], 2)
    elec, k = an["elec"], R["E_gas_PCS"] / an["q_util_total"]
    usos = [("Ventiladores de las unidades de tratamiento de aire", elec["ventiladores"], "Electricidad"),
            ("Compresor de la enfriadora", elec["compresor"], "Electricidad"),
            ("Recalentamiento después de la serpentina", an["q_recal"] * k, "Gas"),
            ("Agua caliente sanitaria", an["q_acs"] * k, "Gas"),
            ("Calefacción del aire", an["q_cal"] * k, "Gas"),
            ("Ventiladores del condensador", elec["vent_condensador"], "Electricidad"),
            ("Bombas de agua helada", elec["bombas"], "Electricidad")]
    T["tabla_usos"] = tabla(["Uso final", "Energético", "MWh/año", "% del total", "kWh/m²·año"],
                            [(u, e, n(v / 1e3), n(v / R["E_total"] * 100, 1) + " %", n(v / P["A_cub"], 1)) for u, v, e in usos]
                            + [("**Total**", "", f"**{n(R['E_total'] / 1e3)}**", "100 %", f"**{n(R['i_total_cub'], 1)}**")], (44, 14, 12, 12, 12))
    V["MWh_vent"] = n(elec["ventiladores"] / 1e3)
    V["pct_vent"] = n(elec["ventiladores"] / R["E_total"] * 100, 1)
    V["MWh_comp"] = n(elec["compresor"] / 1e3)
    V["pct_comp"] = n(elec["compresor"] / R["E_total"] * 100, 1)
    V["MWh_recal_gas"] = n(an["q_recal"] * k / 1e3)
    V["pct_recal_gas"] = n(an["q_recal"] * k / R["E_total"] * 100, 1)
    V["MWh_acs_gas"] = n(an["q_acs"] * k / 1e3)
    V["MWh_vcond"] = n(elec["vent_condensador"] / 1e3)
    V["MWh_bombas"] = n(elec["bombas"] / 1e3)
    V["q_recal_MWh"] = n(an["q_recal"] / 1e3)
    V["q_total_MWh"] = n(an["q_util_total"] / 1e3)
    V["pct_recal_util"] = n(an["q_recal"] / an["q_util_total"] * 100)
    V["Q_cond_MWh"] = n(J["Q_cond_kWh"] / 1e3)
    V["Q_cond_sobre_recal"] = n(J["Q_cond_kWh"] / an["q_recal"], 1)
    V["frio_MWh"] = n(J["frio_entregado_kWh"] / 1e3)
    V["COP_planta"] = n(J["frio_entregado_kWh"] / (elec["compresor"] + elec["vent_condensador"] + elec["bombas"]), 2)
    V["EFLH"] = n(J["frio_entregado_kWh"] / d["Q_L"])
    mes = {m["mes"]: m for m in an["mensual"]}
    V["frio_ene"] = n(mes["ene"]["Q_L"] / 1e3)
    V["frio_jul"] = n(mes["jul"]["Q_L"] / 1e3)
    V["calor_ene"] = n(mes["ene"]["Q_cal"] / 1e3)
    V["calor_dic"] = n(mes["dic"]["Q_cal"] / 1e3)
    V["calor_jul"] = n(mes["jul"]["Q_cal"] / 1e3)
    V["dT_dia"] = n(P["rango_diario"] / 2, 1)
    V["dT_cond"] = n(P["dT_cond"])
    V["T_cond_min"] = n(P["T_cond_min"])
    V["f_vent_cond"] = n(P["f_vent_cond"] * 100, 1)
    V["dT_ah"] = n(P["dT_aguahelada"])
    V["dP_bomba"] = n(P["dP_bomba"] / 1e3)
    V["HR_serp"] = n(P["HR_serp"] * 100)
    for g, k in (("CH4", "gas_CH4"), ("C2H6", "gas_C2H6"), ("C3H8", "gas_C3H8"), ("N2", "gas_N2"), ("CO2", "gas_CO2")):
        V["gas_" + g] = n(P[k], 2)
    V["ach_G1"] = n(c["Z"]["G1"]["ach_tot"])
    V["ach_G2"] = n(c["Z"]["G2"]["ach_tot"])
    V["ach_G4"] = n(c["Z"]["G4"]["ach_tot"])
    fr = [x[1] for x in gr.REF["PART"]]
    V["part_min"] = n(min(fr) * 100)
    V["part_max"] = n(max(fr) * 100)
    V["eq_min"] = n(J["total_equivalente_edificio"]["min"])
    V["eq_max"] = n(J["total_equivalente_edificio"]["max"])

    # ---- sensibilidad
    S = sorted(J["sensibilidad"], key=lambda s: -abs(s["delta"]))
    faltan = [s["nombre"] for s in S[:12] if s["nombre"] not in NOMBRES_SENS]
    if faltan:
        sys.exit(f"Faltan nombres con tildes para la sensibilidad: {faltan}")
    T["tabla_sens"] = tabla(["Variación de un supuesto (los demás quedan en su valor base)", "Energía final [MWh/año]", "Diferencia"],
                            [(NOMBRES_SENS[s["nombre"]], n(s["E_total_kWh"] / 1e3), ("+" if s["delta"] > 0 else "−") + n(abs(s["delta"]) * 100, 1) + " %")
                             for s in S[:12]], (62, 16, 12))
    Es = [s["E_total_kWh"] / P["A_cub"] for s in J["sensibilidad"]]
    V["sens_min"] = n(min(Es))
    V["sens_max"] = n(max(Es))

    # ---- caso detallado: quirofano en verano pico
    Tv, Wv = ed.estado_exterior_verano(c)
    r = ed.proceso(c, "G1", caud, Tv, Wv, 1.0, P["q_sol_pico"])
    z = Z["G1"]
    W_set = ah.w_desde_hr(r["T_r"], z["hr_ver"], P["presion"])
    est = [("A", "Aire exterior", Tv, Wv), ("B", "Local (consigna)", r["T_r"], W_set), ("C", "Mezcla con retorno", r["T_mix"], r["W_mix"]),
           ("D", "Salida de la serpentina", r["T_c"], r["W_c"]), ("E", "Tras el recalentador", r["T_obj"], r["W_c"]),
           ("F", "Impulsión (tras el ventilador)", r["T_sup"], r["W_c"])]
    T["tabla_psicro"] = tabla(["Estado", "Descripción", "T [°C]", "ω [g/kg]", "h [kJ/kg]", "HR [%]"],
                              [(a, b, n(t, 1), n(w * 1000, 2), n(ah.entalpia(t, w), 1), n(ah.hr_desde_w(t, w, P["presion"]) * 100)) for a, b, t, w in est],
                              (8, 36, 12, 12, 14, 10))
    V["T_ext_ver"] = n(Tv)
    V["Tbh_ver"] = n(P["T_bh_ver"])
    V["W_ext_ver"] = n(Wv * 1000, 1)
    V["Q_serp_G1"] = n(r["Q_coil"], 1)
    V["Q_sens_G1"] = n(r["Q_coil_sens"], 1)
    V["Q_lat_G1"] = n(r["Q_coil_lat"], 1)
    V["Q_recal_G1"] = n(r["Q_recal"], 1)
    V["T_mix_G1"] = n(r["T_mix"], 1)
    V["T_c_G1"] = n(r["T_c"], 1)
    V["T_obj_G1"] = n(r["T_obj"], 1)
    V["T_sup_G1"] = n(r["T_sup"], 1)
    V["dT_vent_G1"] = n(r["dT_vent"], 1)
    V["calor_vent_G1"] = n(r["calor_vent"], 1)
    V["oa_G1"] = n(caud["G1"]["m_oa"] / caud["G1"]["m_sup"] * 100)

    # ---- ciclo de refrigeracion
    cic = rf.ciclo(P["T_ev"], d["planta"]["T_cond"], P["refrigerante"], P["sobrecal"], P["subenf"], P["eta_is"], P["eta_motor"])
    p_ev, p_c = cic["P_ev"] / 1e3, cic["P_c"] / 1e3
    T["tabla_ciclo"] = tabla(["Estado", "Descripción", "T [°C]", "P [kPa]", "h [kJ/kg]"],
                             [("1", "Salida del evaporador (vapor sobrecalentado 5 K)", n(cic["T1"], 1), n(p_ev), n(cic["h1"], 1)),
                              ("2s", "Salida del compresor, isentrópica", "–", n(p_c), n(cic["h2s"], 1)),
                              ("2", f"Salida del compresor, real (rendimiento isentrópico {n(P['eta_is'], 2)})", n(cic["T2"], 1), n(p_c), n(cic["h2"], 1)),
                              ("3", "Salida del condensador (subenfriado 4 K)", n(cic["T3"], 1), n(p_c), n(cic["h3"], 1)),
                              ("4", f"Salida de la válvula de expansión (título {n(cic['x4'], 2)})", n(P["T_ev"], 1), n(p_ev), n(cic["h4"], 1))],
                             (8, 50, 12, 12, 14))
    V["p_ev"] = n(p_ev)
    V["p_c"] = n(p_c)
    V["q_L_ref"] = n(cic["q_L"], 1)
    V["w_ref"] = n(cic["w"], 1)
    V["q_H_ref"] = n(cic["q_H"], 1)
    V["cop_eje"] = n(cic["cop_comp"], 2)
    V["cop_elec"] = n(cic["cop_elec"], 2)
    V["cop_carnot"] = n(cic["cop_carnot"], 2)
    V["eta_carnot"] = n(cic["cop_elec"] / cic["cop_carnot"] * 100)
    V["m_ref"] = n(d["Q_L"] / cic["q_L"], 1)
    V["T_ev"] = n(P["T_ev"])
    V["T2_ref"] = n(cic["T2"])

    # ---- combustion
    cal = cb.caldera(P)
    pc, bal = cal["pc"], cal["balance"]
    prod, reac = bal["productos"], bal["reactivos"]
    V["o2_reac"] = n(reac["O2"], 3)
    V["n2_aire"] = n(reac["N2_aire"], 3)
    V["co2_prod"] = n(prod["CO2"], 3)
    V["h2o_prod"] = n(prod["H2O"], 3)
    V["n2_prod"] = n(prod["N2"], 3)
    V["o2_prod"] = n(prod["O2"], 3)
    V["aire_st"] = n(bal["o2_estequiometrico"] * (1 + 79 / 21), 3)
    V["lambda"] = n(P["lambda_aire"], 2)
    V["exceso"] = n((P["lambda_aire"] - 1) * 100)
    V["PCS_kcal"] = n(pc["PCS_kcal_m3"])
    V["PCS_kWh"] = n(pc["PCS_kWh_m3"], 3)
    V["PCI_kWh"] = n(pc["PCI_kWh_m3"], 3)
    V["PCS_PCI"] = n(pc["relacion_PCS_PCI"], 3)
    V["eta_PCI"] = n(cal["eta_PCI"] * 100, 1)
    V["eta_PCS"] = n(cal["eta_PCS"] * 100, 1)
    V["q_gases"] = n(cal["q_gases"] * 100, 1)
    V["y_H2O"] = n(cal["y_H2O"] * 100, 1)
    V["T_rocio"] = n(cal["T_rocio"], 1)
    V["T_gases"] = n(P["T_gases"])
    V["T_llama"] = n(J["T_llama_adiabatica"])
    V["gas_m3_kWh"] = n(1 / (cal["eta_PCI"] * pc["PCI_kWh_m3"]), 4)

    # ---- referencias
    ref = gr.REF
    T["tabla_ref"] = tabla(["Referencia", "kWh/m²·año", "Observación"],
                           [("Garrahan (CABA), HCWH 2021", n(ref["AR"][0][1]), "Edificio completo, estimado por auditoría"),
                            ("CEMAR (Rosario), HCWH 2021", n(ref["AR"][1][1]), "Edificio completo, estimado por auditoría"),
                            ("Giordano (San Juan), HCWH 2021", n(ref["AR"][2][1]), "Edificio completo, estimado por auditoría"),
                            ("23 hospitales internacionales (Hospitecnia)", f"mediana {n(ref['INT']['mediana'])}; rango {n(ref['INT']['minimo'])} a {n(ref['INT']['maximo'])}", "Edificio completo"),
                            ("Modelo español del artículo (Hospitecnia)", f"{n(ref['ES_final'][0])} a {n(ref['ES_final'][1])}", "Energía final, edificio completo"),
                            ("**Este modelo, solo sistema térmico**", f"**{n(R['i_total_cub'])}**", f"Equivale a {n(J['total_equivalente_edificio']['min'])} a {n(J['total_equivalente_edificio']['max'])} para el edificio completo")],
                           (40, 26, 34))

    # ---- anexo: supuestos principales
    base = {i: (v, e) for (i, _k, _n, v, _u, e, _f) in supuestos._FILAS}
    filas_anexo = []
    for i, nom, uni in ANEXO:
        v, e = base[i]
        filas_anexo.append((i, nom, _fmt_valor(v), uni, e))
    T["tabla_anexo"] = tabla(["ID", "Parámetro", "Valor", "Unidad", "Estado"], filas_anexo, (6, 58, 12, 12, 12))
    estados = [e for (*_x, e, _f) in supuestos._FILAS]
    V["n_filas"] = n(len(estados))
    V["n_dato"] = n(estados.count("DATO"))
    V["n_supuesto"] = n(estados.count("SUPUESTO"))
    V["n_const"] = n(estados.count("CONSTANTE"))
    V["n_anexo"] = n(len(ANEXO))

    return V, T


def render(V, T):
    with open(PLANTILLA, encoding="utf-8") as f:
        s = f.read()
    usados = set()

    def sub(m):
        k = m.group(1)
        if k in T:
            usados.add(k)
            return T[k]
        mat = k.endswith("_m") and k[:-2] in V
        base = k[:-2] if mat else k
        if base not in V:
            sys.exit(f"Falta el valor {{{{{k}}}}} en la plantilla")
        usados.add(base)
        v = V[base]
        if mat:
            v = v.replace(",", "\\text{,}").replace(".", "\\,")
        return v

    out = re.sub(r"\{\{(\w+)\}\}", sub, s)
    sin_usar = sorted((set(V) | set(T)) - usados)
    if sin_usar:
        print("aviso: valores calculados que la plantilla no usa:", ", ".join(sin_usar))
    with open(MD, "w", encoding="utf-8") as f:
        f.write(out)
    return out


def a_docx():
    cmd = ["pandoc", MD, "-o", DOCX, "--from", "markdown+pipe_tables+tex_math_dollars+yaml_metadata_block", "--columns=30",
           "--resource-path", RAIZ + ":" + INFORME]
    subprocess.run(cmd, check=True, cwd=INFORME)
    from . import estilo_docx
    estilo_docx.aplicar(DOCX)


def _chrome():
    for c in (os.environ.get("CHROME"), "/opt/pw-browsers/chromium", shutil.which("google-chrome"), shutil.which("chromium"),
              shutil.which("chromium-browser")):
        if c and os.path.exists(c):
            return c
    return None


def a_pdf():
    """PDF por HTML con MathML impreso con Chromium (LibreOffice sin el modulo Math no dibuja las ecuaciones del DOCX)."""
    chrome = _chrome()
    if chrome is None:
        print("aviso: no hay Chromium; el PDF sale de LibreOffice y no trae las ecuaciones")
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", INFORME, DOCX], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return
    with tempfile.TemporaryDirectory() as td:
        html = os.path.join(td, "borrador.html")
        subprocess.run(["pandoc", MD, "-o", html, "--standalone", "--embed-resources", "--mathml", "--columns=30",
                        "--css", CSS, "-V", "document-css=false", "--resource-path", RAIZ + ":" + INFORME], check=True, cwd=INFORME)
        subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={PDF}", "file://" + html], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    V, T = valores()
    render(V, T)
    a_docx()
    if "--sin-pdf" not in sys.argv:
        a_pdf()
    print("escrito:", os.path.relpath(MD, RAIZ))


if __name__ == "__main__":
    main()
