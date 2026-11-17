"""Figura 7 del informe: reparto de la exergia de entrada (electricidad + combustible) entre exergia util,
perdidas al ambiente y destruccion por equipo, en los dos estados analizados (diagrama de Grassmann simplificado).

Uso (desde la carpeta del proyecto):  python -m calculo.figuras_exergia
Escribe ../figuras/fig07_exergia.png con el estilo de calculo/figuras.py (azul = electricidad, naranja = gas).
Ninguna cifra se copia a mano: todo sale de calculo/exergia.py.
"""
import os
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from . import exergia as xg
from . import supuestos
from .figuras import AQUA, AZUL, GRID, GRIS, INK, INK2, NARANJA, RAIZ, _guardar, coma

# colores de cada categoria; texto claro u oscuro segun el contraste con el relleno
CAT = [
    ("util", "Exergía útil (aire acondicionado y ACS)", AQUA, INK),
    ("perdidas", "Pérdidas al ambiente", GRIS, INK),
    ("Compresor y motor", "Destrucción: compresor y su motor", AZUL, "white"),
    ("Condensador, válvula y evaporador", "Destrucción: condensador, válvula y evaporador", "#6aa3e8", INK),
    ("Ventiladores y bombas", "Destrucción: ventiladores y bombas", "#b4cff2", INK),
    ("Tratamiento del aire", "Destrucción: mezcla, serpentina y recalentador", INK2, "white"),
    ("Caldera y ACS", "Destrucción: caldera y calentamiento de ACS", NARANJA, INK),
]
UMBRAL_ROTULO = 6.8        # [%] ancho minimo de un segmento para rotularlo por dentro


def _valores(res):
    """Valores [kW] de cada categoria de CAT para un resultado de exergia.analisis."""
    g = res["global"]
    v = {"util": g["P_total"], "perdidas": g["L_total"]}
    v.update(res["destruccion_grupos"])
    return v, g["X_in"]


def fig_exergia(estados=None, c=None):
    """Escribe ../figuras/fig07_exergia.png y devuelve la ruta."""
    if estados is None:
        c = c or supuestos.defaults()
        estados = xg.estados_de_analisis(c)
    claves = ["verano_pico", "max_recalentamiento"]
    datos = []
    for k in claves:
        e = estados[k]
        v, x_in = _valores(e["resultado"])
        datos.append((e, v, x_in))

    fig = plt.figure(figsize=(8.0, 6.9))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 0.95], hspace=0.22)
    ax = fig.add_subplot(gs[0])
    axt = fig.add_subplot(gs[1])

    # ---------------------------------------------------------------- barras apiladas
    ys = {0: (3.95, 3.20), 1: (1.55, 0.80)}              # (barra de entrada, barra de destino) de cada estado
    h_in, h_out = 0.30, 0.56
    for i, (e, v, x_in) in enumerate(datos):
        g = e["resultado"]["global"]
        y_in, y_out = ys[i]
        pe, pg = g["X_elec"] / x_in * 100.0, g["X_comb"] / x_in * 100.0
        ax.barh(y_in, pe, height=h_in, color=AZUL, edgecolor="white", lw=1.2)
        ax.barh(y_in, pg, height=h_in, left=pe, color=NARANJA, edgecolor="white", lw=1.2)
        ax.text(1.0, y_in, f"Electricidad {coma(pe, 1)} %", va="center", ha="left", fontsize=8, color="white")
        ax.text(pe + pg / 2, y_in, "Gas" if pg < 12 else f"Gas natural {coma(pg, 1)} %", va="center", ha="center", fontsize=8,
                color=INK)
        # barra de destino
        izq = 0.0
        for clave, _nom, col, tcol in CAT:
            w = max(v[clave], 0.0) / x_in * 100.0
            ax.barh(y_out, w, height=h_out, left=izq, color=col, edgecolor="white", lw=1.2)
            if w >= UMBRAL_ROTULO:
                ax.text(izq + w / 2, y_out, f"{coma(w, 1)} %", va="center", ha="center", fontsize=8, color=tcol,
                        fontweight="bold")
            izq += w
        # titulo del estado (dos lineas, encima de la barra de entrada)
        est = e["resultado"]["estado"]
        ax.text(0.0, y_in + 0.58, e["nombre"], fontsize=9.5, fontweight="bold", color=INK, ha="left", va="bottom")
        ax.text(0.0, y_in + 0.27,
                f"Estado muerto = estado exterior: {coma(est['T0'], 1)} °C, {coma(est['W0'] * 1000, 1)} g/kg  ·  "
                f"entrada {coma(x_in, 0)} kW ({coma(g['X_elec'], 0)} electricidad + {coma(g['X_comb'], 0)} gas)",
                fontsize=8, color=INK2, ha="left", va="bottom")
    ax.set_xlim(0, 100)
    ax.set_ylim(0.45, 4.95)
    ax.set_yticks([ys[0][0], ys[0][1], ys[1][0], ys[1][1]])
    ax.set_yticklabels(["Entrada", "Destino", "Entrada", "Destino"], fontsize=8)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Porcentaje de la exergía de entrada (electricidad + combustible) [%]")
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)

    # ---------------------------------------------------------------- tabla con los valores
    axt.axis("off")
    axt.set_xlim(0, 1)
    axt.set_ylim(0, 1)
    n = len(CAT) + 2                                       # encabezado + categorias + total de entrada
    fila = 1.0 / n
    cx = {"sw": 0.0, "nom": 0.035, "kw1": 0.60, "pc1": 0.69, "kw2": 0.835, "pc2": 0.925}
    y = 1.0 - fila / 2
    axt.text(cx["nom"], y, "Categoría", fontsize=8.5, fontweight="bold", color=INK, va="center")
    axt.text((cx["kw1"] + cx["pc1"]) / 2, y + 0.03, "Verano pico", fontsize=8.5, fontweight="bold", color=INK, va="center", ha="center")
    axt.text((cx["kw2"] + cx["pc2"]) / 2, y + 0.03, "Máx. recalentamiento", fontsize=8.5, fontweight="bold", color=INK, va="center",
             ha="center")
    axt.text(cx["kw1"], y - 0.045, "kW", fontsize=7.5, color=INK2, ha="right", va="center")
    axt.text(cx["pc1"], y - 0.045, "%", fontsize=7.5, color=INK2, ha="right", va="center")
    axt.text(cx["kw2"], y - 0.045, "kW", fontsize=7.5, color=INK2, ha="right", va="center")
    axt.text(cx["pc2"], y - 0.045, "%", fontsize=7.5, color=INK2, ha="right", va="center")
    axt.plot([0, 1], [1.0 - fila + 0.002] * 2, color=GRID, lw=0.8)
    for j, (clave, nombre, col, _t) in enumerate(CAT):
        y = 1.0 - fila * (j + 1.5)
        axt.add_patch(plt.Rectangle((cx["sw"], y - fila * 0.28), 0.022, fila * 0.56, fc=col, ec="none"))
        axt.text(cx["nom"], y, nombre, fontsize=8, color=INK, va="center")
        for (e, v, x_in), kw, pc in zip(datos, ("kw1", "kw2"), ("pc1", "pc2")):
            val = v[clave]
            axt.text(cx[kw], y, coma(val, 1), fontsize=8, color=INK, ha="right", va="center")
            axt.text(cx[pc], y, coma(val / x_in * 100.0, 1), fontsize=8, color=INK, ha="right", va="center")
    y = 1.0 - fila * (len(CAT) + 1.5)
    axt.plot([0, 1], [y + fila / 2] * 2, color=GRID, lw=0.8)
    axt.text(cx["nom"], y, "Exergía de entrada (electricidad + gas natural)", fontsize=8, fontweight="bold", color=INK, va="center")
    for (e, v, x_in), kw, pc in zip(datos, ("kw1", "kw2"), ("pc1", "pc2")):
        axt.text(cx[kw], y, coma(x_in, 1), fontsize=8, fontweight="bold", color=INK, ha="right", va="center")
        axt.text(cx[pc], y, "100,0", fontsize=8, fontweight="bold", color=INK, ha="right", va="center")

    nota = ("Pérdidas: aire caliente del condensador, condensado, gases de escape y pérdidas del ACS. Exergía útil: aumento neto de "
            "exergía del aire impulsado más el ACS. En el máximo recalentamiento el aire tratado casi no gana exergía: se enfría y se "
            "recalienta en torno al estado muerto. Exergía química del gas natural: valores recordados, a verificar con el libro de la cátedra.")
    axt.text(0.0, -0.02, textwrap.fill(nota, 118), fontsize=7, color=INK2, ha="left", va="top", linespacing=1.4)
    return _guardar(fig, "fig07_exergia.png")


def main():
    ruta = fig_exergia()
    print("escrita:", os.path.relpath(ruta, RAIZ))


if __name__ == "__main__":
    main()
