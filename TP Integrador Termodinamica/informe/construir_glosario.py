#!/usr/bin/env python3
"""Genera el glosario de siglas, unidades y símbolos desde una sola fuente.

Salidas:
- informe/glosario_para_informe_entregado.md y .docx: para pegar en el informe del grupo
  (por ejemplo como «Anexo B»), con subíndices reales.
- presentacion/guion_diapositivas_10_a_12.md: reemplaza (o agrega) la sección «## Glosario»,
  con una columna «Cómo decirlo» para la exposición oral.

Cada definición sale de lo que dice el informe entregado (secciones 1.4, 2, 3 y 4, tablas 4 y 10)
o es la definición habitual del término.
"""
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
INFORME = RAIZ / "informe"
GUION = RAIZ / "presentacion" / "guion_diapositivas_10_a_12.md"

# (sigla, significado, cómo decirlo)
SIGLAS = [
    ("A y B", "Alternativas del informe. A es el sistema base; B agrega un condensador de agua que aprovecha el calor que hoy se tira al ambiente (sección 4.1)", "«alternativa A», «alternativa B»"),
    ("ACS", "Agua caliente sanitaria", "«a-ce-ese» o «agua caliente sanitaria»"),
    ("AMBA", "Área Metropolitana de Buenos Aires", "«amba»"),
    ("ASHRAE", "Sociedad estadounidense de ingenieros de calefacción, refrigeración y aire acondicionado. Su norma 170 fija las renovaciones de aire y la humedad de los establecimientos de salud", "«ásh-rei»"),
    ("CO₂", "Dióxido de carbono (emisiones de la combustión del gas y de la generación eléctrica)", "«ce-o-dos» o «dióxido de carbono»"),
    ("COP", "Coeficiente de desempeño: frío (o calor) entregado por cada unidad de energía consumida. El COP eléctrico de la enfriadora usa la electricidad del compresor con su motor", "«cop» o «coeficiente de desempeño»"),
    ("G1 a G5", "Zonas térmicas del hospital: G1 quirófanos, G2 terapia intensiva, G3 internación general, G4 guardia, imágenes y laboratorio, G5 consultorios y administración (tabla 4)", "«zona uno», «el quirófano»"),
    ("HR", "Humedad relativa del aire", "«humedad relativa»"),
    ("I, V1 y V2", "Estados de diseño: I, invierno (1,1 °C); V1, pico de verano (33,9 °C y 12,0 g/kg); V2, verano húmedo (25,9 °C y 16,8 g/kg)", "«el invierno», «el pico de verano», «el día húmedo de verano»"),
    ("M1, M2 y M3", "Medidas de mejora de la sección 4.3: M1 caldera de condensación, M2 recuperador de calor del aire expulsado, M3 bomba de calor. En la estimación anual de la sección 4.5 se nombran por su nombre", "decí el nombre, no el número"),
    ("PCI y PCS", "Poder calorífico inferior y superior del gas natural. El PCS cuenta además el calor latente del vapor de agua de los humos (PCS/PCI = 1,108)", "«poder calorífico inferior» y «superior»"),
    ("R134a", "Refrigerante de la enfriadora (tetrafluoroetano, un HFC)", "«erre ciento treinta y cuatro a»"),
    ("SAMIC", "Servicio de Atención Médica Integral para la Comunidad (tipo de hospital público del Favaloro)", "«samic»"),
]

# (unidad, significado)
UNIDADES = [
    ("kW, kWh y MWh", "Kilowatt (potencia); kilowatt-hora y megawatt-hora (energía; 1 MWh = 1.000 kWh)"),
    ("kWp", "Kilowatt pico: potencia máxima de un panel solar en condiciones normalizadas"),
    ("t y t/MWh", "Toneladas de CO₂; toneladas de CO₂ por MWh de electricidad (0,38 en la sección 4.5, un supuesto)"),
    ("m³/h y kg/h", "Caudal de gas natural o de aire; masa de CO₂ emitida por hora"),
    ("g/kg", "Gramos de vapor de agua por kilo de aire seco (humedad específica ω)"),
    ("°C y K", "Grados Celsius y kelvin (K = °C + 273,15); una diferencia de 1 K equivale a una de 1 °C"),
    ("kPa", "Kilopascal (presión)"),
]

# (símbolo, significado) con subíndices escritos como X_y
SIMBOLOS = [
    ("ω", "Humedad específica del aire (g de vapor por kg de aire seco)"),
    ("h", "Entalpía específica (kJ/kg)"),
    ("T y p", "Temperatura y presión"),
    ("Q_L", "Capacidad frigorífica: calor que la enfriadora saca del agua helada (kW); q_L es el mismo calor por kg de refrigerante"),
    ("Q_cond", "Calor que se cede en el condensador: Q_cond = Q_L + W_eje"),
    ("Q_serp, Q_lat y Q_rec", "Calor de la serpentina de enfriamiento, su parte latente (condensación del vapor) y calor del recalentador"),
    ("W_eje, W_el y W_vent", "Potencia en el eje del compresor, eléctrica del compresor (con su motor) y del ventilador"),
    ("ṁ_a y V̇", "Caudal de masa de aire seco y caudal de volumen"),
    ("η_is, η_mot y η_vent", "Rendimientos isentrópico del compresor, del motor y del ventilador"),
    ("η", "Rendimiento de la caldera: 89,9 % sobre PCI (81,2 % sobre PCS)"),
    ("T_0", "Temperatura del estado muerto, que es el aire exterior de cada estado: la referencia de la exergía"),
    ("X, X_Q y X_dest", "Exergía; exergía del calor, X_Q = Q (1 − T_0/T); exergía destruida, X_dest = T_0 S_gen"),
    ("S_gen", "Entropía generada"),
    ("ψ", "Exergía específica del aire (por kg)"),
]


def tabla(filas, cabecera, anchos=None):
    n = len(cabecera)
    sep = ["---"] * n if not anchos else ["-" * max(3, int(a)) for a in anchos]
    out = ["| " + " | ".join(cabecera) + " |", "|" + "|".join(sep) + "|"]
    for f in filas:
        out.append("| " + " | ".join(f) + " |")
    return "\n".join(out)


def para_guion():
    s = ["## Glosario", "",
         "Siglas, unidades y símbolos que aparecen en las tres diapositivas y en el informe. La última columna de las siglas dice cómo conviene pronunciarlas.", "",
         "**Siglas**", "",
         tabla([list(f) for f in SIGLAS], ["Sigla", "Significado", "Cómo decirlo"]), "",
         "**Unidades**", "",
         tabla([list(f) for f in UNIDADES], ["Unidad", "Significado"]), "",
         "**Símbolos de las fórmulas del informe**", "",
         tabla([list(f) for f in SIMBOLOS], ["Símbolo", "Significado"]), ""]
    return "\n".join(s)


def sub(texto):
    """X_y -> X~y~ (subíndice de pandoc)."""
    return re.sub(r"([A-Za-zηψωṁ̇V])_([A-Za-z0-9]+)", r"\1~\2~", texto)


def para_informe():
    s = ["## Anexo B. Glosario de siglas, unidades y símbolos", "",
         "**Siglas**", "",
         tabla([[a, b] for a, b, _ in SIGLAS], ["Sigla", "Significado"], [18, 82]), "",
         "**Unidades**", "",
         tabla([list(f) for f in UNIDADES], ["Unidad", "Significado"], [18, 82]), "",
         "**Símbolos**", "",
         tabla([[sub(a), sub(b)] for a, b in SIMBOLOS], ["Símbolo", "Significado"], [24, 76]), ""]
    return "\n".join(s)


def main():
    # 1) guion: reemplaza la sección Glosario si existe, o la agrega al final
    t = GUION.read_text(encoding="utf-8")
    nuevo = para_guion()
    if "\n## Glosario" in t:
        t = t[: t.index("\n## Glosario")].rstrip() + "\n\n" + nuevo
    else:
        t = t.rstrip() + "\n\n" + nuevo
    GUION.write_text(t, encoding="utf-8")

    # 2) informe: md + docx (pandoc)
    md = INFORME / "glosario_para_informe_entregado.md"
    md.write_text(para_informe(), encoding="utf-8")
    try:
        subprocess.run(["pandoc", str(md), "-f", "markdown+subscript", "-t", "docx",
                        "-o", str(INFORME / "glosario_para_informe_entregado.docx")], check=True)
    except Exception as e:  # pandoc ausente: queda el md
        print("pandoc no disponible:", e, file=sys.stderr)
    print("glosario generado")


if __name__ == "__main__":
    main()
