"""Combustion de gas natural y rendimiento de la caldera.

Reaccion de cada hidrocarburo CxHy:  CxHy + (x + y/4) O2 -> x CO2 + (y/2) H2O
Aire: 21 % O2 y 79 % N2 en moles. Gases ideales. Sin disociacion.
Entalpias de formacion a 25 C y 1 atm [kJ/kmol] (tablas de termodinamica).
"""
import numpy as np
from CoolProp.CoolProp import PropsSI
from scipy.integrate import quad
from scipy.optimize import brentq

R_UNIV = 8.314462          # kJ/(kmol K)
T0 = 298.15                # K, referencia de entalpias de formacion
N2_POR_O2 = 79.0 / 21.0

# (atomos C, atomos H, entalpia de formacion [kJ/kmol])
COMB = {"CH4": (1, 4, -74850.0), "C2H6": (2, 6, -84680.0), "C3H8": (3, 8, -103850.0)}
HF_CO2 = -393520.0
HF_H2O_G = -241820.0
HF_H2O_L = -285830.0

_NOMBRE_CP = {"CO2": "CO2", "H2O": "Water", "N2": "Nitrogen", "O2": "Oxygen"}


def _cp0(especie, T):
    """Calor especifico molar de gas ideal [kJ/(kmol K)] (CoolProp, termino ideal)."""
    return PropsSI("CP0MOLAR", "T", T, "P", 1000.0, _NOMBRE_CP[especie])


def dh_sensible(especie, T_C):
    """Entalpia sensible [kJ/kmol] desde 25 C hasta T_C, por integracion de cp ideal."""
    T = T_C + 273.15
    val, _ = quad(lambda t: _cp0(especie, t), T0, T)
    return val


def composicion(P):
    y = {"CH4": P["gas_CH4"], "C2H6": P["gas_C2H6"], "C3H8": P["gas_C3H8"], "N2": P["gas_N2"], "CO2": P["gas_CO2"]}
    s = sum(y.values())
    assert abs(s - 1.0) < 1e-9, f"la composicion suma {s}"
    return y


def balance(P):
    """Balance molar por kmol de combustible. Devuelve reactivos y productos."""
    y = composicion(P)
    lam = P["lambda_aire"]
    o2_st = sum(y[c] * (COMB[c][0] + COMB[c][1] / 4.0) for c in COMB)
    o2 = lam * o2_st
    n2_aire = N2_POR_O2 * o2
    prod = {
        "CO2": sum(y[c] * COMB[c][0] for c in COMB) + y["CO2"],
        "H2O": sum(y[c] * COMB[c][1] / 2.0 for c in COMB),
        "N2": y["N2"] + n2_aire,
        "O2": (lam - 1.0) * o2_st,
    }
    reac = {"combustible": 1.0, "O2": o2, "N2_aire": n2_aire, "aire_total": o2 + n2_aire}
    # Control de atomos (kmol de atomos por kmol de combustible)
    c_in = sum(y[c] * COMB[c][0] for c in COMB) + y["CO2"]
    h_in = sum(y[c] * COMB[c][1] for c in COMB)
    o_in = 2 * o2 + 2 * y["CO2"]
    n_in = 2 * (y["N2"] + n2_aire)
    c_out, h_out = prod["CO2"], 2 * prod["H2O"]
    o_out = 2 * prod["CO2"] + prod["H2O"] + 2 * prod["O2"]
    n_out = 2 * prod["N2"]
    atomos = dict(C=(c_in, c_out), H=(h_in, h_out), O=(o_in, o_out), N=(n_in, n_out))
    return dict(y=y, o2_estequiometrico=o2_st, reactivos=reac, productos=prod, atomos=atomos,
                n_productos=sum(prod.values()), aire_kmol_por_kmol=reac["aire_total"])


def poder_calorifico(P):
    """PCS y PCI [kJ/kmol de combustible y MJ/m3 estandar] del gas natural."""
    y = composicion(P)
    hhv = 0.0
    lhv = 0.0
    for c, (x, h, hf) in COMB.items():
        hhv += y[c] * (x * -HF_CO2 + (h / 2.0) * -HF_H2O_L + hf)
        lhv += y[c] * (x * -HF_CO2 + (h / 2.0) * -HF_H2O_G + hf)
    Tref = P["T_ref_gas"] + 273.15
    v_molar = R_UNIV * Tref / 101.325          # m3/kmol a 15 C y 101,325 kPa
    return dict(PCS_kJ_kmol=hhv, PCI_kJ_kmol=lhv, v_molar=v_molar,
                PCS_MJ_m3=hhv / v_molar / 1000.0, PCI_MJ_m3=lhv / v_molar / 1000.0,
                PCS_kWh_m3=hhv / v_molar / 3600.0, PCI_kWh_m3=lhv / v_molar / 3600.0,
                PCS_kcal_m3=hhv / v_molar / 4.1868, relacion_PCS_PCI=hhv / lhv)


def caldera(P):
    """Rendimiento de la caldera sobre PCI por balance de energia de los gases de escape."""
    b = balance(P)
    pc = poder_calorifico(P)
    prod = b["productos"]
    h_prod = sum(n * dh_sensible(e, P["T_gases"]) for e, n in prod.items())
    # reactivos a T_aire_comb: aire (O2 y N2); el combustible se toma a la misma temperatura
    r = b["reactivos"]
    h_reac = r["O2"] * dh_sensible("O2", P["T_aire_comb"]) + r["N2_aire"] * dh_sensible("N2", P["T_aire_comb"])
    lhv = pc["PCI_kJ_kmol"]
    q_gases = (h_prod - h_reac) / lhv
    eta = 1.0 - q_gases - P["f_rad"]
    # Punto de rocio de los gases (agua en los productos)
    y_h2o = prod["H2O"] / b["n_productos"]
    p_w = y_h2o * 101325.0
    t_rocio = PropsSI("T", "P", p_w, "Q", 1, "Water") - 273.15
    return dict(eta_PCI=eta, q_gases=q_gases, y_H2O=y_h2o, T_rocio=t_rocio, balance=b, pc=pc,
                eta_PCS=eta * lhv / pc["PCS_kJ_kmol"])


def temperatura_llama_adiabatica(P):
    """Temperatura de llama adiabatica [C] con combustion completa y sin disociacion."""
    b = balance(P)
    pc = poder_calorifico(P)
    r = b["reactivos"]
    h_reac = r["O2"] * dh_sensible("O2", P["T_aire_comb"]) + r["N2_aire"] * dh_sensible("N2", P["T_aire_comb"])
    objetivo = pc["PCI_kJ_kmol"] + h_reac
    f = lambda T: sum(n * dh_sensible(e, T) for e, n in b["productos"].items()) - objetivo
    return brentq(f, 500.0, 2800.0)


def consumo_gas(q_util_kWh, eta_PCI, pc):
    """Energia del combustible (PCI y PCS, kWh) y volumen (m3 estandar) para entregar q_util_kWh."""
    e_pci = q_util_kWh / eta_PCI
    e_pcs = e_pci * pc["relacion_PCS_PCI"]
    return dict(E_PCI_kWh=e_pci, E_PCS_kWh=e_pcs, V_m3=e_pcs / pc["PCS_kWh_m3"])
