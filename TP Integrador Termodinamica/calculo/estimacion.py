"""Estimacion del consumo de energia del sistema termico del hospital.

Metodo:
  1. Puntos de diseno (verano pico e invierno): capacidades de la enfriadora y de la caldera.
  2. Consumo anual: cada mes se parte en una mitad diurna y una nocturna (12 h x dias del mes);
     en cada una se calcula el tratamiento del aire de cada zona, la potencia de la enfriadora y
     la de la caldera, y se multiplica por las horas.
  3. Agua caliente sanitaria: demanda constante.

Frontera: sistema termico (frio, recalentamiento, calefaccion, humidificacion, ACS) y sus auxiliares
(ventiladores, bombas, ventiladores del condensador). No incluye iluminacion, equipos medicos,
cocina ni lavanderia.
"""
import copy

from . import aire_humedo as ah
from . import combustion as cb
from . import edificio as ed
from . import refrigeracion as rf


def _planta(c, Q_L_kW, T_ext):
    """Potencia electrica de la enfriadora y sus auxiliares para una carga frigorifica Q_L [kW]."""
    P = c["P"]
    if Q_L_kW <= 0:
        return dict(W_comp=0.0, W_cond=0.0, W_bomba=0.0, COP=None, T_cond=None, Q_cond=0.0)
    cop, T_cond, r = rf.cop_vs_exterior(T_ext, c)
    W_comp = Q_L_kW / cop                                  # potencia electrica del compresor
    Q_cond = Q_L_kW + W_comp * P["eta_motor"]              # calor rechazado = Q_L + trabajo en el eje
    W_cond = P["f_vent_cond"] * Q_cond
    m_w = Q_L_kW / (ah.CP_W * P["dT_aguahelada"])          # kg/s de agua helada
    W_bomba = (m_w / 1000.0) * P["dP_bomba"] / P["eta_bomba"] / 1000.0
    return dict(W_comp=W_comp, W_cond=W_cond, W_bomba=W_bomba, COP=cop, T_cond=T_cond, Q_cond=Q_cond)


def acs(c):
    """Demanda de ACS [kW medios y kWh/anio utiles]."""
    P = c["P"]
    camas = P["camas_gen"] + P["camas_uti"]
    kg_dia = P["L_cama_dia"] * camas
    kJ_dia = kg_dia * ah.CP_W * (P["T_acs"] - P["T_agua_fria"]) * P["f_perd_acs"]
    kW = kJ_dia / 86400.0
    return dict(kW=kW, kWh_anio=kW * 8760.0, kWh_dia=kJ_dia / 3600.0)


def diseno(c):
    """Cargas de diseno de verano (pico) e invierno."""
    P, Z = c["P"], c["Z"]
    caud = ed.caudales(c)
    Tv, Wv = ed.estado_exterior_verano(c)
    Ti, Wi = ed.estado_exterior_invierno(c)
    ver, inv = {}, {}
    for g in Z:
        ver[g] = ed.proceso(c, g, caud, Tv, Wv, 1.0, P["q_sol_pico"])
        inv[g] = ed.proceso(c, g, caud, Ti, Wi, 0.0, 0.0)
    Q_L = sum(v["Q_coil"] for v in ver.values())
    plan = _planta(c, Q_L, Tv)
    a = acs(c)
    caldera = cb.caldera(P)
    Q_cal_inv = sum(v["Q_cal"] + v["Q_recal"] + v["Q_hum"] for v in inv.values())
    return dict(caudales=caud, verano=ver, invierno=inv, Q_L=Q_L, Q_recal_verano=sum(v["Q_recal"] for v in ver.values()),
                planta=plan, Q_caldera_invierno=Q_cal_inv, acs=a, caldera=caldera, T_ext_verano=Tv, W_ext_verano=Wv,
                T_ext_invierno=Ti, W_ext_invierno=Wi)


def anual(c):
    """Consumo anual de energia. Devuelve desglose por uso y por zona."""
    P, Z, clima = c["P"], c["Z"], c["clima"]
    caud = ed.caudales(c)
    dis_acs = acs(c)
    cal = cb.caldera(P)
    eta, pc = cal["eta_PCI"], cal["pc"]

    # Acumuladores [kWh]
    zon = {g: dict(serp=0.0, recal=0.0, cal=0.0, hum=0.0, vent=0.0, serp_sens=0.0, serp_lat=0.0) for g in Z}
    pl = dict(comp=0.0, cond=0.0, bomba=0.0, Q_L=0.0, Q_cond=0.0)
    mensual = []
    for i, mes in enumerate(clima["meses"]):
        T_m, HR_m, dias = clima["T"][i], clima["HR"][i], clima["dias"][i]
        W_m = ah.w_desde_hr(T_m, HR_m, P["presion"])
        horas = 12.0 * dias
        fila = dict(mes=mes, Q_L=0.0, Q_cal=0.0, W_comp=0.0)
        for mitad in ("dia", "noche"):
            T_out = T_m + (P["rango_diario"] / 2.0 if mitad == "dia" else -P["rango_diario"] / 2.0)
            q_sol = P["q_sol_dia"] if mitad == "dia" else 0.0
            Q_L = 0.0
            for g, z in Z.items():
                if mitad == "noche" and not z["opera_noche"]:
                    continue
                f_int = z["f_dia"] if mitad == "dia" else z["f_noche"]
                W_est = min(W_m, ah.w_desde_hr(T_out, 1.0, P["presion"]))   # la humedad no supera la saturacion
                r = ed.proceso(c, g, caud, T_out, W_est, f_int, q_sol)
                fd = z["f_dias"]                                              # fraccion de los dias en que opera la zona
                zon[g]["serp"] += r["Q_coil"] * horas * fd
                zon[g]["serp_sens"] += r["Q_coil_sens"] * horas * fd
                zon[g]["serp_lat"] += r["Q_coil_lat"] * horas * fd
                zon[g]["recal"] += r["Q_recal"] * horas * fd
                zon[g]["cal"] += r["Q_cal"] * horas * fd
                zon[g]["hum"] += r["Q_hum"] * horas * fd
                zon[g]["vent"] += caud[g]["P_vent_kW"] * horas * fd
                Q_L += r["Q_coil"] * fd
                fila["Q_cal"] += (r["Q_recal"] + r["Q_cal"] + r["Q_hum"]) * horas * fd
            p = _planta(c, Q_L, T_out)
            pl["comp"] += p["W_comp"] * horas
            pl["cond"] += p["W_cond"] * horas
            pl["bomba"] += p["W_bomba"] * horas
            pl["Q_L"] += Q_L * horas
            pl["Q_cond"] += p["Q_cond"] * horas
            fila["Q_L"] += Q_L * horas
            fila["W_comp"] += p["W_comp"] * horas
        mensual.append(fila)

    # Calor util entregado por la caldera [kWh]
    q_aire = sum(zon[g]["recal"] + zon[g]["cal"] + zon[g]["hum"] for g in Z)
    q_recal = sum(zon[g]["recal"] for g in Z)
    q_cal = sum(zon[g]["cal"] for g in Z)
    q_hum = sum(zon[g]["hum"] for g in Z)
    q_acs = dis_acs["kWh_anio"]
    q_total = q_aire + q_acs
    gas = cb.consumo_gas(q_total, eta, pc)

    elec = dict(compresor=pl["comp"], vent_condensador=pl["cond"], bombas=pl["bomba"],
                ventiladores=sum(zon[g]["vent"] for g in Z))
    elec["total"] = sum(elec.values())
    return dict(zonas=zon, planta=pl, mensual=mensual, q_recal=q_recal, q_cal=q_cal, q_hum=q_hum, q_acs=q_acs,
                q_util_total=q_total, gas=gas, elec=elec, eta_caldera=eta, pc=pc,
                serp_total=sum(zon[g]["serp"] for g in Z))


def resumen(c):
    """Ejecuta diseno y anual, y calcula las intensidades [kWh/m2 y anio]."""
    P = c["P"]
    A, a_cond = ed.superficies(c)
    d = diseno(c)
    an = anual(c)
    E_el = an["elec"]["total"]
    E_gas = an["gas"]["E_PCS_kWh"]
    E_tot = E_el + E_gas
    cop_estacional = an["planta"]["Q_L"] / an["elec"]["compresor"] if an["elec"]["compresor"] > 0 else None
    return dict(
        A=A, a_cond=a_cond, diseno=d, anual=an,
        E_elec=E_el, E_gas_PCS=E_gas, E_gas_PCI=an["gas"]["E_PCI_kWh"], V_gas_m3=an["gas"]["V_m3"], E_total=E_tot,
        i_total_cub=E_tot / P["A_cub"], i_elec_cub=E_el / P["A_cub"], i_gas_cub=E_gas / P["A_cub"],
        i_total_cond=E_tot / a_cond, cop_estacional=cop_estacional,
        frac_gas=E_gas / E_tot,
    )


def sensibilidad(c0, variaciones=None):
    """Efecto de variar cada supuesto clave sobre la energia final total [kWh/anio]."""
    base = resumen(c0)["E_total"]

    def escalar_zonas(c, clave, f):
        for z in c["Z"].values():
            z[clave] *= f

    def clima_dT(c, dT):
        c["clima"]["T"] = [t + dT for t in c["clima"]["T"]]

    def clima_dHR(c, d):
        c["clima"]["HR"] = [min(max(h + d, 0.2), 0.98) for h in c["clima"]["HR"]]

    V = variaciones or [
        ("ACS por cama: 55 L/dia", lambda c: c["P"].__setitem__("L_cama_dia", 55.0)),
        ("ACS por cama: 200 L/dia", lambda c: c["P"].__setitem__("L_cama_dia", 200.0)),
        ("Temperatura media mensual -2 K", lambda c: clima_dT(c, -2.0)),
        ("Temperatura media mensual +2 K", lambda c: clima_dT(c, +2.0)),
        ("Humedad relativa media -8 puntos", lambda c: clima_dHR(c, -0.08)),
        ("Humedad relativa media +8 puntos", lambda c: clima_dHR(c, +0.08)),
        ("Ganancias internas -30 %", lambda c: (escalar_zonas(c, "q_s", 0.7), escalar_zonas(c, "q_l", 0.7))),
        ("Ganancias internas +30 %", lambda c: (escalar_zonas(c, "q_s", 1.3), escalar_zonas(c, "q_l", 1.3))),
        ("Conductancia de la envolvente -30 %", lambda c: c["P"].__setitem__("UA_m2", c["P"]["UA_m2"] * 0.7)),
        ("Conductancia de la envolvente +30 %", lambda c: c["P"].__setitem__("UA_m2", c["P"]["UA_m2"] * 1.3)),
        ("Aire exterior minimo -25 %", lambda c: escalar_zonas(c, "ach_oa", 0.75)),
        ("Aire exterior minimo +25 %", lambda c: escalar_zonas(c, "ach_oa", 1.25)),
        ("Quirofanos: 15 renovaciones totales", lambda c: c["Z"]["G1"].__setitem__("ach_tot", 15)),
        ("Quirofanos: 25 renovaciones totales", lambda c: c["Z"]["G1"].__setitem__("ach_tot", 25)),
        ("Rendimiento isentropico 0,65", lambda c: c["P"].__setitem__("eta_is", 0.65)),
        ("Rendimiento isentropico 0,78", lambda c: c["P"].__setitem__("eta_is", 0.78)),
        ("Exceso de aire 5 % (lambda 1,05)", lambda c: c["P"].__setitem__("lambda_aire", 1.05)),
        ("Exceso de aire 30 % (lambda 1,30)", lambda c: c["P"].__setitem__("lambda_aire", 1.30)),
        ("Gases de escape a 160 C", lambda c: c["P"].__setitem__("T_gases", 160.0)),
        ("Gases de escape a 230 C", lambda c: c["P"].__setitem__("T_gases", 230.0)),
        ("Humedad maxima de verano 60 % en quirofanos, terapia intensiva e internacion",
         lambda c: [c["Z"][g].__setitem__("hr_ver", 0.60) for g in ("G1", "G2", "G3")]),
        ("Ventiladores: presion +30 % (proxy de ventiladores de retorno)", lambda c: escalar_zonas(c, "dp_vent", 1.3)),
        ("Caldera con perdidas de ciclado (f_rad 10 %)", lambda c: c["P"].__setitem__("f_rad", 0.10)),
        ("Ventilador sin calor en el aire (sin calor de ventilador)", lambda c: c["P"].__setitem__("f_calor_vent", 0.0)),
        ("Consultorios y administracion de lunes a sabado (6/7)", lambda c: c["Z"]["G5"].__setitem__("f_dias", 6.0 / 7.0)),
        ("Superficie climatizada 75 %", lambda c: c["P"].__setitem__("f_acond", 0.75)),
        ("Superficie climatizada 95 %", lambda c: c["P"].__setitem__("f_acond", 0.95)),
        ("Consultorios y administracion tambien funcionan 24 h", lambda c: c["Z"]["G5"].__setitem__("opera_noche", True)),
        ("Guardia, diagnostico y laboratorio: 20 % de las areas generales", lambda c: c["P"].__setitem__("f_g4_24h", 0.20)),
        ("Guardia, diagnostico y laboratorio: 50 % de las areas generales", lambda c: c["P"].__setitem__("f_g4_24h", 0.50)),
        ("Humedad relativa de verano 5 puntos menos (todas las zonas)",
         lambda c: [z.__setitem__("hr_ver", z["hr_ver"] - 0.05) for z in c["Z"].values()]),
    ]
    filas = []
    for nombre, f in V:
        c = copy.deepcopy(c0)
        f(c)
        e = resumen(c)["E_total"]
        filas.append(dict(nombre=nombre, E_total=e, delta=(e - base) / base))
    return base, filas
