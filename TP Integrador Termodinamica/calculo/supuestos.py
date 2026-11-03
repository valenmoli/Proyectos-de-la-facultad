"""Datos de entrada y supuestos del modelo.

Cada parametro lleva: id, valor, unidad, estado y fuente o justificacion.

Estados:
  DATO       valor leido de un documento recibido (ver datos/).
  SUPUESTO   valor fundamentado pero SIN fuente citable todavia. Se reemplaza por el dato
             citable cuando exista y su efecto se mide en el analisis de sensibilidad.
  CONSTANTE  convencion, propiedad fisica o parametro de calculo.

Este archivo es la unica fuente de los supuestos: la tabla del informe se genera desde aca.
"""
import copy

# --------------------------------------------------------------------------------------
# Parametros escalares: (id, clave, nombre, valor, unidad, estado, fuente)
# --------------------------------------------------------------------------------------
_FILAS = [
    # Edificio
    ("E1", "A_cub", "Superficie cubierta total", 18352.0, "m2", "DATO",
     "Presidencia de la Nacion, presentacion del Hospital Favaloro (datos/favaloro_nordelta.md, FA-03). Otra cifra: mas de 20.000 m2 (FA-04)"),
    ("E2", "f_acond", "Fraccion de la superficie cubierta que se climatiza", 0.85, "-", "SUPUESTO",
     "Circulaciones, locales tecnicos, morgue y depositos no se climatizan; valor tipico de edificio hospitalario"),
    ("E3", "camas_gen", "Camas de internacion general", 144, "camas", "DATO",
     "Gobierno de la Provincia de Buenos Aires, 28/07/2020 (FA-06). Se interpreta como parte del total del hospital"),
    ("E4", "camas_uti", "Camas de terapia intensiva", 14, "camas", "DATO", "Idem (FA-06)"),
    ("E5", "n_or", "Cantidad de quirofanos", 6, "quirofanos", "DATO", "Presentacion de Presidencia (FA-07), cifra de programa"),
    ("E6", "a_or", "Superficie por quirofano", 42.0, "m2", "SUPUESTO", "Quirofano general de 6 a 7 m de lado"),
    ("E7", "a_uti_cama", "Superficie por cama de terapia intensiva", 24.0, "m2/cama", "SUPUESTO", "Box de UTI con circulacion y apoyo"),
    ("E8", "a_gen_cama", "Superficie por cama de internacion general", 28.0, "m2/cama", "SUPUESTO", "Habitacion con bano y local de apoyo"),
    ("E9", "h_techo", "Altura libre de los locales", 3.0, "m", "SUPUESTO", "Convencion de diseno"),
    ("E10", "UA_m2", "Conductancia de la envolvente por m2 de piso expuesto", 0.6, "W/(m2 K)", "SUPUESTO",
     "Edificio de tres pisos con 25 % de vidrio: techo, muros y vidrios en conjunto"),
    ("E11", "q_sol_pico", "Ganancia solar en el punto de diseno de verano", 20.0, "W/m2", "SUPUESTO", "Hora pico, zonas expuestas"),
    ("E12", "q_sol_dia", "Ganancia solar media de las 12 h diurnas (anual)", 8.0, "W/m2", "SUPUESTO", "Promedio diurno anual; es 0 de noche"),
    ("E13", "rho_aire", "Densidad del aire para convertir caudales", 1.2, "kg/m3", "CONSTANTE", "Aire a unos 20 C"),
    ("E14", "f_g4_24h", "Fraccion de las areas generales climatizadas que funciona las 24 h (guardia, diagnostico por imagenes, laboratorio)", 0.35, "-", "SUPUESTO",
     "La gacetilla provincial dice que la guardia atiende las 24 h (datos/favaloro_nordelta.md, FA-09); el resto (consultorios, administracion, docencia) funciona de dia"),
    # Clima (AMBA)
    ("C1", "T_bs_ver", "Temperatura de bulbo seco de diseno, verano", 34.0, "C", "SUPUESTO",
     "Conocimiento general sobre Buenos Aires; reemplazar por dato del SMN o ASHRAE"),
    ("C2", "T_bh_ver", "Temperatura de bulbo humedo coincidente, verano", 25.0, "C", "SUPUESTO", "Idem"),
    ("C3", "T_inv", "Temperatura de bulbo seco de diseno, invierno", 2.0, "C", "SUPUESTO", "Idem"),
    ("C4", "HR_inv", "Humedad relativa de diseno, invierno", 0.80, "-", "SUPUESTO", "Idem"),
    ("C5", "presion", "Presion atmosferica", 101325.0, "Pa", "CONSTANTE", "Nivel del mar (Buenos Aires esta a unos 25 m: diferencia de 0,3 %)"),
    ("C6", "rango_diario", "Amplitud diaria de temperatura (maxima menos minima)", 9.0, "K", "SUPUESTO", "Aproximado; se usa para partir cada mes en mitad diurna y nocturna"),
    # Aire humedo / unidades de tratamiento de aire
    ("A1", "T_sup_min", "Temperatura minima del aire de impulsion", 13.0, "C", "CONSTANTE", "Limite de confort y de condensacion en difusores"),
    ("A2", "T_sup_max", "Temperatura maxima del aire de impulsion", 35.0, "C", "CONSTANTE", "Limite de calefaccion por aire"),
    ("A3", "HR_serp", "Humedad relativa del aire a la salida de la serpentina", 0.95, "-", "CONSTANTE", "Serpentina de agua helada con aproximacion al saturado"),
    ("A4", "T_cambio_estacion", "Temperatura exterior bajo la cual rigen las consignas de invierno", 18.0, "C", "SUPUESTO", "Criterio de cambio de estacion"),
    ("A5", "eta_vent", "Rendimiento total de los ventiladores", 0.60, "-", "SUPUESTO", "Ventilador, motor y transmision"),
    ("A6", "T_agua_red", "Temperatura del agua de red (para el vapor de humidificacion)", 15.0, "C", "SUPUESTO", "Aproximado"),
    ("A7", "h_fg", "Calor latente de vaporizacion del agua (referencia de 0 C)", 2501.0, "kJ/kg", "CONSTANTE", "Propiedades del agua"),
    # Refrigeracion
    ("R1", "refrigerante", "Refrigerante de la enfriadora", "R134a", "-", "SUPUESTO", "Enfriadora de tornillo; HFC habitual, propiedades en CoolProp"),
    ("R2", "T_ev", "Temperatura de evaporacion", 3.0, "C", "SUPUESTO", "Agua helada 7/12 C con aproximacion del evaporador"),
    ("R3", "sobrecal", "Sobrecalentamiento a la salida del evaporador", 5.0, "K", "SUPUESTO", "Valor tipico"),
    ("R4", "subenf", "Subenfriamiento a la salida del condensador", 4.0, "K", "SUPUESTO", "Valor tipico"),
    ("R5", "eta_is", "Rendimiento isentropico del compresor", 0.72, "-", "SUPUESTO", "Compresor de tornillo"),
    ("R6", "eta_motor", "Rendimiento del motor electrico del compresor", 0.94, "-", "SUPUESTO", "Valor tipico"),
    ("R7", "dT_cond", "Diferencia entre la temperatura de condensacion y la exterior", 12.0, "K", "SUPUESTO", "Condensador enfriado por aire"),
    ("R8", "T_cond_min", "Temperatura minima de condensacion", 32.0, "C", "SUPUESTO", "Control de presion de descarga: el compresor de tornillo necesita una diferencia de presion minima"),
    ("R9", "f_vent_cond", "Potencia de ventiladores del condensador / calor rechazado", 0.025, "-", "SUPUESTO", "Valor tipico"),
    ("R10", "dT_aguahelada", "Salto de temperatura del agua helada", 5.0, "K", "SUPUESTO", "Agua helada 7/12 C"),
    ("R11", "dP_bomba", "Altura de las bombas de agua helada", 250000.0, "Pa", "SUPUESTO", "Circuito primario y secundario en conjunto"),
    ("R12", "eta_bomba", "Rendimiento total de las bombas", 0.60, "-", "SUPUESTO", "Valor tipico"),
    # Combustion y caldera
    ("B1", "gas_CH4", "Gas natural: metano", 0.91, "fraccion molar", "SUPUESTO", "Composicion tipica; verificar con ENARGAS"),
    ("B2", "gas_C2H6", "Gas natural: etano", 0.05, "fraccion molar", "SUPUESTO", "Idem"),
    ("B3", "gas_C3H8", "Gas natural: propano", 0.01, "fraccion molar", "SUPUESTO", "Idem"),
    ("B4", "gas_N2", "Gas natural: nitrogeno", 0.02, "fraccion molar", "SUPUESTO", "Idem"),
    ("B5", "gas_CO2", "Gas natural: dioxido de carbono", 0.01, "fraccion molar", "SUPUESTO", "Idem"),
    ("B6", "lambda_aire", "Relacion de aire (1 = estequiometrico)", 1.15, "-", "SUPUESTO", "15 % de exceso de aire"),
    ("B7", "T_gases", "Temperatura de los gases de escape", 190.0, "C", "SUPUESTO", "Caldera sin condensacion"),
    ("B8", "T_aire_comb", "Temperatura del aire y del gas de combustion", 15.0, "C", "SUPUESTO", "Sala de calderas"),
    ("B9", "f_rad", "Perdidas por radiacion y funcionamiento / calor liberado", 0.02, "-", "SUPUESTO", "Valor tipico"),
    ("B10", "T_ref_gas", "Temperatura de referencia del volumen de gas", 15.0, "C", "CONSTANTE", "m3 estandar a 15 C y 101,325 kPa"),
    # Agua caliente sanitaria
    ("S1", "L_cama_dia", "Consumo de ACS por cama y dia", 100.0, "L/(cama dia)", "SUPUESTO",
     "Entre los casos medidos (50 a 55) y los ratios de diseno (200 a 300) del articulo de Hospitecnia (E-14)"),
    ("S2", "T_acs", "Temperatura del ACS", 60.0, "C", "DATO", "Hospitecnia, ref. (7): 55 L/dia y cama a 60 C"),
    ("S3", "T_agua_fria", "Temperatura del agua fria de entrada", 17.0, "C", "SUPUESTO", "Media anual aproximada de Buenos Aires"),
    ("S4", "f_perd_acs", "Factor por perdidas de acumulacion y recirculacion", 1.30, "-", "SUPUESTO",
     "El articulo muestra 1,6 veces entre su tabla y el calor sensible (datos/hospitecnia_datos.md, seccion E)"),
]

# --------------------------------------------------------------------------------------
# Clima mensual aproximado (valores de conocimiento general, a reemplazar por el SMN)
# --------------------------------------------------------------------------------------
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
DIAS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
T_MEDIA = [24.9, 23.7, 22.0, 18.3, 14.6, 11.6, 10.9, 12.3, 14.2, 17.6, 20.6, 23.4]       # C
HR_MEDIA = [0.66, 0.70, 0.73, 0.75, 0.78, 0.79, 0.77, 0.73, 0.71, 0.70, 0.67, 0.65]      # -

# --------------------------------------------------------------------------------------
# Zonas termicas. Cada una se trata como un sistema de aire de caudal constante con
# serpentina de enfriamiento, recalentamiento, calefaccion y humidificacion.
# ach_tot: renovaciones totales (minimas); ach_oa: renovaciones de aire exterior (minimas)
# q_s, q_l: ganancias internas sensible y latente a plena actividad [W/m2]
# f_dia, f_noche: fraccion de actividad en la mitad diurna / nocturna
# f_env: fraccion de la envolvente expuesta (0 = interior)
# opera_noche: si el sistema funciona tambien en la mitad nocturna
# --------------------------------------------------------------------------------------
_ZONAS = {
    "G1": dict(nombre="Quirofanos", ach_tot=20, ach_oa=4, q_s=60.0, q_l=10.0, f_dia=0.8, f_noche=0.0,
               t_ver=22.0, hr_ver=0.55, t_inv=22.0, hr_min=0.30, f_env=0.0, dp_vent=1400.0, opera_noche=True),
    "G2": dict(nombre="Terapia intensiva", ach_tot=6, ach_oa=2, q_s=40.0, q_l=8.0, f_dia=1.0, f_noche=1.0,
               t_ver=23.0, hr_ver=0.55, t_inv=23.0, hr_min=0.30, f_env=0.5, dp_vent=1000.0, opera_noche=True),
    "G3": dict(nombre="Internacion general", ach_tot=4, ach_oa=2, q_s=25.0, q_l=5.0, f_dia=0.9, f_noche=0.7,
               t_ver=24.0, hr_ver=0.55, t_inv=22.0, hr_min=0.30, f_env=1.0, dp_vent=900.0, opera_noche=True),
    "G4": dict(nombre="Guardia, diagnostico por imagenes y laboratorio (24 h)", ach_tot=6, ach_oa=2, q_s=35.0, q_l=8.0, f_dia=0.9, f_noche=0.5,
               t_ver=24.0, hr_ver=0.60, t_inv=22.0, hr_min=0.30, f_env=1.0, dp_vent=1000.0, opera_noche=True),
    "G5": dict(nombre="Consultorios, administracion y docencia (de dia)", ach_tot=3, ach_oa=1, q_s=25.0, q_l=6.0, f_dia=0.9, f_noche=0.0,
               t_ver=24.0, hr_ver=0.60, t_inv=22.0, hr_min=0.30, f_env=1.0, dp_vent=900.0, opera_noche=False),
}
_ZONAS_FUENTE = {
    "G1": "Condiciones y renovaciones de quirofano segun ASHRAE 170 (valores recordados, a verificar); HR de consigna 55 % = maximo 60 % menos 5 puntos de margen; ganancias y horarios: supuesto",
    "G2": "Renovaciones de terapia intensiva segun ASHRAE 170 (valores recordados, a verificar); ganancias: supuesto",
    "G3": "Habitacion de internacion segun ASHRAE 170 (valores recordados, a verificar); ganancias: supuesto",
    "G4": "Funciona las 24 h (la guardia atiende las 24 h segun la gacetilla provincial); renovaciones y ganancias: supuesto; HR de consigna 60 % (limite de confort)",
    "G5": "Funcionan 12 h por dia (de dia); renovaciones y ganancias: supuesto; HR de consigna 60 % (limite de confort)",
}


def defaults():
    """Devuelve una copia editable de la configuracion: {'P': escalares, 'Z': zonas, 'clima': {...}}."""
    P = {k: v for (_i, k, _n, v, _u, _e, _f) in _FILAS}
    return copy.deepcopy({
        "P": P,
        "Z": _ZONAS,
        "clima": {"T": T_MEDIA, "HR": HR_MEDIA, "dias": DIAS, "meses": MESES},
    })


def filas():
    return list(_FILAS)


def tabla_md():
    """Tabla Markdown de supuestos para el informe."""
    out = ["| ID | Parametro | Valor | Unidad | Estado | Fuente o justificacion |", "|---|---|---|---|---|---|"]
    for (i, _k, n, v, u, e, f) in _FILAS:
        vs = f"{v:,.2f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)
        out.append(f"| {i} | {n} | {vs} | {u} | {e} | {f} |")
    out += ["", "**Zonas termicas** (cada una es un sistema de aire de caudal constante):", "",
            "| Zona | Nombre | ACH total | ACH aire ext. | q sens. | q lat. | f dia | f noche | T ver | HR ver | T inv | HR min inv | f env | dP vent. | Opera de noche | Fuente |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, z in _ZONAS.items():
        out.append(
            f"| {k} | {z['nombre']} | {z['ach_tot']} | {z['ach_oa']} | {z['q_s']:g} W/m2 | {z['q_l']:g} W/m2 | {z['f_dia']:g} | {z['f_noche']:g} | "
            f"{z['t_ver']:g} C | {z['hr_ver']*100:g} % | {z['t_inv']:g} C | {z['hr_min']*100:g} % | {z['f_env']:g} | {z['dp_vent']:g} Pa | "
            f"{'si' if z['opera_noche'] else 'no'} | {_ZONAS_FUENTE[k]} |")
    out += ["", "**Clima mensual aproximado** (SUPUESTO, conocimiento general; reemplazar por datos del SMN):", "",
            "| Mes | " + " | ".join(MESES) + " |", "|---|" + "---|" * 12,
            "| T media [C] | " + " | ".join(f"{t:g}" for t in T_MEDIA) + " |",
            "| HR media [%] | " + " | ".join(f"{h*100:g}" for h in HR_MEDIA) + " |"]
    return "\n".join(out)
