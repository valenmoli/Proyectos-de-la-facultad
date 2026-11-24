"""Tablas y valores nuevos de la memoria de calculo (todo sale del modelo; no se copia ninguna cifra a mano).

construir_documentos.py llama a:
  tablas_memoria(c, V, T)   -> {clave: markdown}   tablas y bloques de texto que la plantilla inserta como {{clave}}
  valores_memoria(c, V, T)  -> {clave: texto}      valores formateados (coma decimal y punto de miles) como {{mx_...}};
                                                  dentro de una ecuacion se usa {{mx_..._m}}

Las funciones de calculo (caso_g1, caso_ciclo, ...) devuelven numeros sin redondear; el formato se aplica al armar las
tablas y los valores, y los tests comprueban que las cuentas impresas se reproducen a mano con los numeros impresos.
Los textos de respaldo usan las marcas de referencias.py: [n] para una fuente numerada ([n]* si solo se conoce por un
extracto) y «supuesto» para toda decision o valor propio.
"""
import copy
import importlib.metadata as md
import json
import re

from CoolProp.CoolProp import PropsSI

from . import aire_humedo as ah
from . import combustion as cb
from . import edificio as ed
from . import equipos as eq
from . import estimacion as es
from . import exergia as ex
from . import mejoras as mj
from . import referencias
from . import refrigeracion as rf
from . import supuestos
from .construir_borrador import n, tabla
from .nombres import NOMBRES_SENS

# Punto de diseno de verano (estimacion.diseno): actividad plena en todas las zonas y ganancia solar pico.
F_ACT_DISENO = 1.0


def nn(x, nd=0):
    """Formato argentino con signo menos tipografico."""
    return n(x, nd).replace("-", "−")


def R(clave):
    """Marca de una fuente numerada: '[6]\\*' o '[1]'."""
    return referencias.marca(clave)


SUP_CORRIENTE = "supuesto (valor de uso corriente)"


# ====================================================================================================================
# 1. Caso resuelto de aire humedo: zona G1 (los 6 quirofanos juntos), verano pico
# ====================================================================================================================
def caso_g1(c):
    P, z = c["P"], c["Z"]["G1"]
    pres = P["presion"]
    caud = ed.caudales(c)
    cd = caud["G1"]
    Tv, Wv = ed.estado_exterior_verano(c)
    r = ed.proceso(c, "G1", caud, Tv, Wv, F_ACT_DISENO, P["q_sol_pico"])
    A = cd["A"]
    T_r = z["t_ver"]
    W_r = ah.w_desde_hr(T_r, z["hr_ver"], pres)
    cp_r = ah.cp_ah(W_r)
    h_ext, h_ret = ah.entalpia(Tv, Wv), ah.entalpia(T_r, W_r)
    m_a, m_ae = cd["m_sup"], cd["m_oa"]
    x_ae = m_ae / m_a
    Qs = A * (z["q_s"] * F_ACT_DISENO + z["f_env"] * (P["UA_m2"] * (Tv - T_r) + P["q_sol_pico"])) / 1000.0
    Ql = A * z["q_l"] * F_ACT_DISENO / 1000.0
    V_s = m_a / P["rho_aire"]                                # m3/s
    W_vent = V_s * z["dp_vent"] / 1000.0 / P["eta_vent"]     # kW
    h_c = ah.entalpia(r["T_c"], r["W_c"])
    h_f = ah.h_agua_liquida(r["T_c"])
    m_cond = m_a * (r["W_mix"] - r["W_c"])
    cp_c = ah.cp_ah(r["W_c"])
    return dict(
        A=A, h_techo=P["h_techo"], ach_tot=z["ach_tot"], ach_oa=z["ach_oa"], V_m3h=cd["V_sup_m3h"], V_s=V_s, rho=P["rho_aire"],
        m_a=m_a, m_ae=m_ae, x_ae=x_ae, m_sens=cd["m_sens"], m_ach=cd["m_ach"], T_min=P["T_sup_min"],
        T_ext=Tv, W_ext=Wv, h_ext=h_ext, T_r=T_r, hr=z["hr_ver"], W_r=W_r, h_ret=h_ret, cp_r=cp_r,
        h_mix=r["h_mix"], W_mix=r["W_mix"], T_mix=r["T_mix"], q_s=z["q_s"], q_l=z["q_l"], f_act=F_ACT_DISENO, q_sol=P["q_sol_pico"],
        f_env=z["f_env"], Qs=Qs, Ql=Ql, T_imp=r["T_sup"], dT_vent=r["dT_vent"], dp=z["dp_vent"], eta_vent=P["eta_vent"],
        W_vent=W_vent, T_obj=r["T_obj"], W_c=r["W_c"], T_c=r["T_c"], h_c=h_c, h_f=h_f, m_cond=m_cond, cp_c=cp_c,
        Q_serp=r["Q_coil"], Q_lat=r["Q_coil_lat"], Q_sens=r["Q_coil_sens"], Q_rec=r["Q_recal"], HR_serp=P["HR_serp"],
        h_fg=P["h_fg"], r=r, Q_s_modelo=r["Q_s_zona_kW"], f_dia=z["f_dia"], q_sol_dia=P["q_sol_dia"],
    )


# ====================================================================================================================
# 2. Refrigeracion: ciclo al punto de diseno
# ====================================================================================================================
def caso_ciclo(c):
    P = c["P"]
    d = es.diseno(c)
    pl = d["planta"]
    cic = rf.ciclo(P["T_ev"], pl["T_cond"], P["refrigerante"], P["sobrecal"], P["subenf"], P["eta_is"], P["eta_motor"])
    Q_L = d["Q_L"]
    m_ref = Q_L / cic["q_L"]
    W_comp = Q_L / cic["cop_elec"]
    Q_cond = Q_L + P["eta_motor"] * W_comp
    m_w = Q_L / (ah.CP_W * P["dT_aguahelada"])
    W_bomba = (m_w / 1000.0) * P["dP_bomba"] / P["eta_bomba"] / 1000.0
    return dict(cic=cic, P=P, Q_L=Q_L, m_ref=m_ref, W_comp=W_comp, Q_cond=Q_cond, W_cond=P["f_vent_cond"] * Q_cond,
                m_w=m_w, W_bomba=W_bomba, T_cond=pl["T_cond"], T_ext=P["T_bs_ver"], eta_II=cic["cop_elec"] / cic["cop_carnot"],
                modelo=pl)


# ====================================================================================================================
# 3. Combustion: PCI como suma ponderada, perdida de gases y consumo de diseno
# ====================================================================================================================
def caso_comb(c):
    P = c["P"]
    cal = cb.caldera(P)
    b, pc = cal["balance"], cal["pc"]
    y = b["y"]
    comp = []
    for k, (x, h, hf) in cb.COMB.items():
        pci_i = x * (-cb.HF_CO2) + (h / 2.0) * (-cb.HF_H2O_G) + hf
        pcs_i = x * (-cb.HF_CO2) + (h / 2.0) * (-cb.HF_H2O_L) + hf
        comp.append(dict(nombre=k, y=y[k], pci=pci_i, pcs=pcs_i))
    pci_mezcla = sum(f["y"] * f["pci"] for f in comp)
    pcs_mezcla = sum(f["y"] * f["pcs"] for f in comp)
    inertes = y["N2"] + y["CO2"]
    prod, reac = b["productos"], b["reactivos"]
    esp = []
    for e in ("CO2", "H2O", "N2", "O2"):
        dh = cb.dh_sensible(e, P["T_gases"])
        esp.append(dict(nombre=e, n=prod[e], dh=dh, nh=prod[e] * dh))
    H_prod = sum(f["nh"] for f in esp)
    dh_o2 = cb.dh_sensible("O2", P["T_aire_comb"])
    dh_n2 = cb.dh_sensible("N2", P["T_aire_comb"])
    H_reac = reac["O2"] * dh_o2 + reac["N2_aire"] * dh_n2
    q_gases = (H_prod - H_reac) / pci_mezcla
    eta = 1.0 - q_gases - P["f_rad"]
    d = es.diseno(c)
    Q_inv = d["Q_caldera_invierno"]
    Q_acs_med = d["acs"]["kW"]
    f_punta = eq.SUPUESTOS["f_punta_acs"]["valor"]
    Q_acs_punta = f_punta * Q_acs_med
    Q_dis = Q_inv + Q_acs_punta
    E_pci = Q_dis / eta
    V_gas_h = E_pci / pc["PCI_kWh_m3"]
    n_prod = b["n_productos"]
    n_aire = reac["aire_total"]
    return dict(P=P, cal=cal, pc=pc, b=b, comp=comp, pci_mezcla=pci_mezcla, pcs_mezcla=pcs_mezcla, inertes=inertes,
                esp=esp, H_prod=H_prod, H_reac=H_reac, dh_o2=dh_o2, dh_n2=dh_n2, q_gases=q_gases, eta=eta,
                Q_inv=Q_inv, Q_acs_med=Q_acs_med, f_punta=f_punta, Q_acs_punta=Q_acs_punta, Q_dis=Q_dis, E_pci=E_pci,
                V_gas_h=V_gas_h, n_prod=n_prod, n_aire=n_aire, h_aire=H_reac / n_aire, h_gases=H_prod / n_prod,
                y_prod={e: prod[e] / n_prod for e in prod}, v_molar=pc["v_molar"])


# ====================================================================================================================
# 4. Anual: frio, calor rechazado, calor util, COP
# ====================================================================================================================
def balance_anual(c):
    P = c["P"]
    Rr = es.resumen(c)
    an = Rr["anual"]
    frio, W_comp = an["planta"]["Q_L"], an["elec"]["compresor"]
    Q_cond = an["planta"]["Q_cond"]
    W_cond, W_bomba, W_vent = an["elec"]["vent_condensador"], an["elec"]["bombas"], an["elec"]["ventiladores"]
    q = dict(recal=an["q_recal"], cal=an["q_cal"], hum=an["q_hum"], acs=an["q_acs"], total=an["q_util_total"])
    eta, pc = an["eta_caldera"], an["pc"]
    return dict(Rr=Rr, an=an, frio=frio, W_comp=W_comp, Q_cond=Q_cond, W_cond=W_cond, W_bomba=W_bomba, W_vent=W_vent,
                eta_mot=P["eta_motor"], q=q, eta=eta, pc=pc, E_gas_PCI=an["gas"]["E_PCI_kWh"], E_gas_PCS=an["gas"]["E_PCS_kWh"],
                V_gas=an["gas"]["V_m3"], E_elec=an["elec"]["total"], E_total=Rr["E_total"], cop_comp=frio / W_comp,
                cop_planta=frio / (W_comp + W_cond + W_bomba), cop_cond_ref=None)


# ====================================================================================================================
# 5. Cargas de diseno por zona (verano e invierno)
# ====================================================================================================================
def cargas_zona(c):
    d = es.diseno(c)
    filas = []
    for g in c["Z"]:
        v, i = d["verano"][g], d["invierno"][g]
        filas.append(dict(zona=g, serp=v["Q_coil"], sens=v["Q_coil_sens"], lat=v["Q_coil_lat"], rec=v["Q_recal"],
                          cal=i["Q_cal"] + i["Q_recal"], hum=i["Q_hum"], T_c=v["T_c"], T_sup=v["T_sup"]))
    tot = {k: sum(f[k] for f in filas) for k in ("serp", "sens", "lat", "rec", "cal", "hum")}
    return dict(filas=filas, total=tot, Q_L=d["Q_L"], Q_caldera_inv=d["Q_caldera_invierno"], d=d)


# ====================================================================================================================
# 6. Estados de las demas corrientes
# ====================================================================================================================
def estados_corrientes(c):
    P = c["P"]
    com = caso_comb(c)
    d = es.diseno(c)
    Ti, Wi = ed.estado_exterior_invierno(c)
    cpw = ah.CP_W
    camas = P["camas_gen"] + P["camas_uti"]
    return dict(
        com=com, Ti=Ti, Wi=Wi, hi=ah.entalpia(Ti, Wi), HRi=P["HR_inv"], pres=P["presion"] / 1000.0,
        cpw=cpw, T_ah=(ex._par(c, "T_cw_ida"), ex._par(c, "T_cw_ida") + P["dT_aguahelada"]),
        T_hw=(ex._par(c, "T_hw_ida"), ex._par(c, "T_hw_ret")), Q_L=d["Q_L"], m_ah=d["Q_L"] / (cpw * P["dT_aguahelada"]),
        Q_cal=com["Q_dis"], m_ac=com["Q_dis"] / (cpw * (ex._par(c, "T_hw_ida") - ex._par(c, "T_hw_ret"))),
        T_red=P["T_agua_fria"], T_acs=P["T_acs"],
        m_acs=P["L_cama_dia"] * camas / 86400.0, Q_acs=d["acs"]["kW"], h_vapor=2676.0, f_perd=P["f_perd_acs"],
        L=P["L_cama_dia"], camas=camas, dP=P["dP_bomba"] / 1000.0)


# ====================================================================================================================
# 7. Sensibilidad a las superficies y otras variaciones puntuales
# ====================================================================================================================
def _E(c, f=None):
    c2 = copy.deepcopy(c)
    if f:
        f(c2)
    return es.resumen(c2)["E_total"]


def sens_superficies(c):
    P = c["P"]
    base = _E(c)
    dE = lambda f: _E(c, f) / base - 1.0
    out = {}
    for clave, k in (("gen", "a_gen_cama"), ("or", "a_or"), ("uti", "a_uti_cama")):
        out[clave] = (dE(lambda c2, k=k: c2["P"].__setitem__(k, P[k] + 6.0)), dE(lambda c2, k=k: c2["P"].__setitem__(k, P[k] - 6.0)))
    out["acond"] = (dE(lambda c2: c2["P"].__setitem__("f_acond", 0.95)), dE(lambda c2: c2["P"].__setitem__("f_acond", 0.75)))
    out["g4"] = (dE(lambda c2: c2["P"].__setitem__("f_g4_24h", 0.50)), dE(lambda c2: c2["P"].__setitem__("f_g4_24h", 0.20)))
    out["est15"] = dE(lambda c2: c2["P"].__setitem__("T_cambio_estacion", 15.0))
    out["est21"] = dE(lambda c2: c2["P"].__setitem__("T_cambio_estacion", 21.0))
    out["fan0"] = dE(lambda c2: c2["P"].__setitem__("f_calor_vent", 0.0))
    out["eta065"] = dE(lambda c2: c2["P"].__setitem__("eta_is", 0.65))
    out["eta078"] = dE(lambda c2: c2["P"].__setitem__("eta_is", 0.78))
    return out


# ====================================================================================================================
# 8. Lectura de la tabla de mejoras
# ====================================================================================================================
def lectura_mejoras(c):
    base, filas = mj.comparar(c)
    por = {f["clave"]: f for f in filas}
    ahorro = lambda k: base["E_total"] - por[k]["E_total"]
    E_B = por["B"]["E_total"]
    m1_con_b = E_B - mj.anual_variante(c, {"rec_cond": True, "caldera_cond": True})["E_total"]
    m4_con_b = E_B - mj.anual_variante(c, {"rec_cond": True, "dp_vent": 0.8})["E_total"]

    def desglose(k):
        """Ahorro (positivo) de electricidad de los ventiladores y del resto, y gas (PCS) de mas (positivo) respecto del caso base."""
        d = por[k]["detalle"]
        d_vent = base["elec"]["ventiladores"] - d["elec"]["ventiladores"]
        d_resto = (base["E_elec"] - d["E_elec"]) - d_vent
        return dict(d_vent=d_vent, d_comp=base["elec"]["compresor"] - d["elec"]["compresor"], d_resto=d_resto,
                    d_gas=d["E_PCS"] - base["E_PCS"], d_E=ahorro(k), d_co2=por[k]["d_co2"])

    return dict(
        base=base, por=por, ahorro_ind=sum(ahorro(k) for k in ("B", "M1", "M2", "M3", "M4", "M5", "M6")), ahorro_paq=ahorro("P"),
        m1_solo=ahorro("M1"), m1_con_b=m1_con_b, m4_solo=ahorro("M4"), m4_con_b=m4_con_b, E_B=E_B,
        m4=desglose("M4"), m6=desglose("M6"),
    )


# ====================================================================================================================
# 9. Exergia de la caldera en el maximo recalentamiento
# ====================================================================================================================
def exergia_caldera(c):
    E = ex.estados_de_analisis(c)
    b = E["max_recalentamiento"]["resultado"]
    cal, glob = b["caldera"], b["global"]
    tb = {t["clave"]: t for t in b["tabla"]}
    X = cal["X_comb"]
    return dict(
        X_comb=X, X_aire=cal["X_aire"], D_comb=cal["D_combustion"], D_transf=cal["D_transferencia"], X_calor=cal["X_calor"],
        X_gas=cal["X_gas_quim"] + cal["X_gas_fis"], X_rad=cal["X_rad"], D_cal=cal["D_total"], eta=cal["eta_ex"],
        D_acs=tb["acs"]["X_dest"], D_total=glob["D_total"], X_in=glob["X_in"], D_cal_acs=b["destruccion_grupos"]["Caldera y ACS"],
        T_llama=cal["T_llama"], T0=E["max_recalentamiento"]["condiciones"]["T_out"])


# ====================================================================================================================
# Contraste del R134a con valores de tabla de uso corriente (de tabla, no del modelo)
# ====================================================================================================================
TABLA_R134A = {0: (293.0, 198.6), 40: (1017.0, 163.0)}      # T [C] -> (p_sat [kPa], h_fg [kJ/kg]); supuesto: valores de uso corriente


def contraste_r134a():
    out = []
    for T, (p_tab, hfg_tab) in TABLA_R134A.items():
        p = PropsSI("P", "T", T + 273.15, "Q", 1, "R134a") / 1e3
        hfg = (PropsSI("H", "T", T + 273.15, "Q", 1, "R134a") - PropsSI("H", "T", T + 273.15, "Q", 0, "R134a")) / 1e3
        out.append(dict(T=T, p=p, hfg=hfg, p_tab=p_tab, hfg_tab=hfg_tab, dp=p / p_tab - 1.0, dh=hfg / hfg_tab - 1.0))
    return out


# ====================================================================================================================
# Cache: los casos tardan un par de segundos en conjunto y se piden desde tablas y valores
# ====================================================================================================================
_CACHE = {}


def _ctx(c):
    clave = json.dumps(c, sort_keys=True, default=str)
    if clave not in _CACHE:
        _CACHE.clear()
        _CACHE[clave] = dict(
            g1=caso_g1(c), ciclo=caso_ciclo(c), comb=caso_comb(c), anual=balance_anual(c), cargas=cargas_zona(c),
            corr=estados_corrientes(c), sup=sens_superficies(c), mej=lectura_mejoras(c), exc=exergia_caldera(c),
            r134a=contraste_r134a(), eqp=eq.resumen_equipos(c), sens_all=es.sensibilidad(c))
    return _CACHE[clave]


# ====================================================================================================================
# Texto de respaldo de los parametros (marca + motivo). {clave} se reemplaza por la marca de la referencia.
# ====================================================================================================================
def _refs():
    return {c: R(c) for c, _t, _s in referencias.REFERENCIAS}


def _valor(v, factor=1.0):
    if isinstance(v, str):
        return v
    if isinstance(v, tuple):
        return ", ".join(str(x) for x in v)
    v = v * factor
    if isinstance(v, int) or (isinstance(v, float) and v == int(v) and abs(v) >= 100):
        return n(v)
    if abs(v) >= 1000:
        return n(v)
    return supuestos._fmt(float(v))


# (id o grupo de ids, nombre con tildes, unidad, motivo). Un motivo sin marca de fuente empieza con «supuesto» o «constante».
def _params_modelo(S):
    sup = SUP_CORRIENTE
    return [
        (("E1",), "Superficie cubierta total", "m²", "{presidencia} cifra oficial de la presentación del hospital; otra fuente cita «más de 20.000 m²» sin aclarar si es superficie cubierta {gacetilla}"),
        (("E2",), "Fracción de la superficie cubierta que se climatiza", "–", f"supuesto: casi todo se climatiza; se excluyen locales técnicos, morgue y depósitos (con 95 y 75 % la energía cambia {S['acond_txt']})"),
        (("E3",), "Camas de internación general", "camas", "{gacetilla} la atribuye a la sala de cuidados progresivos; se toma como parte del total del hospital (interpretación propia; {presidencia} prevé 160 camas de internación)"),
        (("E4",), "Camas de terapia intensiva", "camas", "{gacetilla} mismo criterio que E3"),
        (("E5",), "Cantidad de quirófanos", "–", "{presidencia} cifra de programa"),
        (("E6",), "Superficie por quirófano", "m²", "supuesto: unos 6,5 × 6,5 m con el equipamiento fijo; {fgi} pide al menos 400 pie² (37,2 m²) libres"),
        (("E7",), "Superficie por cama de terapia intensiva", "m²/cama", "supuesto: 9 m² por cama de paciente {res748} por 2,7 de apoyo y circulación"),
        (("E8",), "Superficie por cama de internación general", "m²/cama", "supuesto: habitación con baño, office y circulaciones, sin referencia (±6 m² cambian la energía ±1,6 %)"),
        (("E9",), "Altura libre de los locales", "m", "supuesto: convención de diseño"),
        (("E10",), "Conductancia de la envolvente por m² de piso expuesto", "W/(m² K)", "supuesto: tres pisos con 25 % de vidrio; techo, muros y vidrios en conjunto"),
        (("E11",), "Ganancia solar del punto de diseño de verano", "W/m²", "supuesto: hora pico en las zonas expuestas"),
        (("E12",), "Ganancia solar media de las 12 h diurnas", "W/m²", "supuesto: promedio diurno anual; 0 de noche"),
        (("E13",), "Densidad del aire para convertir caudales", "kg/m³", "supuesto: convención (aire a unos 20 °C)"),
        (("E14",), "Fracción de las áreas generales que funciona las 24 h", "–", "supuesto: la guardia atiende las 24 h {gacetilla}; el resto (consultorios, administración y docencia) funciona de día"),
        (("C1",), "Temperatura de bulbo seco de diseño, verano", "°C", sup),
        (("C2",), "Temperatura de bulbo húmedo coincidente, verano", "°C", sup),
        (("C3",), "Temperatura de bulbo seco de diseño, invierno", "°C", sup),
        (("C4",), "Humedad relativa de diseño, invierno", "–", sup),
        (("C5",), "Presión atmosférica", "kPa", "supuesto: nivel del mar (Buenos Aires está a unos 25 m: diferencia de 0,3 %)"),
        (("C6",), "Amplitud diaria de temperatura (máxima menos mínima)", "K", "supuesto: aproximada; parte cada mes en mitad diurna y nocturna"),
        (("A1",), "Temperatura mínima del aire de impulsión", "°C", "supuesto: límite de confort y de condensación en difusores"),
        (("A2",), "Temperatura máxima del aire de impulsión", "°C", "supuesto: límite de calefacción por aire"),
        (("A3",), "Humedad relativa del aire a la salida de la serpentina", "–", "supuesto: serpentina de agua helada con aproximación al saturado"),
        (("A4",), "Temperatura exterior bajo la cual rigen las consignas de invierno", "°C", f"supuesto: criterio de cambio de estación (a 15 y 21 °C la energía cambia {S['est_txt']})"),
        (("A5",), "Rendimiento total de los ventiladores", "–", "supuesto: ventilador, motor y transmisión"),
        (("A6",), "Temperatura del agua de red para el vapor de humidificación", "°C", "supuesto: igual que S3"),
        (("A7",), "Calor latente de vaporización del agua (referencia de 0 °C)", "kJ/kg", "constante: propiedad del agua"),
        (("A8",), "Fracción de la potencia del ventilador que se disipa como calor en el aire", "–", f"supuesto: el ventilador aspira después de la serpentina; con el motor fuera de la corriente sería 0,85 a 0,95 (sin calor de ventilador la energía sube {S['fan_txt']})"),
        (("R1",), "Refrigerante de la enfriadora", "–", "supuesto: HFC habitual en enfriadoras de tornillo; propiedades de {coolprop}"),
        (("R2",), "Temperatura de evaporación", "°C", "supuesto: agua helada 7/12 °C con aproximación del evaporador"),
        (("R3",), "Sobrecalentamiento a la salida del evaporador", "K", sup),
        (("R4",), "Subenfriamiento a la salida del condensador", "K", sup),
        (("R5",), "Rendimiento isentrópico del compresor", "–", f"supuesto: compresor de tornillo (con 0,65 y 0,78 la energía cambia {S['eta_txt']})"),
        (("R6",), "Rendimiento del motor eléctrico del compresor", "–", sup),
        (("R7",), "Diferencia entre condensación y temperatura exterior", "K", "supuesto: condensador enfriado por aire"),
        (("R8",), "Temperatura mínima de condensación", "°C", "supuesto: el control de presión de descarga del compresor de tornillo exige una diferencia de presión mínima"),
        (("R9",), "Potencia de ventiladores del condensador / calor rechazado", "–", sup),
        (("R10",), "Salto de temperatura del agua helada", "K", "supuesto: agua helada 7/12 °C"),
        (("R11",), "Diferencia de presión de las bombas de agua helada", "kPa", "supuesto: circuitos primario y secundario en conjunto (unos 25 m de columna de agua)"),
        (("R12",), "Rendimiento total de las bombas", "–", sup),
        (("B1", "B2", "B3", "B4", "B5"), "Gas natural: CH₄, C₂H₆, C₃H₈, N₂ y CO₂ (fracción molar)", "–", "supuesto: composición típica del gas natural"),
        (("B6",), "Relación de aire (1 = estequiométrico)", "–", "supuesto: 15 % de exceso de aire"),
        (("B7",), "Temperatura de los gases de escape", "°C", "supuesto: caldera sin condensación"),
        (("B8",), "Temperatura del aire de combustión", "°C", "supuesto: aire de la sala de calderas; el gas entra a 25 °C (referencia de las entalpías) y no aporta calor sensible"),
        (("B9",), "Pérdidas por radiación y funcionamiento / calor liberado", "–", sup),
        (("B10",), "Temperatura de referencia del volumen de gas", "°C", "constante: m³ estándar a 15 °C y 101,325 kPa"),
        (("S1",), "Consumo de ACS por cama y día", "L/(cama día)", "supuesto: entre los casos medidos (50 a 55) y los ratios de diseño (200 a 300) de {hospitecnia}"),
        (("S2",), "Temperatura del ACS", "°C", "{hospitecnia} 55 L por cama y día a 60 °C"),
        (("S3",), "Temperatura del agua fría de entrada", "°C", "supuesto: media anual aproximada del agua de red de Buenos Aires"),
        (("S4",), "Factor por pérdidas de acumulación y recirculación", "–", "supuesto: {hospitecnia} muestra 1,6 veces entre su tabla y el calor sensible; se toma 1,3"),
    ]


_CONV = {"R11": 1e-3, "C5": 1e-3}


def _txt_sens(a, b=None):
    """'+x / -y %' o '±x %' si los dos signos coinciden en la primera decimal."""
    if b is None:
        return ("+" if a > 0 else "−") + n(abs(a) * 100, 1) + " %"
    if abs(abs(a) - abs(b)) * 100 < 0.05:
        return "±" + n(abs(a) * 100, 1) + " %"
    return ("+" if a > 0 else "−") + n(abs(a) * 100, 1) + " % y " + ("+" if b > 0 else "−") + n(abs(b) * 100, 1) + " %"


def tabla_parametros(c):
    x = _ctx(c)
    sup = x["sup"]
    S = dict(acond_txt=_txt_sens(*sup["acond"]), est_txt=_txt_sens(sup["est15"]) + " y " + _txt_sens(sup["est21"]),
             fan_txt=_txt_sens(sup["fan0"]), eta_txt=_txt_sens(sup["eta065"]) + " y " + _txt_sens(sup["eta078"]))
    filas_modelo = {f[0]: f for f in supuestos.filas()}
    refs = _refs()
    out = []
    for ids, nombre, uni, motivo in _params_modelo(S):
        vals = [_valor(filas_modelo[i][3], _CONV.get(i, 1.0)) for i in ids]
        val = " / ".join(vals)
        idt = ids[0] if len(ids) == 1 else f"{ids[0]}–{ids[-1]}"
        out.append((idt, nombre, val, uni, motivo.format(**refs)))
    return tabla(["ID", "Parámetro", "Valor", "Unidad", "Respaldo: marca y motivo"], out, (5, 30, 9, 8, 48))


def ids_params_modelo():
    return [i for ids, *_ in _params_modelo(dict(acond_txt="", est_txt="", fan_txt="", eta_txt="")) for i in ids]


# ---- parametros de las mejoras (PM1 a PM14)
_PM = {
    "PM1": ("Temperatura del agua caliente del recuperador de calor del condensador", "°C",
            "supuesto: la serpentina de recalentamiento lleva el aire de unos 13 °C a 17-19 °C y alcanza con agua tibia; un hospital con enfriadoras de recuperación usa agua a 46 °C (115 °F) en vez de 82 °C (180 °F) de caldera {trane}"),
    "PM2": ("Diferencia mínima entre la condensación y el agua caliente del recuperador", "K", "supuesto: intercambiador de placas típico"),
    "PM3": ("Temperatura de los gases de escape de la caldera de condensación", "°C", "supuesto: agua de retorno a 40 °C y 5 K de aproximación; por debajo del rocío de los gases (unos 56 °C)"),
    "PM4": ("Superficie de colectores solares para el ACS", "m²", "supuesto: unos 5 % de la azotea (6.117 m² por nivel); tamaño que no produce excedentes en verano"),
    "PM5": ("Rendimiento medio anual de los colectores (sobre irradiación horizontal)", "–", "supuesto: colector plano a 40-60 °C con pérdidas ópticas y térmicas, sin dato de catálogo"),
    "PM6": ("Irradiación global horizontal anual", "kWh/(m² año)",
            "{gsa} informe de un punto de la provincia de Buenos Aires a unos 300 km: es una cota alta para la ciudad"),
    "PM7": ("Latitud del hospital", "°", "supuesto: La Matanza, Buenos Aires"),
    "PM8": ("Potencia fotovoltaica instalada", "kWp", "supuesto: unos 1.250 m² de paneles (5 m²/kWp) sobre una azotea de 6.117 m² con equipos"),
    "PM9": ("Relación de rendimiento (performance ratio) de la instalación fotovoltaica", "–", "supuesto: valor habitual de instalaciones nuevas (0,75 a 0,85)"),
    "PM10": ("Efectividad del recuperador del aire de extracción con circuito de agua", "–", "supuesto: valor de uso corriente (45 a 55 % con aislación total entre corrientes)"),
    "PM11": ("Caída de presión adicional del recuperador (cada lado)", "Pa", "supuesto: serpentina de 4 filas en cada corriente"),
    "PM12": ("Factor sobre la presión de los ventiladores en la mejora M4", "–", "supuesto: filtros y conductos de menor pérdida, ventiladores de velocidad variable"),
    "PM13": ("Factor de emisión de la electricidad de la red", "t CO₂/MWh",
             "{cammesa} meta de 380 kg CO₂e/MWh para 2023: es una meta y no un dato medido; otras citas dan 0,29 y 0,40 t/MWh (se prueba el rango en la sección 8)"),
    "PM14": ("Temperatura mínima de descarga del compresor para recuperar calor sin subir la condensación", "°C", "supuesto: agua a 45 °C más 5 K de aproximación"),
}


def tabla_params_mejoras():
    refs = _refs()
    filas = []
    for (i, _k, _nom, v, _u_, _e, _j) in mj.PARAMETROS:
        nombre, uni, motivo = _PM[i]
        filas.append((i, nombre, _valor(v), uni, motivo.format(**refs)))
    return tabla(["ID", "Parámetro", "Valor", "Unidad", "Respaldo: marca y motivo"], filas, (5, 30, 8, 9, 48))


# ====================================================================================================================
# Tablas del capitulo 1 y 2: sistemas, estados de las corrientes, propiedades y nomenclatura
# ====================================================================================================================
def tabla_nomenclatura():
    f = [("$\\dot m_a$", "caudal de aire seco [kg/s]", "$\\dot X_F,\\ \\dot X_P,\\ \\dot X_L,\\ \\dot X_D$", "exergía del combustible, del producto, perdida y destruida [kW]"),
         ("$\\omega$", "humedad específica [kg/kg de aire seco; g/kg en tablas]", "$T_0$", "temperatura del estado muerto, la del aire exterior [K]"),
         ("$h$", "entalpía específica [kJ/kg; kJ/kmol en la combustión]", "$\\rho$", "densidad [kg/m³]"),
         ("$T$, $P$", "temperatura [°C] y presión [kPa]", "$\\Delta p$", "caída de presión [Pa o kPa]"),
         ("$\\dot Q$", "flujo de calor [kW]; $\\dot Q_L$ es el frío de la enfriadora", "$f_{act}$", "actividad: fracción de la ganancia interna de plena actividad [–]"),
         ("$\\dot W$", "potencia eléctrica o mecánica [kW]", "$f_{env}$, $U$", "fracción de envolvente expuesta [–]; conductancia [W/(m² K)]"),
         ("$\\eta$", "rendimiento [–]: $\\eta_{is}$ isentrópico, $\\eta_{mot}$ del motor, $\\eta_{vent}$ del ventilador", "$q_s$, $q_l$", "ganancias internas sensible y latente a plena actividad [W/m²]"),
         ("$q_L$, $q_H$, $w$", "efecto frigorífico, calor rechazado y trabajo de compresión por kg de refrigerante [kJ/kg]", "$\\lambda$", "relación de aire de la combustión (1 = estequiométrico) [–]"),
         ("$COP$", "coeficiente de desempeño [–]", "$y_i$, $n_i$", "fracción molar [–] y moles por kmol de gas [kmol/kmol]"),
         ("$PCI$, $PCS$", "poder calorífico inferior y superior [kJ/kmol; kWh/m³ estándar]", "$E$", "energía anual [MWh]; final = electricidad + gas (PCS)")]
    return tabla(["Símbolo", "Significado y unidad", "Símbolo", "Significado y unidad"], f, (11, 39, 11, 39))


def tabla_sistemas(c):
    P = c["P"]
    T_f, T_c_ = _ctx(c)["corr"]["T_ah"]
    T_h1, T_h2 = _ctx(c)["corr"]["T_hw"]
    f_perd = (P["f_perd_acs"] - 1.0) * 100
    filas = [
        ("**Unidad de tratamiento de aire** (una por zona)",
         "Mezcla de aire exterior y de retorno, serpentina de enfriamiento, recalentador, ventilador de impulsión y humidificador de vapor",
         "Aire exterior y aire de retorno; electricidad del ventilador; calor del agua caliente (recalentador y calefacción); vapor de humidificación (invierno)",
         f"Aire de impulsión; calor retirado por el agua helada ({n(T_f)} → {n(T_c_)} °C); condensado de la serpentina"),
        ("**Enfriadora** (R134a)",
         "Compresor, condensador, válvula de expansión y evaporador",
         f"Calor del agua helada ({n(T_c_)} → {n(T_f)} °C) en el evaporador; electricidad del compresor",
         "Calor rechazado al aire exterior en el condensador (hoy se pierde)"),
        ("**Caldera de gas natural**",
         "Cámara de combustión e intercambiador de calor",
         f"Gas natural (25 °C) y aire de combustión ({n(P['T_aire_comb'])} °C), a 101,3 kPa",
         f"Gases de escape ({n(P['T_gases'])} °C); calor útil al agua caliente ({n(T_h1)} → {n(T_h2)} °C); pérdidas por radiación ({n(P['f_rad'] * 100, 1)} % del PCI)"),
        ("**Producción de ACS**",
         "Acumulación y recirculación del agua caliente sanitaria",
         f"Agua de red ({n(P['T_agua_fria'])} °C); calor de la caldera",
         f"Agua caliente a {n(P['T_acs'])} °C; pérdidas de acumulación y recirculación ({n(f_perd)} % del calor útil)"),
    ]
    return tabla(["Sistema", "Límite del volumen de control", "Entra", "Sale"], filas, (14, 26, 30, 30))


def tabla_estados_corrientes(c):
    x = _ctx(c)
    P, k, com = c["P"], x["corr"], x["comb"]
    cpw = k["cpw"]
    T_f, T_c_ = k["T_ah"]
    T_h1, T_h2 = k["T_hw"]
    f = [
        ("Gas natural",
         "25", "101,3", "$h$ = 0 (referencia); energía química: PCI = %s kWh/m³ = %s kJ/m³" % (n(com["pc"]["PCI_kWh_m3"], 3), n(com["pc"]["PCI_MJ_m3"] * 1000)),
         "supuesto: composición típica (%s %% de CH₄); entra a la referencia de las entalpías y no aporta calor sensible" % n(P["gas_CH4"] * 100)),
        ("Aire de combustión",
         n(P["T_aire_comb"]), "101,3", "$h$ = %s kJ/kmol; $c_p$ ≈ %s kJ/(kmol K)" % (nn(com["h_aire"], 1), n(-com["h_aire"] / (25.0 - P["T_aire_comb"]), 1)),
         "supuesto: aire de la sala de calderas; 21 %% de O₂ y 79 %% de N₂; $\\lambda$ = %s" % n(P["lambda_aire"], 2)),
        ("Gases de escape",
         n(P["T_gases"]), "101,3", "$h$ = %s kJ/kmol; $c_p$ ≈ %s kJ/(kmol K)" % (n(com["h_gases"]), n(com["h_gases"] / (P["T_gases"] - 25.0), 1)),
         "%s %% de agua (CO₂ %s %%, N₂ %s %%, O₂ %s %%); punto de rocío %s °C: no condensan" % (
             n(com["y_prod"]["H2O"] * 100, 1), n(com["y_prod"]["CO2"] * 100, 1), n(com["y_prod"]["N2"] * 100, 1), n(com["y_prod"]["O2"] * 100, 1), n(com["cal"]["T_rocio"], 1))),
        ("Agua helada",
         f"{n(T_f)} (impulsión) y {n(T_c_)} (retorno)", "no se calcula (solo $\\Delta p$ = %s kPa de las bombas)" % n(k["dP"]),
         "$c_p$ = %s kJ/(kg K); $h$ = %s y %s kJ/kg" % (n(cpw, 3), n(cpw * T_f, 1), n(cpw * T_c_, 1)),
         "supuesto: agua 7/12 °C (salto de %s K); $\\dot m_w$ = %s kg/s para %s kW de frío" % (n(P["dT_aguahelada"]), n(k["m_ah"], 1), n(k["Q_L"]))),
        ("Agua caliente",
         f"{n(T_h1)} (impulsión) y {n(T_h2)} (retorno)", "idem",
         "$c_p$ = %s kJ/(kg K); $h$ = %s y %s kJ/kg" % (n(cpw, 3), n(cpw * T_h1, 1), n(cpw * T_h2, 1)),
         "supuesto: circuito de recalentamiento, calefacción y ACS que el modelo base no fija; $\\dot m$ = %s kg/s para %s kW" % (n(k["m_ac"], 1), n(k["Q_cal"]))),
        ("ACS",
         f"{n(k['T_red'])} (entrada) y {n(k['T_acs'])} (salida)", "idem",
         "$c_p$ = %s kJ/(kg K); $h$ = %s y %s kJ/kg" % (n(cpw, 3), n(cpw * k["T_red"], 1), n(cpw * k["T_acs"], 1)),
         "%s L por cama y día (supuesto); $\\dot m$ = %s kg/s; $\\dot Q$ = %s kW con $f_{perd}$ = %s" % (n(k["L"]), n(k["m_acs"], 3), n(k["Q_acs"], 1), n(k["f_perd"], 1))),
        ("Aire exterior de invierno (diseño)",
         n(k["Ti"]), "101,3", "$\\omega$ = %s g/kg; $h$ = %s kJ/kg" % (n(k["Wi"] * 1000, 2), n(k["hi"], 1)),
         "supuesto (valor de uso corriente): %s %% de humedad relativa" % n(k["HRi"] * 100)),
    ]
    return tabla(["Corriente", "T [°C]", "P [kPa]", "$h$ o $c_p$", "Observaciones y respaldo"], f, (13, 14, 12, 26, 35))


def tabla_propiedades(c):
    r = _refs()
    pc = _ctx(c)["comb"]
    ver_cp, ver_ps = md.version("CoolProp"), md.version("psychrolib")
    f = [
        ("Aire húmedo", "$\\omega$, $h$, humedad relativa, temperatura de rocío y de bulbo húmedo a 101,325 kPa; $c_{p,a}$ = 1,006 y $c_{p,v}$ = 1,86 kJ/(kg K); $h_{fg}$ = 2.501 kJ/kg",
         f"psychrolib {ver_ps} {r['coolprop']} (psicrometría de ASHRAE en unidades SI); las tres constantes son las de su ecuación de entalpía", "Estados del aire, cargas de serpentina y recalentador (sección 3)"),
        ("Agua líquida y vapor", "$c_p$ = 4,186 kJ/(kg K); $h_g$ = 2.676 kJ/kg (vapor saturado a 101,3 kPa); calor latente a 25 °C: 44.010 kJ/kmol; presión de saturación",
         f"constantes del modelo: {SUP_CORRIENTE}; presión de saturación de CoolProp {ver_cp} {r['coolprop']}", "ACS, humidificación, agua helada y caliente, rocío y caldera de condensación"),
        ("R134a", "presión de saturación, $h$, $s$, $T$ a partir de ($P$, $h$), título y densidad",
         f"CoolProp {ver_cp} {r['coolprop']}", "Ciclo de la enfriadora (sección 4); comparación con R1234ze(E) y R1234yf (sección 8)"),
        ("CO₂, H₂O, N₂ y O₂ (aire y gases de combustión)", "$c_p$ de gas ideal (término ideal de CoolProp), integrado desde 25 °C hasta $T$",
         f"CoolProp {ver_cp} {r['coolprop']}", "Pérdida por gases, temperatura de llama, caldera de condensación (sección 5)"),
        ("CH₄, C₂H₆, C₃H₈, CO₂, H₂O", "entalpías de formación a 25 °C [kJ/kmol]: −74.850; −84.680; −103.850; −393.520; −241.820 (vapor) y −285.830 (líquido)",
         f"tablas de termodinámica: {SUP_CORRIENTE}", "PCI, PCS y temperatura de llama (sección 5)"),
        ("Gas natural", f"composición {n(c['P']['gas_CH4'] * 100)}/{n(c['P']['gas_C2H6'] * 100)}/{n(c['P']['gas_C3H8'] * 100)}/{n(c['P']['gas_N2'] * 100)}/{n(c['P']['gas_CO2'] * 100)} % molar (CH₄, C₂H₆, C₃H₈, N₂, CO₂); PCS y PCI se calculan",
         "supuesto: composición típica del gas de red", "Combustión y consumo de gas (sección 5)"),
        ("Exergía química estándar", "valores por kmol de cada componente del gas natural, del aire y de los gases (sección 9)",
         f"{SUP_CORRIENTE}: los atribuidos a Szargut", "Exergía del combustible (sección 9)"),
    ]
    return tabla(["Sustancia", "Propiedades", "Fuente", "Dónde se usa"], f, (14, 30, 31, 25))


def linea_r134a():
    cont = contraste_r134a()
    partes = [f"a {n(f['T'])} °C, {n(f['p'], 1)} kPa y $h_{{fg}}$ = {n(f['hfg'], 1)} kJ/kg (CoolProp) contra {n(f['p_tab'])} kPa y {n(f['hfg_tab'], 1)} kJ/kg de la tabla" for f in cont]
    dif = max(max(abs(f["dp"]), abs(f["dh"])) for f in cont) * 100
    return ("**Contraste del R134a.** En dos puntos de saturación, " + "; ".join(partes) + f" (diferencias menores que {n(max(dif, 0.1) + 0.0, 1)} %); "
            "los valores de tabla son los de uso corriente y están sin contrastar con el texto (supuesto).")


# ====================================================================================================================
# Tablas del caso de aire humedo, cargas por zona y ciclo
# ====================================================================================================================
def tabla_psicro(c):
    g = _ctx(c)["g1"]
    P = c["P"]
    pres = P["presion"]
    r = g["r"]
    est = [("A", "Aire exterior", g["T_ext"], g["W_ext"], g["h_ext"]),
           ("B", "Local (consigna) y retorno", g["T_r"], g["W_r"], g["h_ret"]),
           ("C", f"Mezcla con el retorno ({n(g['x_ae'] * 100)} % de aire exterior)", g["T_mix"], g["W_mix"], g["h_mix"]),
           ("D", f"Salida de la serpentina ({n(g['HR_serp'] * 100)} % de HR)", g["T_c"], g["W_c"], g["h_c"]),
           ("E", "Tras el recalentador", g["T_obj"], g["W_c"], ah.entalpia(g["T_obj"], g["W_c"])),
           ("F", f"Impulsión, tras el ventilador (+{n(g['dT_vent'], 3)} K)", g["T_imp"], g["W_c"], ah.entalpia(g["T_imp"], g["W_c"]))]
    filas = [(a, b, nn(t, 2), nn(w * 1000, 3), nn(h, 2), n(ah.hr_desde_w(t, w, pres) * 100)) for a, b, t, w, h in est]
    return tabla(["Estado", "Descripción", "T [°C]", "ω [g/kg]", "h [kJ/kg]", "HR [%]"], filas, (8, 38, 11, 12, 12, 9))


def tabla_cargas(c):
    cz = _ctx(c)["cargas"]
    nom = {"G1": "G1 Quirófanos", "G2": "G2 Terapia intensiva", "G3": "G3 Internación general", "G4": "G4 Guardia, imágenes y laboratorio", "G5": "G5 Consultorios y administración"}
    filas = [(nom[f["zona"]], n(f["serp"], 1), n(f["sens"], 1), n(f["lat"], 1), n(f["rec"], 1), n(f["cal"], 1), n(f["hum"], 1)) for f in cz["filas"]]
    t = cz["total"]
    filas.append(("**Total**", f"**{n(t['serp'], 1)}**", f"**{n(t['sens'], 1)}**", f"**{n(t['lat'], 1)}**", f"**{n(t['rec'], 1)}**", f"**{n(t['cal'], 1)}**", f"**{n(t['hum'], 1)}**"))
    return tabla(["Zona", "Serpentina [kW]", "Sensible [kW]", "Latente [kW]", "Recalentamiento (verano) [kW]", "Calefacción (invierno) [kW]", "Humidificación (invierno) [kW]"],
                 filas, (27, 12, 11, 11, 14, 13, 14))


def tabla_ciclo(c):
    cc = _ctx(c)["ciclo"]
    cic, P = cc["cic"], cc["P"]
    f = [("1", "Salida del evaporador (vapor sobrecalentado %s K)" % n(P["sobrecal"]), n(cic["T1"], 2), n(cic["P_ev"] / 1e3, 1), n(cic["h1"], 2)),
         ("2s", "Salida del compresor, isentrópica", "–", n(cic["P_c"] / 1e3, 1), n(cic["h2s"], 2)),
         ("2", "Salida del compresor, real (rendimiento isentrópico %s)" % n(P["eta_is"], 2), n(cic["T2"], 2), n(cic["P_c"] / 1e3, 1), n(cic["h2"], 2)),
         ("3", "Salida del condensador (subenfriado %s K)" % n(P["subenf"]), n(cic["T3"], 2), n(cic["P_c"] / 1e3, 1), n(cic["h3"], 2)),
         ("4", "Salida de la válvula de expansión (título %s)" % n(cic["x4"], 2), n(P["T_ev"], 2), n(cic["P_ev"] / 1e3, 1), n(cic["h4"], 2))]
    return tabla(["Estado", "Descripción", "T [°C]", "P [kPa]", "h [kJ/kg]"], f, (8, 50, 11, 12, 12))


def tabla_pci(c):
    cm = _ctx(c)["comb"]
    nombres = {"CH4": "CH₄", "C2H6": "C₂H₆", "C3H8": "C₃H₈"}
    filas = [(nombres[f["nombre"]], n(f["y"], 2), n(f["pci"]), n(f["y"] * f["pci"]), n(f["pcs"]), n(f["y"] * f["pcs"])) for f in cm["comp"]]
    filas.append(("N₂ y CO₂ (inertes)", n(cm["inertes"], 2), "0", "0", "0", "0"))
    filas.append(("**Mezcla**", "**1,00**", "", f"**{n(cm['pci_mezcla'])}**", "", f"**{n(cm['pcs_mezcla'])}**"))
    return tabla(["Componente", "$y_i$ [kmol/kmol]", "$PCI_i$ [kJ/kmol]", "$y_i\\,PCI_i$ [kJ/kmol de gas]", "$PCS_i$ [kJ/kmol]", "$y_i\\,PCS_i$ [kJ/kmol de gas]"], filas, (18, 14, 16, 18, 16, 18))


def tabla_gases(c):
    cm = _ctx(c)["comb"]
    P = cm["P"]
    nom = {"CO2": "CO₂", "H2O": "H₂O", "N2": "N₂", "O2": "O₂"}
    r = cm["b"]["reactivos"]
    filas = [(nom[f["nombre"]] + " (producto)", n(f["n"], 3), n(f["dh"]), n(f["nh"])) for f in cm["esp"]]
    filas.append(("**Σ productos: $H_{prod}$**", "**%s**" % n(cm["n_prod"], 3), "", "**%s**" % n(cm["H_prod"])))
    filas.append((f"O₂ del aire ({n(P['T_aire_comb'])} °C)", n(r["O2"], 3), nn(cm["dh_o2"], 1), nn(r["O2"] * cm["dh_o2"])))
    filas.append((f"N₂ del aire ({n(P['T_aire_comb'])} °C)", n(r["N2_aire"], 3), nn(cm["dh_n2"], 1), nn(r["N2_aire"] * cm["dh_n2"])))
    filas.append(("**Σ reactivos: $H_{reac}$**", "**%s**" % n(cm["n_aire"], 3), "", "**%s**" % nn(cm["H_reac"])))
    return tabla(["Especie", "$n_i$ [kmol/kmol de gas]", "$\\Delta h_i$ [kJ/kmol]", "$n_i\\,\\Delta h_i$ [kJ/kmol de gas]"], filas, (30, 22, 20, 28))


# ====================================================================================================================
# Texto: lectura de la tabla de mejoras, refrigerante, nota de superficies, atomos
# ====================================================================================================================
def texto_lectura_mejoras(c):
    m = _ctx(c)["mej"]
    base, por = m["base"], m["por"]
    M = lambda x: n(x / 1e3)
    m4, m6 = m["m4"], m["m6"]
    d_ua = _sens_c(c, lambda c2: c2["P"].__setitem__("UA_m2", c2["P"]["UA_m2"] * 0.7))
    d_gi = _sens_c(c, lambda c2: [(z.__setitem__("q_s", z["q_s"] * 0.7), z.__setitem__("q_l", z["q_l"] * 0.7)) for z in c2["Z"].values()])
    p1 = (f"**Las medidas casi se suman, pero cada una depende de las demás.** Sueltas, las siete medidas (B y M1 a M6) ahorran {M(m['ahorro_ind'])} MWh y el paquete, {M(m['ahorro_paq'])} MWh. "
          f"Que los totales casi coincidan no significa que las medidas sean independientes: unos efectos se compensan con otros. Con B, la caldera de condensación (M1) ahorra {M(m['m1_con_b'])} MWh en vez de {M(m['m1_solo'])}, porque B ya quitó "
          f"gran parte del gas del recalentamiento y queda menos gas al que mejorarle el rendimiento. Con B, los ventiladores de menor presión (M4) ahorran {M(m['m4_con_b'])} MWh en vez de "
          f"{M(m['m4_solo'])}: el calor que el ventilador deja de ceder al aire hay que reponerlo, y con B lo repone el calor del condensador, que de otro modo se tiraría, y no el gas.")
    p2 = (f"**M4, ventiladores con 20 % menos de presión.** A caudal constante la potencia $\\dot W = \\dot V\\,\\Delta p/\\eta$ es proporcional a la presión: los ventiladores consumen {M(m4['d_vent'])} MWh menos "
          f"y el compresor y los ventiladores del condensador, {M(m4['d_resto'])} MWh menos (donde la serpentina solo enfría hasta $T_{{obj}}$, que ahora es más alta, hay menos carga). "
          f"Pero toda esa potencia se disipaba como calor en el aire de impulsión, y ahora el recalentador y la calefacción deben aportarlo: la caldera usa {M(m4['d_gas'])} MWh más de gas (PCS). "
          f"La energía final baja solo {n(por['M4']['d_E'] * -100, 1)} %, porque se cambia trabajo por calor que se paga con gas; "
          f"las emisiones bajan {n(por['M4']['d_co2'] * -100, 1)} %, porque el gas emite menos CO\u2082 por kWh que la electricidad de la red ({n(mj.factor_co2_gas(c['P']), 3)} kg por kWh de PCI contra {n(mj.parametro('ef_elec'), 2)} kg por kWh). "
          f"Desde la Segunda Ley, la potencia de un ventilador es trabajo puro que se degrada a calor a baja temperatura dentro del aire: evitarla es ganar exergía, aunque la energía neta cambie poco.")
    p3 = (f"**M6, quirófanos al 50 % de noche.** De noche el quirófano no tiene actividad ($f_{{act}}$ = 0) y se baja el caudal de G1 a la mitad. La potencia del ventilador sigue las leyes de los ventiladores, "
          f"$\\dot W \\propto \\dot V^3$ para un mismo sistema de conductos: a la mitad del caudal queda en $0{{,}}5^3$ = 12,5 % y se ahorra el 87,5 % de la potencia de G1 en esas horas ({M(m6['d_vent'])} MWh por año); "
          f"además hay menos aire exterior que enfriar o calentar ({M(m6['d_resto'])} MWh menos de electricidad en el compresor y los ventiladores del condensador y {M(-m6['d_gas'])} MWh menos de gas). El ahorro es chico (energía {n(por['M6']['d_E'] * -100, 1)} %, "
          f"emisiones {n(por['M6']['d_co2'] * -100, 1)} %) porque G1 ocupa {n(_ctx(c)['g1']['A'])} m\u00b2 y el ajuste vale solo 12 h por día. El adendo de ASHRAE 170 recomienda una evaluación de riesgo antes de ajustar "
          f"la ventilación de un quirófano {R('ashrae170')}; el modelo no calcula la presurización de la sala.")
    p4 = (f"**Qué no conviene priorizar.** Reducir un 30 % la conductancia de la envolvente cambia la energía {_txt_sens(d_ua)} y reducir un 30 % las ganancias internas (por ejemplo, con iluminación LED), {_txt_sens(d_gi)}"
          f"{': con menos calor interno el aire se recalienta más' if d_gi > 0 else ''}. El consumo está en el aire (renovaciones, humedad y ventiladores), no en la envolvente. "
          f"Las medidas que ahorran gas bajan más la energía que las emisiones; las que ahorran electricidad (fotovoltaica, ventiladores) bajan más las emisiones.")
    return "\n\n".join([p1, p2, p3, p4])


def _sens_c(c, f):
    return _E(c, f) / _E(c) - 1.0


def texto_refrigerante(c):
    refs = {r["refrigerante"]: r for r in mj.refrigerantes(c)}
    r134, ze = refs["R134a"], refs["R1234ze(E)"]
    caida = (1 - ze["q_vol"] / r134["q_vol"]) * 100
    mas = (r134["q_vol"] / ze["q_vol"] - 1) * 100
    return (f"El R134a tiene un PCA de 1.430 y la Enmienda de Kigali obliga a reducir los HFC {R('kigali')} (Argentina la ratificó en 2019 y puso los HFC bajo licencia de importación en 2020). "
            f"Con el modelo de ciclo y el mismo rendimiento isentrópico supuesto, a las mismas temperaturas de evaporación y condensación ({n(c['P']['T_ev'])} y 46 °C), el R1234ze(E) (PCA menor que 1) da el mismo COP "
            f"({n(ze['cop_elec'], 2)} contra {n(r134['cop_elec'], 2)}; en una máquina real puede ser algo menor) pero {n(caida)} % menos capacidad volumétrica, "
            f"o sea un compresor {n(mas)} % más grande, y es ligeramente inflamable (clase A2L), lo que pesa en un hospital. El R513A (PCA 631) no está en la biblioteca de propiedades "
            f"que se usó, así que no se calculó. Los PCA y la clasificación de seguridad son supuestos (valores de uso corriente).")


def texto_atomos(c):
    b = _ctx(c)["comb"]["b"]
    a = b["atomos"]
    partes = [f"{k} {n(v[0], 3)}" for k, v in a.items()]
    ok = all(abs(v[0] - v[1]) < 1e-9 for v in a.values())
    return ("**Control de la reacción:** el balance de átomos cierra" if ok else "**Control de la reacción (no cierra):**") + \
           f" ({'; '.join(partes)} kmol de átomos por kmol de gas, iguales a la entrada y a la salida); el aire estequiométrico es {n(b['o2_estequiometrico'] * (1 + 79 / 21), 3)} kmol por kmol de gas."


def texto_nota_m2(c):
    s = _ctx(c)["sup"]
    pm = lambda t: _txt_sens(*t)
    return (f"±6 m² por cama de internación general cambian la energía {pm(s['gen'])}; por quirófano, {pm(s['or'])}; por cama de terapia intensiva, {pm(s['uti'])}; climatizar el 95 % o el 75 % "
            f"de la superficie cubierta en vez del 85 % la cambia {pm(s['acond'])}; y que la guardia, el diagnóstico y el laboratorio ocupen el 50 % o el 20 % de las áreas generales en vez del "
            f"{n(c['P']['f_g4_24h'] * 100)} % la cambia {pm(s['g4'])}. Las áreas de cada zona pesan poco; lo que pesa es cuánta superficie se climatiza y cuántas horas funciona.")


def texto_resp_zonas():
    return (f"Respaldo: renovaciones de G1 y G3 y rango de las consignas de G1 a G3 según {R('ashrae170')} (la humedad de consigna de 55 % es el máximo de 60 % menos 5 puntos de margen de control: supuesto); "
            f"renovaciones de G2, G4 (promedio ponderado de sala de espera y triage, shock, imágenes y laboratorio) y G5, consignas de G4 y G5 (24 °C y 60 %, dentro de la zona de confort de {R('givoni')}) "
            f"y funcionamiento de cada zona: supuesto (valor de uso corriente).")


# ====================================================================================================================
# Exergia: texto de la seccion (de texto_exergia.py, con las marcas nuevas) y complementos
# ====================================================================================================================
def _extra_exergia(c):
    E = ex.estados_de_analisis(c)
    a, b = E["verano_pico"]["resultado"], E["max_recalentamiento"]["resultado"]
    ea = a["enfriadora"]
    T0a = E["verano_pico"]["condiciones"]["T_out"] + 273.15
    cw_in = ex._par(c, "T_cw_ida")
    cw_out = cw_in + c["P"]["dT_aguahelada"]
    X_frio = ea["Q_L"] * (T0a / ea["T_cw"] - 1.0)
    x = exergia_caldera(c)
    sp = lambda v: n(v, 1)
    par1 = (f"**Eficiencia exergética de la enfriadora (verano pico).** El producto es la exergía del frío, $\\dot X_{{frío}} = \\dot Q_L\\,(T_0/T_{{cw}} - 1)$ = {n(ea['Q_L'], 1)} · "
            f"({n(T0a, 2)}/{n(ea['T_cw'], 2)} − 1) = {sp(X_frio)} kW, con $T_{{cw}}$ = {n(ea['T_cw'] - 273.15, 1)} °C la temperatura media logarítmica del agua helada ({n(cw_in)} y {n(cw_out)} °C). "
            f"Contra la electricidad del compresor ({sp(ea['W_comp'])} kW) da $\\eta$ = {sp(X_frio / ea['W_comp'] * 100)} %; con los ventiladores del condensador y las bombas "
            f"({sp(ea['W_cond'])} y {sp(ea['W_bomba'])} kW), {sp(X_frio / (ea['W_comp'] + ea['W_cond'] + ea['W_bomba']) * 100)} %. El frío a {n(ea['T_cw'] - 273.15, 1)} °C con exterior a {n(T0a - 273.15)} °C "
            f"vale solo el {sp(ea['T0_sobre_Tcw_menos_1'] * 100)} % de su energía en exergía: por eso la eficiencia exergética es tan baja aunque el COP ({n(ea['COP'], 2)}) sea alto.")
    filas = [("Exergía del combustible ($\\dot X_F$)", sp(x["X_comb"]), "100,0"),
             ("Aporte del aire de combustión", sp(x["X_aire"]), sp(x["X_aire"] / x["X_comb"] * 100)),
             ("Destruida en la combustión", sp(x["D_comb"]), sp(x["D_comb"] / x["X_comb"] * 100)),
             ("Destruida en la transferencia de calor al agua", sp(x["D_transf"]), sp(x["D_transf"] / x["X_comb"] * 100)),
             ("Calor útil al agua ($\\dot X_P$)", sp(x["X_calor"]), sp(x["X_calor"] / x["X_comb"] * 100)),
             ("Gases de escape (química y térmica)", sp(x["X_gas"]), sp(x["X_gas"] / x["X_comb"] * 100)),
             ("Radiación y funcionamiento", sp(x["X_rad"]), sp(x["X_rad"] / x["X_comb"] * 100))]
    t = tabla(["Caldera, máximo recalentamiento", "Exergía [kW]", "% de la exergía del combustible"], filas, (52, 20, 28))
    par2 = (f"**Cómo leer las dos cifras de la caldera en el máximo recalentamiento.** La fila «Caldera» de la tabla por equipo es la caldera sola: destruye {sp(x['D_cal'])} kW "
            f"(= {sp(x['D_comb'])} + {sp(x['D_transf'])}, tabla siguiente), el {sp(x['D_cal'] / x['D_total'] * 100)} % de lo destruido en total ({sp(x['D_total'])} kW) y el {sp(x['D_cal'] / x['X_in'] * 100)} % de la entrada ({sp(x['X_in'])} kW). "
            f"El grupo «Caldera y ACS» del reparto por grupos suma además el calentamiento del ACS ({sp(x['D_acs'])} kW): {sp(x['D_cal_acs'])} kW, el {sp(x['D_cal_acs'] / x['D_total'] * 100)} % de lo destruido y el "
            f"{sp(x['D_cal_acs'] / x['X_in'] * 100)} % de la entrada. La eficiencia exergética de la caldera es $\\dot X_P/\\dot X_F$ = {sp(x['X_calor'])}/{sp(x['X_comb'])} = {sp(x['eta'] * 100)} %, "
            f"con una llama adiabática teórica de {n(x['T_llama'])} °C.")
    cap = "Table: Tabla Mexcal. Balance de exergía de la caldera en el máximo recalentamiento (diciembre, noche). El aire de combustión aporta una fracción mínima; los porcentajes suman 100,2 % con él."
    return "\n\n".join([par1, par2, t, cap])


def memoria_exergia(c, V, T):
    from . import texto_exergia
    _inf, mem, _v = texto_exergia.redactar(c, dict(V), dict(T))
    mem = re.sub(r"(?m)^## 8\.(\d)", r"## 9.\1", mem)
    mem = re.sub(r"\*\*recordadas?,? a (?:cotejar|verificar) con el libro de la c[aá]tedra\*\*", "**supuesto** (valores de uso corriente)", mem)
    mem = re.sub(r"\*\*A confirmar con la c[aá]tedra\*\*:\s*otra convenci[oó]n la llamar[ií]a p[eé]rdida\.", "Convención adoptada (supuesto): otra la llamaría pérdida.", mem)
    extra = _extra_exergia(c)
    mem, k = re.subn(r"(?m)^(## 9\.3 )", lambda m: extra + "\n\n" + m.group(1), mem, count=1)
    if k == 0:
        mem = mem + "\n\n" + extra
    return mem.strip()


# ====================================================================================================================
# Seleccion de equipos y ubicacion (texto propio de la memoria)
# ====================================================================================================================
_EQ_FILAS = [
    (("Q1", "Q2", "Q3"), "Niveles del edificio", "{n_niv} niveles iguales", "–",
     "supuesto: {presidencia} lista tres pisos y no menciona planta baja; cada nivel tiene {bruta} m² brutos y {clim} m² climatizados; el 1.er piso se toma a nivel de calle"),
    (("Q4", "Q5", "Q6"), "Planta tipo: forma, orientación y calle", "rectángulo 4:3; norte arriba; calle al sur", "–",
     "supuesto: sin plano de implantación; solo ubica el dibujo (el modelo térmico no distingue orientaciones)"),
    (("Q7", "Q8", "Q9"), "Planta tipo: núcleo técnico, zonas y circulación", "núcleo en la esquina sudeste; zonas por franjas", "–",
     "supuesto: el núcleo (locales técnicos, morgue y depósitos: {no_clim} m² por nivel) se agrupa del lado de la calle y se apila en los tres niveles; la circulación está dentro de la superficie de cada zona"),
    (("Q10", "Q11"), "Enfriadoras en servicio / de reserva", "{n_serv} / {n_res}", "unidades",
     "supuesto: N+1; con la 30XA 1002 dos en servicio dan {cap2} kW y faltan {falta2} kW ({falta2_pct} %) de los {QL} kW de diseño; con tres cada una trabaja al {carga} %; con una parada quedan {cap_parada} kW (+{margen_pct} %)"),
    (("Q12", "Q13", "Q14", "Q15", "Q16", "Q17", "Q18", "Q19"), "Enfriadora de ejemplo: Carrier AquaForce 30XA 1002", "{cap} kW; {pot} kW; R-134a", "kW",
     "{carrier} capacidad nominal con aire exterior a 35 °C y agua 12/7 °C y potencia de los compresores solos; la familia va de {fam_min} a {fam_max} kW"),
    (("Q20",), "Margen de diseño sobre la carga pico (solo informativo)", "0,1", "–", "supuesto: práctica habitual de selección; no cambia la selección"),
    (("Q21", "Q22", "Q23"), "Huella en azotea y peso operativo por enfriadora", "{huella_L} × {huella_W} m; {peso} t", "–",
     "supuesto: sin dimensiones de catálogo; la huella es el área reservada por unidad con espacios de servicio"),
    (("Q24",), "Sobrecarga de referencia de una azotea de uso corriente", "{q_ref}", "kN/m²", "supuesto (valor de uso corriente, entre 1 y 5 kN/m² según el acceso a la azotea)"),
    (("Q25",), "Aceleración de la gravedad", "9,81", "m/s²", "constante"),
    (("Q30",), "Punta de ACS / ACS media", "{f_punta}", "–", "supuesto: el modelo da solo el ACS medio; se suma al punto de diseño de invierno (coincidencia conservadora)"),
    (("Q31", "Q32"), "Calderas de agua caliente en servicio / de reserva", "1 / 1", "unidades", "supuesto: configuración 2 × 100 % (N+1)"),
    (("Q33", "Q34", "Q35"), "Caldera de condensación de ejemplo: Viessmann Vitocrossal 300 CM3C", "{cap_cond} kW máx.; {cap_cond_min} kW mín.; {eta_cond} sobre PCS", "–",
     "{viessmann} capacidades por unidad (se pueden poner en cascada) y rendimiento máximo con retorno frío (no es valor de operación)"),
    (("Q36",), "Unidades de reserva de la cascada de condensación", "1", "unidades", "supuesto: configuración 3+1"),
    (("Q37",), "Velocidad de los gases en la chimenea", "{v_chim}", "m/s", "supuesto: quemador con tiraje forzado; predimensionamiento"),
    (("Q40", "Q41", "Q42"), "UTAs: caudal máximo en zonas no críticas; unidades por quirófano; unidades de terapia", "{V_max}; 1; 1", "m³/h; –; –",
     "supuesto: criterio de predimensionamiento; una UTA con filtro HEPA por quirófano (zona independiente) y una para la terapia intensiva"),
    (("Q50", "Q51", "Q52", "Q53"), "Agua helada: velocidad máxima, serie DN, diámetro interior y densidad", "{v_agua} m/s; DN 150 a 350; ID = DN; 1.000 kg/m³", "–",
     "supuesto (velocidad de predimensionamiento; diámetro interior igual al nominal, con lo que la velocidad real es algo menor); serie nominal y densidad: constante"),
    (("Q54", "Q55", "Q56", "Q57"), "Shafts: velocidad de impulsión y de retorno, exfiltración y área de un shaft", "{v_imp} y {v_ret} m/s; 0 m³/h; {a_shaft} m²", "–",
     "supuesto: predimensionamiento; con exfiltración nula todo el aire exterior sale por la extracción; {a_shaft} m² es el área neta de conducto (el shaft real ocupa más)"),
    (("Q60",), "Pesos y puntajes de la matriz azotea / patio", "tabla Mmatriz", "–", "supuesto: juicio de ingeniería, sin ensayo ni cálculo de ruido; se muestra la sensibilidad a los pesos"),
]


def ids_equipos():
    return [i for ids, *_ in _EQ_FILAS for i in ids]


def tabla_supuestos_equipos(c):
    r = _ctx(c)["eqp"]
    p, en, ni = r["p"], r["enfriadoras"], r["niveles"]
    ca = r["calderas"]
    d = dict(n_niv=n(p["n_niveles"]), bruta=n(ni["bruta_nivel"]), clim=n(ni["clim_nivel"]), no_clim=n(ni["bruta_nivel"] - ni["clim_nivel"]),
             n_serv=n(en["n_serv"]), n_res=n(en["n_res"]), cap2=n(en["alt_2mas1"]["cap_servicio"]), falta2=n(en["alt_2mas1"]["faltante_kW"], 1),
             falta2_pct=n(en["alt_2mas1"]["faltante_rel"] * 100, 1), QL=n(en["Q_L"]), carga=n(en["carga_relativa_unidad"] * 100),
             cap_parada=n(en["cap_una_parada"]), margen_pct=n(en["margen_una_parada_rel"] * 100), cap=n(p["cap_enf"]), pot=n(p["pot_enf"], 1),
             fam_min=n(p["cap_fam_min"]), fam_max=n(p["cap_fam_max"]), huella_L=n(p["huella_L"]), huella_W=n(p["huella_W"], 1), peso=n(p["peso_op_t"]),
             q_ref=n(p["q_ref_cubierta"]), f_punta=n(p["f_punta_acs"]), cap_cond=n(p["cap_cond"]), cap_cond_min=n(p["cap_cond_min"]),
             eta_cond=n(p["eta_cond_PCS"], 2), v_chim=n(p["v_chimenea"]), V_max=n(p["V_max_uta"]), v_agua=n(p["v_agua"]), v_imp=n(p["v_imp"]),
             v_ret=n(p["v_ret"]), a_shaft=n(p["area_shaft"]))
    refs = _refs()
    filas = []
    for ids, nombre, valor, uni, motivo in _EQ_FILAS:
        idt = ids[0] if len(ids) == 1 else f"{ids[0]}–{ids[-1]}"
        filas.append((idt, nombre, valor.format(**d), uni, motivo.format(**d, **refs)))
    return tabla(["ID", "Parámetro", "Valor", "Unidad", "Respaldo: marca y motivo"], filas, (8, 29, 18, 8, 37))


def memoria_equipos(c):
    x = _ctx(c)
    r = x["eqp"]
    P = c["P"]
    en, ca, ut, hi, sh, az, ni, cop, mz, pt = (r[k] for k in ("enfriadoras", "calderas", "utas", "hidraulica", "shafts", "azotea", "niveles", "cop", "matriz", "planta"))
    p = r["p"]
    k1 = lambda v: n(v, 1)
    sec = []
    sec.append(f"""## 10.1 Enfriadoras

Carga de diseño $\\dot Q_L$ = {k1(en['Q_L'])} kW (suma de las serpentinas, tabla Mcargas). Con {n(en['n_serv'])} unidades en servicio cada una debe dar $\\dot Q_L/{n(en['n_serv'])}$ = {k1(en['req_unidad'])} kW. \
La Carrier AquaForce 30XA 1002 da {n(en['cap_unidad'])} kW nominales a 35 °C de aire exterior y agua 12/7 °C, con {k1(en['pot_unidad'])} kW de compresores {R('carrier')}. \
Con una unidad parada quedan ${n(en['n_total'] - 1)} \\cdot {n(en['cap_unidad'])}$ = {n(en['cap_una_parada'])} kW: margen de +{k1(en['margen_una_parada_kW'])} kW (+{n(en['margen_una_parada_rel'] * 100)} %), \
con cada unidad en servicio al {k1(en['carga_relativa_unidad'] * 100)} % de su capacidad nominal. Con el calor de las bombas ({k1(en['calor_bombas_max_kW'])} kW, que la carga no incluye) la carga sería \
{k1(en['Q_L'] + en['calor_bombas_max_kW'])} kW y sobran {k1(en['margen_con_bombas_kW'])} kW. La configuración 2+1 con la misma unidad da {n(en['alt_2mas1']['cap_servicio'])} kW y no cumple \
(faltan {k1(en['alt_2mas1']['faltante_kW'])} kW, {k1(en['alt_2mas1']['faltante_rel'] * 100)} %); necesitaría una unidad de al menos {n(en['alt_2mas1']['req_unidad_redondeada'])} kW, cuya existencia en el catálogo no se verificó.

**COP del catálogo contra el del modelo.** COP de catálogo (compresores solos, 35 °C de aire) {R('carrier')}: {n(p['cap_enf'], 0)}/{k1(p['pot_enf'])} = {n(cop['cop_catalogo'], 2)}. \
COP del modelo (compresor solo, 34 °C de aire exterior, condensación a {n(cop['T_cond_modelo_34'])} °C): {n(cop['cop_modelo_34'], 2)}, {k1(cop['dif_rel_34'] * 100)} % por encima. \
Al mismo aire de 35 °C (condensación a {n(cop['T_cond_modelo_35'])} °C) el modelo da {n(cop['cop_modelo_35'], 2)}, {k1(cop['dif_rel_35'] * 100)} % respecto del catálogo: el {n(cop['fraccion_por_temperatura'] * 100)} % de la \
diferencia viene de comparar 34 °C con 35 °C. Esa coincidencia a 35 °C no valida el modelo: $\\eta_{{is}}$ = {n(P['eta_is'], 2)} y $\\eta_{{mot}}$ = {n(P['eta_motor'], 2)} son supuestos, el modelo no incluye componentes \
de una máquina real (por ejemplo, economizador y variador) y la pendiente del COP con la temperatura de la máquina real no está verificada. Ninguno de los dos COP incluye ventiladores del condensador ni bombas.
""")
    sec.append(f"""## 10.2 Calderas

Carga de diseño $\\dot Q_{{cal}}$ = {k1(ca['Q_invierno'])} + {k1(ca['Q_acs_punta'])} = {k1(ca['Q_diseno'])} kW (calefacción y humidificación de invierno más la punta de ACS, el doble de la media: supuesto). \
El vapor de humidificación son {k1(ca['Q_vapor'])} kW; sin él, el agua caliente necesita {k1(ca['Q_agua_caliente_sin_vapor'])} kW. Con el rendimiento del modelo ({n(ca['eta_PCI_modelo'] * 100, 1)} % sobre PCI) el consumo de gas de diseño \
es de {k1(ca['V_gas_m3h'])} m³/h estándar (sección 5). Chimenea: gases de {n(ca['V_gases_m3h'])} m³/h a {n(P['T_gases'])} °C con {n(p['v_chimenea'])} m/s dan un diámetro de {n(ca['D_chimenea'] * 1000)} mm, es decir DN {n(ca['DN_chimenea'])}. \
Condensación como cota superior: {n(p['eta_cond_PCS'] * 100)} % sobre PCS {R('viessmann')} contra {k1(ca['eta_PCS_modelo'] * 100)} % del modelo, hasta {k1(ca['ahorro_gas_max'] * 100)} % menos de gas, solo si el retorno baja del punto \
de rocío de {k1(ca['T_rocio_gases'])} °C. Con la caldera de condensación de ejemplo hacen falta {n(ca['opcion_b']['n_servicio'])} unidades en servicio de {n(ca['opcion_b']['cap_unidad'])} kW más {n(ca['opcion_b']['n_reserva'])} de reserva: \
con una parada quedan {n(ca['opcion_b']['cap_una_parada'])} kW, suficiente; con {n(ca['opcion_b']['n'] - 1)} unidades en total quedarían {n(ca['opcion_b']['cap_3_unidades_una_parada'])} kW y no alcanza.
""")
    filas_ut = []
    for g in ("G1", "G2", "G3", "G4", "G5"):
        z = ut["por_zona"][g]
        filas_ut.append((g, n(z["n"]), n(z["caudal_unidad"]), n(z["V_total"]), z["ubicacion"], "sí" if z["hepa"] else "no"))
    filas_ut.append(("**Total**", f"**{n(ut['n_total'])}**", "", f"**{n(ut['V_total'])}**", f"{n(ut['n_cubierta'])} en cubierta, {n(ut['n_criticas'])} en cuartos técnicos", ""))
    sec.append("## 10.3 Unidades de tratamiento de aire\n\n" + tabla(["Zona", "Unidades", "Caudal por unidad [m³/h]", "Caudal de la zona [m³/h]", "Ubicación", "HEPA"], filas_ut, (8, 11, 17, 17, 38, 9))
               + "\n\nTable: Tabla Muta. Unidades de tratamiento de aire (criterio: una por quirófano y hasta %s m³/h por unidad en las demás zonas)." % n(p["V_max_uta"]))
    filas_sh = []
    for g in ("G1", "G2", "G3", "G4", "G5"):
        s = sh["por_zona"][g]
        if g == "G1":
            ns = f"1 (compartido con G2)"
        elif g == "G2":
            ns = "en el de G1"
        else:
            ns = n(s["n_shafts"])
        filas_sh.append((g, n(s["V_sup"]), n(s["A_imp"], 2), n(s["A_ret"], 2), n(s["A_vertical"], 2), ns, s["modo"]))
    filas_sh.append(("**Total**", f"**{n(sum(sh['por_zona'][g]['V_sup'] for g in sh['por_zona']))}**", f"**{n(sh['A_imp_total'], 2)}**", f"**{n(sh['A_ret_total'], 2)}**",
                     f"**{n(sh['A_vertical_total'], 2)}**", f"**{n(sh['n_shafts_agrupados'])}**", ""))
    a12 = sh["A_grupos"]["G1+G2"]
    sec.append(f"""## 10.4 Hidráulica y conductos

Caudal de agua helada $\\dot m_w = \\dot Q_L/(c_p\\,\\Delta T)$ = {k1(hi['m_w'])} kg/s ({n(hi['principal']['V_m3h'])} m³/h). Diámetro para {n(p['v_agua'], 1)} m/s: $D = \\sqrt{{4\\dot V/(\\pi v)}}$ = {n(hi['principal']['D_calc_mm'])} mm, \
por lo que DN {n(hi['principal']['DN'])} con una velocidad real de {n(hi['principal']['v_real'], 2)} m/s; el ramal por enfriadora (un tercio del caudal, {n(hi['ramal_enfriadora']['V_m3h'])} m³/h), DN {n(hi['ramal_enfriadora']['DN'])} \
({n(hi['ramal_enfriadora']['v_real'], 2)} m/s); si una unidad trabajara a su capacidad nominal el caudal sería mayor y convendría DN {n(hi['ramal_a_capacidad_nominal']['DN'])}.

{tabla(["Zona", "Impulsión [m³/h]", "A impulsión [m²]", "A retorno [m²]", "Shaft vertical [m²]", "Shafts", "Modo"], filas_sh, (7, 12, 11, 11, 12, 12, 35))}

Table: Tabla Mshafts. Shafts de aire (impulsión a {n(p['v_imp'])} m/s y retorno a {n(p['v_ret'])} m/s; para las zonas con la UTA en su nivel el shaft vertical lleva solo aire exterior y extracción). \
G1 y G2 comparten un shaft ({n(a12, 2)} m² juntos, menos de los {n(p['area_shaft'])} m² de un shaft): por eso las filas suman 1 + 3 + 5 + 5 = {n(sh['n_shafts_agrupados'])} y no 15.
""")
    # ---- azotea y ubicacion
    filas_mz = [(m[1], n(m[2] * 100) + " %", str(m[3]), str(m[4]), m[5]) for m in eq.MATRIZ_UBICACION]
    t_mz = tabla(["Criterio", "Peso", "Azotea (1 a 5)", "Patio (1 a 5)", "Razón"], filas_mz, (20, 7, 9, 9, 55))
    A_fv = mj.parametro("kWp_fv") * 5.0
    A_sol = mj.parametro("A_solar")
    sec.append(f"""## 10.5 Azotea y ubicación

Huella de {n(p['huella_L'])} × {n(p['huella_W'], 1)} = {n(az['A_unidad'])} m² por unidad, {n(az['n_unidades'])} unidades ({n(az['A_total'])} m² en total, {k1(az['fraccion_cubierta'] * 100)} % de la cubierta de {n(az['A_cubierta'])} m²). \
Carga media $q = {n(p['peso_op_t'])} \\cdot {n(p['g'], 2).replace(',', '{,}')} / {n(az['A_unidad'])}$ = {n(az['q_kN_m2'], 2)} kN/m² contra {n(az['q_ref'], 1)} kN/m² de sobrecarga de referencia de una azotea de uso corriente \
(supuesto: valor de uso corriente, entre 1 y 5 kN/m² según el acceso), es decir {n(az['q_sobre_ref'], 2)} veces. La carga bajo los apoyos es mayor: hace falta plataforma o vigas y la verificación \
del calculista, y el peso de {n(p['peso_op_t'])} t por unidad es supuesto.

El núcleo técnico ({n(pt['nucleo']['area'])} m², de {n(pt['nucleo']['ancho'], 1)} × {n(pt['nucleo']['prof'], 1)} m) ocupa la esquina sudeste, del lado de la calle y en el mismo lugar en cada nivel: los shafts se apilan, el agua helada \
baja por ellos desde la azotea y las enfriadoras se izan desde la calle. En el 2.º piso, quirófanos y terapia intensiva quedan contiguos al núcleo, donde están sus {n(ut['n_criticas'])} UTAs (conductos cortos); \
la internación va en dos alas y la guardia y los consultorios, en el 1.er piso, con acceso desde la calle. Las calderas van en un anexo a nivel de calle (acceso, medidor y regulador de gas, ventilación permanente \
y chimenea por fuera del edificio).

![Figura Mplanta. Planta tipo a escala del 1.er y 2.º piso (rectángulo equivalente de {n(pt['W'], 1)} × {n(pt['H'], 1)} m): la superficie dibujada de cada zona es proporcional a sus m² del modelo; \
la distribución en franjas, la calle al sur y el núcleo técnico en la esquina sudeste son supuestos, sin planos del edificio real.](../figuras/fig11_planta_tipo.png){{width=11.5cm}}

{t_mz}

Table: Tabla Mmatriz. Matriz de decisión entre azotea y patio a nivel (puntajes de 1 a 5, supuestos: juicio de ingeniería). Puntaje ponderado: azotea {n(mz['base']['azotea'], 2)}, patio {n(mz['base']['patio'], 2)}; \
con pesos iguales {n(mz['pesos_iguales']['azotea'], 2)} en ambos; con estructura e izaje al doble, azotea {n(mz['estructura_e_izaje_x2']['azotea'], 2)} y patio {n(mz['estructura_e_izaje_x2']['patio'], 2)}.

**La decisión no es robusta.** Con los pesos de la tabla gana la azotea ({n(mz['base']['azotea'], 2)} contra {n(mz['base']['patio'], 2)}), pero con pesos iguales empatan ({n(mz['pesos_iguales']['azotea'], 2)} en ambos) y si estructura e izaje valen \
el doble gana el patio ({n(mz['estructura_e_izaje_x2']['patio'], 2)} contra {n(mz['estructura_e_izaje_x2']['azotea'], 2)}). Se elige la azotea por el aire libre para el condensador y los recorridos cortos hacia las {n(ut['n_cubierta'])} UTAs de cubierta; \
si el calculista descarta la losa, el patio a nivel es la alternativa. Las reservas para solar térmico ({n(A_sol)} m²) y fotovoltaica (unos {n(A_fv)} m²) caben junto con las enfriadoras ({n(az['A_total'])} m²): \
suman {n(A_sol + A_fv + az['A_total'])} m² de los {n(az['A_cubierta'])} m² de la cubierta. No se dimensionaron las UTAs ni la sala de calderas.
""")
    sec.append("## 10.6 Supuestos de la selección de equipos\n\n::: {custom-style=\"Largo\"}\n" + tabla_supuestos_equipos(c)
               + "\n\nTable: Tabla Mequip. Supuestos de la selección y ubicación de equipos, con su respaldo.\n:::")
    return "\n\n".join(sec)


# ====================================================================================================================
# Lista de referencias de la memoria (misma numeracion que el informe)
# ====================================================================================================================
def lista_referencias():
    lineas = []
    for i, (cl, texto, sec) in enumerate(referencias.REFERENCIAS, start=1):
        lineas.append(f"[{i}]{chr(92) + '*' if sec else ''} {texto}")
    pie = ("\\* Fuente conocida por un extracto de búsqueda: se usó el dato citado y no se abrió el documento original; el dato citado se tomó de ese extracto.")
    return "\n\n".join(lineas) + "\n\n" + pie


# ====================================================================================================================
# Cifras del informe y donde se calculan
# ====================================================================================================================
def exergia_resumen(c):
    E = ex.estados_de_analisis(c)
    a, b = E["verano_pico"]["resultado"], E["max_recalentamiento"]["resultado"]
    g = lambda r, k: [v for kk, v in r["destruccion_grupos"].items() if kk.startswith(k)][0]
    ga, gb = a["global"], b["global"]
    return dict(X_in_a=ga["X_in"], D_a=ga["D_total"] / ga["X_in"], P_a=ga["P_total"] / ga["X_in"], eta_a=ga["eta_global"],
                comp_a=g(a, "Compresor") / ga["X_in"], cve_a=g(a, "Condensador") / ga["X_in"], vent_a=g(a, "Ventiladores") / ga["X_in"],
                X_in_b=gb["X_in"], D_b=gb["D_total"] / gb["X_in"], eta_enf=a["enfriadora"]["eta_compresor_grupo"], eta_planta=a["enfriadora"]["eta_planta"],
                eta_cal_a=a["caldera"]["eta_ex"], eta_cal_b=b["caldera"]["eta_ex"], fcarnot=a["enfriadora"]["T0_sobre_Tcw_menos_1"],
                comb_pci=a["caldera"]["ex_comb_sobre_PCI"], cal_comb_b=b["caldera"]["D_combustion"] / b["caldera"]["X_comb"],
                cal_transf_b=b["caldera"]["D_transferencia"] / b["caldera"]["X_comb"],
                calD_b=[t for t in b["tabla"] if t["clave"] == "caldera"][0]["X_dest"] / gb["D_total"])


def tabla_cifras(c):
    x = _ctx(c)
    P = c["P"]
    g, cc, cm, an, cz, mj_, eqp = x["g1"], x["ciclo"], x["comb"], x["anual"], x["cargas"], x["mej"], x["eqp"]
    xe = exergia_resumen(c)
    por = mj_["por"]
    k1 = lambda v: n(v, 1)
    M = lambda v: n(v / 1e3)
    A_cub = P["A_cub"]
    pct = lambda v: n(abs(v) * 100, 1) + " %"
    sg = lambda v: ("\u2212" if v < 0 else "+") + n(abs(v) * 100, 1) + " %"
    f = []
    add = lambda *r: f.append(r)
    add("Capacidad frigorífica de diseño", f"{n(cz['Q_L'])} kW ({n(cz['Q_L'] * 1000 / A_cub)} W/m² cubierto)", "$\\dot Q_L = \\sum \\dot Q_{serp}$ de las cinco zonas, verano pico ($f_{act}$ = 1, $q_{sol}$ = 20 W/m²)", "Tabla Mcargas; 3.3")
    add("Serpentina y recalentador de los quirófanos", f"{k1(g['Q_serp'])} kW ({k1(g['Q_sens'])} sensibles y {k1(g['Q_lat'])} latentes); {k1(g['Q_rec'])} kW",
        "$\\dot m_a[(h_{mez} - h_c) - (\\omega_{mez} - \\omega_c)\\,h_f]$; $\\dot m_a\\,c_{p,ah}\\,(T_{obj} - T_c)$", "3.2")
    add("Temperaturas del aire en el quirófano", f"mezcla {k1(g['T_mix'])}; serpentina {k1(g['T_c'])}; recalentador {k1(g['T_obj'])}; impulsión {k1(g['T_imp'])} °C", "balances de la mezcla, de la serpentina y del ventilador", "Tabla Mpsicro; 3.2")
    add("Calefacción y humidificación de invierno (diseño)", f"{n(cz['total']['cal'])} y {n(cz['total']['hum'])} kW ({n(cz['Q_caldera_inv'])} kW en total)", "suma por zona de calefacción y vapor, 2 °C y 80 % de humedad relativa", "Tabla Mcargas")
    add("Demanda media de ACS", f"{k1(x['corr']['Q_acs'])} kW ({n(x['corr']['Q_acs'] * 8.76)} MWh por año)", "$L\\,N_{camas}\\,c_p\\,\\Delta T\\,f_{perd}/86.400$", "6.1")
    add("COP del compresor al diseño; COP de Carnot; relación", f"{n(cc['cic']['cop_elec'], 2)}; {n(cc['cic']['cop_carnot'], 2)}; {n(cc['eta_II'] * 100)} %", "$q_L\\,\\eta_{mot}/w$; $T_{ev}/(T_{cond} - T_{ev})$", "Tabla Mciclo; 4.2")
    add("Potencia del compresor, calor rechazado y caudal de refrigerante al diseño", f"{n(cc['W_comp'])} kW; {n(cc['Q_cond'])} kW; {k1(cc['m_ref'])} kg/s", "$\\dot Q_L/COP_{el}$; $\\dot Q_L + \\eta_{mot}\\dot W_{comp}$; $\\dot Q_L/q_L$", "4.2")
    add("Temperatura de condensación del diseño", f"{n(cc['T_cond'])} °C ({n(cc['cic']['P_c'] / 1e3)} kPa)", "máx($T_{ext} + 12$ K; 32 °C)", "Tabla Mciclo; 4.2")
    add("Poder calorífico del gas natural", f"PCS {n(cm['pc']['PCS_kcal_m3'])} kcal/m³; PCI {n(cm['pc']['PCI_kWh_m3'], 3)} kWh/m³", "$\\sum y_i\\,PCI_i$ y $\\sum y_i\\,PCS_i$ sobre el volumen molar", "Tabla Mpci; 5.1")
    add("Pérdida por gases, rendimiento de la caldera", f"{k1(cm['q_gases'] * 100)} % del PCI; {k1(cm['eta'] * 100)} % sobre PCI ({k1(cm['cal']['eta_PCS'] * 100)} % sobre PCS)", "$(H_{prod} - H_{reac})/PCI$; $1 - q_{gases} - f_{rad}$", "Tabla Mgases; 5.2")
    add("Punto de rocío y agua en los gases", f"{k1(cm['cal']['T_rocio'])} °C; {k1(cm['cal']['y_H2O'] * 100)} %", "presión parcial del agua $y_{H_2O}\\,P$", "Tabla Mcomb")
    add("Temperatura de llama adiabática", f"{n(cb.temperatura_llama_adiabatica(P))} °C", "$\\sum n_i\\,\\Delta h_i(T_{llama}) = PCI + H_{reac}$", "5.2; Tabla Mcomb")
    add("Consumo de gas de diseño", f"{k1(cm['V_gas_h'])} m³/h estándar ({n(cm['E_pci'])} kW de PCI)", "$\\dot Q_{cal}/\\eta/PCI$", "5.2")
    add("Emisión de CO₂ del gas", f"{n(mj.factor_co2_gas(P), 3)} kg por kWh de PCI ({n(mj.factor_co2_gas(P) / 3.6 * 1000, 1)} kg/GJ)", "$n_{CO_2} \\cdot 44{,}01/(PCI/3.600)$", "Tabla Mcomb")
    add("Energía final anual; por m² cubierto", f"{M(an['E_total'])} MWh; {k1(an['E_total'] / A_cub)} kWh/m² ({n(an['E_elec'] / A_cub)} electricidad + {n(an['E_gas_PCS'] / A_cub)} gas)", "electricidad + gas (PCS)", "Tabla Musos; 6.3")
    add("Electricidad y gas anuales", f"{M(an['E_elec'])} MWh; {M(an['E_gas_PCS'])} MWh ({n(round(an['V_gas'], -3) / 1e3)} mil m³)", "suma de los usos finales; $Q_{util}/\\eta \\cdot PCS/PCI$", "Tabla Musos; 6.3")
    k_gas = an["E_gas_PCS"] / an["q"]["total"]
    usos = [("ventiladores", an["W_vent"]), ("compresor", an["W_comp"]), ("recalentamiento", an["q"]["recal"] * k_gas), ("ACS", an["q"]["acs"] * k_gas),
            ("calefacción", an["q"]["cal"] * k_gas), ("condensador", an["W_cond"]), ("bombas", an["W_bomba"])]
    add("Reparto por uso final", "; ".join(f"{nom} {pct(v / an['E_total'])}" for nom, v in usos), "uso final / energía final", "Tabla Musos")
    add("Calor útil de la caldera; parte de recalentamiento", f"{M(an['q']['total'])} MWh; {M(an['q']['recal'])} MWh ({n(an['q']['recal'] / an['q']['total'] * 100)} %)", "$Q_{rec} + Q_{cal} + Q_{hum} + Q_{ACS}$", "6.3")
    add("Frío entregado; horas equivalentes", f"{M(an['frio'])} MWh; {n(an['frio'] / cz['Q_L'])} h", "$\\sum \\dot Q_{L,i}\\,h_i$; frío / $\\dot Q_L$", "6.3")
    add("Calor rechazado por el condensador en el año", f"{M(an['Q_cond'])} MWh ({k1(an['Q_cond'] / an['q']['recal'])} veces el recalentamiento)", "$Q_L + \\eta_{mot}\\,W_{comp}$ = frío + 0,94 · trabajo del compresor", "6.3")
    add("COP anual del compresor y de la planta", f"{n(an['cop_comp'], 2)} y {n(an['cop_planta'], 2)}", "$Q_L/W_{comp}$; $Q_L/(W_{comp} + W_{cond} + W_{bomba})$", "6.3")
    sb, sf = x["sens_all"]
    Es = [v["E_total"] / A_cub for v in sf]
    top = sorted(sf, key=lambda v: -abs(v["delta"]))[:3]
    add("Rango de la sensibilidad (un supuesto por vez)", f"{n(min(Es))} a {n(max(Es))} kWh/m² por año", "$E_{variante}/A_{cub}$ de todas las variaciones del modelo; los extremos están en la tabla Msens", "Tabla Msens")
    add("Supuestos que más mueven el resultado", "; ".join(f"{NOMBRES_SENS.get(v['nombre'], v['nombre'])} {_txt_sens(v['delta'])}" for v in top), "$E_{variante}/E_{base} - 1$", "Tabla Msens")
    base = mj_["base"]
    B = por["B"]
    add("Alternativa B: ahorro de energía y de CO₂", f"{sg(B['d_E'])} ({M(base['E_total'] - B['E_total'])} MWh de menos); {sg(B['d_co2'])}", "$E_B/E_A - 1$ con el mejor modo por estado (sección 8)", "Tabla Mmejoras; 8.2")
    add("Paquete B + M1 a M6: ahorro de energía y de CO₂", f"{sg(por['P']['d_E'])} ({M(base['E_total'] - por['P']['E_total'])} MWh de menos); {sg(por['P']['d_co2'])}", "$E_P/E_A - 1$", "Tabla Mmejoras")
    add("Emisiones del caso base", f"{n(base['co2_t'])} t de CO₂ por año ({n(base['co2_gas_t'])} del gas y {n(base['co2_elec_t'])} de la electricidad)", "$E_{PCI}\\cdot 0{,}202 + E_{elec}\\cdot 0{,}38$", "Tabla Mmejoras; 8.1")
    add("Mejoras M1 a M6 (energía final)", "; ".join(f"{k} {sg(por[k]['d_E'])}" for k in ("M1", "M2", "M3", "M4", "M5", "M6")), "$E_{variante}/E_A - 1$", "Tabla Mmejoras")
    add("Aporte de M1 y M4 con B", f"M1: {M(mj_['m1_con_b'])} MWh en vez de {M(mj_['m1_solo'])}; M4: {M(mj_['m4_con_b'])} en vez de {M(mj_['m4_solo'])}", "ahorro de la variante sobre B", "8.3")
    add("Exergía que entra y reparto en el verano pico", f"{n(xe['X_in_a'])} kW; destruida {k1(xe['D_a'] * 100)} %; útil {k1(xe['P_a'] * 100)} %; compresor {k1(xe['comp_a'] * 100)} %, condensador, válvula y evaporador {k1(xe['cve_a'] * 100)} %, ventiladores y bombas {k1(xe['vent_a'] * 100)} %", "$\\dot X_F = \\dot X_P + \\dot X_L + \\dot X_D$ por grupo de equipos", "Tabla M14a; sección 9")
    add("Eficiencia exergética de la enfriadora", f"{k1(xe['eta_enf'] * 100)} % (compresor); {k1(xe['eta_planta'] * 100)} % (con ventiladores del condensador y bombas); el frío vale {k1(xe['fcarnot'] * 100)} % de su energía", "$\\dot Q_L(T_0/T_{cw} - 1)/\\dot W$", "Tabla M15; sección 9")
    add("Exergía de la caldera, máximo recalentamiento", f"eficiencia {k1(xe['eta_cal_b'] * 100)} %; destruida {k1(xe['cal_comb_b'] * 100)} % en la combustión y {k1(xe['cal_transf_b'] * 100)} % en la transferencia (del combustible); {k1(xe['calD_b'] * 100)} % de lo destruido", "$D/\\dot X_F$ por etapa", "Tabla Mexcal; tabla M16")
    add("Exergía química del gas natural", f"{n(xe['comb_pci'], 3)} veces su PCI", "$\\sum y_i\\,ex_i + R\\,T_0\\sum y_i \\ln y_i$ sobre el PCI", "Sección 9")
    add("Enfriadoras", f"{n(eqp['enfriadoras']['n_serv'])} + {n(eqp['enfriadoras']['n_res'])} de {n(eqp['enfriadoras']['cap_unidad'])} kW: {n(eqp['enfriadoras']['cap_una_parada'])} kW con una parada (+{n(eqp['enfriadoras']['margen_una_parada_rel'] * 100)} %)", "$(N_{total} - 1)\\,Q_{unidad}$ contra $\\dot Q_L$", "10.1")
    add("Calderas y chimenea", f"{k1(eqp['calderas']['Q_diseno'])} kW; DN {n(eqp['calderas']['DN_chimenea'])}", "$\\dot Q_{inv} + 2\\,\\dot Q_{ACS}$; $D = \\sqrt{4\\dot V/(\\pi v)}$", "10.2")
    add("UTAs, agua helada y shafts", f"{n(eqp['utas']['n_total'])} UTAs ({n(eqp['utas']['n_cubierta'])} en cubierta); DN {n(eqp['hidraulica']['principal']['DN'])}; {n(eqp['shafts']['n_shafts_agrupados'])} shafts", "caudal / velocidad de diseño", "Tabla Muta; tabla Mshafts; 10.3 y 10.4")
    add("Azotea: carga media y puntaje de la matriz", f"{n(eqp['azotea']['q_kN_m2'], 2)} kN/m²; azotea {n(eqp['matriz']['base']['azotea'], 2)} contra patio {n(eqp['matriz']['base']['patio'], 2)}", "peso / huella; promedio ponderado", "Tabla Mmatriz; 10.5")
    return tabla(["Cifra del informe", "Valor", "Ecuación o cálculo", "Dónde"], f, (20, 33, 29, 18))


# ====================================================================================================================
# API que usa construir_documentos.py
# ====================================================================================================================
def valores_memoria(c, V, T):
    x = _ctx(c)
    P = c["P"]
    g, cc, cm, an, cz = x["g1"], x["ciclo"], x["comb"], x["anual"], x["cargas"]
    cic = cc["cic"]
    v = {}

    def put(k, val, nd=0):
        v["mx_" + k] = nn(val, nd)

    put("q_sol_pico", P["q_sol_pico"])
    put("q_sol_dia", P["q_sol_dia"])
    # ---- caso resuelto de aire humedo (zona G1)
    put("g1_A", g["A"]); put("g1_h", g["h_techo"]); put("g1_ach", g["ach_tot"]); put("g1_ach_oa", g["ach_oa"])
    put("g1_Tr", g["T_r"]); put("g1_hr", g["hr"] * 100); put("g1_qs", g["q_s"]); put("g1_ql", g["q_l"])
    put("g1_dp", g["dp"]); put("g1_dp_kPa", g["dp"] / 1000.0, 1); put("g1_eta", g["eta_vent"], 2)
    put("g1_V", g["V_m3h"]); put("g1_Vs", g["V_s"], 3); put("g1_ma", g["m_a"], 2); put("g1_mae", g["m_ae"], 3)
    put("g1_xae", g["x_ae"], 2); put("g1_xret", 1.0 - g["x_ae"], 2); put("g1_msens", g["m_sens"], 2)
    put("g1_Wext", g["W_ext"] * 1000, 3); put("g1_hext", g["h_ext"], 2); put("g1_hret", g["h_ret"], 2)
    put("g1_Wr", g["W_r"] * 1000, 3); put("g1_Wr_k", g["W_r"], 6); put("g1_cpr", g["cp_r"], 4)
    put("g1_hmez", g["h_mix"], 2); put("g1_Wmez", g["W_mix"] * 1000, 3); put("g1_Tmez", g["T_mix"], 2)
    put("g1_Qs", g["Qs"], 2); put("g1_Ql", g["Ql"], 2)
    put("g1_Timp", g["T_imp"], 2); put("g1_Timp3", g["T_imp"], 3)
    put("g1_Wc", g["W_c"] * 1000, 3); put("g1_Wc_k", g["W_c"], 6)
    put("g1_Wvent", g["W_vent"], 1); put("g1_dTvent", g["dT_vent"], 3); put("g1_dTvent2", g["dT_vent"], 2)
    put("g1_Tobj", g["T_obj"], 3); put("g1_Tobj2", g["T_obj"], 2)
    put("g1_Tc", g["T_c"], 3); put("g1_Tc2", g["T_c"], 2); put("g1_hc", g["h_c"], 2); put("g1_hf", g["h_f"], 2)
    dW = g["W_mix"] - g["W_c"]
    put("g1_dWk", dW, 6)
    put("g1_mcond_gs", g["m_cond"] * 1000, 2); put("g1_mcond_h", g["m_cond"] * 3600, 1)
    put("g1_corchete", (g["h_mix"] - g["h_c"]) - dW * g["h_f"], 2)
    put("g1_Qserp", g["Q_serp"], 1); put("g1_Qlat", g["Q_lat"], 1); put("g1_Qsens", g["Q_sens"], 1)
    put("g1_cpc", g["cp_c"], 4); put("g1_dTobj", g["T_obj"] - g["T_c"], 3); put("g1_Qrec", g["Q_rec"], 1)
    put("g1_hr_imp", ah.hr_desde_w(g["T_imp"], g["W_c"], P["presion"]) * 100)
    put("g1_msens_V", g["m_sens"] / g["rho"] * 3600.0); put("g1_msens_ach", g["m_sens"] / g["rho"] * 3600.0 / (g["A"] * g["h_techo"]), 1)
    put("g1_ratio", g["m_ach"] / g["m_sens"], 1)
    # ---- cargas por zona
    put("QL", cz["Q_L"], 1)
    put("QL_wm2", cz["Q_L"] * 1000 / P["A_cub"])
    v["mx_cargas_suma"] = " + ".join(nn(f["serp"], 1) for f in cz["filas"])
    # ---- ciclo
    put("cic_pev", cic["P_ev"] / 1e3, 1); put("cic_pc", cic["P_c"] / 1e3, 1); put("cic_Tcond", cc["T_cond"])
    for k in ("h1", "h2", "h2s", "h3", "h4"):
        put("cic_" + k, cic[k], 2)
    put("cic_qL", cic["q_L"], 2); put("cic_w", cic["w"], 2); put("cic_qH", cic["q_H"], 2)
    put("cic_copeje", cic["cop_comp"], 3); put("cic_copel", cic["cop_elec"], 3); put("cic_copel2", cic["cop_elec"], 2)
    put("cic_carnot", cic["cop_carnot"], 3)
    put("cic_Tev_K", P["T_ev"] + 273.15, 2); put("cic_Tc_K", cc["T_cond"] + 273.15, 2)
    put("cic_etaII", cc["eta_II"] * 100, 1)
    put("cic_Wcomp", cc["W_comp"], 1); put("cic_mref", cc["m_ref"], 3); put("cic_Qcond", cc["Q_cond"], 1)
    put("cic_Wcond", cc["W_cond"], 1); put("cic_mw", cc["m_w"], 2); put("cic_Wbomba", cc["W_bomba"], 1)
    # ---- combustion
    v["mx_pci_suma"] = " + ".join(f"{nn(f['y'], 2)} \\cdot {n(f['pci'])}" for f in cm["comp"])
    put("pci", cm["pci_mezcla"]); put("pcs", cm["pcs_mezcla"]); put("vmolar", cm["v_molar"], 3)
    put("pcs_pci", cm["pcs_mezcla"] / cm["pci_mezcla"], 4)
    put("pci_m3", cm["pci_mezcla"] / cm["v_molar"]); put("pcs_m3", cm["pcs_mezcla"] / cm["v_molar"])
    put("hprod", cm["H_prod"]); put("hreac", cm["H_reac"]); put("dho2", cm["dh_o2"], 1); put("dhn2", cm["dh_n2"], 1)
    put("n2aire", cm["b"]["reactivos"]["N2_aire"], 3)
    put("qgases", cm["q_gases"], 4); put("frad", P["f_rad"], 2); put("eta", cm["eta"], 4)
    put("Qinv", cm["Q_inv"], 1); put("f_punta", cm["f_punta"]); put("Qacs_med", cm["Q_acs_med"], 1); put("Qacs_punta", cm["Q_acs_punta"], 1)
    put("Qdis", cm["Q_dis"], 1); put("Epci", cm["E_pci"], 1); put("Vgas_h", cm["V_gas_h"], 1)
    put("pv", cm["y_prod"]["H2O"] * P["presion"] / 1000.0, 2)
    # ---- ACS y anual
    put("acs_kW", x["corr"]["Q_acs"], 1); put("acs_MWh", x["corr"]["Q_acs"] * 8.76, 1)
    M = lambda w: w / 1e3
    q = an["q"]
    put("q_rec", M(q["recal"])); put("q_cal", M(q["cal"])); put("q_hum", M(q["hum"])); put("q_acs", M(q["acs"])); put("q_tot", M(q["total"]))
    put("pct_rec", q["recal"] / q["total"] * 100)
    put("Egas", M(an["E_gas_PCS"])); put("Vgas", an["V_gas"]); put("Eelec", M(an["E_elec"])); put("Etot", M(an["E_total"]))
    put("Etot_i", an["E_total"] / P["A_cub"], 1)
    put("e_comp", M(an["W_comp"])); put("e_cond", M(an["W_cond"])); put("e_bomb", M(an["W_bomba"])); put("e_vent", M(an["W_vent"]))
    put("frio", M(an["frio"]), 1); put("frio2", M(an["frio"]), 2)
    put("e_comp1", M(an["W_comp"]), 1); put("e_comp2", M(an["W_comp"]), 2); put("e_cond2", M(an["W_cond"]), 2); put("e_bomb2", M(an["W_bomba"]), 2)
    put("Qcond", M(an["Q_cond"])); put("Qcond2", M(an["Q_cond"]), 2)
    put("EFLH", an["frio"] / cz["Q_L"])
    put("cond_sobre_rec", an["Q_cond"] / q["recal"], 1)
    put("cop_comp", an["cop_comp"], 2); put("cop_planta", an["cop_planta"], 2)
    # ---- mejoras: numeros de M2, M3 y M5 y emisiones del caso base
    mj_ = x["mej"]
    base, por = mj_["base"], mj_["por"]
    put("PR", mj.parametro("PR_fv"), 2); put("eta_solar", mj.parametro("eta_solar"), 2)
    put("solar_MWh", por["M2"]["detalle"]["solar_kWh"] / 1e3)
    put("fv_MWh", por["M5"]["detalle"]["fv_kWh"] / 1e3)
    put("fv_MWh1500", min(mj.parametro("kWp_fv") * 1500.0 * mj.parametro("PR_fv"), base["E_elec"]) / 1e3)
    sb = mj.anual_variante(c, {"rec_extraccion": True, "bypass": False})
    v["mx_M3_sinbp_dE"] = _txt_sens(sb["E_total"] / base["E_total"] - 1.0)
    v["mx_M3_sinbp_dC"] = _txt_sens(sb["co2_t"] / base["co2_t"] - 1.0)
    put("co2_gas_pcs", mj.factor_co2_gas(P) * cm["pc"]["PCI_kWh_m3"] / cm["pc"]["PCS_kWh_m3"], 3)
    put("co2_gas_kg4", mj.factor_co2_gas(P), 4)
    put("Epci_anual", base["E_PCI"] / 1e3); put("co2_gas_t", base["co2_gas_t"]); put("co2_elec_t", base["co2_elec_t"]); put("co2_tot_t", base["co2_t"])
    # ---- textos
    v["mx_linea_r134a"] = linea_r134a()
    v["mx_atomos"] = texto_atomos(c)
    v["mx_nota_m2"] = texto_nota_m2(c)
    v["mx_lectura_mejoras"] = texto_lectura_mejoras(c)
    v["mx_refrigerante"] = texto_refrigerante(c)
    v["mx_resp_zonas"] = texto_resp_zonas()
    return v


def tablas_memoria(c, V, T):
    t = {
        "tabla_nomenclatura": tabla_nomenclatura(),
        "tabla_sistemas": tabla_sistemas(c),
        "tabla_estados_corrientes": tabla_estados_corrientes(c),
        "tabla_propiedades": tabla_propiedades(c),
        "tabla_psicro_m": tabla_psicro(c),
        "tabla_cargas": tabla_cargas(c),
        "tabla_ciclo_m": tabla_ciclo(c),
        "tabla_pci": tabla_pci(c),
        "tabla_gases": tabla_gases(c),
        "tabla_params_mejoras_m": tabla_params_mejoras(),
        "tabla_parametros_m": tabla_parametros(c),
        "tabla_cifras": tabla_cifras(c),
        "tabla_otras_variaciones": tabla_otras_variaciones(c),
        "lista_referencias_m": lista_referencias(),
        "memoria_exergia": memoria_exergia(c, V, T),
        "memoria_equipos": memoria_equipos(c),
    }
    return t


# ====================================================================================================================
# Otras variaciones que cita el informe (un supuesto por vez, respecto del caso base)
# ====================================================================================================================
def variaciones_extra(c):
    base = _ctx(c)["anual"]["E_total"]
    P = c["P"]
    z = lambda c2, g, k, v: c2["Z"][g].__setitem__(k, v)
    var = [("Quirófanos: 15 renovaciones totales por hora (en vez de 20)", lambda c2: z(c2, "G1", "ach_tot", 15)),
           ("Quirófanos: 25 renovaciones totales por hora", lambda c2: z(c2, "G1", "ach_tot", 25)),
           ("Quirófanos: 6 renovaciones de aire exterior por hora (en vez de 4)", lambda c2: z(c2, "G1", "ach_oa", 6)),
           ("Consignas de verano de G3, G4 y G5 a 26 °C (en vez de 24 °C)", lambda c2: [z(c2, g, "t_ver", 26.0) for g in ("G3", "G4", "G5")]),
           ("ACS de 55 L por cama y día (en vez de 100)", lambda c2: c2["P"].__setitem__("L_cama_dia", 55.0)),
           ("Humedad relativa media del clima 4 puntos menor", lambda c2: c2["clima"].__setitem__("HR", [h - 0.04 for h in c2["clima"]["HR"]]))]
    out = []
    for nombre, f in var:
        e = _E(c, f)
        out.append((nombre, e, e / base - 1.0))
    b0 = mj.anual_variante(c, {})
    sb = mj.anual_variante(c, {"rec_extraccion": True, "bypass": False})
    out.append(("M3, recuperador del aire de extracción, sin compuertas de bypass (las emisiones cambian %s)" % _txt_sens(sb["co2_t"] / b0["co2_t"] - 1.0), sb["E_total"], sb["E_total"] / b0["E_total"] - 1.0))
    fv = min(mj.parametro("kWp_fv") * 1500.0 * mj.parametro("PR_fv"), b0["E_elec"])
    out.append(("M5, fotovoltaica, con 1.500 kWh/m² de irradiación (en vez de %s)" % n(mj.parametro("GHI_anual")), b0["E_total"] - fv, -fv / b0["E_total"]))
    return base, out


def tabla_otras_variaciones(c):
    base, out = variaciones_extra(c)
    filas = [(nom, n(e / 1e3), _txt_sens(d)) for nom, e, d in out]
    return tabla(["Variación de un supuesto (los demás quedan en su valor base)", "Energía final [MWh/año]", "Diferencia"], filas, (66, 18, 12))
