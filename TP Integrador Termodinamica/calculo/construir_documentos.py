"""Construye el informe tecnico y la memoria de calculo desde sus plantillas y el modelo.

Uso (desde la carpeta del proyecto):  python -m calculo.construir_documentos [--sin-pdf]
Lee:   informe/informe.plantilla.md y informe/memoria_calculo.plantilla.md
Escribe: informe/informe_tecnico.{md,docx,pdf} e informe/memoria_calculo.{md,docx,pdf}

Las plantillas usan {{nombre}} para un valor ya formateado y {{nombre_m}} para el mismo valor dentro de una ecuacion.
Las secciones que dependen de los modulos de exergia y de equipos se arman con calculo/texto_exergia.py y
calculo/texto_equipos.py (cada uno devuelve el Markdown del informe y el de la memoria).
"""
import copy
import os
import re
import subprocess
import sys

from . import construir_borrador as cbm
from . import estimacion as es
from . import mejoras as mj
from . import supuestos

RAIZ = cbm.RAIZ
INFORME = cbm.INFORME
n = cbm.n
tabla = cbm.tabla

DOCS = [("informe.plantilla.md", "informe_tecnico"), ("memoria_calculo.plantilla.md", "memoria_calculo")]


def _sens(J, nombre):
    d = [s["delta"] for s in J["sensibilidad"] if s["nombre"] == nombre]
    if len(d) != 1:
        sys.exit(f"falta la sensibilidad '{nombre}': correr python -m calculo.generar_resultados")
    return d[0]


def _fila_variacion(c, f, nd=1):
    """Variacion relativa de la energia final al aplicar f(c) (copia)."""
    base = es.resumen(c)["E_total"]
    c2 = copy.deepcopy(c)
    f(c2)
    return es.resumen(c2)["E_total"] / base - 1.0


def valores_nuevos(V, T):
    import json
    c = supuestos.defaults()
    P = c["P"]
    R = es.resumen(c)
    with open(os.path.join(INFORME, "resultados_consumo.json"), encoding="utf-8") as f:
        J = json.load(f)
    caud = R["diseno"]["caudales"]
    A = R["A"]

    # ---- superficies y decisiones del edificio
    V["A_nivel"] = n(P["A_cub"] / 3.0)
    V["f_g4_pct"] = n(P["f_g4_24h"] * 100)
    V["gross_per_bed"] = n(P["A_cub"] / (P["camas_gen"] + P["camas_uti"]))
    V["ref_bed_hospitecnia"] = "148"
    V["ref_bed_cruce"] = "157"
    pm = lambda x: n(abs(x) * 100, 1)
    V["sens_a_gen"] = pm(_fila_variacion(c, lambda c2: c2["P"].__setitem__("a_gen_cama", P["a_gen_cama"] + 6.0)))
    V["sens_a_or"] = pm(_fila_variacion(c, lambda c2: c2["P"].__setitem__("a_or", P["a_or"] + 6.0)))
    V["sens_a_uti"] = pm(_fila_variacion(c, lambda c2: c2["P"].__setitem__("a_uti_cama", P["a_uti_cama"] + 6.0)))
    V["sens_f_acond"] = pm(_sens(J, "Superficie climatizada 95 %"))
    V["sens_g4"] = pm(_sens(J, "Guardia, diagnostico y laboratorio: 50 % de las areas generales"))

    # ---- condiciones y renovaciones
    Z = c["Z"]
    V["T_G1"] = n(Z["G1"]["t_ver"])
    V["T_G2"] = n(Z["G2"]["t_ver"])
    V["qs_G1"] = n(Z["G1"]["q_s"])
    m_sens = caud["G1"]["m_sens"]
    V["m3h_load_G1"] = n(m_sens / P["rho_aire"] * 3600)
    V["ach_load_G1"] = n(m_sens / P["rho_aire"] * 3600 / (A["G1"] * P["h_techo"]), 1)
    V["ratio_norm_load"] = n(caud["G1"]["m_ach"] / m_sens, 1)
    V["s_oa_g1_6"] = "+" + pm(_fila_variacion(c, lambda c2: c2["Z"]["G1"].__setitem__("ach_oa", 6)))
    V["s_ach15"] = "−" + pm(_sens(J, "Quirofanos: 15 renovaciones totales"))
    V["s_ach25"] = "+" + pm(_sens(J, "Quirofanos: 25 renovaciones totales"))
    V["s_hr5"] = "+" + pm(_sens(J, "Humedad relativa de verano 5 puntos menos (todas las zonas)"))

    # ---- clima
    cl = c["clima"]
    V["T_ene_smn"], V["T_jul_smn"], V["T_dic_smn"] = "24,9", "11,0", "23,6"          # cita: SMN 1991-2020 via pagina que reproduce la tabla
    V["T_ene"], V["T_jul"], V["T_dic"] = n(cl["T"][0], 1), n(cl["T"][6], 1), n(cl["T"][11], 1)
    V["HR_smn"] = "68"
    V["HR_media"] = n(sum(h * d for h, d in zip(cl["HR"], cl["dias"])) / sum(cl["dias"]) * 100)
    V["s_hr4"] = pm(_fila_variacion(c, lambda c2: c2["clima"].__setitem__("HR", [h - 0.04 for h in c2["clima"]["HR"]])))

    # ---- ACS y sensibilidades para el texto
    V["s_acs55"] = "−" + pm(_sens(J, "ACS por cama: 55 L/dia"))
    V["s_acs200"] = "+" + pm(_sens(J, "ACS por cama: 200 L/dia"))
    V["s_ua30"] = pm(_sens(J, "Conductancia de la envolvente -30 %"))
    V["s_gi30"] = pm(_sens(J, "Ganancias internas -30 %"))
    V["s_g5_24h"] = "+" + pm(_sens(J, "Consultorios y administracion tambien funcionan 24 h"))
    V["s_tp2"] = "+" + pm(_sens(J, "Temperatura media mensual +2 K"))
    V["s_tm2"] = "−" + pm(_sens(J, "Temperatura media mensual -2 K"))

    # ---- mejoras y emisiones
    base, filas = mj.comparar(c)
    por = {f["clave"]: f for f in filas}
    for k in ("B", "M1", "M2", "M3", "M4", "M5", "P"):
        V["dE_" + k] = pm(por[k]["d_E"])
        V["dC_" + k] = pm(por[k]["d_co2"])
    bdet = por["B"]["detalle"]
    V["rec_MWh"] = n(bdet["q_rec_cond"] / 1e3)
    V["rec_horas"] = n(bdet["horas_rec"])
    V["ahorro_gas_B"] = n((base["E_PCS"] - bdet["E_PCS"]) / 1e3)
    V["extra_comp_B"] = n((bdet["elec"]["compresor"] - base["elec"]["compresor"]) / 1e3)
    for f_, k in ((0.75, "B75"), (0.5, "B50")):
        r = mj.anual_variante(c, {"rec_cond": {"f": f_}})
        V["dE_" + k] = pm(r["E_total"] / base["E_total"] - 1)
    V["T_agua_rec"] = n(mj.parametro("T_agua_rec"))
    V["T_cond_rec"] = n(mj.parametro("T_agua_rec") + mj.parametro("pinch_rec"))
    V["co2_t"] = n(base["co2_t"])
    V["co2_gas_t"] = n(base["co2_gas_t"])
    fco2_ = mj.factor_co2_gas(P)
    for ef, suf in ((0.29, "lo"), (0.40, "hi")):
        co2 = lambda r: r["E_PCI"] * fco2_ / 1000.0 + r["E_elec"] * ef / 1000.0
        V["dC_P_" + suf] = pm(co2(por["P"]["detalle"]) / co2(base) - 1)
        V["dC_B_" + suf] = pm(co2(por["B"]["detalle"]) / co2(base) - 1)
    V["co2_elec_t"] = n(base["co2_elec_t"])
    fco2 = mj.factor_co2_gas(P)
    pc = es.cb.poder_calorifico(P)
    V["co2_gas_kg"] = n(fco2, 3)
    V["co2_gas_GJ"] = n(fco2 / 3.6 * 1000, 1)
    V["co2_gas_pcs"] = n(fco2 * pc["PCI_kWh_m3"] / pc["PCS_kWh_m3"], 3)
    V["ef_elec"] = n(mj.parametro("ef_elec"), 2)
    V["solar_frac"] = n(por["M2"]["detalle"]["solar_kWh"] / por["M2"]["detalle"]["q_acs"] * 100)
    V["A_solar"] = n(mj.parametro("A_solar"))
    V["kWp"] = n(mj.parametro("kWp_fv"))
    V["fv_MWh"] = n(por["M5"]["detalle"]["fv_kWh"] / 1e3)
    V["fv_yield"] = n(mj.parametro("GHI_anual") * mj.parametro("PR_fv"))
    V["eps_rec"] = n(mj.parametro("eps_rec"), 2)
    V["lat"] = n(mj.parametro("lat"), 1)
    V["GHI"] = n(mj.parametro("GHI_anual"))
    _H, Kt = mj.irradiacion_mensual(mj.parametro("lat"), mj.parametro("GHI_anual"))
    V["Kt"] = n(Kt, 2)
    cd = mj.caldera_condensacion(P, mj.parametro("T_gases_cond"))
    V["T_gases_cond"] = n(mj.parametro("T_gases_cond"))
    V["frac_cond_cald"] = n(cd["frac_cond"] * 100)
    V["eta_cond_PCI"] = n(cd["eta_PCI"] * 100, 1)
    V["eta_cond_PCS"] = n(cd["eta_PCS"] * 100, 1)
    V["eta_PCS_base"] = V["eta_PCS"]

    # refrigerantes
    ref = {r["refrigerante"]: r for r in mj.refrigerantes(c)}
    V["cop_134"] = n(ref["R134a"]["cop_elec"], 2)
    V["cop_ze"] = n(ref["R1234ze(E)"]["cop_elec"], 2)
    V["caida_qvol"] = n((1 - ref["R1234ze(E)"]["q_vol"] / ref["R134a"]["q_vol"]) * 100)
    V["mas_compresor"] = n((ref["R134a"]["q_vol"] / ref["R1234ze(E)"]["q_vol"] - 1) * 100)
    V["cop_catalogo"] = n(988.0 / 288.2, 2)

    # tests
    out = subprocess.run([sys.executable, "-m", "pytest", "calculo/tests", "-q", "-p", "no:cacheprovider"], cwd=RAIZ, capture_output=True, text=True).stdout
    m = re.search(r"(\d+) passed", out)
    V["n_tests"] = m.group(1) if m else "?"

    # ---- tablas
    nombres = {"B": ("Alternativa B: recuperar el calor del condensador",
                     "Aprovecha el calor que se rechaza a {T_cond_min} a {T_cond_anual_max} °C (hasta {T_cond_rec} °C cuando recupera) en vez de quemar gas en una llama de {T_llama} °C; cuesta trabajo extra del compresor"),
               "M1": ("M1. Caldera de condensación",
                      "Los gases salen a {T_gases_cond} °C, por debajo del rocío ({T_rocio} °C): condensa el {frac_cond_cald} % del agua formada y recupera su calor latente; el rendimiento sobre PCS pasa de {eta_PCS_base} a {eta_cond_PCS} %"),
               "M2": ("M2. Solar térmico para el ACS",
                      "{A_solar} m² de colectores cubren el {solar_frac} % del calor del ACS, una demanda constante de {acs_kW} kW medios que el sol atiende bien"),
               "M3": ("M3. Recuperador del aire de extracción",
                      "Precalienta o preenfría el aire exterior con el que sale, sin mezclar las corrientes (circuito de agua, efectividad {eps_rec}); solo trabaja cuando conviene (bypass)"),
               "M4": ("M4. Ventiladores con 20 % menos de presión",
                      "La potencia del ventilador es proporcional a la presión; pero el calor que ya no cede al aire hay que reponerlo con gas, por eso el ahorro neto es chico"),
               "M5": ("M5. Fotovoltaica de {kWp} kWp",
                      "Produce {fv_MWh} MWh por año ({fv_yield} kWh por kWp) que descuentan electricidad de la red; no depende del resto del sistema"),
               "P": ("Paquete B + M1 a M5", "Combinación de todas; no es la suma, porque las medidas se pisan")}
    filas = []
    for k in ("B", "M5", "M2", "M3", "M1", "M4", "P"):
        f = por[k]
        nm, porque = nombres[k]
        filas.append((nm.format(**V), porque.format(**V),
                      f"−{n(-f['d_E'] * 100, 1)} % ({n((base['E_total'] - f['E_total']) / 1e3)} MWh)",
                      f"−{n(-f['d_co2'] * 100, 1)} % ({n(base['co2_t'] - f['co2_t'])} t)"))
    T["tabla_mejoras"] = tabla(["Medida", "Por qué ahorra", "Energía final", "CO₂"], filas, (20, 48, 16, 16))
    det = [base_fila(base)] + [por[k] for k in ("B", "M1", "M2", "M3", "M4", "M5", "P")]
    nom_det = {"A": "A. Caso base", "B": "B. Recuperación del condensador", "M1": "M1. Caldera de condensación", "M2": "M2. Solar térmico para el ACS",
               "M3": "M3. Recuperador del aire de extracción", "M4": "M4. Ventiladores, 20 % menos de presión", "M5": "M5. Fotovoltaica",
               "P": "Paquete B + M1 a M5"}
    T["tabla_mejoras_detalle"] = tabla(
        ["Variante", "Energía final [MWh]", "Electricidad [MWh]", "Gas (PCS) [MWh]", "CO₂ [t]", "Energía", "CO₂"],
        [(nom_det[f["clave"]], n(f["E_total"] / 1e3), n(f["E_elec"] / 1e3), n(f["E_PCS"] / 1e3), n(f["co2_t"]),
          ("–" if f["clave"] == "A" else "−" + n(-f["d_E"] * 100, 1) + " %"), ("–" if f["clave"] == "A" else "−" + n(-f["d_co2"] * 100, 1) + " %"))
         for f in det], (34, 12, 12, 12, 9, 9, 9))
    T["tabla_params_mejoras"] = tabla(["ID", "Parámetro", "Valor", "Unidad", "Nivel", "Respaldo"],
                                      [(i, nom, supuestos._fmt(v) if not isinstance(v, str) else v, u, e, j) for (i, _k, nom, v, u, e, j) in mj.PARAMETROS],
                                      (5, 28, 8, 9, 12, 38))
    # tabla corta de sensibilidad para el informe
    S = sorted(J["sensibilidad"], key=lambda s: -abs(s["delta"]))
    sel = [s for s in S if s["nombre"].startswith(("Humedad relativa de verano 5", "Consultorios y administracion tambien", "Ventilador sin calor",
                                                     "ACS por cama: 200", "Cambio de estacion a 21", "Temperatura media mensual +2"))]
    T["tabla_sens_corta"] = tabla(["Variación de un supuesto", "Energía final [MWh/año]", "Diferencia"],
                                  [(cbm.NOMBRES_SENS.get(s["nombre"], s["nombre"]), n(s["E_total_kWh"] / 1e3), ("+" if s["delta"] > 0 else "−") + n(abs(s["delta"]) * 100, 1) + " %")
                                   for s in sel], (62, 18, 12))
    return V, T


def base_fila(base):
    return dict(clave="A", nombre="Alternativa A: caso base", E_total=base["E_total"], E_elec=base["E_elec"], E_PCS=base["E_PCS"],
                co2_t=base["co2_t"], d_E=0.0, d_co2=0.0)


def render(plantilla, salida, V, T, extra=None):
    with open(os.path.join(INFORME, plantilla), encoding="utf-8") as f:
        s = f.read()
    extra = extra or {}
    for k, v in extra.items():
        s = s.replace(k, v)

    def sub(m):
        k = m.group(1)
        if k in T:
            return T[k]
        mat = k.endswith("_m") and k[:-2] in V
        base = k[:-2] if mat else k
        if base not in V:
            sys.exit(f"Falta el valor {{{{{k}}}}} en {plantilla}")
        v = V[base]
        if mat:
            v = v.replace(",", "\\text{,}").replace(".", "\\,")
        return v

    out = re.sub(r"\{\{(\w+)\}\}", sub, s)
    pend = re.findall(r"<<[A-Z0-9_]+>>", out)
    if pend:
        print("aviso: quedan marcadores sin reemplazar en", plantilla, ":", sorted(set(pend)))
    partes = re.split(r"(\$\$.*?\$\$|\$[^$\n]*?\$)", out, flags=re.S)
    unidades = r"(%|°C|K|kW|kWh|MWh|kg|kJ|kPa|Pa|m²|m³|kcal|kmol|h|L|t)(?![A-Za-záéíóúñÁÉÍÓÚÑ])"
    for i in range(0, len(partes), 2):
        partes[i] = re.sub(r"(\d) " + unidades, "\\1\u00a0\\2", partes[i])
    out = "".join(partes)
    md = os.path.join(INFORME, salida + ".md")
    with open(md, "w", encoding="utf-8") as f:
        f.write(out)
    return md


def a_docx_pdf(salida, pdf=True):
    md = os.path.join(INFORME, salida + ".md")
    docx = os.path.join(INFORME, salida + ".docx")
    subprocess.run(["pandoc", md, "-o", docx, "--from", "markdown+pipe_tables+tex_math_dollars+yaml_metadata_block", "--columns=30",
                    "--resource-path", RAIZ + ":" + INFORME], check=True, cwd=INFORME)
    from . import estilo_docx
    estilo_docx.aplicar(docx)
    if pdf:
        cbm.MD, cbm.DOCX, cbm.PDF = md, docx, os.path.join(INFORME, salida + ".pdf")
        cbm.a_pdf()


def secciones_agentes(V, T, c):
    """Texto de exergia y de equipos (informe y memoria), si los modulos de redaccion existen."""
    extra_inf, extra_mem = {}, {}
    try:
        from . import texto_exergia
        inf, mem, vv = texto_exergia.redactar(c, V, T)
        V.update(vv)
        extra_inf["<<EXERGIA>>"], extra_mem["{{seccion_exergia_memoria}}"] = inf, mem
        extra_inf["<<RESUMEN_EXERGIA>>"] = vv.get("_resumen", "")
        extra_inf["<<CONCL3>>"] = vv.get("_concl3", "")
    except ImportError:
        pass
    try:
        from . import texto_equipos
        inf, mem, vv = texto_equipos.redactar(c, V, T)
        V.update(vv)
        extra_inf["<<EQUIPOS>>"], extra_mem["{{seccion_equipos_memoria}}"] = inf, mem
    except ImportError:
        pass
    return extra_inf, extra_mem


def main():
    V, T = cbm.valores()
    V, T = valores_nuevos(V, T)
    c = supuestos.defaults()
    extra_inf, extra_mem = secciones_agentes(V, T, c)
    pdf = "--sin-pdf" not in sys.argv
    for (plantilla, salida), extra in zip(DOCS, (extra_inf, extra_mem)):
        render(plantilla, salida, V, T, extra)
        a_docx_pdf(salida, pdf)
        print("escrito:", salida)


if __name__ == "__main__":
    main()
