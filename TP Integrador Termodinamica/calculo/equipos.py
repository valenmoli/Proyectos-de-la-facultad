"""Equipos y ubicacion en el edificio: ejemplo de maquinas que cumplen lo calculado y donde ponerlas.

Pedido de la docente: "poner un ejemplo de una maquina que cumpla lo que calculamos y proponer donde
ponerla, como ingenieros civiles; un plano simplificado de las zonas y m2 y ubicar las maquinas".

Este modulo NO cambia el modelo termico: toma de el las cargas de diseno (Q_L, caldera de invierno, ACS,
caudales de aire por zona) y de ahi dimensiona y ubica los equipos:

  1. niveles       superficie de cada zona por nivel (3 niveles de igual superficie bruta)
  2. enfriadoras   configuracion 3 en servicio + 1 de reserva con un ejemplo de catalogo (FUENTE SECUNDARIA) y su margen
  3. calderas      carga de diseno, 2 x 100 % y alternativa de condensacion en cascada 3+1
  4. utas          cantidad, caudal y nivel de cada unidad de tratamiento de aire
  5. hidraulica    agua helada (caudal y diametro DN), gas y chimenea
  6. shafts        areas de los shafts verticales de aire
  7. azotea        huella y carga de las enfriadoras sobre la losa
  8. matriz        decision enfriadoras en azotea o en patio tecnico a nivel
  9. planta_tipo   geometria (en metros) de la planta tipo: zonas, nucleo tecnico, UTAs criticas y accesos

Todo numero que no sale del modelo esta en SUPUESTOS con su estado (DATO / SUPUESTO / FUENTE SECUNDARIA /
RECORDADO / CONSTANTE) para volcarlo a una tabla (tabla_supuestos_md()).

Uso (desde la carpeta del proyecto):  python -m calculo.equipos
"""
import math

from . import aire_humedo as ah
from . import combustion as cb
from . import edificio as ed
from . import estimacion as es
from . import refrigeracion as rf

# --------------------------------------------------------------------------------------
# Supuestos nuevos: (id, clave, nombre, valor, unidad, estado, justificacion)
#
# Estados:
#   DATO               valor leido de un documento recibido (datos/)
#   SUPUESTO           decision de diseno o valor fundamentado sin fuente citable
#   FUENTE SECUNDARIA  resultado de una busqueda web sobre catalogos; NO se pudo abrir el catalogo
#   RECORDADO          valor de memoria del autor, a verificar
#   CONSTANTE          convencion, propiedad fisica o serie normalizada
# --------------------------------------------------------------------------------------
_FILAS = [
    # Edificio y niveles
    ("Q1", "n_niveles", "Cantidad de niveles del edificio", 3, "niveles", "SUPUESTO",
     "datos/favaloro_nordelta.md FA-08 (DATO) lista tres pisos y no menciona planta baja; se toma un edificio de tres niveles"),
    ("Q2", "niveles_iguales", "Superficie bruta de cada nivel", "iguales (A_cub / n)", "-", "SUPUESTO",
     "Sin planos: cada nivel recibe la misma superficie bruta (6.117 m2) y la misma superficie climatizada (5.200 m2)"),
    ("Q3", "nivel_calle", "El 1.er nivel esta a nivel de calle", "1.er nivel", "-", "SUPUESTO",
     "Como FA-08 no menciona planta baja, el 1.er piso se toma a nivel de calle; el anexo de calderas se apoya en ese nivel"),
    ("Q4", "aspecto_planta", "Relacion largo/ancho de la planta rectangular equivalente (solo para la figura)", 4.0 / 3.0, "-", "SUPUESTO",
     "Esquema de la planta de cubierta con la misma superficie que un nivel; no hay planos del edificio real"),
    ("Q5", "orientacion", "Orientacion de las plantas dibujadas", "norte arriba", "-", "SUPUESTO",
     "Sin plano de implantación: se dibuja el norte hacia arriba solo para ubicar el dibujo. El modelo térmico no distingue orientaciones (una sola radiación pico para toda la envolvente)"),
    ("Q6", "calle", "Lado de la calle (frente y accesos)", "sur", "-", "SUPUESTO",
     "Sin plano de implantación: la calle se supone al sur. Del lado de la calle van los accesos, el núcleo técnico, el anexo de calderas y el izaje de las enfriadoras"),
    ("Q7", "nucleo_planta", "Ubicacion del nucleo tecnico en planta", "esquina sudeste, mismo lugar en cada nivel", "-", "SUPUESTO",
     "Los locales técnicos, la morgue y los depósitos de cada nivel (superficie no climatizada: 918 m2) se agrupan en un bloque en el borde sur, del lado de la calle, para acortar el "
     "recorrido del agua helada desde las enfriadoras de la azotea y de los conductos de las zonas críticas; los shafts se apilan en él. Sus dimensiones salen de la superficie y de "
     "la columna este (Q8). La morgue y los depósitos no tienen m2 propios: están dentro de esos 918 m2"),
    ("Q8", "distribucion_planta", "Distribucion de las zonas dentro de la planta tipo", "franjas; ver planta_tipo()", "-", "SUPUESTO",
     "Zonas como rectángulos de superficie exactamente proporcional a sus m2, por franjas. 2.º piso: columna este con núcleo, G1 y G2 contiguos al núcleo (conducto corto desde las UTAs "
     "del cuarto técnico) y administración; internación G3 en dos alas (sur y norte) de igual superficie. 1.er piso: franja sur con consultorios (ingreso) y núcleo, y G4 en L con el acceso de guardia "
     "en el sudoeste. Sin planos del edificio real"),
    ("Q9", "circulacion", "Circulacion (pasillos y halls)", "dentro de la superficie climatizada de cada zona", "-", "SUPUESTO",
     "No se le asigna superficie propia ni queda un hueco en el dibujo: las áreas de zona del modelo ya la incluyen"),
    # Enfriadoras
    ("Q10", "n_serv", "Enfriadoras en servicio", 3, "unidades", "SUPUESTO",
     "N = 3 de una configuración N+1. Con la 30XA 1002 (988 kW) dos en servicio dan 1.976 kW y no alcanzan los 1.987 kW de diseño (faltan 11,2 kW, 0,6 %); con tres cada una trabaja al 67 % "
     "de su capacidad nominal en el diseño. Queda sobredimensionada respecto del pico: la opción más ajustada es 2+1 con una unidad de al menos 994 kW, y la 30XA 1102 no está verificada"),
    ("Q11", "n_res", "Enfriadoras de reserva", 1, "unidades", "SUPUESTO",
     "1 de reserva, 4 unidades iguales. Con una parada quedan 3 x 988 = 2.964 kW para 1.987 kW de diseño (margen +49 %). El margen cubre el calor de las bombas de agua helada "
     "(que la carga de diseño no incluye) y la diferencia entre los 34 °C de diseño y los 35 °C del catálogo"),
    ("Q12", "modelo_enf", "Enfriadora de ejemplo", "Carrier AquaForce 30XA 1002", "-", "FUENTE SECUNDARIA",
     "Dato de catalogo conocido por un extracto. Enfriadora de tornillo condensada por aire"),
    ("Q13", "cap_enf", "Capacidad nominal de la enfriadora de ejemplo", 988.0, "kW", "FUENTE SECUNDARIA",
     "Idem Q12. Con aire exterior a 35 C y agua helada 12/7 C"),
    ("Q14", "pot_enf", "Potencia absorbida por los compresores de la enfriadora de ejemplo", 288.2, "kW", "FUENTE SECUNDARIA",
     "Idem Q12, mismas condiciones nominales. Solo compresores"),
    ("Q15", "T_aire_cat", "Temperatura del aire exterior de la capacidad de catalogo", 35.0, "C", "FUENTE SECUNDARIA", "Idem Q12"),
    ("Q16", "T_agua_cat", "Agua helada de catalogo (entrada / salida del evaporador)", "12 / 7", "C", "FUENTE SECUNDARIA",
     "Idem Q12; salto de 5 K, igual al del modelo (R10)"),
    ("Q17", "cap_fam_min", "Capacidad minima de la familia 30XA", 267.0, "kW", "FUENTE SECUNDARIA", "Idem Q12"),
    ("Q18", "cap_fam_max", "Capacidad maxima de la familia 30XA", 1682.0, "kW", "FUENTE SECUNDARIA", "Idem Q12"),
    ("Q19", "refrig_cat", "Refrigerante de la enfriadora de ejemplo", "R-134a", "-", "FUENTE SECUNDARIA", "Idem Q12; coincide con el del modelo (R1)"),
    ("Q20", "margen_diseno", "Margen de diseno sobre la carga pico (solo informativo)", 0.10, "-", "SUPUESTO",
     "Practica habitual de seleccion; el modelo da la carga pico sin margen. No cambia la seleccion base"),
    ("Q21", "huella_L", "Largo de la huella en azotea por enfriadora", 14.0, "m", "SUPUESTO",
     "Sin dimensiones del catalogo; se interpreta como el area reservada por unidad, con espacios de servicio"),
    ("Q22", "huella_W", "Ancho de la huella en azotea por enfriadora", 3.5, "m", "SUPUESTO", "Idem Q21"),
    ("Q23", "peso_op_t", "Peso operativo por enfriadora", 12.0, "t", "SUPUESTO",
     "A confirmar con el catalogo (peso operativo incluye el agua del evaporador y el refrigerante)"),
    ("Q24", "q_ref_cubierta", "Sobrecarga de referencia de una azotea de uso corriente", 2.0, "kN/m2", "SUPUESTO",
     "Solo orden de magnitud para comparar. RECORDADO: los reglamentos de cargas dan entre 1 y 5 kN/m2 segun el acceso a la azotea (CIRSOC 101, verificar)"),
    ("Q25", "g", "Aceleracion de la gravedad", 9.81, "m/s2", "CONSTANTE", "Para pasar toneladas a kN"),
    # Calderas
    ("Q30", "f_punta_acs", "Factor de simultaneidad: punta de ACS / ACS media", 2.0, "-", "SUPUESTO",
     "El modelo da solo el ACS medio (43 kW); el pico no se calcula. Se suma al punto de diseno de invierno (coincidencia conservadora)"),
    ("Q31", "cald_n_serv", "Calderas de agua caliente en servicio (pirotubulares a gas, 100 % cada una)", 1, "unidades", "SUPUESTO", "Configuracion 2 x 100 %"),
    ("Q32", "cald_n_res", "Calderas de agua caliente de reserva", 1, "unidades", "SUPUESTO", "Configuracion 2 x 100 % (N+1), sin marca"),
    ("Q33", "cap_cond", "Capacidad maxima por unidad de la caldera de condensacion de ejemplo (Viessmann Vitocrossal 300 CM3C)", 311.0, "kW", "FUENTE SECUNDARIA",
     "Dato de catalogo conocido por un extracto"),
    ("Q34", "cap_cond_min", "Capacidad minima por unidad de la caldera de ejemplo", 87.0, "kW", "FUENTE SECUNDARIA", "Idem Q33; las unidades se pueden poner en cascada"),
    ("Q35", "eta_cond_PCS", "Rendimiento maximo de la caldera de condensacion", 0.98, "-", "FUENTE SECUNDARIA",
     "Idem Q33; sobre PCS y con retorno frio (maximo, no valor de operacion)"),
    ("Q36", "cond_n_res", "Unidades de reserva de la cascada de condensacion", 1, "unidades", "SUPUESTO", "Configuracion 3+1: 3 en servicio y 1 de reserva"),
    ("Q37", "v_chimenea", "Velocidad de los gases en la chimenea", 8.0, "m/s", "SUPUESTO", "Quemador con ventilador (tiraje forzado); predimensionamiento"),
    # UTAs
    ("Q40", "V_max_uta", "Caudal maximo por UTA (zonas no criticas)", 25000.0, "m3/h", "SUPUESTO", "Criterio de predimensionamiento"),
    ("Q41", "uta_por_or", "UTAs por quirofano (con filtro HEPA)", 1, "unidades", "SUPUESTO", "Una UTA por quirofano; cada quirofano es una zona independiente"),
    ("Q42", "uta_uti", "UTAs de terapia intensiva (con filtro HEPA)", 1, "unidades", "SUPUESTO", "Una UTA para la unidad"),
    # Hidraulica y conductos
    ("Q50", "v_agua", "Velocidad maxima del agua helada en la canieria principal", 2.0, "m/s", "SUPUESTO", "Predimensionamiento"),
    ("Q51", "serie_DN", "Serie de diametros nominales disponibles", (150, 200, 250, 300, 350), "mm", "CONSTANTE", "Serie nominal DN"),
    ("Q52", "id_igual_dn", "Diametro interior de la canieria = DN", "ID = DN", "-", "SUPUESTO",
     "Aproximacion; en tubo de acero el interior real de DN 250 o mayor es algo mayor, asi que la velocidad real es algo menor"),
    ("Q53", "rho_agua", "Densidad del agua helada", 1000.0, "kg/m3", "CONSTANTE", "Agua a 7 a 12 C"),
    ("Q54", "v_imp", "Velocidad del aire de impulsion en los shafts", 6.0, "m/s", "SUPUESTO", "Predimensionamiento"),
    ("Q55", "v_ret", "Velocidad del aire de retorno en los shafts", 5.0, "m/s", "SUPUESTO", "Predimensionamiento"),
    ("Q56", "exfiltracion", "Caudal de exfiltracion", 0.0, "m3/h", "SUPUESTO",
     "Retorno = impulsion - aire exterior - exfiltracion; con exfiltracion nula todo el aire exterior sale por la extraccion"),
    ("Q57", "area_shaft", "Area de un shaft tipo", 2.0, "m2", "SUPUESTO",
     "Orden de magnitud para contar shafts; es area neta de conducto: el shaft real ocupa mas (aislacion, compuertas cortafuego, acceso)"),
    # Ubicacion
    ("Q60", "matriz", "Pesos y puntajes de la matriz de decision azotea / patio a nivel", "ver MATRIZ_UBICACION", "-", "SUPUESTO",
     "Juicio de ingenieria, sin ensayo ni calculo de ruido; el resultado se muestra con su sensibilidad a los pesos"),
]

SUPUESTOS = {
    k: dict(id=i, nombre=n, valor=v, unidad=u, estado=e, justificacion=j)
    for (i, k, n, v, u, e, j) in _FILAS
}

ESTADOS = ("DATO", "SUPUESTO", "FUENTE SECUNDARIA", "RECORDADO", "CONSTANTE")


def parametros():
    """Valores de los supuestos {clave: valor} (copia editable)."""
    return {k: v["valor"] for k, v in SUPUESTOS.items()}


def coma(x, nd=0):
    """Formato argentino: separador de miles con punto y decimal con coma."""
    s = f"{x:,.{nd}f}"
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def _techo(x, tol=1e-9):
    return int(math.ceil(x - tol))


def tabla_supuestos_md():
    """Tabla Markdown de los supuestos de este modulo (para volcar al informe)."""
    out = ["| ID | Parametro | Valor | Unidad | Estado | Justificacion |", "|---|---|---|---|---|---|"]
    for k, s in SUPUESTOS.items():
        v = s["valor"]
        if isinstance(v, float):
            vs = f"{v:.6g}".replace(".", ",")
        elif isinstance(v, tuple):
            vs = ", ".join(str(x) for x in v)
        else:
            vs = str(v)
        out.append(f"| {s['id']} | {s['nombre']} | {vs} | {s['unidad']} | {s['estado']} | {s['justificacion']} |")
    return "\n".join(out)


# --------------------------------------------------------------------------------------
# 1. Niveles
# --------------------------------------------------------------------------------------
NOMBRES_ZONA = {
    "G1": "Quirófanos",
    "G2": "Terapia intensiva",
    "G3": "Internación general",
    "G4": "Guardia, diagnóstico y laboratorio",
    "G5": "Consultorios, administración y docencia",
}
NOMBRES_NIVEL = {1: "1.er piso", 2: "2.º piso", 3: "3.er piso"}


def niveles(c, p=None):
    """Superficie de cada zona en cada nivel.

    Tres niveles de igual superficie bruta A_cub/3 y de igual superficie climatizada A_cond/3.
      2.º piso  G1 + G2 + G3 y el resto de G5 hasta completar la superficie climatizada del nivel
      1.er piso G4 y G5 hasta completar la superficie climatizada del nivel
      3.er piso lo que queda de G5
    La superficie no climatizada de cada nivel (locales tecnicos, morgue, depositos) es bruta - climatizada.
    """
    p = p or parametros()
    P = c["P"]
    A, a_cond = ed.superficies(c)
    n = int(p["n_niveles"])
    if n != 3:
        raise NotImplementedError("La asignacion de zonas esta definida para 3 niveles")
    bruta = P["A_cub"] / n
    cap = a_cond / n
    criticas = A["G1"] + A["G2"] + A["G3"]
    if criticas > cap + 1e-9:
        raise ValueError("G1 + G2 + G3 no entran en un nivel climatizado")
    if A["G4"] > cap + 1e-9:
        raise ValueError("G4 no entra en un nivel climatizado")
    pool = A["G5"]
    g5_n2 = min(pool, cap - criticas)
    pool -= g5_n2
    g5_n1 = min(pool, cap - A["G4"])
    pool -= g5_n1
    g5_n3 = pool
    if g5_n3 > cap + 1e-6:
        raise ValueError("G5 no entra en los tres niveles")

    def nivel(num, zonas):
        zonas = [(g, a, t) for (g, a, t) in zonas if a > 1e-9]
        clim = sum(a for _g, a, _t in zonas)
        return dict(nivel=num, nombre=NOMBRES_NIVEL[num], zonas=zonas, clim=clim, bruta=bruta, no_clim=bruta - clim)

    niv = [
        nivel(1, [("G4", A["G4"], "Guardia, diagnóstico y laboratorio"), ("G5", g5_n1, "Consultorios")]),
        nivel(2, [("G1", A["G1"], "Quirófanos"), ("G2", A["G2"], "Terapia intensiva"), ("G3", A["G3"], "Internación general"),
                  ("G5", g5_n2, "Administración")]),
        nivel(3, [("G5", g5_n3, "Administración y docencia")]),
    ]
    por_zona = {g: {} for g in A}
    for nv in niv:
        for g, a, _t in nv["zonas"]:
            por_zona[g][nv["nivel"]] = a
    return dict(niveles=niv, bruta_nivel=bruta, clim_nivel=cap, A_cub=P["A_cub"], A_cond=a_cond, A_zona=A,
                por_zona=por_zona, no_clim_total=sum(nv["no_clim"] for nv in niv))


# --------------------------------------------------------------------------------------
# 2. Enfriadoras
# --------------------------------------------------------------------------------------
def enfriadoras(c, p=None, d=None):
    """Configuracion N+1 de enfriadoras iguales (por defecto 3 en servicio + 1 de reserva) y comparacion con la enfriadora de ejemplo.

    cap_servicio es la capacidad de las unidades en servicio (N x cap); cap_una_parada es la que queda si cualquiera de las
    n_total unidades esta parada. Con n_res = 1 las dos coinciden.
    """
    p = p or parametros()
    d = d or es.diseno(c)
    P = c["P"]
    Q_L = d["Q_L"]
    W_bomba = d["planta"]["W_bomba"]
    n_serv, n_res = int(p["n_serv"]), int(p["n_res"])
    n_tot = n_serv + n_res
    cap_u, pot_u = p["cap_enf"], p["pot_enf"]
    req_u = Q_L / n_serv                                  # capacidad minima por unidad en servicio
    cap_serv = n_serv * cap_u
    cap_parada = (n_tot - 1) * cap_u                      # con una unidad cualquiera parada
    margen = cap_serv - Q_L
    cumple = cap_serv >= Q_L
    faltante = max(0.0, Q_L - cap_serv)
    req_u_margen = Q_L * (1.0 + p["margen_diseno"]) / n_serv
    # Menor cantidad de unidades en servicio con esta misma unidad
    n_serv_min = _techo(Q_L / cap_u)
    # Alternativa mas ajustada: 2 en servicio + 1 de reserva (tres unidades)
    n2 = 2
    cap_2 = n2 * cap_u
    alt_2mas1 = dict(n_serv=n2, n_res=1, n_total=n2 + 1, cap_servicio=cap_2, margen_kW=cap_2 - Q_L, faltante_kW=max(0.0, Q_L - cap_2),
                     faltante_rel=max(0.0, Q_L - cap_2) / Q_L, cumple=cap_2 >= Q_L, req_unidad=Q_L / n2, req_unidad_redondeada=_techo(Q_L / n2),
                     req_unidad_con_margen=Q_L * (1.0 + p["margen_diseno"]) / n2)
    # Con n_serv unidades en servicio, mas la reserva funcionando a carga parcial
    carga_rel = (Q_L / n_serv) / cap_u
    if cumple:
        salida = (
            f"Con {n_serv} unidades en servicio + {n_res} de reserva ({n_tot} iguales) la 30XA 1002 da {coma(cap_serv)} kW con una unidad parada, contra "
            f"{coma(Q_L, 1)} kW de carga de diseño (margen +{coma(margen, 1)} kW, +{coma(margen / Q_L * 100)} %): cumple, con cada unidad en servicio al "
            f"{coma(carga_rel * 100)} % de su capacidad nominal. Queda sobredimensionada respecto del pico: el margen cubre el calor de las bombas de agua helada "
            f"(hasta {coma(W_bomba, 1)} kW, no incluido en la carga) y la diferencia entre los {coma(P['T_bs_ver'])} °C de diseño y los {coma(p['T_aire_cat'])} °C del catálogo. "
            f"Alternativas: (1) {alt_2mas1['n_serv']} en servicio + 1 de reserva con la misma unidad da {coma(alt_2mas1['cap_servicio'])} kW de {coma(Q_L, 1)} kW: "
            f"faltan {coma(alt_2mas1['faltante_kW'], 1)} kW ({coma(alt_2mas1['faltante_rel'] * 100, 1)} %) y no cumple. (2) La opción más ajustada es 2+1 con una unidad de "
            f"al menos {coma(alt_2mas1['req_unidad_redondeada'])} kW ({coma(alt_2mas1['req_unidad'], 1)} kW sin margen; {coma(alt_2mas1['req_unidad_con_margen'])} kW si se quiere "
            f"{coma(p['margen_diseno'] * 100)} % de margen): sería el tamaño siguiente de la familia, 30XA 1102, cuya capacidad no está verificada acá. (3) Pedir la capacidad de la "
            f"30XA 1002 a {coma(P['T_bs_ver'])} °C, la temperatura de diseño del modelo: sería algo mayor que a {coma(p['T_aire_cat'])} °C y podría acercar la 2+1, pero no hay cifra verificada."
        )
    else:
        salida = (
            f"Con {n_serv} unidades en servicio la 30XA 1002 cubre {coma(cap_serv)} kW de {coma(Q_L, 1)} kW "
            f"(faltan {coma(faltante, 1)} kW, {coma(faltante / Q_L * 100, 1)} %). Salidas: (1) pasar a {n_serv_min} unidades en servicio + {n_res} de reserva con esta misma unidad. "
            f"(2) Elegir un tamaño mayor de la familia (30XA 1102, no verificada) con al menos {coma(req_u, 1)} kW por unidad ({coma(req_u_margen)} kW si se quiere "
            f"{coma(p['margen_diseno'] * 100)} % de margen). (3) Pedir la capacidad de la 30XA 1002 a {coma(P['T_bs_ver'])} °C, la temperatura de diseño del modelo: "
            f"sería algo mayor que a {coma(p['T_aire_cat'])} °C, pero no hay cifra verificada."
        )
    return dict(
        Q_L=Q_L, n_serv=n_serv, n_res=n_res, n_total=n_tot, modelo=p["modelo_enf"],
        cap_unidad=cap_u, pot_unidad=pot_u, cap_servicio=cap_serv, req_unidad=req_u,
        req_unidad_con_margen=req_u_margen, margen_kW=margen, margen_rel=margen / Q_L, cumple=cumple,
        faltante_kW=faltante, n_serv_minimo_con_esta_unidad=n_serv_min, req_unidad_3_en_servicio=Q_L / 3.0,
        cap_una_parada=cap_parada, margen_una_parada_kW=cap_parada - Q_L, margen_una_parada_rel=(cap_parada - Q_L) / Q_L,
        cumple_con_una_parada=cap_parada >= Q_L,
        carga_por_unidad_kW=Q_L / n_serv, carga_relativa_unidad=carga_rel, carga_relativa_todas=Q_L / (n_tot * cap_u),
        alt_2mas1=alt_2mas1,
        m_w_unidad=cap_u / (ah.CP_W * P["dT_aguahelada"]), salida=salida,
        calor_bombas_max_kW=W_bomba, cubre_con_bombas=cap_parada >= Q_L + W_bomba, margen_con_bombas_kW=cap_parada - (Q_L + W_bomba),
        nota_bombas=(f"Q_L es la suma de las serpentinas: no incluye el calor de las bombas de agua helada, que el modelo cuenta solo como "
                     f"electricidad ({coma(W_bomba, 1)} kW). Si se disipara todo en el agua, la carga de las enfriadoras subiria hasta "
                     f"{coma(Q_L + W_bomba, 1)} kW."),
    )


def comparacion_cop(c, p=None, d=None):
    """COP del catalogo (solo compresores, 35 C) contra el COP electrico del modelo (34 C)."""
    p = p or parametros()
    d = d or es.diseno(c)
    P = c["P"]
    cop_cat = p["cap_enf"] / p["pot_enf"]
    cop_mod = d["planta"]["COP"]
    T_cond_mod = d["planta"]["T_cond"]
    cop_mod_35, T_cond_35, _ = rf.cop_vs_exterior(p["T_aire_cat"], c)
    dif = cop_mod / cop_cat - 1.0
    dif_35 = cop_mod_35 / cop_cat - 1.0
    frac = (cop_mod - cop_mod_35) / (cop_mod - cop_cat)          # parte de la diferencia que explica 1 K de aire exterior
    texto = (
        f"COP de catálogo (compresores solos, 35 °C de aire): {coma(cop_cat, 2)}. COP del modelo (compresor solo, 34 °C de aire exterior, "
        f"condensación a {coma(T_cond_mod)} °C): {coma(cop_mod, 2)}, {coma(dif * 100, 1)} % por encima. Al mismo aire de 35 °C "
        f"(condensación a {coma(T_cond_35)} °C) el modelo da {coma(cop_mod_35, 2)}, {coma(dif_35 * 100, 1)} % respecto del catálogo: "
        f"el {coma(frac * 100)} % de la diferencia viene de comparar 34 °C con 35 °C. Esa coincidencia a 35 °C no valida el modelo: "
        f"η_is = {coma(P['eta_is'], 2)} y η_motor = {coma(P['eta_motor'], 2)} son supuestos, el catálogo incluye pérdidas de aceite, "
        f"economizador y variador que el modelo no tiene, y la pendiente del COP con la temperatura de la máquina real no está verificada. "
        f"Ninguno de los dos COP incluye ventiladores del condensador ni bombas."
    )
    return dict(cop_catalogo=cop_cat, cop_modelo_34=cop_mod, T_cond_modelo_34=T_cond_mod, cop_modelo_35=cop_mod_35,
                T_cond_modelo_35=T_cond_35, dif_rel_34=dif, dif_rel_35=dif_35, fraccion_por_temperatura=frac,
                W_comp_modelo_a_cap_cat=p["cap_enf"] / cop_mod, texto=texto)


# --------------------------------------------------------------------------------------
# 3. Calderas
# --------------------------------------------------------------------------------------
R_UNIV = cb.R_UNIV   # kJ/(kmol K)


def calderas(c, p=None, d=None):
    """Carga de diseno de la planta de calor y dos configuraciones: 2 x 100 % y cascada de condensacion 3+1."""
    p = p or parametros()
    d = d or es.diseno(c)
    P = c["P"]
    Q_inv = d["Q_caldera_invierno"]
    Q_vapor = sum(v["Q_hum"] for v in d["invierno"].values())
    Q_acs_media = d["acs"]["kW"]
    Q_acs_punta = p["f_punta_acs"] * Q_acs_media
    Q_dis = Q_inv + Q_acs_punta
    cal = d["caldera"]
    eta, pc = cal["eta_PCI"], cal["pc"]

    # Opcion A: 2 x 100 %
    n_a = int(p["cald_n_serv"]) + int(p["cald_n_res"])
    # Opcion B: cascada de unidades de condensacion
    cap = p["cap_cond"]
    n_b_serv = _techo(Q_dis / cap)
    n_b_res = int(p["cond_n_res"])
    n_b = n_b_serv + n_b_res
    cap_b_una_parada = (n_b - 1) * cap
    # Si fueran solo 3 unidades en total (una parada = 2 en servicio)
    cap_3_una_parada = 2 * cap

    # Gas y gases de combustion con la caldera del modelo a plena carga de diseno (una sola en servicio)
    E_pci = Q_dis / eta                                                   # kW de combustible (PCI)
    V_gas_m3h = E_pci / pc["PCI_kWh_m3"]                                  # m3 estandar por hora
    n_fuel = E_pci / pc["PCI_kJ_kmol"]                                    # kmol/s de gas natural
    n_gases = n_fuel * cal["balance"]["n_productos"]                      # kmol/s de gases de escape
    V_gases = n_gases * R_UNIV * (P["T_gases"] + 273.15) / 101.325        # m3/s a T_gases
    A_chim = V_gases / p["v_chimenea"]
    D_chim = math.sqrt(4.0 * A_chim / math.pi)
    DN_chim = _dn_para(D_chim, p["serie_DN"])

    # Potencial de la condensacion (cota superior)
    eta_pcs_modelo = cal["eta_PCS"]
    ahorro_max = 1.0 - eta_pcs_modelo / p["eta_cond_PCS"]
    return dict(
        Q_invierno=Q_inv, Q_vapor=Q_vapor, Q_agua_caliente_sin_vapor=Q_inv - Q_vapor,
        Q_acs_media=Q_acs_media, Q_acs_punta=Q_acs_punta, Q_diseno=Q_dis,
        opcion_a=dict(n=n_a, cap_unidad=Q_dis, cap_con_una_parada=Q_dis, tipo="pirotubular de agua caliente a gas, 100 % cada una"),
        opcion_b=dict(n_servicio=n_b_serv, n_reserva=n_b_res, n=n_b, cap_unidad=cap, cap_instalada=n_b * cap,
                      cap_una_parada=cap_b_una_parada, cumple_con_una_parada=cap_b_una_parada >= Q_dis,
                      carga_relativa_servicio=Q_dis / (n_b_serv * cap), cap_3_unidades_una_parada=cap_3_una_parada,
                      cumple_con_3_unidades=cap_3_una_parada >= Q_dis, minima_unidad=p["cap_cond_min"]),
        eta_PCI_modelo=eta, eta_PCS_modelo=eta_pcs_modelo, T_rocio_gases=cal["T_rocio"],
        ahorro_gas_max=ahorro_max, E_comb_PCI_kW=E_pci, V_gas_m3h=V_gas_m3h, V_gases_m3s=V_gases, V_gases_m3h=V_gases * 3600.0,
        A_chimenea=A_chim, D_chimenea=D_chim, DN_chimenea=DN_chim,
    )


# --------------------------------------------------------------------------------------
# 4. UTAs
# --------------------------------------------------------------------------------------
def utas(c, p=None, d=None, niv=None):
    """Lista de UTAs con caudal, nivel de instalacion y niveles que atienden."""
    p = p or parametros()
    d = d or es.diseno(c)
    niv = niv or niveles(c, p)
    P = c["P"]
    caud = d["caudales"]
    lista, resumen = [], {}
    for g in c["Z"]:
        V = caud[g]["V_sup_m3h"]
        niveles_zona = sorted(niv["por_zona"][g])
        if g == "G1":
            n = int(P["n_or"]) * int(p["uta_por_or"])
            critica, hepa = True, True
        elif g == "G2":
            n = int(p["uta_uti"])
            critica, hepa = True, True
        else:
            n = _techo(V / p["V_max_uta"])
            critica, hepa = False, False
        if critica:
            if len(niveles_zona) != 1:
                raise ValueError(f"{g} es critica y debe estar en un solo nivel")
            ubic = f"cuarto técnico del {NOMBRES_NIVEL[niveles_zona[0]]}"
            nivel_uta = niveles_zona[0]
        else:
            ubic = "cubierta"
            nivel_uta = "cubierta"
        for i in range(n):
            lista.append(dict(id=f"UTA-{g}-{i + 1}", zona=g, caudal_m3h=V / n, ubicacion=ubic, nivel=nivel_uta,
                              sirve=niveles_zona, hepa=hepa, critica=critica))
        resumen[g] = dict(n=n, V_total=V, caudal_unidad=V / n, ubicacion=ubic, nivel=nivel_uta, critica=critica, hepa=hepa,
                          sirve=niveles_zona, cumple_criterio=(critica or V / n <= p["V_max_uta"] + 1e-9))
    return dict(lista=lista, por_zona=resumen, n_total=len(lista), n_cubierta=sum(1 for u in lista if u["nivel"] == "cubierta"),
                n_criticas=sum(1 for u in lista if u["critica"]), V_total=sum(r["V_total"] for r in resumen.values()))


# --------------------------------------------------------------------------------------
# 5. Hidraulica del agua helada
# --------------------------------------------------------------------------------------
def _dn_para(D_calc_m, serie):
    for dn in sorted(serie):
        if dn / 1000.0 >= D_calc_m - 1e-12:
            return dn
    raise ValueError(f"Ningun DN de la serie {tuple(serie)} alcanza para {D_calc_m * 1000:.0f} mm")


def _tramo(m_w, p):
    V = m_w / p["rho_agua"]                                          # m3/s
    D_calc = math.sqrt(4.0 * V / (math.pi * p["v_agua"]))
    dn = _dn_para(D_calc, p["serie_DN"])
    v_real = 4.0 * V / (math.pi * (dn / 1000.0) ** 2)
    return dict(m_w=m_w, V_m3h=V * 3600.0, V_Ls=V * 1000.0, D_calc_mm=D_calc * 1000.0, DN=dn, v_real=v_real)


def hidraulica(c, p=None, d=None):
    """Caudal de agua helada y diametro de la canieria principal y de cada ramal de enfriadora."""
    p = p or parametros()
    d = d or es.diseno(c)
    P = c["P"]
    Q_L = d["Q_L"]
    m_w = Q_L / (ah.CP_W * P["dT_aguahelada"])
    principal = _tramo(m_w, p)
    ramal = _tramo(m_w / int(p["n_serv"]), p)                       # caudal de diseno repartido entre las unidades en servicio
    ramal_nominal = _tramo(p["cap_enf"] / (ah.CP_W * P["dT_aguahelada"]), p)   # si una unidad trabajara a su capacidad nominal
    return dict(Q_L=Q_L, dT=P["dT_aguahelada"], m_w=m_w, principal=principal, ramal_enfriadora=ramal,
                ramal_a_capacidad_nominal=ramal_nominal)


# --------------------------------------------------------------------------------------
# 6. Shafts verticales de aire
# --------------------------------------------------------------------------------------
def shafts(c, p=None, d=None, u=None):
    """Areas de los shafts verticales de aire.

    Impulsion V_sup a v_imp; retorno = V_sup - V_aire_exterior - exfiltracion a v_ret.
    Zonas con UTA en cubierta: el shaft vertical lleva la impulsion y el retorno completos.
    Zonas criticas con UTA en el cuarto tecnico del mismo nivel: la impulsion y el retorno van en conductos
    horizontales; el shaft vertical solo lleva el aire exterior (a v_imp) y la extraccion (a v_ret, igual al
    aire exterior con exfiltracion nula) hasta la cubierta.
    """
    p = p or parametros()
    d = d or es.diseno(c)
    u = u or utas(c, p, d)
    rho = c["P"]["rho_aire"]
    por_zona = {}
    for g in c["Z"]:
        cd = d["caudales"][g]
        V_sup = cd["V_sup_m3h"]
        V_oa = cd["m_oa"] / rho * 3600.0
        V_ret = V_sup - V_oa - p["exfiltracion"]
        A_imp = V_sup / 3600.0 / p["v_imp"]
        A_ret = V_ret / 3600.0 / p["v_ret"]
        critica = u["por_zona"][g]["critica"]
        if critica:
            A_vert = V_oa / 3600.0 / p["v_imp"] + (V_oa + p["exfiltracion"]) / 3600.0 / p["v_ret"]
            modo = "UTA en el nivel: el shaft lleva aire exterior y extracción"
        else:
            A_vert = A_imp + A_ret
            modo = "UTA en cubierta: el shaft lleva impulsión y retorno"
        por_zona[g] = dict(V_sup=V_sup, V_oa=V_oa, V_ret=V_ret, A_imp=A_imp, A_ret=A_ret, A_total=A_imp + A_ret,
                           A_vertical=A_vert, modo=modo, critica=critica, n_shafts=_techo(A_vert / p["area_shaft"]))
    A_vert_tot = sum(z["A_vertical"] for z in por_zona.values())
    # G1 y G2 comparten el shaft de aire exterior y extraccion (0,5 m2 en total)
    grupos = {
        "G1+G2": por_zona["G1"]["A_vertical"] + por_zona["G2"]["A_vertical"],
        "G3": por_zona["G3"]["A_vertical"], "G4": por_zona["G4"]["A_vertical"], "G5": por_zona["G5"]["A_vertical"],
    }
    n_grupos = {k: _techo(a / p["area_shaft"]) for k, a in grupos.items()}
    return dict(
        por_zona=por_zona,
        A_imp_total=sum(z["A_imp"] for z in por_zona.values()),
        A_ret_total=sum(z["A_ret"] for z in por_zona.values()),
        A_total=sum(z["A_total"] for z in por_zona.values()),
        A_vertical_total=A_vert_tot,
        n_shafts_por_area=_techo(A_vert_tot / p["area_shaft"]),
        A_grupos=grupos, n_shafts_por_grupo=n_grupos, n_shafts_agrupados=sum(n_grupos.values()),
    )


# --------------------------------------------------------------------------------------
# 7. Azotea: huella y carga
# --------------------------------------------------------------------------------------
def azotea(c, p=None):
    """Huella y carga de las enfriadoras (todas las unidades, incluida la de reserva) sobre la losa de cubierta."""
    p = p or parametros()
    n = int(p["n_serv"]) + int(p["n_res"])
    A_unidad = p["huella_L"] * p["huella_W"]
    peso_kN = p["peso_op_t"] * p["g"]                       # t * m/s2 = kN
    q = peso_kN / A_unidad
    A_cub_nivel = c["P"]["A_cub"] / p["n_niveles"]
    return dict(n_unidades=n, A_unidad=A_unidad, A_total=n * A_unidad, peso_unidad_kN=peso_kN, peso_total_kN=n * peso_kN,
                q_kN_m2=q, q_ref=p["q_ref_cubierta"], q_sobre_ref=q / p["q_ref_cubierta"], supera_ref=q > p["q_ref_cubierta"],
                A_cubierta=A_cub_nivel, fraccion_cubierta=n * A_unidad / A_cub_nivel)


# --------------------------------------------------------------------------------------
# 8. Matriz de decision: enfriadoras en azotea o en patio tecnico a nivel
# --------------------------------------------------------------------------------------
# (clave, criterio, peso, puntaje azotea, puntaje patio, justificacion). Puntajes 1 (malo) a 5 (bueno).
MATRIZ_UBICACION = [
    ("aire", "Aire libre para el condensador", 0.20, 5, 2,
     "En azotea el aire circula sin obstáculos. Un patio técnico rodeado por el edificio recircula el aire caliente de descarga"),
    ("ruido", "Ruido hacia internación y terapia intensiva", 0.20, 3, 2,
     "En azotea el ruido queda arriba del 3.er piso (administración y docencia), separado de la internación por una losa. En el patio a nivel el equipo queda frente a ventanas del 1.er y 2.º piso"),
    ("estructura", "Carga estructural", 0.15, 2, 5,
     "La azotea exige losa y vigas para equipos (ver la carga en kN/m²). A nivel el suelo la absorbe sin problema"),
    ("izaje", "Izaje y montaje", 0.15, 2, 4,
     "Cuatro unidades de 14 m y 12 t a unos 15 m de altura: grúa móvil grande y corte de calle. A nivel basta una grúa menor para descargar del camión"),
    ("canerias", "Recorrido de cañerías hacia las UTAs", 0.15, 4, 2,
     "11 de las 18 UTAs están en cubierta: las cañerías horizontales son cortas. Desde un patio a nivel habría que subir todo el agua helada por el núcleo técnico"),
    ("mantenimiento", "Acceso para mantenimiento", 0.15, 3, 4,
     "Azotea: acceso por escalera o montacargas, protección contra caídas, sin camión. Patio: acceso directo, reemplazo de componentes más fácil"),
]
UBICACIONES = ("azotea", "patio a nivel")


def matriz_ubicacion(matriz=None):
    """Puntaje ponderado de cada ubicacion, con dos variantes de pesos para ver la sensibilidad."""
    matriz = matriz or MATRIZ_UBICACION

    def total(pesos):
        s = sum(pesos)
        a = sum(w * f[3] for w, f in zip(pesos, matriz)) / s
        b = sum(w * f[4] for w, f in zip(pesos, matriz)) / s
        return dict(azotea=a, patio=b, ganador="azotea" if a > b + 1e-12 else ("patio a nivel" if b > a + 1e-12 else "empate"))

    base = [f[2] for f in matriz]
    iguales = [1.0] * len(matriz)
    estruct = [w * (2.0 if f[0] in ("estructura", "izaje") else 1.0) for w, f in zip(base, matriz)]
    return dict(base=total(base), pesos_iguales=total(iguales), estructura_e_izaje_x2=total(estruct),
                suma_pesos=sum(base), ganador=total(base)["ganador"])


# --------------------------------------------------------------------------------------
# Texto de ubicacion (criterios civiles), para el informe
# --------------------------------------------------------------------------------------
UBICACION = {
    "enfriadoras": "Azotea, sobre el nucleo tecnico vertical (junto al borde de cubierta del lado de la calle): el agua helada baja por los shafts "
                   "del nucleo y las UTAs de cubierta quedan a corta distancia. Plataforma estructural con vigas bajo los apoyos y aislacion de vibraciones. "
                   "Barrera acustica hacia el lado de las habitaciones.",
    "calderas": "Anexo a nivel de calle, con acceso desde la calle: medidor y regulador de gas en el limite del predio, ventilacion permanente de la sala "
                "(aire de combustion y renovacion), techo liviano o paneles de alivio, deteccion de gas, chimenea por fuera del edificio hasta superar la "
                "cubierta (altura segun la norma de ENARGAS, no calculada).",
    "gas": "Acometida desde la calle al medidor y regulador del anexo; la canieria de gas no entra al edificio principal. El diametro lo define el "
           "proyectista matriculado con la presion de red; aca solo se da el caudal de diseno.",
    "izaje": "Grua movil desde la calle hasta la cubierta, del lado de las enfriadoras; se planifica el montaje antes de cerrar la losa y el parapeto. "
             "Las UTAs de cubierta se izan por la misma zona.",
}


# --------------------------------------------------------------------------------------
# 9. Planta tipo: geometria en metros (para la figura 11 y para comprobar que las areas cierran)
# --------------------------------------------------------------------------------------
def _area_rects(rects):
    return sum((x1 - x0) * (y1 - y0) for (x0, y0, x1, y1) in rects)


def planta_tipo(c, p=None, niv=None, sh=None, ut=None):
    """Planta tipo del 1.er y del 2.º piso como rectangulos de superficie exactamente proporcional a los m2 del modelo.

    Rectangulo equivalente de relacion largo/ancho Q4 con la superficie bruta de un nivel (x hacia el este, y hacia el norte, origen en la
    esquina sudoeste; la calle esta al sur, Q5 y Q6). Se arma por franjas, con cortes que dependen solo de las superficies:
      columna este (ancho wE)   2.º piso: nucleo tecnico (sur) + G1 y G2 contiguos al nucleo + G5 administracion (norte)
                                1.er piso: el mismo nucleo, con los consultorios G5 pegados a su oeste
      resto (oeste)             2.º piso: G3 internacion en dos alas (sur y norte) de igual superficie
                                1.er piso: G4 en L (franja norte completa + pie en el sudoeste, con el acceso de guardia)
    El nucleo tecnico (superficie no climatizada de cada nivel: locales tecnicos, morgue y depositos) ocupa el mismo lugar en los dos pisos.
    Cada bloque es {id, zona, nombre, rects: [(x0, y0, x1, y1)], area_modelo, area_dibujada}.
    """
    p = p or parametros()
    niv = niv or niveles(c, p)
    sh = sh or shafts(c, p)
    ut = ut or utas(c, p, None, niv)
    A = niv["bruta_nivel"]
    Wm = math.sqrt(A * p["aspecto_planta"])
    Hm = A / Wm
    por = {nv["nivel"]: {g: a for g, a, _t in nv["zonas"]} for nv in niv["niveles"]}
    n1, n2 = por[1], por[2]
    if set(n1) != {"G4", "G5"} or set(n2) != {"G1", "G2", "G3", "G5"}:
        raise NotImplementedError("La planta tipo esta definida para la asignacion de zonas por defecto")
    a_nc = niv["niveles"][0]["no_clim"]
    wE = (a_nc + n2["G1"] + n2["G2"] + n2["G5"]) / Hm            # ancho de la columna este
    dc = a_nc / wE                                                # profundidad del nucleo
    xE = Wm - wE
    nucleo_r = (xE, 0.0, Wm, dc)

    def bloque(id_, zona, nombre, rects, area_modelo):
        return dict(id=id_, zona=zona, nombre=nombre, rects=rects, area_modelo=area_modelo, area_dibujada=_area_rects(rects))

    nucleo = bloque("NUCLEO", None, "Núcleo técnico", [nucleo_r], a_nc)

    # 1.er piso
    w5 = n1["G5"] / dc
    pie = xE - w5                                                 # ancho del pie de G4 en el sudoeste
    if dc >= Hm or pie < -1e-9:
        raise ValueError("Las superficies no entran en la planta tipo del 1.er piso")
    g4_rects = [(0.0, dc, Wm, Hm)] + ([(0.0, 0.0, pie, dc)] if pie > 1e-9 else [])
    bl1 = [bloque("G4", "G4", "Guardia, diagnóstico y laboratorio", g4_rects, n1["G4"]),
           bloque("G5", "G5", "Consultorios", [(pie, 0.0, xE, dc)], n1["G5"]), dict(nucleo)]
    nivel1 = dict(nivel=1, nombre=NOMBRES_NIVEL[1], bloques=bl1, ingreso_x=pie + w5 / 2.0, acceso_guardia_x=pie / 2.0, ancho_pie_g4=pie)

    # 2.º piso
    dcr = (n2["G1"] + n2["G2"]) / wE                              # profundidad del bloque critico
    w1 = n2["G1"] / dcr
    y_g5 = dc + dcr
    if y_g5 >= Hm:
        raise ValueError("Las superficies no entran en la planta tipo del 2.º piso")
    bl2 = [bloque("G1", "G1", "Quirófanos", [(xE, dc, xE + w1, y_g5)], n2["G1"]),
           bloque("G2", "G2", "Terapia intensiva", [(xE + w1, dc, Wm, y_g5)], n2["G2"]),
           bloque("G3-sur", "G3", "Internación, ala sur", [(0.0, 0.0, xE, Hm / 2.0)], n2["G3"] / 2.0),
           bloque("G3-norte", "G3", "Internación, ala norte", [(0.0, Hm / 2.0, xE, Hm)], n2["G3"] / 2.0),
           bloque("G5", "G5", "Administración", [(xE, y_g5, Wm, Hm)], n2["G5"]), dict(nucleo)]
    nivel2 = dict(nivel=2, nombre=NOMBRES_NIVEL[2], bloques=bl2,
                  utas_criticas=dict(G1=ut["por_zona"]["G1"]["n"], G2=ut["por_zona"]["G2"]["n"]), x_g1_g2=xE + w1)

    nuc = dict(x0=xE, y0=0.0, x1=Wm, y1=dc, ancho=wE, prof=dc, area=a_nc, n_shafts=sh["n_shafts_agrupados"],
               area_shaft=p["area_shaft"], area_shafts=sh["n_shafts_agrupados"] * p["area_shaft"],
               area_vertical_neta=sh["A_vertical_total"])
    return dict(W=Wm, H=Hm, A_nivel=A, aspecto=p["aspecto_planta"], wE=wE, dc=dc, xE=xE, nucleo=nuc, niveles={1: nivel1, 2: nivel2},
                nota_3er_piso="El 3.er piso es todo G5 (administración y docencia) sobre el mismo núcleo técnico.")


# --------------------------------------------------------------------------------------
# Resumen
# --------------------------------------------------------------------------------------
def resumen_equipos(c, p=None):
    p = p or parametros()
    d = es.diseno(c)
    niv = niveles(c, p)
    ut = utas(c, p, d, niv)
    sh = shafts(c, p, d, ut)
    return dict(
        p=p, diseno=d, niveles=niv, enfriadoras=enfriadoras(c, p, d), cop=comparacion_cop(c, p, d),
        calderas=calderas(c, p, d), utas=ut, hidraulica=hidraulica(c, p, d), shafts=sh,
        azotea=azotea(c, p), matriz=matriz_ubicacion(), planta=planta_tipo(c, p, niv, sh, ut),
    )


def main():
    from . import supuestos
    c = supuestos.defaults()
    R = resumen_equipos(c)
    niv, enf, cop, cal, ut, hid, sh, az, mx = (R[k] for k in ("niveles", "enfriadoras", "cop", "calderas", "utas", "hidraulica", "shafts", "azotea", "matriz"))
    print(f"Niveles: bruta {coma(niv['bruta_nivel'])} m2, climatizada {coma(niv['clim_nivel'])} m2 por nivel")
    for nv in niv["niveles"]:
        zs = "; ".join(f"{g} {coma(a)} m2" for g, a, _t in nv["zonas"])
        print(f"  {nv['nombre']}: {zs}; no climatizada {coma(nv['no_clim'])} m2")
    print(f"Enfriadoras: Q_L {coma(enf['Q_L'], 1)} kW; {enf['n_serv']}+{enf['n_res']} de {enf['modelo']} "
          f"({coma(enf['cap_unidad'])} kW): servicio {coma(enf['cap_servicio'])} kW, con una parada {coma(enf['cap_una_parada'])} kW, "
          f"margen {coma(enf['margen_kW'], 1)} kW ({coma(enf['margen_rel'] * 100, 1)} %), carga por unidad {coma(enf['carga_relativa_unidad'] * 100, 1)} %")
    if enf["salida"]:
        print("  ", enf["salida"])
    print("  ", cop["texto"])
    print(f"Calderas: diseno {coma(cal['Q_diseno'], 1)} kW (invierno {coma(cal['Q_invierno'], 1)} + ACS punta {coma(cal['Q_acs_punta'], 1)}); "
          f"cascada {cal['opcion_b']['n_servicio']}+{cal['opcion_b']['n_reserva']} de {coma(cal['opcion_b']['cap_unidad'])} kW, "
          f"con una parada {coma(cal['opcion_b']['cap_una_parada'])} kW")
    print(f"UTAs: {ut['n_total']} ({ut['n_cubierta']} en cubierta, {ut['n_criticas']} críticas en cuarto técnico)")
    for g, r in ut["por_zona"].items():
        print(f"  {g}: {r['n']} x {coma(r['caudal_unidad'])} m3/h, {r['ubicacion']}")
    print(f"Agua helada: {coma(hid['m_w'], 1)} kg/s, DN {hid['principal']['DN']} (v = {coma(hid['principal']['v_real'], 2)} m/s); "
          f"ramal por enfriadora DN {hid['ramal_enfriadora']['DN']} (v = {coma(hid['ramal_enfriadora']['v_real'], 2)} m/s)")
    print(f"Shafts: impulsión {coma(sh['A_imp_total'], 1)} m2, retorno {coma(sh['A_ret_total'], 1)} m2; verticales {coma(sh['A_vertical_total'], 1)} m2 "
          f"-> {sh['n_shafts_por_area']} shafts de {coma(R['p']['area_shaft'], 1)} m2")
    print(f"Azotea: {az['n_unidades']} unidades de {coma(az['A_unidad'])} m2 = {coma(az['A_total'])} m2, carga {coma(az['q_kN_m2'], 2)} kN/m2 ({coma(az['q_sobre_ref'], 2)} veces la referencia)")
    print(f"Matriz: azotea {coma(mx['base']['azotea'], 2)} / patio {coma(mx['base']['patio'], 2)} -> {mx['ganador']}")
    pl = R["planta"]
    print(f"Planta tipo: {coma(pl['W'], 1)} x {coma(pl['H'], 1)} m; nucleo {coma(pl['nucleo']['ancho'], 1)} x {coma(pl['nucleo']['prof'], 1)} m, "
          f"{pl['nucleo']['n_shafts']} shafts de {coma(pl['nucleo']['area_shaft'], 1)} m2")


if __name__ == "__main__":
    main()
