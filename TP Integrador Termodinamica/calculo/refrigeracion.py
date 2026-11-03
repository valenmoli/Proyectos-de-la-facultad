"""Ciclo de refrigeracion por compresion de vapor (CoolProp).

Estados:
  1  salida del evaporador, vapor sobrecalentado
  2  salida del compresor (real, con rendimiento isentropico)
  2s salida del compresor ideal (isentropica)
  3  salida del condensador, liquido subenfriado
  4  salida de la valvula de expansion (isoentalpica)
"""
from CoolProp.CoolProp import PropsSI

K = 273.15


def ciclo(T_ev, T_cond, refrigerante="R134a", sobrecal=5.0, subenf=4.0, eta_is=0.72, eta_motor=0.94):
    """Calcula el ciclo. Temperaturas en C. Entalpias y calores en kJ/kg de refrigerante."""
    Tev, Tc = T_ev + K, T_cond + K
    P_ev = PropsSI("P", "T", Tev, "Q", 1, refrigerante)
    P_c = PropsSI("P", "T", Tc, "Q", 1, refrigerante)
    T1 = Tev + sobrecal
    h1 = PropsSI("H", "P", P_ev, "T", T1, refrigerante) / 1e3
    s1 = PropsSI("S", "P", P_ev, "T", T1, refrigerante) / 1e3
    h2s = PropsSI("H", "P", P_c, "S", s1 * 1e3, refrigerante) / 1e3
    h2 = h1 + (h2s - h1) / eta_is
    T2 = PropsSI("T", "P", P_c, "H", h2 * 1e3, refrigerante)
    T3 = Tc - subenf
    h3 = PropsSI("H", "P", P_c, "T", T3, refrigerante) / 1e3
    h4 = h3
    q_L = h1 - h4                    # efecto frigorifico [kJ/kg]
    w = h2 - h1                      # trabajo de compresion [kJ/kg]
    q_H = h2 - h3                    # calor rechazado [kJ/kg]
    cop_comp = q_L / w               # sobre el trabajo en el eje
    cop_elec = q_L / (w / eta_motor)  # sobre la potencia electrica del compresor
    cop_carnot = Tev / (Tc - Tev)
    return dict(P_ev=P_ev, P_c=P_c, T1=T1 - K, T2=T2 - K, T3=T3 - K, h1=h1, h2=h2, h2s=h2s, h3=h3, h4=h4,
                q_L=q_L, w=w, q_H=q_H, cop_comp=cop_comp, cop_elec=cop_elec, cop_carnot=cop_carnot,
                x4=PropsSI("Q", "P", P_ev, "H", h4 * 1e3, refrigerante))


def cop_vs_exterior(T_ext, c):
    """COP electrico del compresor para una temperatura exterior dada, segun la configuracion c."""
    P = c["P"]
    T_cond = max(T_ext + P["dT_cond"], P["T_cond_min"])
    r = ciclo(P["T_ev"], T_cond, P["refrigerante"], P["sobrecal"], P["subenf"], P["eta_is"], P["eta_motor"])
    return r["cop_elec"], T_cond, r
