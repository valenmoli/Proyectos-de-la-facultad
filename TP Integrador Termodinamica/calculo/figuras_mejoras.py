"""Figuras de las mejoras y de la carta psicrometrica con la zona de confort de Givoni.

Uso (desde la carpeta del proyecto):  python -m calculo.figuras_mejoras
Escribe PNG en ../figuras/: fig09_mejoras.png y fig10_carta_givoni.png
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch, Polygon

from . import aire_humedo as ah
from . import mejoras as mj
from . import supuestos
from .figuras import AQUA, AZUL, GRID, GRIS, INK, INK2, NARANJA, SALIDA, _guardar, coma

# Zona de confort de Givoni (1992) para paises calidos y en desarrollo, segun Lamberts, Dutra y Pereira:
# 18 a 29 C, humedad relativa de 20 a 80 % y humedad especifica de 4 a 17 g/kg (FUENTE SECUNDARIA: herramienta
# de carta bioclimatica que cita ese trabajo, via busqueda web; no se pudo abrir el articulo original)
GIVONI = dict(T_min=18.0, T_max=29.0, HR_min=0.20, HR_max=0.80, W_min=4.0, W_max=17.0)


def zona_givoni(P=101325.0, n=60):
    """Poligono (T, W en g/kg) de la zona de confort: recorta las curvas de 20 y 80 % con los limites de humedad especifica."""
    g = GIVONI
    Ts = np.linspace(g["T_min"], g["T_max"], n)
    inf = [max(ah.w_desde_hr(T, g["HR_min"], P) * 1000, g["W_min"]) for T in Ts]
    sup = [min(ah.w_desde_hr(T, g["HR_max"], P) * 1000, g["W_max"]) for T in Ts]
    return list(zip(Ts, sup)) + list(zip(Ts[::-1], inf[::-1]))


def dentro_givoni(T, W_gkg, P=101325.0):
    g = GIVONI
    hr = ah.hr_desde_w(T, W_gkg / 1000.0, P)
    return g["T_min"] <= T <= g["T_max"] and g["HR_min"] <= hr <= g["HR_max"] and g["W_min"] <= W_gkg <= g["W_max"]


def fig_givoni(c):
    P = c["P"]
    fig, ax = plt.subplots(figsize=(7.2, 4.9))
    Ts = np.linspace(0, 40, 161)
    for rh in (0.2, 0.4, 0.6, 0.8, 1.0):
        W = np.array([ah.w_desde_hr(T, rh, P["presion"]) * 1000 for T in Ts])
        ax.plot(Ts, W, color=GRID if rh < 1 else GRIS, lw=0.9 if rh < 1 else 1.4, zorder=1)
        j = np.where(W <= 23.2)[0][-1]
        ax.text(Ts[j] - 0.3, W[j] + 0.25, f"{int(rh * 100)} %", fontsize=7, color=INK2, ha="right", va="bottom")
    ax.add_patch(Polygon(zona_givoni(P["presion"]), closed=True, fc="#cfeee2", ec=AQUA, lw=1.2, zorder=2, alpha=0.9))
    ax.text(23.5, 5.0, "Zona de confort\n(Givoni)", fontsize=8, color="#0e6e4c", ha="center", va="center", zorder=3)

    # clima mensual (T media y humedad especifica de la media)
    cl = c["clima"]
    pts = [(T, ah.w_desde_hr(T, hr, P["presion"]) * 1000) for T, hr in zip(cl["T"], cl["HR"])]
    pts_c = pts + [pts[0]]
    ax.plot([p[0] for p in pts_c], [p[1] for p in pts_c], color=INK2, lw=1.0, ls=(0, (3, 2)), zorder=4)
    for m, (T, W) in zip(cl["meses"], pts):
        ax.plot(T, W, "o", ms=5, mfc="white", mec=INK2, mew=1.2, zorder=5)
    desp = {"ene": (6, 4), "abr": (-4, -14), "jul": (-8, -14), "oct": (-18, -12)}
    for m, (T, W) in zip(cl["meses"], pts):
        if m in desp:
            ax.annotate(m, (T, W), xytext=desp[m], textcoords="offset points", fontsize=7.5, color=INK2, zorder=6)

    # estado de diseno exterior de verano
    Tv, Wv = P["T_bs_ver"], ah.w_desde_tbh(P["T_bs_ver"], P["T_bh_ver"], P["presion"]) * 1000
    ax.plot(Tv, Wv, "s", ms=7, mfc=NARANJA, mec=INK, mew=1.0, zorder=7)
    ax.annotate(f"Exterior de diseño, verano\n({coma(Tv)} °C; {coma(Wv, 1)} g/kg)", (Tv, Wv), xytext=(-110, 6), textcoords="offset points",
                fontsize=7.5, color=INK, zorder=7)
    # consignas de las zonas
    Z = c["Z"]
    col = {"G1": AZUL, "G2": AZUL, "G3": AZUL, "G4": AZUL, "G5": AZUL}
    etiqueta = {"G1": ("G1", (-20, -3)), "G2": ("G2", (-4, -14)), "G3": ("G3", (7, -4)), "G4": ("G4 y G5", (7, 2))}
    for g, z in Z.items():
        W = ah.w_desde_hr(z["t_ver"], z["hr_ver"], P["presion"]) * 1000
        ax.plot(z["t_ver"], W, "D", ms=6, mfc=col[g], mec="white", mew=0.8, zorder=8)
        if g in etiqueta:
            txt, off = etiqueta[g]
            ax.annotate(txt, (z["t_ver"], W), xytext=off, textcoords="offset points", fontsize=8, fontweight="bold", color=AZUL, zorder=8)
    ax.set_xlim(0, 40)
    ax.set_ylim(0, 24)
    ax.set_xlabel("Temperatura de bulbo seco [°C]")
    ax.set_ylabel("Humedad específica [g de vapor / kg de aire seco]")
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(handles=[Patch(fc="#cfeee2", ec=AQUA, label="Zona de confort de Givoni (18 a 29 °C; 20 a 80 %; 4 a 17 g/kg)"),
                       plt.Line2D([], [], marker="o", ls="--", color=INK2, mfc="white", label="Clima: media de cada mes (supuesto)"),
                       plt.Line2D([], [], marker="D", ls="", color=AZUL, label="Consigna de verano de cada zona")],
              loc="lower right", frameon=False, fontsize=7.5)
    return _guardar(fig, "fig10_carta_givoni.png")


def fig_mejoras(c):
    base, filas = mj.comparar(c)
    filas = [f for f in filas if f["clave"] != "A"]
    paquete = [f for f in filas if f["clave"] == "P"][0]
    sueltas = sorted([f for f in filas if f["clave"] != "P"], key=lambda f: f["d_E"], reverse=True)   # la mayor mejora abajo
    orden = sueltas + [paquete]
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    y = np.arange(len(orden))
    h = 0.36
    for i, f in enumerate(orden):
        ax.barh(i - h / 2, -f["d_E"] * 100, height=h, color=GRIS)
        ax.barh(i + h / 2, -f["d_co2"] * 100, height=h, color=AQUA)
        ax.text(-f["d_E"] * 100 + 0.6, i - h / 2, f"{coma(-f['d_E'] * 100, 1)} %", va="center", fontsize=7.5, color=INK)
        ax.text(-f["d_co2"] * 100 + 0.6, i + h / 2, f"{coma(-f['d_co2'] * 100, 1)} %", va="center", fontsize=7.5, color=INK)
    nombres = {"B": "B. Recuperar el calor\ndel condensador", "M1": "M1. Caldera de condensación", "M2": "M2. Solar térmico para el ACS",
               "M3": "M3. Recuperador del\naire de extracción", "M4": "M4. Ventiladores con 20 %\nmenos de presión", "M5": "M5. Fotovoltaica de 250 kWp",
               "P": "Paquete B + M1 a M5"}
    ax.set_yticks(y)
    ax.set_yticklabels([nombres[f["clave"]] for f in orden], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlim(0, 56)
    ax.set_xlabel("Reducción respecto de la alternativa A [%]")
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend(handles=[Patch(color=GRIS, label="Energía final (electricidad más gas)"), Patch(color=AQUA, label="Emisiones de CO₂")],
              frameon=False, fontsize=8, loc="upper right")
    return _guardar(fig, "fig09_mejoras.png")


def main():
    c = supuestos.defaults()
    for r in (fig_mejoras(c), fig_givoni(c)):
        print("escrita:", os.path.relpath(r, os.path.dirname(SALIDA)))


if __name__ == "__main__":
    main()
