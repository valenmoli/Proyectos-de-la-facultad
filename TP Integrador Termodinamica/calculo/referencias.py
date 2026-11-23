"""Lista unica de referencias del informe y de la memoria.

Las dos entregas citan con el mismo numero [n]. Un asterisco marca las fuentes que solo se
conocen por un extracto de busqueda (no se pudo abrir el original): hay que cotejarlas antes
de entregar. Se usa asi en las plantillas: {{R_ashrae170}} da "[6]*".
"""

# (clave, texto de la referencia, secundaria)
REFERENCIAS = [
    ("presidencia", "Presidencia de la Nación, presentación del Hospital SAMIC «Dr. René Favaloro» (documento recibido).", False),
    ("gacetilla", "Gobierno de la Provincia de Buenos Aires, gacetilla del 28/07/2020 sobre el Hospital Favaloro (documento recibido).", False),
    ("hospitecnia", "Gallostra Isern, Sánchez-Vaqué y Túnica Buira, *Caracterización de consumos energéticos y suministros en hospitales*, Hospitecnia, 2022 (hospitales españoles: sirve para órdenes de magnitud, no como valor de diseño; documento recibido).", False),
    ("hcwh", "HCWH y K-CEP, *Energy efficiency and cooling audits in health care facilities in Argentina, China, and the Philippines*, 2021 (documento recibido).", False),
    ("elcruce", "Medina y Marini, Hospital de Alta Complejidad El Cruce, 2010 (documento recibido).", False),
    ("ashrae170", "ASHRAE Standard 170 (adendo de 2025) y ASHRAE Handbook, capítulo de hospitales: renovaciones, temperaturas y humedades.", True),
    ("fgi", "FGI Guidelines for Design and Construction of Hospitals: quirófano de 400 pie².", True),
    ("res748", "Resolución 748/2014 (Argentina), requisitos de terapia intensiva: 9 m² por cama (emisor y texto no verificados).", True),
    ("givoni", "Givoni (1992), carta bioclimática, según Lamberts, Dutra y Pereira.", True),
    ("smn", "Servicio Meteorológico Nacional, normales 1991-2020 de Buenos Aires (vía una página que reproduce la tabla).", True),
    ("gsa", "Global Solar Atlas: irradiación global horizontal.", True),
    ("cammesa", "CAMMESA, factor de emisión de la red eléctrica (meta 2023), visto en el perfil de DitchCarbon; Climate Transparency vía Carbon Footprint y Ember (0,29 a 0,40 t/MWh).", True),
    ("carrier", "Carrier, enfriadora AquaForce 30XA 1002: catálogo.", True),
    ("viessmann", "Viessmann, caldera de condensación Vitocrossal 300 CM3C: catálogo.", True),
    ("trane", "Trane, recuperación de calor del condensador en un hospital, *Consulting-Specifying Engineer*.", True),
    ("kigali", "Enmienda de Kigali al Protocolo de Montreal (ratificada por Argentina en 2019) y Resolución 104/2020 (licencias de importación de HFC).", True),
    ("coolprop", "CoolProp y psychrolib: propiedades del refrigerante, de los gases y del aire húmedo (código).", False),
]

_NUM = {c: i + 1 for i, (c, _t, _s) in enumerate(REFERENCIAS)}
_SEC = {c: s for c, _t, s in REFERENCIAS}


def marca(clave):
    """'[6]\\*' si la fuente es secundaria, '[6]' si no."""
    return f"[{_NUM[clave]}]" + ("\\*" if _SEC[clave] else "")


def valores_ref():
    """Marcadores {{R_clave}} para las plantillas."""
    return {"R_" + c: marca(c) for c in _NUM}


def lista_referencias():
    lineas = [f"[{_NUM[c]}]{'\\*' if s else ''} {t}" for c, t, s in REFERENCIAS]
    return "\n\n".join(lineas) + ("\n\n\\* Fuente conocida por un extracto (no se accedió al documento completo): el dato citado se tomó de ese extracto.")
