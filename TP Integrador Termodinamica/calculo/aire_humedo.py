"""Aire humedo: propiedades psicrometricas (psychrolib, ASHRAE) en SI.

Unidades: temperatura en C, humedad especifica W en kg de vapor por kg de aire seco,
entalpia en kJ por kg de aire seco, presion en Pa.
"""
import psychrolib as ps
from scipy.optimize import brentq

ps.SetUnitSystem(ps.SI)

P0 = 101325.0
H_FG = 2501.0          # kJ/kg, calor latente a 0 C
CP_A = 1.006           # kJ/(kg K), aire seco
CP_V = 1.86            # kJ/(kg K), vapor de agua
CP_W = 4.186           # kJ/(kg K), agua liquida


def w_desde_hr(T, HR, P=P0):
    return ps.GetHumRatioFromRelHum(T, HR, P)


def w_desde_tbh(T, Tbh, P=P0):
    return ps.GetHumRatioFromTWetBulb(T, Tbh, P)


def hr_desde_w(T, W, P=P0):
    return ps.GetRelHumFromHumRatio(T, W, P)


def entalpia(T, W):
    """kJ por kg de aire seco."""
    return ps.GetMoistAirEnthalpy(T, W) / 1000.0


def t_desde_entalpia(h, W):
    return ps.GetTDryBulbFromEnthalpyAndHumRatio(h * 1000.0, W)


def t_rocio(W, P=P0):
    return ps.GetTDewPointFromHumRatio(20.0, W, P)


def t_serpentina(W, HR, P=P0):
    """Temperatura a la que el aire saturado al HR dado tiene la humedad W."""
    f = lambda T: ps.GetHumRatioFromRelHum(T, HR, P) - W
    return brentq(f, -5.0, 45.0)


def cp_ah(W):
    """Calor especifico del aire humedo por kg de aire seco [kJ/(kg K)]."""
    return CP_A + CP_V * W


def h_agua_liquida(T):
    return CP_W * T
