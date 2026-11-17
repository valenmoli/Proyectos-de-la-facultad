"""Analisis exergetico del sistema termico del hospital (Consigna 3 y 4).

Metodo: balance de exergia por equipo con el esquema combustible - producto - perdida (F, P, L)
y destruccion D, de modo que para cada equipo  F = P + L + D  (todo en kW).

  F  exergia suministrada al equipo (electricidad, combustible, agua caliente, agua helada...)
  P  exergia del producto del equipo (la que aprovecha el equipo siguiente o el usuario final)
  L  exergia que sale al ambiente sin aprovecharse (condensado, aire caliente del condensador,
     gases de escape, perdidas de la caldera y del ACS)
  D  exergia destruida (generacion de entropia por T0, Gouy-Stodola)

Estado muerto: T0 y la humedad W0 del estado exterior del estado analizado, P0 = 101.325 Pa.
Frontera global: unidades de tratamiento de aire (mezcla, serpentina, recalentador, ventilador),
enfriadora (motor, compresor, condensador, valvula, evaporador) con sus auxiliares, caldera y ACS.
Las zonas quedan FUERA de la frontera: el producto del lado del aire es el aumento neto de exergia
de la corriente tratada, X_impulsion - X_retorno - X_aire_exterior (puede ser negativo).

Exergia total de entrada = electricidad + exergia quimica del gas natural. Cierre del balance:
X_in = P_aire + P_ACS + sum(L) + sum(D)   (error relativo < 1e-6).

SUPUESTOS NUEVOS de este modulo (ver SUPUESTOS al final de los parametros): circuito de agua caliente
80/60 C, agua helada 7/12 C, efectividad 0,5 del condensador, calor de la caldera perdido a 70 C, etc.
Las exergias quimicas estandar (Szargut) estan RECORDADAS, no verificadas con el libro de la catedra.

Unidades: kW, kJ/kg de aire seco o de agua, kJ/kmol en la combustion; temperaturas en C salvo T0K.
"""
import functools
import math

from CoolProp.CoolProp import PropsSI
from scipy.integrate import quad

from . import aire_humedo as ah
from . import combustion as cb
from . import edificio as ed
from . import estimacion as es
from . import refrigeracion as rf

import psychrolib as ps

K = 273.15
P0 = 101325.0                       # Pa, presion del estado muerto
R_A = ps.R_DA_SI / 1000.0           # kJ/(kg K), aire seco (psychrolib: 287,042 J/(kg K))
MV_MA = 0.621945                    # Mv/Ma, el mismo valor que usa psychrolib
R_V = R_A / MV_MA                   # kJ/(kg K), vapor de agua (0,4615)
V_LIQ = 1.0e-3                      # m3/kg, agua liquida (incompresible)

# --------------------------------------------------------------------------------------
# Parametros nuevos (no estan en supuestos.py; se pueden pisar con c["P"][clave])
# (id, clave, nombre, valor, unidad, estado, fuente)
# --------------------------------------------------------------------------------------
SUPUESTOS = [
    ("X1", "T_hw_ida", "Temperatura de ida del circuito de agua caliente (recalentador, calefaccion, ACS)", 80.0, "C", "SUPUESTO",
     "Circuito 80/60 C habitual; el modelo base no lo fija (solo calcula calor util)"),
    ("X2", "T_hw_ret", "Temperatura de retorno del circuito de agua caliente", 60.0, "C", "SUPUESTO", "Idem (X1)"),
    ("X3", "T_cw_ida", "Temperatura de ida del agua helada (entra a la serpentina); el retorno es ida + dT_aguahelada", 7.0, "C", "SUPUESTO",
     "Agua helada 7/12 C, coherente con R2 y R10 de supuestos.py"),
    ("X4", "eps_cond", "Efectividad del condensador por aire: (T_aire_sal - T_ext)/(T_cond - T_ext)", 0.5, "-", "SUPUESTO",
     "El modelo base no da el caudal de aire del condensador; solo reparte entre destruccion y perdida, no cambia el total"),
    ("X5", "T_rad", "Temperatura a la que la caldera pierde el calor de radiacion y funcionamiento", 70.0, "C", "SUPUESTO",
     "Temperatura media del agua del circuito 80/60; su efecto es del orden de 0,2 % de la exergia del combustible"),
    ("X6", "T_perd_acs", "Temperatura a la que se pierde el calor de acumulacion y recirculacion del ACS", 60.0, "C", "SUPUESTO",
     "Acumulador y anillo a la temperatura del ACS (S2)"),
]
_X_DEF = {k: v for (_i, k, _n, v, _u, _e, _f) in SUPUESTOS}

# Exergias quimicas estandar [kJ/kmol] (Szargut, entorno de referencia a 298,15 K).
# ESTADO: RECORDADO, a verificar con el libro de la catedra. No hay fuente citable cargada en datos/.
EX_QUIM = {"CH4": 831650.0, "C2H6": 1495840.0, "C3H8": 2154000.0, "N2": 720.0, "CO2": 19870.0,
           "O2": 3970.0, "H2O": 9500.0}
EX_QUIM_ESTADO = "recordado, a verificar con el libro de la catedra"


def _par(c, clave):
    return c["P"].get(clave, _X_DEF[clave])


# --------------------------------------------------------------------------------------
# Exergia del aire humedo y del agua
# --------------------------------------------------------------------------------------
def ex_aire(T, W, T0, W0):
    """Exergia del aire humedo [kJ/kg de aire seco] con P = P0 (Kotas, Bejan et al.).

    Mezcla de gases ideales (aire seco + vapor) con calores especificos constantes.
      ex = (cp_a + W cp_v) T0 (T/T0 - 1 - ln(T/T0))                                   termino termico
         + R_a T0 [(1 + Wt) ln((1 + Wt0)/(1 + Wt)) + Wt ln(Wt/Wt0)]                   termino de mezcla
    con Wt = W / 0,622 (moles de vapor por mol de aire seco; 0,622 = Mv/Ma) y el subindice 0 del estado muerto.
    El termino de presion es nulo porque P = P0. Vale 0 en el estado muerto y es >= 0 en todo estado.
    """
    t, t0 = T + K, T0 + K
    termico = (ah.CP_A + W * ah.CP_V) * t0 * (t / t0 - 1.0 - math.log(t / t0))
    wt, wt0 = W / MV_MA, W0 / MV_MA
    mezcla = (1.0 + wt) * math.log((1.0 + wt0) / (1.0 + wt))
    if wt > 0.0:
        mezcla += wt * math.log(wt / wt0)
    return termico + R_A * t0 * mezcla


def ex_agua_termica(T, T0):
    """Exergia termica del agua liquida incompresible [kJ/kg]: cp[(T - T0) - T0 ln(T/T0)].

    Sirve para los circuitos cerrados (agua helada, agua caliente, ACS): el termino quimico se cancela
    entre la entrada y la salida porque el caudal es el mismo.
    """
    t, t0 = T + K, T0 + K
    return ah.CP_W * ((t - t0) - t0 * math.log(t / t0))


def ex_agua_abierta(T, T0, W0):
    """Exergia del agua liquida que sale del sistema (condensado, agua de reposicion) [kJ/kg].

    Suma al termino termico el quimico respecto del vapor del aire exterior: el liquido a T0 no esta en
    equilibrio con el vapor ambiente si la humedad relativa es menor que 1,
        ex_quim = R_v T0 ln(p_sat(T0)/p_v0) + v (P0 - p_sat(T0)).
    Es la misma referencia que usa el termino de mezcla de ex_aire (derivada de ex_aire respecto de W en la
    saturacion = ex_quim; ver los tests). Sin este termino la serpentina se sobreestima en R_v T0 ln(1/HR0) por kg
    de condensado (unos 100 kJ/kg a 34 C y 45 % de humedad).
    """
    pv0 = ps.GetVapPresFromHumRatio(W0, P0)
    psat0 = ps.GetSatVapPres(T0)
    quim = R_V * (T0 + K) * math.log(psat0 / pv0) + V_LIQ * (P0 - psat0) / 1000.0
    return ex_agua_termica(T, T0) + quim


def temp_media_log(Ta, Tb):
    """Temperatura media logaritmica [K] de una corriente de agua que va de Ta a Tb [C]."""
    if abs(Ta - Tb) < 1e-12:
        return Ta + K
    return (Ta - Tb) / math.log((Ta + K) / (Tb + K))


def factor_exergia_frio(T0, T_cw_K):
    """Exergia del frio por unidad de calor extraido a la temperatura media T_cw: T0/T_cw - 1."""
    return (T0 + K) / T_cw_K - 1.0


# --------------------------------------------------------------------------------------
# Exergia quimica y fisica en la combustion [kJ/kmol]
# --------------------------------------------------------------------------------------
def ex_quimica_mezcla(n, T0):
    """Exergia quimica de una mezcla ideal de gases [kJ] para las cantidades n {especie: kmol}.

    ex = sum n_i ex_i + n R T0 sum y_i ln y_i  (Bejan et al., mezcla ideal); ex_i de EX_QUIM (recordadas).
    """
    n = {e: v for e, v in n.items() if v > 0.0}
    ntot = sum(n.values())
    suma = sum(v * EX_QUIM[e] for e, v in n.items())
    mezcla = ntot * cb.R_UNIV * (T0 + K) * sum((v / ntot) * math.log(v / ntot) for v in n.values())
    return suma + mezcla


def ex_quimica_gas_natural(P, T0):
    """Exergia quimica del gas natural [kJ/kmol de combustible] con la composicion de P."""
    return ex_quimica_mezcla(cb.composicion(P), T0)


@functools.lru_cache(maxsize=256)
def _ex_fisica_especie(especie, T_C, T0_C):
    """Exergia fisica de un gas ideal [kJ/kmol] a T_C respecto de T0_C: int cp dT - T0 int cp/T dT."""
    a, b = T0_C + K, T_C + K
    h = quad(lambda t: cb._cp0(especie, t), a, b)[0]
    s = quad(lambda t: cb._cp0(especie, t) / t, a, b)[0]
    return h - a * s


def _ex_fisica_mezcla(n, T_C, T0_C):
    return sum(v * _ex_fisica_especie(e, T_C, T0_C) for e, v in n.items() if v > 0.0)


def caldera_por_kmol(P, T0):
    """Balance exergetico de la caldera por kmol de combustible [kJ/kmol] con T0 en C.

    Entra: exergia quimica del gas (el gas se toma a 25 C y no se le asigna exergia fisica) y el aire de
    combustion (quimica por la misma tabla y fisica a T_aire_comb). Sale: calor util al agua, gases de escape
    (fisica a T_gases + quimica de los productos como mezcla), calor de radiacion y funcionamiento, destruccion.
    La destruccion se reparte en combustion (reactor adiabatico hasta la llama) y transferencia de calor.
    """
    b = cb.balance(P)
    cal = cb.caldera(P)
    pc = cal["pc"]
    prod, reac = b["productos"], b["reactivos"]
    aire = {"O2": reac["O2"], "N2": reac["N2_aire"]}
    x_comb = ex_quimica_gas_natural(P, T0)
    x_aire = ex_quimica_mezcla(aire, T0) + _ex_fisica_mezcla(aire, P["T_aire_comb"], T0)
    x_gas_q = ex_quimica_mezcla(prod, T0)
    x_gas_f = _ex_fisica_mezcla(prod, P["T_gases"], T0)
    T_ad = cb.temperatura_llama_adiabatica(P)
    x_ad = x_gas_q + _ex_fisica_mezcla(prod, T_ad, T0)
    PCI = pc["PCI_kJ_kmol"]
    return dict(PCI=PCI, eta=cal["eta_PCI"], x_comb=x_comb, x_aire=x_aire, x_gas_quim=x_gas_q, x_gas_fis=x_gas_f,
                x_prod_adiabatico=x_ad, T_llama=T_ad, balance=b, cal=cal)


# --------------------------------------------------------------------------------------
# Auxiliares del ciclo de refrigeracion (entropias con CoolProp)
# --------------------------------------------------------------------------------------
def _entropias_ciclo(r, fluido):
    """Entropias [kJ/(kg K)] de los estados 1 a 4 del ciclo de rf.ciclo."""
    Pev, Pc = r["P_ev"], r["P_c"]
    s1 = PropsSI("S", "P", Pev, "T", r["T1"] + K, fluido) / 1e3
    s2 = PropsSI("S", "P", Pc, "H", r["h2"] * 1e3, fluido) / 1e3
    s3 = PropsSI("S", "P", Pc, "T", r["T3"] + K, fluido) / 1e3
    s4 = PropsSI("S", "P", Pev, "H", r["h4"] * 1e3, fluido) / 1e3
    return s1, s2, s3, s4


def cop_reversible(T_frio_K, T_ambiente_K):
    """COP de un refrigerador reversible entre T_frio y T_ambiente."""
    return T_frio_K / (T_ambiente_K - T_frio_K)


def _fila(clave, equipo, grupo, F, Pr, L, D, eta_definida=True, nota=""):
    eta = Pr / F if (eta_definida and F > 1e-12 and Pr > 0.0) else None
    return dict(clave=clave, equipo=equipo, grupo=grupo, X_in=F, X_util=Pr, X_perdida=L, X_dest=D, eta_ex=eta, nota=nota)


# Agrupacion para la figura: clave de fila -> categoria de destruccion
GRUPOS_DEST = {
    "motor": "Compresor y motor", "compresor": "Compresor y motor",
    "condensador": "Condensador, válvula y evaporador", "valvula": "Condensador, válvula y evaporador",
    "evaporador": "Condensador, válvula y evaporador",
    "ventilador": "Ventiladores y bombas", "perdida_carga_aire": "Ventiladores y bombas",
    "vent_condensador": "Ventiladores y bombas", "bombas": "Ventiladores y bombas",
    "perdida_carga_agua": "Ventiladores y bombas",
    "mezcla": "Tratamiento del aire", "serpentina": "Tratamiento del aire", "recalentador": "Tratamiento del aire",
    "humidificador": "Tratamiento del aire",
    "caldera": "Caldera y ACS", "acs": "Caldera y ACS",
}
ORDEN_GRUPOS = ["Compresor y motor", "Condensador, válvula y evaporador", "Ventiladores y bombas",
                "Tratamiento del aire", "Caldera y ACS"]


# --------------------------------------------------------------------------------------
# Unidad de tratamiento de aire de una zona
# --------------------------------------------------------------------------------------
def _uta(c, g, caud_g, r, fd, T_out, W_out, T0, W0):
    """Corrientes y filas de exergia de la UTA de la zona g, ya ponderadas por fd [kW]."""
    P = c["P"]
    m, m_oa = caud_g["m_sup"], caud_g["m_oa"]
    x = m_oa / m
    ex = lambda T, W: ex_aire(T, W, T0, W0)

    # humedad del retorno, deducida de la mezcla del modelo (sin repetir su logica)
    W_ret = (r["W_mix"] - x * W_out) / (1.0 - x) if x < 1.0 else r["W_mix"]
    h_chk = x * ah.entalpia(T_out, W_out) + (1.0 - x) * ah.entalpia(r["T_r"], W_ret)
    if abs(h_chk - r["h_mix"]) > 1e-6 * max(1.0, abs(r["h_mix"])):
        raise ValueError(f"La mezcla de la zona {g} no es coherente con edificio.proceso")

    Q_coil, Q_heat, Q_hum = r["Q_coil"], r["Q_recal"] + r["Q_cal"], r["Q_hum"]
    T_c, W_c = r["T_c"], r["W_c"]
    T_h = T_c + Q_heat / (m * ah.cp_ah(W_c)) if Q_heat > 0.0 else T_c
    T_sup = r["T_sup"]
    W_fin = r["W_sup_min"] if Q_hum > 0.0 else W_c
    m_s = m * (W_fin - W_c) if Q_hum > 0.0 else 0.0               # kg/s de vapor
    m_cond = m * (r["W_mix"] - W_c) if r["enfria"] else 0.0       # kg/s de condensado

    x_oa = m_oa * ex(T_out, W_out)
    x_ret = (m - m_oa) * ex(r["T_r"], W_ret)
    x_mix = m * ex(r["T_mix"], r["W_mix"])
    x_c = m * ex(T_c, W_c)
    x_h = m * ex(T_h, W_c)
    x_f = m * ex(T_sup, W_c)                                      # salida del ventilador, antes de humidificar
    x_fin = m * ex(T_sup, W_fin)
    x_cond = m_cond * ex_agua_abierta(T_c, T0, W0)
    x_fw = m_s * ex_agua_abierta(P["T_agua_red"], T0, W0)         # agua de reposicion del humidificador

    # agua helada y agua caliente (circuitos cerrados)
    T_cw_in, T_cw_out = _par(c, "T_cw_ida"), _par(c, "T_cw_ida") + P["dT_aguahelada"]
    T_hw_in, T_hw_out = _par(c, "T_hw_ida"), _par(c, "T_hw_ret")
    m_cw = Q_coil / (ah.CP_W * P["dT_aguahelada"])
    m_hw = Q_heat / (ah.CP_W * (T_hw_in - T_hw_out))
    F_serp = m_cw * (ex_agua_termica(T_cw_in, T0) - ex_agua_termica(T_cw_out, T0))
    F_rec = m_hw * (ex_agua_termica(T_hw_in, T0) - ex_agua_termica(T_hw_out, T0))

    # vapor: exergia agregada por la caldera = Q_hum (1 - T0 (s_v - s_fw)/(h_v - h_fw)) con CoolProp
    if Q_hum > 0.0:
        hv, sv = PropsSI("H", "P", P0, "Q", 1, "Water") / 1e3, PropsSI("S", "P", P0, "Q", 1, "Water") / 1e3
        hf = PropsSI("H", "T", P["T_agua_red"] + K, "P", P0, "Water") / 1e3
        sf = PropsSI("S", "T", P["T_agua_red"] + K, "P", P0, "Water") / 1e3
        F_hum = Q_hum * (1.0 - (T0 + K) * (sv - sf) / (hv - hf))
    else:
        F_hum = 0.0

    Pv = caud_g["P_vent_kW"]
    eta_v = P["eta_vent"]
    D_mix = x_oa + x_ret - x_mix

    filas = {
        "mezcla": (D_mix, 0.0, 0.0, D_mix),
        "serpentina": (F_serp, x_c - x_mix, x_cond, F_serp - (x_c - x_mix) - x_cond),
        "recalentador": (F_rec, x_h - x_c, 0.0, F_rec - (x_h - x_c)),
        "ventilador": (Pv, eta_v * Pv, 0.0, Pv - eta_v * Pv),
        "perdida_carga_aire": (eta_v * Pv, x_f - x_h, 0.0, eta_v * Pv - (x_f - x_h)),
        "humidificador": (F_hum, (x_fin - x_f) - x_fw, 0.0, F_hum - ((x_fin - x_f) - x_fw)),
    }
    filas = {k: tuple(fd * v for v in t) for k, t in filas.items()}
    P_aire = fd * (x_fin - x_ret - x_oa - x_fw)
    return dict(
        fd=fd, m_sup=m * fd, m_oa=m_oa * fd, T_mix=r["T_mix"], W_mix=r["W_mix"], T_c=T_c, W_c=W_c, T_obj=r["T_obj"],
        T_sup=T_sup, T_ret=r["T_r"], W_ret=W_ret, W_fin=W_fin,
        Q_coil=fd * Q_coil, Q_heat=fd * Q_heat, Q_hum=fd * Q_hum, P_vent=fd * Pv, m_cond=fd * m_cond, m_vapor=fd * m_s,
        x_oa=fd * x_oa, x_ret=fd * x_ret, x_mix=fd * x_mix, x_c=fd * x_c, x_h=fd * x_h, x_f=fd * x_f, x_fin=fd * x_fin,
        x_cond=fd * x_cond, x_fw=fd * x_fw, F_serp=fd * F_serp, F_rec=fd * F_rec, F_hum=fd * F_hum,
        P_aire=P_aire, filas=filas)


# --------------------------------------------------------------------------------------
# Analisis de un estado
# --------------------------------------------------------------------------------------
def analisis(c, T_out, W_out, f_int_por_zona, q_sol, f_dias_activos=True, T0=None, W0=None):
    """Balance exergetico completo del sistema en un estado exterior dado [kW].

    c: configuracion de supuestos.defaults(). T_out [C], W_out [kg/kg]: estado exterior (aire de las UTA y
    del condensador). f_int_por_zona: {zona: fraccion de actividad} (las zonas ausentes o con None no operan) o
    un numero para todas. q_sol [W/m2]. f_dias_activos: pondera cada zona por Z[g]['f_dias'] como estimacion.anual.
    T0 [C], W0: estado muerto; por defecto el estado exterior (T0, W0 = T_out, W_out), P0 = 101.325 Pa.

    Devuelve un dict con 'tabla' (una fila por equipo con X_in, X_util, X_perdida, X_dest, eta_ex y su participacion
    en la destruccion total), 'global', 'perdidas', 'destruccion_grupos', 'enfriadora', 'caldera', 'acs', 'zonas',
    'estado' y 'verificaciones'.
    """
    P, Z = c["P"], c["Z"]
    T0 = T_out if T0 is None else T0
    W0 = W_out if W0 is None else W0
    caud = ed.caudales(c)
    if not isinstance(f_int_por_zona, dict):
        f_int_por_zona = {g: f_int_por_zona for g in Z}

    # ---- UTA por zona
    zonas = {}
    for g in Z:
        f_int = f_int_por_zona.get(g)
        if f_int is None:
            continue
        r = ed.proceso(c, g, caud, T_out, W_out, f_int, q_sol)
        fd = Z[g]["f_dias"] if f_dias_activos else 1.0
        zonas[g] = _uta(c, g, caud[g], r, fd, T_out, W_out, T0, W0)

    def suma(clave_fila, idx):
        return sum(z["filas"][clave_fila][idx] for z in zonas.values())

    Q_L = sum(z["Q_coil"] for z in zonas.values())
    Q_heat = sum(z["Q_heat"] for z in zonas.values())
    Q_hum = sum(z["Q_hum"] for z in zonas.values())
    W_vent = sum(z["P_vent"] for z in zonas.values())
    T0K = T0 + K

    filas = {}
    for clave, nombre in (("mezcla", "Mezcla de aire exterior y retorno"),
                          ("serpentina", "Serpentina de enfriamiento y deshumidificación"),
                          ("recalentador", "Recalentador y calefacción (agua 80/60 °C)"),
                          ("humidificador", "Humidificador de vapor"),
                          ("ventilador", "Ventiladores de impulsión"),
                          ("perdida_carga_aire", "Pérdidas de carga del aire (filtros, serpentinas, conductos)")):
        F, Pr, L, D = (suma(clave, i) for i in range(4))
        filas[clave] = (nombre, "aire", F, Pr, L, D)

    # ---- enfriadora
    enf = dict(Q_L=Q_L, activa=Q_L > 0.0)
    T_cw_in, T_cw_out = _par(c, "T_cw_ida"), _par(c, "T_cw_ida") + P["dT_aguahelada"]
    T_cw = temp_media_log(T_cw_out, T_cw_in)
    W_comp = W_cond = W_bomba = 0.0
    L_plume = 0.0
    X_frio = 0.0
    if Q_L > 0.0:
        pl = es._planta(c, Q_L, T_out)
        cop, T_cond, rc = rf.cop_vs_exterior(T_out, c)
        fl = P["refrigerante"]
        s1, s2, s3, s4 = _entropias_ciclo(rc, fl)
        m_r = Q_L / rc["q_L"]
        W_comp, W_cond, W_bomba = pl["W_comp"], pl["W_cond"], pl["W_bomba"]
        W_eje = W_comp * P["eta_motor"]
        if abs(W_eje - m_r * rc["w"]) > 1e-9 * W_eje:
            raise ValueError("El trabajo en el eje no coincide con m_r (h2 - h1)")
        psi = lambda h, s: h - T0K * s
        D_comp = T0K * m_r * (s2 - s1)
        D_valv = T0K * m_r * (s4 - s3)
        F_cond = m_r * (psi(rc["h2"], s2) - psi(rc["h3"], s3))
        F_evap = m_r * (psi(rc["h4"], s4) - psi(rc["h1"], s1))
        m_cw = Q_L / (ah.CP_W * P["dT_aguahelada"])
        X_frio = m_cw * (ex_agua_termica(T_cw_in, T0) - ex_agua_termica(T_cw_out, T0))
        # calor rechazado al aire exterior: sale a T_ext + eps (T_cond - T_ext); se pierde la exergia
        # termica neta del aire caliente respecto del aire de entrada (a T_out)
        Q_H = m_r * rc["q_H"]
        T_ao = T_out + _par(c, "eps_cond") * (T_cond - T_out)
        if T_ao > T_out + 1e-9:
            cpa = ah.cp_ah(W_out)
            m_a = Q_H / (cpa * (T_ao - T_out))
            et = lambda T: cpa * T0K * ((T + K) / T0K - 1.0 - math.log((T + K) / T0K))
            L_plume = m_a * (et(T_ao) - et(T_out))
        else:
            m_a = 0.0
        filas["motor"] = ("Motor eléctrico del compresor", "frio", W_comp, W_eje, 0.0, W_comp - W_eje)
        filas["compresor"] = ("Compresor (compresión real)", "frio", W_eje, m_r * (psi(rc["h2"], s2) - psi(rc["h1"], s1)), 0.0, D_comp)
        filas["condensador"] = ("Condensador por aire", "frio", F_cond, 0.0, L_plume, F_cond - L_plume)
        filas["valvula"] = ("Válvula de expansión", "frio", D_valv, 0.0, 0.0, D_valv)
        filas["evaporador"] = ("Evaporador (agua helada / R134a)", "frio", F_evap, X_frio, 0.0, F_evap - X_frio)
        filas["vent_condensador"] = ("Ventiladores del condensador", "frio", W_cond, 0.0, 0.0, W_cond)
        Vdp = P["eta_bomba"] * W_bomba
        filas["bombas"] = ("Bombas de agua helada", "frio", W_bomba, Vdp, 0.0, W_bomba - Vdp)
        filas["perdida_carga_agua"] = ("Pérdidas de carga del agua helada", "frio", Vdp, 0.0, 0.0, Vdp)
        enf.update(COP=cop, T_cond=T_cond, m_r=m_r, T_cw=T_cw, T_cw_in=T_cw_in, T_cw_out=T_cw_out, Q_H=Q_H, T_aire_sal=T_ao,
                   m_aire_cond=m_a, W_comp=W_comp, W_cond=W_cond, W_bomba=W_bomba, W_eje=W_eje, X_frio=X_frio,
                   L_aire_condensador=L_plume, cop_carnot_ciclo=rc["cop_carnot"], cop_comp=rc["cop_comp"],
                   cop_reversible_agua=cop_reversible(T_cw, T0K), s=(s1, s2, s3, s4),
                   D_gs_compresor=D_comp, D_gs_valvula=D_valv)
        enf["eta_compresor_grupo"] = X_frio / W_comp                      # exergia del frio / electricidad del compresor
        enf["eta_planta"] = X_frio / (W_comp + W_cond + W_bomba)          # incluye ventiladores del condensador y bombas
        enf["T0_sobre_Tcw_menos_1"] = factor_exergia_frio(T0, T_cw)
        enf["frio_bien_definido"] = T_cw_out < T0

    # ---- caldera y ACS
    a = es.acs(c)
    Q_acs = a["kW"]
    Q_net_acs = Q_acs / P["f_perd_acs"]
    T_hw_in, T_hw_out = _par(c, "T_hw_ida"), _par(c, "T_hw_ret")
    ex_hw = ex_agua_termica(T_hw_in, T0) - ex_agua_termica(T_hw_out, T0)       # kJ/kg de agua del circuito
    F_acs = Q_acs / (ah.CP_W * (T_hw_in - T_hw_out)) * ex_hw
    m_acs = Q_net_acs / (ah.CP_W * (P["T_acs"] - P["T_agua_fria"]))
    P_acs = m_acs * (ex_agua_termica(P["T_acs"], T0) - ex_agua_termica(P["T_agua_fria"], T0))
    L_acs = (Q_acs - Q_net_acs) * (1.0 - T0K / (_par(c, "T_perd_acs") + K))
    filas["acs"] = ("Calentamiento de ACS (intercambiador y acumulación)", "calor", F_acs, P_acs, L_acs, F_acs - P_acs - L_acs)

    Q_hw = Q_heat + Q_acs                                  # calor al circuito de agua caliente
    Q_util = Q_hw + Q_hum                                  # calor util total de la caldera
    cpk = caldera_por_kmol(P, T0)
    eta_c = cpk["eta"]
    E_PCI = Q_util / eta_c
    n_f = E_PCI / cpk["PCI"]                               # kmol/s de gas natural
    X_comb = n_f * cpk["x_comb"]
    X_air = n_f * cpk["x_aire"]
    X_gas_q, X_gas_f = n_f * cpk["x_gas_quim"], n_f * cpk["x_gas_fis"]
    X_rad = P["f_rad"] * E_PCI * (1.0 - T0K / (_par(c, "T_rad") + K))
    X_hw = Q_hw / (ah.CP_W * (T_hw_in - T_hw_out)) * ex_hw
    X_vap = sum(z["F_hum"] for z in zonas.values())
    X_heat = X_hw + X_vap
    L_gas = X_gas_q + X_gas_f - X_air                      # exergia neta que sale con los gases (descontado el aire que entra)
    L_caldera = L_gas + X_rad
    D_caldera = X_comb - X_heat - L_caldera
    D_comb = n_f * (cpk["x_comb"] + cpk["x_aire"] - cpk["x_prod_adiabatico"])
    D_transf = D_caldera - D_comb
    filas["caldera"] = ("Caldera de gas natural (combustión y transferencia)", "calor", X_comb, X_heat, L_caldera, D_caldera)

    # ---- tabla
    orden = ["mezcla", "serpentina", "recalentador", "humidificador", "ventilador", "perdida_carga_aire", "motor", "compresor",
             "condensador", "valvula", "evaporador", "vent_condensador", "bombas", "perdida_carga_agua", "caldera", "acs"]
    sin_eta = {"mezcla", "serpentina", "recalentador", "humidificador", "perdida_carga_aire", "condensador", "valvula",
               "vent_condensador", "perdida_carga_agua"}
    notas = {
        "mezcla": "sin producto: F = D",
        "serpentina": "producto: variación de exergía del aire; no se define eficiencia (T0 por encima del aire tratado)",
        "recalentador": "producto: variación de exergía del aire; no se define eficiencia (aire por debajo de T0)",
        "humidificador": "vapor saturado a 101,3 kPa; solo opera en invierno",
        "ventilador": "producto: trabajo de flujo V ΔP; eta = rendimiento del ventilador",
        "perdida_carga_aire": "el trabajo de flujo se disipa; producto: ganancia de exergía por el calor del ventilador",
        "motor": "el calor del motor se disipa a T ≈ T0: se contabiliza como destrucción",
        "compresor": "D = T0 m (s2 - s1)",
        "condensador": "L: exergía del aire caliente (efectividad 0,5); D: transferencia y mezcla con el ambiente",
        "valvula": "D = T0 m (s4 - s3)",
        "evaporador": "producto: exergía del frío del agua helada",
        "vent_condensador": "sin producto definido: se contabiliza destruida",
        "bombas": "producto: trabajo de flujo V ΔP",
        "perdida_carga_agua": "el trabajo de flujo se disipa",
        "caldera": "producto: exergía del calor al agua 80/60 °C (y del vapor)",
        "acs": "producto: exergía del agua a 60 °C respecto del agua de red",
    }
    tabla = []
    D_total = sum(filas[k][5] for k in orden if k in filas)
    for k in orden:
        if k not in filas:
            continue
        nombre, grupo, F, Pr, L, D = filas[k]
        definida = k not in sin_eta
        if k == "evaporador":
            definida = enf.get("frio_bien_definido", False)
        fila = _fila(k, nombre, grupo, F, Pr, L, D, eta_definida=definida, nota=notas[k])
        fila["particip_dest"] = D / D_total if D_total > 0 else 0.0
        tabla.append(fila)

    # ---- balance global
    X_elec = W_comp + W_cond + W_bomba + W_vent
    X_in = X_elec + X_comb
    P_aire = sum(z["P_aire"] for z in zonas.values())
    L_cond = sum(z["x_cond"] for z in zonas.values())
    perdidas = {"condensado": L_cond, "aire_condensador": L_plume, "gases_escape": L_gas, "radiacion_caldera": X_rad,
                "perdidas_acs": L_acs}
    L_total = sum(perdidas.values())
    P_total = P_aire + P_acs
    cierre = X_in - (P_total + L_total + D_total)
    glob = dict(X_elec=X_elec, X_comb=X_comb, X_in=X_in, P_aire=P_aire, P_acs=P_acs, P_total=P_total, L_total=L_total,
                D_total=D_total, cierre_abs=cierre, cierre_rel=abs(cierre) / X_in if X_in > 0 else 0.0,
                # el producto del aire (X_impulsion - X_retorno - X_exterior) solo es una medida de servicio si es > 0;
                # si no, la eficiencia global no esta bien definida y se informa solo la razon de referencia
                eta_global=P_total / X_in if (X_in > 0 and P_aire > 0) else None,
                eta_global_ref=P_total / X_in if X_in > 0 else None, producto_aire_bien_definido=P_aire > 0)
    grupos = {gname: sum(f["X_dest"] for f in tabla if GRUPOS_DEST[f["clave"]] == gname) for gname in ORDEN_GRUPOS}

    # ---- caldera y ACS (detalle)
    cald = dict(Q_util=Q_util, Q_agua=Q_hw, Q_vapor=Q_hum, E_PCI=E_PCI, n_f=n_f, eta_PCI=eta_c, T_llama=cpk["T_llama"],
                X_comb=X_comb, X_aire=X_air, X_calor=X_heat, X_gas_quim=X_gas_q, X_gas_fis=X_gas_f, X_rad=X_rad,
                D_total=D_caldera, D_combustion=D_comb, D_transferencia=D_transf,
                eta_ex=X_heat / X_comb, ex_comb_sobre_PCI=cpk["x_comb"] / cpk["PCI"],
                ex_comb_kJ_kmol=cpk["x_comb"], PCI_kJ_kmol=cpk["PCI"], estado_ex_quimicas=EX_QUIM_ESTADO)
    share = Q_acs / Q_util
    acs = dict(Q_kW=Q_acs, Q_util_kW=Q_net_acs, m_kg_s=m_acs, X_comb_asignada=X_comb * share, P=P_acs, L=L_acs,
               D_intercambiador=F_acs - P_acs - L_acs, D_caldera_asignada=D_caldera * share,
               L_caldera_asignada=L_caldera * share,
               eta_cadena=P_acs / (X_comb * share) if X_comb > 0 else None)

    ver = dict(ex_estado_muerto=ex_aire(T0, W0, T0, W0), cierre_rel=glob["cierre_rel"], T_cw_logmedia_K=T_cw)
    if enf["activa"]:
        D_enf = sum(filas[k][5] for k in ("motor", "compresor", "condensador", "valvula", "evaporador"))
        ver["cierre_enfriadora_rel"] = abs(W_comp - (X_frio + L_plume + D_enf)) / W_comp
    estado = dict(T_out=T_out, W_out=W_out, T0=T0, W0=W0, HR_out=ah.hr_desde_w(T_out, W_out, P0), HR0=ah.hr_desde_w(T0, W0, P0),
                  q_sol=q_sol, f_int=dict(f_int_por_zona), f_dias_activos=f_dias_activos, P0=P0)
    res = dict(estado=estado, tabla=tabla, perdidas=perdidas, destruccion_grupos=grupos, enfriadora=enf, caldera=cald,
               acs=acs, zonas=zonas, verificaciones=ver)
    res["global"] = glob
    return res


# --------------------------------------------------------------------------------------
# Estados de analisis
# --------------------------------------------------------------------------------------
def estado_max_recalentamiento(c):
    """Estado (mes x mitad del dia) de mayor potencia de recalentamiento sumada del ano, como en estimacion.anual."""
    P, Z, clima = c["P"], c["Z"], c["clima"]
    caud = ed.caudales(c)
    mejor = None
    for i, mes in enumerate(clima["meses"]):
        T_m, HR_m = clima["T"][i], clima["HR"][i]
        W_m = ah.w_desde_hr(T_m, HR_m, P["presion"])
        for mitad in ("dia", "noche"):
            T_out = T_m + (P["rango_diario"] / 2.0 if mitad == "dia" else -P["rango_diario"] / 2.0)
            q_sol = P["q_sol_dia"] if mitad == "dia" else 0.0
            W_est = min(W_m, ah.w_desde_hr(T_out, 1.0, P["presion"]))
            f_int, Q_rec = {}, 0.0
            for g, z in Z.items():
                if mitad == "noche" and not z["opera_noche"]:
                    continue
                f_int[g] = z["f_dia"] if mitad == "dia" else z["f_noche"]
                r = ed.proceso(c, g, caud, T_out, W_est, f_int[g], q_sol)
                Q_rec += r["Q_recal"] * z["f_dias"]
            if mejor is None or Q_rec > mejor["Q_recal_kW"]:
                mejor = dict(mes=mes, mitad=mitad, T_out=T_out, W_out=W_est, q_sol=q_sol, f_int=f_int, Q_recal_kW=Q_rec,
                             horas=12.0 * clima["dias"][i])
    return mejor


def estados_de_analisis(c):
    """Los dos estados del analisis: verano pico de diseno y maximo recalentamiento del ano."""
    P, Z = c["P"], c["Z"]
    Tv, Wv = ed.estado_exterior_verano(c)
    f1 = {g: 1.0 for g in Z}
    ver = analisis(c, Tv, Wv, f1, P["q_sol_pico"], f_dias_activos=False)
    est = estado_max_recalentamiento(c)
    mr = analisis(c, est["T_out"], est["W_out"], est["f_int"], est["q_sol"], f_dias_activos=True)
    return {
        "verano_pico": dict(nombre="Verano pico de diseño", condiciones=dict(T_out=Tv, W_out=Wv, f_int=f1, q_sol=P["q_sol_pico"],
                                                                         f_dias_activos=False), resultado=ver),
        "max_recalentamiento": dict(nombre=f"Máximo recalentamiento del año ({est['mes']}, {'día' if est['mitad'] == 'dia' else 'noche'})",
                                    condiciones=dict(T_out=est["T_out"], W_out=est["W_out"], f_int=est["f_int"], q_sol=est["q_sol"],
                                                     f_dias_activos=True, mes=est["mes"], mitad=est["mitad"],
                                                     Q_recal_kW=est["Q_recal_kW"]), resultado=mr),
    }


def sensibilidad_T0(c, T0s=(25.0, 17.5)):
    """Verano pico de diseno con otros estados muertos. Para T0 distinto del exterior, la humedad de referencia
    es la del aire a T0 con la humedad relativa media anual del clima (SUPUESTO). Devuelve una lista de dicts."""
    P, Z = c["P"], c["Z"]
    Tv, Wv = ed.estado_exterior_verano(c)
    f1 = {g: 1.0 for g in Z}
    HR_media = sum(c["clima"]["HR"]) / len(c["clima"]["HR"])
    salida = []
    for T0 in (Tv,) + tuple(T0s):
        W0 = Wv if T0 == Tv else ah.w_desde_hr(T0, HR_media, P["presion"])
        r = analisis(c, Tv, Wv, f1, P["q_sol_pico"], f_dias_activos=False, T0=T0, W0=W0)
        g = r["global"]
        fan = next(f for f in r["tabla"] if f["clave"] == "ventilador")
        salida.append(dict(T0=T0, W0=W0, HR0=r["estado"]["HR0"], X_in=g["X_in"], P_total=g["P_total"], L_total=g["L_total"],
                           D_total=g["D_total"], eta_global=g["eta_global"], eta_enfriadora=r["enfriadora"]["eta_planta"],
                           eta_compresor_grupo=r["enfriadora"]["eta_compresor_grupo"], eta_caldera=r["caldera"]["eta_ex"],
                           eta_ventiladores=fan["eta_ex"], destruccion_grupos=r["destruccion_grupos"],
                           D_por_fila={f["clave"]: f["X_dest"] for f in r["tabla"]}, cierre_rel=g["cierre_rel"],
                           resultado=r))
    return salida


# --------------------------------------------------------------------------------------
# Salida de texto
# --------------------------------------------------------------------------------------
def _n(x, nd=1):
    s = f"{x:,.{nd}f}"
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def tabla_texto(res):
    """Tabla de un estado en texto (kW; eficiencias y participacion en %)."""
    e, g = res["estado"], res["global"]
    out = [f"Estado muerto T0 = {_n(e['T0'])} °C, W0 = {_n(e['W0'] * 1000, 2)} g/kg (HR0 {_n(e['HR0'] * 100, 0)} %), P0 = 101,325 kPa",
           f"{'Equipo':<60}{'X_in':>9}{'X_útil':>9}{'X_pérd':>9}{'X_dest':>9}{'eta_ex':>8}{'%dest':>7}"]
    for f in res["tabla"]:
        eta = "—" if f["eta_ex"] is None else _n(f["eta_ex"] * 100, 1)
        out.append(f"{f['equipo'][:59]:<60}{_n(f['X_in']):>9}{_n(f['X_util']):>9}{_n(f['X_perdida']):>9}{_n(f['X_dest']):>9}"
                   f"{eta:>8}{_n(f['particip_dest'] * 100, 1):>7}")
    out.append(f"Entrada: electricidad {_n(g['X_elec'])} kW + combustible {_n(g['X_comb'])} kW = {_n(g['X_in'])} kW")
    out.append(f"Útil: aire {_n(g['P_aire'])} + ACS {_n(g['P_acs'], 2)} kW; pérdidas {_n(g['L_total'])} kW; destrucción {_n(g['D_total'])} kW; "
               f"cierre {g['cierre_rel']:.1e}; eficiencia global "
               + (f"{_n(g['eta_global'] * 100, 1)} %" if g["eta_global"] is not None else
                  f"no definida (producto del aire <= 0; razón de referencia {_n(g['eta_global_ref'] * 100, 1)} %)"))
    return "\n".join(out)


def main():
    from . import supuestos
    c = supuestos.defaults()
    for clave, est in estados_de_analisis(c).items():
        print(f"== {est['nombre']} ==")
        print(tabla_texto(est["resultado"]))
        print()
    print("== Sensibilidad al estado muerto (verano pico) ==")
    for s in sensibilidad_T0(c):
        eg = "no definida" if s["eta_global"] is None else f"{_n(s['eta_global'] * 100, 1)} %"
        print(f"T0 {_n(s['T0'])} °C: D {_n(s['D_total'])} kW, P {_n(s['P_total'])} kW, eta global {eg}, "
              f"enfriadora {_n(s['eta_enfriadora'] * 100, 1)} %, caldera {_n(s['eta_caldera'] * 100, 1)} %")


if __name__ == "__main__":
    main()
