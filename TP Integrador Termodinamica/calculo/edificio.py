"""Zonas del hospital y tratamiento del aire (aire humedo).

Cada zona se trata como un sistema de aire de caudal constante (CAV):

    aire exterior + aire de retorno -> mezcla -> serpentina de agua helada (enfria y deshumidifica)
    -> recalentamiento -> (humidificacion con vapor en invierno) -> impulsion a la zona

Todas las potencias en kW (positivas), temperaturas en C, humedades en kg/kg de aire seco.
"""
from . import aire_humedo as ah


def superficies(c):
    P = c["P"]
    a1 = P["n_or"] * P["a_or"]
    a2 = P["camas_uti"] * P["a_uti_cama"]
    a3 = P["camas_gen"] * P["a_gen_cama"]
    a_cond = P["f_acond"] * P["A_cub"]
    resto = a_cond - a1 - a2 - a3
    if resto <= 0:
        raise ValueError("La superficie climatizada no alcanza para las zonas G1 a G3")
    a4 = P["f_g4_24h"] * resto            # areas generales que funcionan las 24 h
    a5 = resto - a4                       # areas generales de dia
    return {"G1": a1, "G2": a2, "G3": a3, "G4": a4, "G5": a5}, a_cond


def estado_exterior_verano(c):
    P = c["P"]
    return P["T_bs_ver"], ah.w_desde_tbh(P["T_bs_ver"], P["T_bh_ver"], P["presion"])


def estado_exterior_invierno(c):
    P = c["P"]
    return P["T_inv"], ah.w_desde_hr(P["T_inv"], P["HR_inv"], P["presion"])


def caudales(c):
    """Caudal de aire de impulsion y de aire exterior por zona [kg/s], dimensionados en el verano pico.

    m_sup = max(caudal por renovaciones totales, caudal que absorbe la carga sensible pico con la
    temperatura minima de impulsion). El aire exterior es fijo en valor absoluto (renovaciones minimas).
    """
    P, Z = c["P"], c["Z"]
    A, _ = superficies(c)
    out = {}
    for g, z in Z.items():
        T_r = z["t_ver"]
        W_r = ah.w_desde_hr(T_r, z["hr_ver"], P["presion"])
        Q_s_pico = A[g] * (z["q_s"] + z["f_env"] * (P["UA_m2"] * (P["T_bs_ver"] - T_r) + P["q_sol_pico"]))   # W
        m_sens = Q_s_pico / 1000.0 / (ah.cp_ah(W_r) * (T_r - P["T_sup_min"]))
        m_ach = z["ach_tot"] * A[g] * P["h_techo"] / 3600.0 * P["rho_aire"]
        m_oa = z["ach_oa"] * A[g] * P["h_techo"] / 3600.0 * P["rho_aire"]
        m_sup = max(m_ach, m_sens)
        out[g] = dict(A=A[g], m_sup=m_sup, m_oa=min(m_oa, m_sup), m_ach=m_ach, m_sens=m_sens,
                      Q_s_pico_kW=Q_s_pico / 1000.0,
                      V_sup_m3h=m_sup / P["rho_aire"] * 3600.0,
                      P_vent_kW=m_sup / P["rho_aire"] * z["dp_vent"] / 1000.0 / P["eta_vent"])
    return out


def proceso(c, g, caud, T_out, W_out, f_int, q_sol):
    """Tratamiento del aire de la zona g para un estado exterior y una actividad dados.

    Devuelve las cargas de la serpentina, el recalentamiento, la calefaccion y la humidificacion [kW].
    """
    P, z = c["P"], c["Z"][g]
    pres = P["presion"]
    A = caud[g]["A"]
    m_sup, m_oa = caud[g]["m_sup"], caud[g]["m_oa"]
    verano = T_out >= P["T_cambio_estacion"]

    # Consigna de la zona
    T_r = z["t_ver"] if verano else z["t_inv"]
    W_set = ah.w_desde_hr(T_r, z["hr_ver"], pres)     # humedad maxima admisible (deshumidifica por encima)
    W_min = ah.w_desde_hr(T_r, z["hr_min"], pres)     # humedad minima admisible (humidifica por debajo)
    W_ret = W_set if verano else W_min                # humedad del aire de retorno (aproximacion)

    # Cargas de la zona [W]
    Q_s = A * (z["q_s"] * f_int + z["f_env"] * (P["UA_m2"] * (T_out - T_r) + q_sol))   # sensible neta (+ = enfriar)
    Q_l = A * z["q_l"] * f_int                                                          # latente

    # Condiciones de impulsion requeridas
    T_sup = T_r - Q_s / 1000.0 / (m_sup * ah.cp_ah(W_set))
    T_sup = min(max(T_sup, P["T_sup_min"]), P["T_sup_max"])
    term_lat = Q_l / 1000.0 / (m_sup * P["h_fg"])
    W_sup_max = max(W_set - term_lat, 1e-4)
    W_sup_min = max(W_min - term_lat, 1e-4)

    # Mezcla de aire exterior y retorno
    x = m_oa / m_sup
    h_mix = x * ah.entalpia(T_out, W_out) + (1 - x) * ah.entalpia(T_r, W_ret)
    W_mix = x * W_out + (1 - x) * W_ret
    T_mix = ah.t_desde_entalpia(h_mix, W_mix)

    # Serpentina de enfriamiento
    enfria = False
    if W_mix > W_sup_max + 1e-9:                      # hay que deshumidificar
        W_c = W_sup_max
        T_c = ah.t_serpentina(W_c, P["HR_serp"], pres)
        if T_c > T_sup:                               # la serpentina no puede salir mas caliente que la impulsion
            T_c = T_sup
            W_c = min(W_sup_max, ah.w_desde_hr(T_c, P["HR_serp"], pres))
        if T_c >= T_mix:                              # no hay nada que enfriar
            T_c, W_c = T_mix, W_mix
        else:
            enfria = True
    elif T_mix > T_sup + 1e-9:                        # solo enfriamiento sensible
        T_c, W_c, enfria = T_sup, W_mix, True
    else:
        T_c, W_c = T_mix, W_mix

    Q_coil = Q_lat = Q_sens = 0.0
    if enfria:
        h_c = ah.entalpia(T_c, W_c)
        cond = m_sup * (W_mix - W_c) * ah.h_agua_liquida(T_c)          # entalpia del condensado
        Q_coil = m_sup * (h_mix - h_c) - cond
        Q_lat = m_sup * (W_mix - W_c) * P["h_fg"]
        Q_sens = Q_coil - Q_lat

    # Recalentamiento o calefaccion
    Q_recal = Q_cal = 0.0
    if T_c < T_sup - 1e-9:
        calor = m_sup * ah.cp_ah(W_c) * (T_sup - T_c)
        if enfria:
            Q_recal = calor
        else:
            Q_cal = calor

    # Humidificacion con vapor (isotermica)
    Q_hum = 0.0
    if W_c < W_sup_min - 1e-9:
        dW = W_sup_min - W_c
        h_vapor = 2676.0   # kJ/kg, vapor saturado a 101,3 kPa (propiedades del agua)
        Q_hum = m_sup * dW * (h_vapor - ah.h_agua_liquida(P["T_agua_red"]))

    return dict(verano=verano, T_r=T_r, T_sup=T_sup, W_sup_max=W_sup_max, W_sup_min=W_sup_min, T_mix=T_mix, W_mix=W_mix,
                h_mix=h_mix, T_c=T_c, W_c=W_c, enfria=enfria, Q_s_zona_kW=Q_s / 1000.0, Q_l_zona_kW=Q_l / 1000.0,
                Q_coil=Q_coil, Q_coil_sens=Q_sens, Q_coil_lat=Q_lat, Q_recal=Q_recal, Q_cal=Q_cal, Q_hum=Q_hum)
