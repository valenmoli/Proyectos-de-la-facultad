"""Alternativa B y mejoras de sustentabilidad sobre el modelo base (alternativa A).

`anual_variante(c, opciones)` repite el calculo anual de `estimacion.anual` con opciones; sin opciones da
exactamente el mismo resultado que el caso base (lo verifica un test). Cada opcion es una decision de diseno:

  rec_cond        recuperacion del calor del condensador para el recalentamiento y la calefaccion del aire
  caldera_cond    caldera de condensacion (gases de escape a baja temperatura) para el calor del aire
  solar_acs       precalentamiento solar del agua caliente sanitaria
  fv              paneles fotovoltaicos que descuentan electricidad del sistema
  rec_extraccion  recuperador de calor del aire de extraccion con circuito de agua (sin mezcla de corrientes)
  dp_vent         factor sobre la presion de los ventiladores (0,8 = 20 % menos)
  refrigerante    otro refrigerante en la enfriadora

Todo parametro nuevo esta en PARAMETROS con su estado (DATO / SUPUESTO / FUENTE SECUNDARIA / PROPIO).
"""
import copy
import math

from CoolProp.CoolProp import PropsSI

from . import aire_humedo as ah
from . import combustion as cb
from . import edificio as ed
from . import estimacion as es
from . import refrigeracion as rf

# id, clave, nombre, valor, unidad, estado, justificacion
PARAMETROS = [
    ("PM1", "T_agua_rec", "Temperatura del agua caliente del recuperador de calor del condensador", 45.0, "C", "SUPUESTO",
     "Serpentina de recalentamiento que lleva aire de unos 13 C a 17-19 C: alcanza con agua tibia. Un caso de hospital con enfriadoras de "
     "recuperacion de calor usa agua a 115 F (46 C) en lugar de 180 F de caldera (Trane, caso Baylor Scott & White, via busqueda web)"),
    ("PM2", "pinch_rec", "Diferencia minima entre la condensacion y el agua caliente del recuperador", 5.0, "K", "SUPUESTO",
     "Intercambiador de placas tipico"),
    ("PM3", "T_gases_cond", "Temperatura de los gases de escape de la caldera de condensacion", 45.0, "C", "SUPUESTO",
     "Agua de retorno a 40 C y 5 K de aproximacion; por debajo del rocio de los gases (unos 56 C)"),
    ("PM4", "A_solar", "Superficie de colectores solares para el ACS", 300.0, "m2", "SUPUESTO",
     "Unos 5 % de la azotea (6.117 m2 por nivel); tamano que no produce excedentes en verano"),
    ("PM5", "eta_solar", "Rendimiento medio anual de los colectores solares (sobre irradiacion horizontal)", 0.40, "-", "SUPUESTO",
     "Colector plano a 40-60 C con perdidas opticas y termicas; sin dato de catalogo"),
    ("PM6", "GHI_anual", "Irradiacion global horizontal anual", 1700.0, "kWh/m2 anio", "FUENTE SECUNDARIA",
     "Global Solar Atlas, informe de un punto de la provincia de Buenos Aires a unos 300 km (coordenadas -37,16 -59,06), via busqueda web: "
     "es una cota alta para la ciudad; a confirmar con globalsolaratlas.info para las coordenadas del hospital"),
    ("PM7", "lat", "Latitud del hospital", -34.7, "grados", "SUPUESTO", "La Matanza, Buenos Aires"),
    ("PM8", "kWp_fv", "Potencia fotovoltaica instalada", 250.0, "kWp", "SUPUESTO",
     "Unos 1.250 m2 de paneles (5 m2/kWp) sobre una azotea de 6.117 m2 con equipos"),
    ("PM9", "PR_fv", "Relacion de rendimiento (performance ratio) de la instalacion fotovoltaica", 0.80, "-", "SUPUESTO",
     "Valor habitual de instalaciones nuevas (0,75 a 0,85); sin dato propio"),
    ("PM10", "eps_rec", "Efectividad del recuperador de calor del aire de extraccion con circuito de agua", 0.50, "-", "FUENTE SECUNDARIA",
     "Una comparacion de un fabricante da 45 a 55 % para circuitos de agua con aislacion total entre corrientes (via busqueda web)"),
    ("PM11", "dp_rec", "Caida de presion adicional del recuperador (cada lado)", 250.0, "Pa", "SUPUESTO", "Serpentina de 4 filas en cada corriente"),
    ("PM12", "f_dp_vent", "Factor sobre la presion de los ventiladores en la mejora de ventiladores", 0.8, "-", "SUPUESTO",
     "Filtros y conductos de menor perdida, ventiladores de velocidad variable"),
    ("PM13", "ef_elec", "Factor de emision de la electricidad de la red", 0.38, "tCO2/MWh", "FUENTE SECUNDARIA",
     "Meta de CAMMESA de 380 kg CO2e/MWh para 2023 (perfil de DitchCarbon, via busqueda web); es una meta y no un dato medido. "
     "Otras citas de busquedas: 0,288 t/MWh (Climate Transparency, datos de 2021, via Carbon Footprint) y unos 0,40 t/MWh (Ember, 2022). "
     "La Secretaria de Energia publica la serie oficial en datos.gob.ar: reemplazar"),
    ("PM14", "desrec_min_T", "Temperatura minima de descarga del compresor para recuperar calor sin subir la condensacion", 50.0, "C", "SUPUESTO",
     "Agua a 45 C mas 5 K de aproximacion"),
]

MESES_N = [17, 47, 75, 105, 135, 162, 198, 228, 258, 288, 318, 344]    # dia tipico de cada mes (Duffie y Beckman)


def parametro(clave):
    for (_i, k, _n, v, *_r) in PARAMETROS:
        if k == clave:
            return v
    raise KeyError(clave)


# ------------------------------------------------------------------ combustion con condensacion
def caldera_condensacion(P, T_gases_C):
    """Rendimiento de una caldera que enfria los gases por debajo del rocio y condensa parte del agua.

    Balance de energia por kmol de combustible con entalpias de formacion: el calor util es el PCI mas el calor
    latente del agua que condensa, menos la entalpia sensible de lo que sale (gases secos, vapor que queda y
    condensado), mas el aire de combustion, menos las perdidas por radiacion.
    """
    b = cb.balance(P)
    pc = cb.poder_calorifico(P)
    prod, reac = b["productos"], b["reactivos"]
    n_h2o = prod["H2O"]
    n_seco = b["n_productos"] - n_h2o
    p_sat = PropsSI("P", "T", T_gases_C + 273.15, "Q", 1, "Water")
    y_sat = p_sat / 101325.0
    if y_sat >= n_h2o / b["n_productos"]:                      # por encima del rocio no condensa nada
        n_vapor = n_h2o
    else:
        n_vapor = n_seco * y_sat / (1.0 - y_sat)                # vapor que queda en los gases saturados
    n_cond = n_h2o - n_vapor
    L = cb.HF_H2O_G - cb.HF_H2O_L                              # calor latente a 25 C [kJ/kmol]
    h_sal = (sum(n * cb.dh_sensible(e, T_gases_C) for e, n in prod.items() if e != "H2O")
             + n_vapor * cb.dh_sensible("H2O", T_gases_C) + n_cond * 75.3 * (T_gases_C - 25.0))
    h_ent = reac["O2"] * cb.dh_sensible("O2", P["T_aire_comb"]) + reac["N2_aire"] * cb.dh_sensible("N2", P["T_aire_comb"])
    lhv = pc["PCI_kJ_kmol"]
    q_util = lhv + n_cond * L - h_sal + h_ent - P["f_rad"] * lhv
    eta_pci = q_util / lhv
    return dict(eta_PCI=eta_pci, eta_PCS=eta_pci * lhv / pc["PCS_kJ_kmol"], n_cond=n_cond, frac_cond=n_cond / n_h2o, T_gases=T_gases_C)


def factor_co2_gas(P):
    """kg de CO2 por kWh de PCI del gas natural, de la reaccion (kmol de CO2 por kmol de gas)."""
    b = cb.balance(P)
    pc = cb.poder_calorifico(P)
    return b["productos"]["CO2"] * 44.01 / (pc["PCI_kJ_kmol"] / 3600.0)


# ------------------------------------------------------------------ radiacion solar
def irradiacion_mensual(lat_deg, GHI_anual):
    """Irradiacion diaria media mensual sobre superficie horizontal [kWh/m2 dia], con la irradiacion
    extraterrestre (Duffie y Beckman) y un indice de claridad unico calibrado para dar GHI_anual."""
    phi = math.radians(lat_deg)
    dias = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    H0 = []
    for n in MESES_N:
        delta = math.radians(23.45 * math.sin(math.radians(360.0 * (284 + n) / 365.0)))
        E0 = 1.0 + 0.033 * math.cos(math.radians(360.0 * n / 365.0))
        ws = math.acos(-math.tan(phi) * math.tan(delta))
        H0.append(24.0 / math.pi * 1367.0 * E0 * (math.cos(phi) * math.cos(delta) * math.sin(ws) + ws * math.sin(phi) * math.sin(delta)) / 1000.0)
    Kt = GHI_anual / sum(h * d for h, d in zip(H0, dias))
    return [Kt * h for h in H0], Kt


# ------------------------------------------------------------------ calculo anual con opciones
def anual_variante(c0, opc=None):
    opc = opc or {}
    c = copy.deepcopy(c0)
    P, Z, clima = c["P"], c["Z"], c["clima"]
    if opc.get("refrigerante"):
        P["refrigerante"] = opc["refrigerante"]
    if opc.get("dp_vent"):
        for z in Z.values():
            z["dp_vent"] *= opc["dp_vent"]
    caud = ed.caudales(c)
    dis_acs = es.acs(c)
    cal = cb.caldera(P)
    eta_base, pc = cal["eta_PCI"], cal["pc"]
    cond = caldera_condensacion(P, parametro("T_gases_cond")) if opc.get("caldera_cond") else None
    rec = opc.get("rec_cond")
    f_sim = rec.get("f", 1.0) if isinstance(rec, dict) else 1.0   # fraccion de la demanda que coincide con el calor disponible
    ext = opc.get("rec_extraccion")
    eps_rec = opc.get("eps_rec", parametro("eps_rec"))
    bypass = opc.get("bypass", True)                # el recuperador tiene compuertas de bypass del lado del aire
    f_or = opc.get("or_setback")                    # factor de caudal del quirofano de noche (None = sin setback)
    caud_noche = copy.deepcopy(caud)
    if f_or:
        for k_ in ("m_sup", "m_oa", "V_sup_m3h"):
            caud_noche["G1"][k_] *= f_or
        caud_noche["G1"]["P_vent_kW"] *= f_or ** 3   # leyes de los ventiladores: la potencia varia con el cubo del caudal
    dp_rec = opc.get("dp_rec", parametro("dp_rec"))
    H_mes, _Kt = irradiacion_mensual(parametro("lat"), parametro("GHI_anual"))

    zon = {g: dict(serp=0.0, recal=0.0, cal=0.0, hum=0.0, vent=0.0) for g in Z}
    pl = dict(comp=0.0, cond=0.0, bomba=0.0, Q_L=0.0, Q_cond=0.0)
    extra_vent = 0.0           # electricidad de ventiladores y bombas del recuperador de extraccion [kWh]
    q_rec_total = 0.0          # calor recuperado del condensador [kWh]
    horas_rec = 0.0
    solar_kWh = 0.0
    T_cond_min = P["T_cond_min"]
    for i, mes in enumerate(clima["meses"]):
        T_m, HR_m, dias = clima["T"][i], clima["HR"][i], clima["dias"][i]
        W_m = ah.w_desde_hr(T_m, HR_m, P["presion"])
        horas = 12.0 * dias
        for mitad in ("dia", "noche"):
            T_out = T_m + (P["rango_diario"] / 2.0 if mitad == "dia" else -P["rango_diario"] / 2.0)
            q_sol = P["q_sol_dia"] if mitad == "dia" else 0.0
            Q_L, demanda = 0.0, 0.0
            for g, z in Z.items():
                if mitad == "noche" and not z["opera_noche"]:
                    continue
                f_int = z["f_dia"] if mitad == "dia" else z["f_noche"]
                W_est = min(W_m, ah.w_desde_hr(T_out, 1.0, P["presion"]))
                cd = caud_noche if (f_or and mitad == "noche") else caud
                r = ed.proceso(c, g, cd, T_out, W_est, f_int, q_sol)
                if ext:
                    # el recuperador tiene bypass: solo trabaja si baja el costo de energia del estado (serpentina con un
                    # COP de referencia de 4 y calor de caldera con el rendimiento base) mas la potencia de ventiladores extra
                    T_ret = z["t_ver"] if T_out >= P["T_cambio_estacion"] else z["t_inv"]
                    r1 = ed.proceso(c, g, caud, T_out, W_est, f_int, q_sol, T_oa=T_out + eps_rec * (T_ret - T_out))
                    V_oa = caud[g]["m_oa"] / P["rho_aire"]
                    p_extra = 2.0 * V_oa * dp_rec / 1000.0 / P["eta_vent"]
                    costo0 = r["Q_coil"] / 4.0 + (r["Q_recal"] + r["Q_cal"]) / eta_base
                    costo1 = r1["Q_coil"] / 4.0 + (r1["Q_recal"] + r1["Q_cal"]) / eta_base + p_extra
                    if costo1 < costo0 or not bypass:
                        r = r1
                        extra_vent += p_extra * horas * z["f_dias"]
                fd = z["f_dias"]
                zon[g]["serp"] += r["Q_coil"] * horas * fd
                zon[g]["recal"] += r["Q_recal"] * horas * fd
                zon[g]["cal"] += r["Q_cal"] * horas * fd
                zon[g]["hum"] += r["Q_hum"] * horas * fd
                zon[g]["vent"] += cd[g]["P_vent_kW"] * horas * fd
                Q_L += r["Q_coil"] * fd
                demanda += (r["Q_recal"] + r["Q_cal"]) * fd
            p = es._planta(c, Q_L, T_out)
            W_comp, W_cond, Q_cond_aire = p["W_comp"], p["W_cond"], p["Q_cond"]
            if rec and Q_L > 0 and demanda > 0:
                # tres modos por estado: sin recuperar, solo sobrecalentamiento de la descarga (sin subir la condensacion)
                # o condensador de recuperacion (condensa a T_agua + aproximacion); se elige el de mayor ahorro neto
                T_req = parametro("T_agua_rec") + parametro("pinch_rec")
                mejor = (0.0, W_comp, W_cond, Q_cond_aire, 0.0)           # (ahorro neto kWh equiv., W_comp, W_cond, Q_cond_aire, Q_rec)
                ciclo0 = rf.ciclo(P["T_ev"], p["T_cond"], P["refrigerante"], P["sobrecal"], P["subenf"], P["eta_is"], P["eta_motor"])
                if ciclo0["T2"] >= parametro("desrec_min_T"):
                    h_gs = PropsSI("H", "P", ciclo0["P_c"], "Q", 1, P["refrigerante"]) / 1e3
                    f_des = (ciclo0["h2"] - h_gs) / ciclo0["q_H"]
                    q_rec = min(f_sim * demanda, f_des * p["Q_cond"])
                    cand = (q_rec / eta_base, W_comp, P["f_vent_cond"] * (p["Q_cond"] - q_rec), p["Q_cond"] - q_rec, q_rec)
                    if cand[0] - 0.0 > mejor[0]:
                        mejor = cand
                if T_req > p["T_cond"]:
                    ciclo1 = rf.ciclo(P["T_ev"], T_req, P["refrigerante"], P["sobrecal"], P["subenf"], P["eta_is"], P["eta_motor"])
                    W1 = Q_L / ciclo1["cop_elec"]
                    Qc1 = Q_L + W1 * P["eta_motor"]
                    q_rec = min(f_sim * demanda, Qc1)
                    W_cond1 = P["f_vent_cond"] * (Qc1 - q_rec)
                    neto = q_rec / eta_base - (W1 - W_comp) - (W_cond1 - W_cond)
                    if neto > mejor[0]:
                        mejor = (neto, W1, W_cond1, Qc1 - q_rec, q_rec)
                _n, W_comp, W_cond, Q_cond_aire, q_rec = mejor
                q_rec_total += q_rec * horas
                horas_rec += horas if q_rec > 0 else 0.0
            elif rec and Q_L > 0:
                pass
            pl["comp"] += W_comp * horas
            pl["cond"] += W_cond * horas
            pl["bomba"] += p["W_bomba"] * horas
            pl["Q_L"] += Q_L * horas
            pl["Q_cond"] += Q_cond_aire * horas
    # ACS y solar
    q_acs = dis_acs["kWh_anio"]
    if opc.get("solar_acs"):
        for i, dias in enumerate(clima["dias"]):
            util = parametro("A_solar") * parametro("eta_solar") * H_mes[i] * dias
            demanda_mes = dis_acs["kW"] * 24.0 * dias
            solar_kWh += min(util, demanda_mes)
    q_recal = sum(zon[g]["recal"] for g in Z)
    q_cal = sum(zon[g]["cal"] for g in Z)
    q_hum = sum(zon[g]["hum"] for g in Z)
    q_aire = q_recal + q_cal + q_hum
    q_aire_caldera = q_aire - q_rec_total
    q_acs_caldera = q_acs - solar_kWh
    eta_aire = cond["eta_PCI"] if cond else eta_base
    # la humidificacion con vapor a 100 C no condensa: se queda con el rendimiento base (en el caso base es 0)
    gas_aire = cb.consumo_gas((q_aire_caldera - q_hum), eta_aire, pc)
    gas_hum = cb.consumo_gas(q_hum, eta_base, pc)
    gas_acs = cb.consumo_gas(q_acs_caldera, eta_base, pc)
    E_pci = gas_aire["E_PCI_kWh"] + gas_hum["E_PCI_kWh"] + gas_acs["E_PCI_kWh"]
    E_pcs = gas_aire["E_PCS_kWh"] + gas_hum["E_PCS_kWh"] + gas_acs["E_PCS_kWh"]
    elec = dict(compresor=pl["comp"], vent_condensador=pl["cond"], bombas=pl["bomba"],
                ventiladores=sum(zon[g]["vent"] for g in Z) + extra_vent)
    fv_kWh = 0.0
    if opc.get("fv"):
        fv_kWh = parametro("kWp_fv") * parametro("GHI_anual") * parametro("PR_fv")
        fv_kWh = min(fv_kWh, sum(elec.values()))
    elec["total"] = sum(elec.values()) - fv_kWh
    E_total = elec["total"] + E_pcs
    co2_gas = E_pci * factor_co2_gas(P) / 1000.0
    co2_elec = elec["total"] * parametro("ef_elec") / 1000.0
    return dict(zonas=zon, planta=pl, q_recal=q_recal, q_cal=q_cal, q_hum=q_hum, q_acs=q_acs, q_rec_cond=q_rec_total,
                solar_kWh=solar_kWh, fv_kWh=fv_kWh, extra_vent=extra_vent, elec=elec, E_PCS=E_pcs, E_PCI=E_pci,
                V_gas_m3=E_pcs / pc["PCS_kWh_m3"], E_total=E_total, E_elec=elec["total"], i_total_cub=E_total / P["A_cub"],
                co2_gas_t=co2_gas, co2_elec_t=co2_elec, co2_t=co2_gas + co2_elec, eta_aire=eta_aire, caldera_cond=cond,
                horas_rec=horas_rec)


# ------------------------------------------------------------------ catalogo de variantes
VARIANTES = [
    ("A", "Alternativa A: caso base", {}),
    ("B", "Alternativa B: recuperación del calor del condensador", {"rec_cond": True}),
    ("M1", "Caldera de condensación", {"caldera_cond": True}),
    ("M2", "Precalentamiento solar del ACS", {"solar_acs": True}),
    ("M3", "Recuperador de calor del aire de extracción", {"rec_extraccion": True}),
    ("M4", "Ventiladores con 20 % menos de presión", {"dp_vent": 0.8}),
    ("M5", "Paneles fotovoltaicos", {"fv": True}),
    ("M6", "Quirófanos con el caudal al 50 % de noche", {"or_setback": 0.5}),
    ("P", "Paquete: B + M1 a M6",
     {"rec_cond": True, "caldera_cond": True, "solar_acs": True, "rec_extraccion": True, "dp_vent": 0.8, "fv": True, "or_setback": 0.5}),
]


def comparar(c):
    """Corre todas las variantes y devuelve filas con energia, emisiones y diferencias respecto del caso base."""
    base = anual_variante(c, {})
    filas = []
    for clave, nombre, opc in VARIANTES:
        r = base if not opc else anual_variante(c, opc)
        filas.append(dict(clave=clave, nombre=nombre, opciones=opc, E_total=r["E_total"], E_elec=r["E_elec"], E_PCS=r["E_PCS"],
                          co2_t=r["co2_t"], d_E=(r["E_total"] - base["E_total"]) / base["E_total"],
                          d_co2=(r["co2_t"] - base["co2_t"]) / base["co2_t"], i_cub=r["i_total_cub"], detalle=r))
    return base, filas


def refrigerantes(c, T_ev=None, T_cond=None, nombres=("R134a", "R513A", "R1234ze(E)", "R1234yf")):
    """COP del ciclo con otros refrigerantes en las mismas temperaturas (si CoolProp los conoce)."""
    P = c["P"]
    T_ev = P["T_ev"] if T_ev is None else T_ev
    T_cond = 46.0 if T_cond is None else T_cond
    out = []
    for n in nombres:
        try:
            r = rf.ciclo(T_ev, T_cond, n, P["sobrecal"], P["subenf"], P["eta_is"], P["eta_motor"])
            out.append(dict(refrigerante=n, cop_elec=r["cop_elec"], P_ev=r["P_ev"], P_c=r["P_c"], T2=r["T2"], q_L=r["q_L"],
                            q_vol=r["q_L"] / (1.0 / PropsSI("D", "P", r["P_ev"], "T", T_ev + 273.15 + P["sobrecal"], n)) ))
        except Exception as e:                               # CoolProp no tiene todos los refrigerantes
            out.append(dict(refrigerante=n, error=str(e)[:80]))
    return out
