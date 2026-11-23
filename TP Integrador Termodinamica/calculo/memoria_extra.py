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
import math
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

# Punto de diseno de verano (estimacion.diseno): actividad plena en todas las zonas y ganancia solar pico.
F_ACT_DISENO = 1.0


def nn(x, nd=0):
    """Formato argentino con signo menos tipografico."""
    return n(x, nd).replace("-", "−")


def R(clave):
    """Marca de una fuente numerada: '[6]\\*' o '[1]'."""
    return referencias.marca(clave)


SUP_CORRIENTE = "supuesto (valor de uso corriente; a contrastar con la fuente)"


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
        cpw=cpw, T_ah=(P["T_ev"] + 4.0, None), Q_L=d["Q_L"], m_ah=d["Q_L"] / (cpw * P["dT_aguahelada"]),
        Q_cal=com["Q_dis"], m_ac=com["Q_dis"] / (cpw * 20.0), T_red=P["T_agua_fria"], T_acs=P["T_acs"],
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
    m4, m6 = por["M4"]["detalle"], por["M6"]["detalle"]
    m4_B = mj.anual_variante(c, {"rec_cond": True, "dp_vent": 0.8})
    cs = lambda a, b, k: (a["elec"][k] - b["elec"][k])
    return dict(
        base=base, por=por, ahorro_ind=sum(ahorro(k) for k in ("B", "M1", "M2", "M3", "M4", "M5", "M6")), ahorro_paq=ahorro("P"),
        m1_solo=ahorro("M1"), m1_con_b=m1_con_b, m4_solo=ahorro("M4"), m4_con_b=m4_con_b, E_B=E_B,
        m4=dict(d_vent=cs(base, m4, "ventiladores"), d_comp=cs(base, m4, "compresor"), d_gas=m4["E_PCS"] - base["E_PCS"],
                d_E=ahorro("M4"), d_co2=por["M4"]["d_co2"]),
        m4_B=dict(d_gas=m4_B["E_PCS"] - mj.anual_variante(c, {"rec_cond": True})["E_PCS"]),
        m6=dict(d_vent=cs(base, m6, "ventiladores"), d_comp=cs(base, m6, "compresor"), d_gas=m6["E_PCS"] - base["E_PCS"],
                d_E=ahorro("M6"), d_co2=por["M6"]["d_co2"]),
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
            r134a=contraste_r134a(), eqp=eq.resumen_equipos(c))
    return _CACHE[clave]
