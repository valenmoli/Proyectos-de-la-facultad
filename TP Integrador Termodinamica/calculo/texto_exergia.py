"""Redaccion de la seccion de exergia (informe y memoria) desde calculo/exergia.py."""
from . import exergia as ex
from .construir_borrador import n, tabla


def _g(r, nombre_inicio):
    for k, v in r["destruccion_grupos"].items():
        if k.startswith(nombre_inicio):
            return v
    raise KeyError(nombre_inicio)


def _pct(x, tot):
    return n(x / tot * 100, 1)


def redactar(c, V, T):
    E = ex.estados_de_analisis(c)
    a, b = E["verano_pico"]["resultado"], E["max_recalentamiento"]["resultado"]
    ga, gb = a["global"], b["global"]
    ea, eb = a["enfriadora"], b["enfriadora"]
    ca, cbb = a["caldera"], b["caldera"]
    cond_b = E["max_recalentamiento"]["condiciones"]
    sens = ex.sensibilidad_T0(c)
    fila = lambda r, clave: [t for t in r["tabla"] if t["clave"] == clave][0]
    ta, tb = {t["clave"]: t for t in a["tabla"]}, {t["clave"]: t for t in b["tabla"]}

    v = {
        "ex_in_a": n(ga["X_in"]), "ex_el_a": n(ga["X_elec"]), "ex_gas_a": n(ga["X_comb"]),
        "ex_in_b": n(gb["X_in"]), "ex_el_b": n(gb["X_elec"]), "ex_gas_b": n(gb["X_comb"]),
        "ex_D_a": n(ga["D_total"] / ga["X_in"] * 100, 1), "ex_D_b": n(gb["D_total"] / gb["X_in"] * 100, 1),
        "ex_P_a": n(ga["P_total"] / ga["X_in"] * 100, 1), "ex_P_b": n(gb["P_total"] / gb["X_in"] * 100, 1),
        "ex_eta_a": n(ga["eta_global"] * 100, 1) if ga["eta_global"] is not None else "no definida",
        "ex_T0_a": n(E["verano_pico"]["condiciones"]["T_out"], 1), "ex_T0_b": n(cond_b["T_out"], 1), "ex_mes_b": cond_b["mes"],
        "ex_recal_b": n(cond_b["Q_recal_kW"]),
        "ex_enf_a": n((_g(a, "Compresor") + _g(a, "Condensador")) / ga["X_in"] * 100, 1),
        "ex_vent_a": n(_g(a, "Ventiladores") / ga["X_in"] * 100, 1),
        "ex_comp_a": n(_g(a, "Compresor") / ga["X_in"] * 100, 1),
        "ex_cvev_a": n(_g(a, "Condensador") / ga["X_in"] * 100, 1),
        "ex_aire_a": n(_g(a, "Tratamiento") / ga["X_in"] * 100, 1),
        "ex_cal_a": n(_g(a, "Caldera") / ga["X_in"] * 100, 1),
        "ex_cal_b": n(_g(b, "Caldera") / gb["X_in"] * 100, 1),
        "ex_calD_b": n(cbb["D_total"] / _g(b, "Caldera") * 100) if False else n(tb["caldera"]["X_dest"] / gb["D_total"] * 100, 1),
        "ex_eta_enf_comp": n(ea["eta_compresor_grupo"] * 100, 1), "ex_eta_enf_planta": n(ea["eta_planta"] * 100, 1),
        "ex_frio": n(ea["X_frio"], 1), "ex_fcarnot": n(ea["T0_sobre_Tcw_menos_1"] * 100, 1), "ex_Tcw": n(ea["T_cw"] - 273.15, 1),
        "ex_eta_cal_a": n(ca["eta_ex"] * 100, 1), "ex_eta_cal_b": n(cbb["eta_ex"] * 100, 1),
        "ex_comb_pci": n(ca["ex_comb_sobre_PCI"], 3),
        "ex_cal_comb_a": n(ca["D_combustion"] / ca["X_comb"] * 100, 1), "ex_cal_transf_a": n(ca["D_transferencia"] / ca["X_comb"] * 100, 1),
        "ex_cal_comb_b": n(cbb["D_combustion"] / cbb["X_comb"] * 100, 1), "ex_cal_transf_b": n(cbb["D_transferencia"] / cbb["X_comb"] * 100, 1),
        "ex_recal_D_b": n(tb["recalentador"]["X_dest"], 1),
        "ex_sens_D": n(max(abs(s["D_total"] - sens[0]["D_total"]) / sens[0]["D_total"] for s in sens) * 100, 1),
    }
    V.update(v)

    # ---------------------------------------------------------- tabla del informe (por grupo)
    grupos = list(a["destruccion_grupos"].keys())
    nombre_grupo = {"Compresor y motor": "Compresor y motor", "Condensador, válvula y evaporador": "Condensador, válvula y evaporador",
                    "Ventiladores y bombas": "Ventiladores y bombas (con sus pérdidas de carga)", "Tratamiento del aire": "Mezcla, serpentina y recalentador",
                    "Caldera y ACS": "Caldera y ACS"}
    filas = [("**Exergía que entra** (electricidad más gas)", f"**{n(ga['X_in'])}**", "100", f"**{n(gb['X_in'])}**", "100")]
    filas.append(("Exergía útil (aire tratado y ACS)", n(ga["P_total"]), _pct(ga["P_total"], ga["X_in"]), n(gb["P_total"]), _pct(gb["P_total"], gb["X_in"])))
    filas.append(("Pérdidas al ambiente (condensado, aire del condensador, gases)", n(ga["L_total"]), _pct(ga["L_total"], ga["X_in"]), n(gb["L_total"]), _pct(gb["L_total"], gb["X_in"])))
    for g in grupos:
        filas.append(("Destruida en: " + nombre_grupo.get(g, g), n(a["destruccion_grupos"][g]), _pct(a["destruccion_grupos"][g], ga["X_in"]),
                      n(b["destruccion_grupos"][g]), _pct(b["destruccion_grupos"][g], gb["X_in"])))
    filas.append(("**Destruida en total**", f"**{n(ga['D_total'])}**", f"**{_pct(ga['D_total'], ga['X_in'])}**", f"**{n(gb['D_total'])}**", f"**{_pct(gb['D_total'], gb['X_in'])}**"))
    t_inf = tabla(["Exergía [kW]", f"Verano pico (exterior {v['ex_T0_a']} °C): kW", "%", f"Máximo recalentamiento ({v['ex_mes_b']}, noche, {v['ex_T0_b']} °C): kW", "%"],
                  filas, (46, 18, 8, 20, 8))

    inf = f"""**Qué calculamos y con qué criterio.** Para cada equipo planteamos exergía que entra (F), exergía útil que entrega (P), pérdida al ambiente (L) y exergía destruida (D), con F = P + L + D, en kW. Tomamos como **estado muerto el aire exterior** de cada caso (lo que el ambiente da gratis) y analizamos dos casos con la misma función: el **verano pico** (exterior a {v['ex_T0_a']} °C, el que dimensiona la enfriadora) y el **momento del año con más recalentamiento** (diciembre, de noche, exterior a {v['ex_T0_b']} °C, con {v['ex_recal_b']} kW de recalentamiento). Entre los dos se ven las dos mitades del sistema. La exergía química del gas es {v['ex_comb_pci']} veces su PCI, con exergías químicas estándar que **recordamos** y hay que cotejar con el libro de la cátedra. La figura 6 muestra el reparto con sus cifras; el balance por equipo está en la memoria.

![Figura 6. Reparto de la exergía que entra a cada caso entre exergía útil, pérdidas al ambiente y destrucción por grupo de equipos (kW y % de la entrada).](../figuras/fig07_exergia.png){{width=12.5cm}}

1. **Casi toda la exergía se destruye**: {v['ex_D_a']} % en el verano pico y {v['ex_D_b']} % en el recalentamiento. En climatización es lo esperable: el sistema trabaja con calor y frío a temperaturas cercanas a la del ambiente, que valen poco en exergía.
2. **En el verano pico manda la enfriadora y su entorno.** El compresor con su motor ({v['ex_comp_a']} %), el condensador, la válvula y el evaporador ({v['ex_cvev_a']} %) destruyen el {v['ex_enf_a']} % de lo que entra, y los ventiladores y bombas con sus pérdidas de carga otro {v['ex_vent_a']} %. La eficiencia exergética de la enfriadora es de **{v['ex_eta_enf_comp']} %** contando el compresor ({v['ex_eta_enf_planta']} % con ventiladores del condensador y bombas) aunque su COP de {V['cop_elec']} sea alto: el frío de agua a {v['ex_Tcw']} °C con exterior a {v['ex_T0_a']} °C vale solo el {v['ex_fcarnot']} % de su energía en exergía.
3. **En el recalentamiento manda la caldera** (aire y ACS). Destruye el {v['ex_calD_b']} % de lo destruido y su eficiencia exergética es de **{v['ex_eta_cal_b']} %**: el {v['ex_cal_comb_b']} % del combustible se destruye en la combustión (llama adiabática teórica de {V['T_llama']} °C) y el {v['ex_cal_transf_b']} % al pasar el calor al agua a 80/60 °C. **Se quema un combustible cuya llama adiabática teórica es de {V['T_llama']} °C (calculada, sin disociación) para subir el aire unos kelvin.** El calor de 32 a 46 °C que la enfriadora rechaza (32 a 41 °C en los estados medios del año) vale poco en exergía, igual que el que pide el recalentamiento: por eso la alternativa B es buena también desde la Segunda Ley. El {v['ex_cal_transf_b']} % que se destruye al pasar el calor depende del agua a 80/60 °C que supusimos para una caldera convencional; con un circuito de 50/40 °C esa fracción baja, y eso refuerza el argumento de B.
4. **Hay que leer las eficiencias con cuidado.** La global del verano pico es de {v['ex_eta_a']} %, pero en el recalentamiento no se puede definir: el aire sale casi con la misma exergía con que entra. Si se cambia el estado muerto, la destrucción total varía menos de {v['ex_sens_D']} % y el equipo que más destruye no cambia, pero los rangos de eficiencia sí.
"""

    # ---------------------------------------------------------- memoria
    def t_equipos(r, titulo):
        tot = r["global"]["D_total"]
        filas = []
        for t in r["tabla"]:
            filas.append((t["equipo"], n(t["X_in"], 1), n(t["X_util"], 1), n(t["X_perdida"], 1), n(t["X_dest"], 1), n(t["X_dest"] / tot * 100, 1),
                          "–" if t["eta_ex"] is None else n(t["eta_ex"] * 100, 1) + " %"))
        return tabla(["Equipo", "F [kW]", "P [kW]", "L [kW]", "D [kW]", "% de D", "η exergética"], filas, (34, 9, 9, 9, 9, 9, 13))

    filas_s = [(n(s["T0"], 1), n(s["D_total"]), n(s["P_total"], 1), n(s["L_total"]),
                "no definida" if s["eta_global"] is None else n(s["eta_global"] * 100, 1) + " %", n(s["eta_enfriadora"] * 100, 1) + " %",
                n(s["eta_caldera"] * 100, 1) + " %") for s in sens]
    t_sens = tabla(["T0 [°C]", "D total [kW]", "P total [kW]", "L total [kW]", "η global", "η planta de frío (compresor, ventiladores del condensador y bombas)", "η caldera"], filas_s, (10, 14, 14, 14, 14, 16, 14))
    mem = f"""## 8.1 Método

Para cada equipo se plantea el esquema combustible–producto–pérdida, $\\dot X_F = \\dot X_P + \\dot X_L + \\dot X_D$, en kW. El **estado muerto** es el del aire exterior de cada caso ($T_0$, $\\omega_0$, $P_0$ = 101,325 kPa). Exergía de flujo y del calor:

$$\\dot X = \\dot m\\,[(h - h_0) - T_0\\,(s - s_0)], \\qquad \\dot X_Q = \\dot Q\\,\\left(1 - \\frac{{T_0}}{{T}}\\right), \\qquad \\dot X_D = T_0\\,\\dot S_{{gen}}$$

Para el aire húmedo se usa la expresión por kg de aire seco como mezcla de gases ideales, con término térmico $(c_{{p,a}} + \\omega\\,c_{{p,v}})\\,T_0\\,(T/T_0 - 1 - \\ln T/T_0)$ y término de mezcla en función de $\\omega$ y $\\omega_0$; vale 0 en el estado muerto y es no negativa. La exergía del condensado incluye el término químico respecto del vapor ambiente, $R_v T_0 \\ln(p_{{sat}}(T_0)/p_{{v0}})$, unos 102 kJ/kg a 34 °C y 48 % de humedad (sin él la destrucción de la serpentina se sobreestimaría un 50 % (de 62 a 93 kW)). La exergía química del gas natural es la de la mezcla ideal, $\\sum y_i\\,ex_i + R\\,T_0 \\sum y_i \\ln y_i$, con las exergías químicas estándar de Szargut (CH₄ 831.650; C₂H₆ 1.495.840; C₃H₈ 2.154.000; N₂ 720; CO₂ 19.870; O₂ 3.970; H₂O gas 9.500 kJ/kmol): **recordadas, a cotejar con el libro de la cátedra**.

**Eficiencias.** Enfriadora: producto = exergía del frío, $\\dot Q_L\\,(T_0/T_{{cw}} - 1)$ con $T_{{cw}}$ la temperatura media logarítmica del agua helada ({v['ex_Tcw']} °C); caldera: producto = exergía del calor entregado al agua a 80/60 °C. Para el recalentador y el aire el producto puede ser negativo (se calienta aire que está por debajo del estado muerto): ahí solo se informa la destrucción.

## 8.2 Resultados por equipo

{t_inf}

Table: Tabla M14a. Reparto de la exergía de entrada en los dos casos analizados.


**Verano pico** (exterior a {v['ex_T0_a']} °C; entrada {v['ex_in_a']} kW: {v['ex_el_a']} de electricidad y {v['ex_gas_a']} de gas). Cierre del balance global: error relativo menor que $10^{{-12}}$ (es un cierre contable; la verificación física es $D = T_0 \\dot S_{{gen}}$ en la serpentina, el compresor y la válvula).

{t_equipos(a, "")}

Table: Tabla M15. Balance exergético por equipo, verano pico.

**Máximo recalentamiento del año** (diciembre, noche; exterior a {v['ex_T0_b']} °C; entrada {v['ex_in_b']} kW: {v['ex_el_b']} de electricidad y {v['ex_gas_b']} de gas).

{t_equipos(b, "")}

Table: Tabla M16. Balance exergético por equipo, máximo recalentamiento.

## 8.3 Sensibilidad al estado muerto

Repetición del verano pico con otros estados muertos (el aire exterior queda fijo en 34 °C; la humedad de referencia a $T_0 \\neq 34$ °C es la del aire a $T_0$ con la humedad relativa media anual):

{t_sens}

Table: Tabla M17. Sensibilidad al estado muerto. Con $T_0$ menor que el aire tratado, el producto del aire pasa a ser negativo y la eficiencia global deja de estar definida.

## 8.4 Supuestos y convenciones

- Circuito de agua caliente 80/60 °C para el recalentador, la calefacción y el ACS (supuesto; el modelo base no lo fija). Agua helada 7/12 °C (coherente con el modelo).
- Efectividad 0,5 del condensador: el aire sale a $T_{{ext}} + 0{{,}}5\\,(T_{{cond}} - T_{{ext}})$; solo reparte la pérdida y la destrucción del condensador, no cambia el total.
- La pérdida del motor del compresor se cuenta como destrucción (calor disipado a una temperatura cercana a $T_0$). **A confirmar con la cátedra**: otra convención la llamaría pérdida.
- Ventiladores y bombas: producto = trabajo de flujo $\\dot V\\,\\Delta p$, que se disipa después en filtros, serpentinas y conductos (fila de pérdidas de carga). Los ventiladores del condensador no tienen producto.
- Limitaciones: la humidificación del modelo base inyecta vapor a 2.676 kJ/kg de forma isotérmica y no conserva la energía exacta (cerca de 0,7 % de la carga de invierno); el modelo no tiene el caudal de aire del condensador, por eso el reparto entre pérdida y destrucción ahí depende de la efectividad supuesta.
"""
    v["_resumen"] = (f"El análisis exergético muestra que en el verano pico se destruye el {v['ex_D_a']} % de la exergía que entra (la enfriadora y su entorno, el {v['ex_enf_a']} %) "
                     f"y que en el momento de máximo recalentamiento la caldera destruye el {v['ex_calD_b']} % de lo destruido, con una eficiencia exergética de {v['ex_eta_cal_b']} %: "
                     f"se quema gas con una llama adiabática teórica de {V['T_llama']} °C para subir el aire unos kelvin.")
    v["_concl3"] = (f"**En energía:** los ventiladores ({V['pct_vent']} % de la energía final), el compresor ({V['pct_comp']} %) y el gas del recalentamiento ({V['pct_recal_gas']} %) son los mayores consumos "
                    f"(el orden de los dos primeros depende de la presión y el rendimiento supuestos de los ventiladores); las pérdidas propiamente dichas son el calor que el condensador rechaza al ambiente "
                    f"({V['Q_cond_MWh']} MWh por año, unas {V['Q_cond_sobre_recal']} veces el calor de recalentamiento), los gases de escape de la caldera ({V['q_gases']} % del PCI) y la irreversibilidad del compresor. "
                    f"**En exergía:** en el verano pico se destruye el {v['ex_D_a']} % de lo que entra, sobre todo en la enfriadora y su entorno ({v['ex_enf_a']} %) y en ventiladores y bombas ({v['ex_vent_a']} %); "
                    f"en el máximo recalentamiento la caldera (aire y ACS) destruye el {v['ex_calD_b']} % del total destruido (eficiencia exergética de {v['ex_eta_cal_b']} %), "
                    f"porque calienta aire unos kelvin con una llama adiabática teórica de {V['T_llama']} °C.")
    return inf, mem, v
