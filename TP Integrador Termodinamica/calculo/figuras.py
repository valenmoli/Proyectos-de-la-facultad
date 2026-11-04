"""Figuras del informe, generadas desde el modelo (ninguna cifra se copia a mano).

Uso (desde la carpeta del proyecto):  python -m calculo.figuras
Escribe PNG en ../figuras/. Paleta de la guia de visualizacion: azul = electricidad, naranja = gas.
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from CoolProp.CoolProp import PropsSI
from matplotlib.patches import FancyBboxPatch

from . import aire_humedo as ah
from . import edificio as ed
from . import estimacion as es
from . import refrigeracion as rf
from . import supuestos

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "figuras")

INK, INK2, GRID = "#0b0b0b", "#52514e", "#e5e4e0"
AZUL, NARANJA, AQUA, GRIS = "#2a78d6", "#eb6834", "#1baf7a", "#8f8e89"
AZUL_CLARO, NARANJA_CLARO = "#cde2fb", "#fbe0d3"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
    "xtick.color": INK2, "ytick.color": INK2, "text.color": INK, "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.dpi": 200,
})


def coma(x, nd=0):
    s = f"{x:,.{nd}f}"
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def _guardar(fig, nombre):
    os.makedirs(SALIDA, exist_ok=True)
    ruta = os.path.join(SALIDA, nombre)
    fig.savefig(ruta, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    return ruta


# ------------------------------------------------------------------ 1. esquema
def fig_esquema():
    fig, ax = plt.subplots(figsize=(7.4, 4.5))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 5.9)
    ax.axis("off")

    def caja(x, y, w, h, txt, fc, ec=INK2, fs=8):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03,rounding_size=0.08", fc=fc, ec=ec, lw=1.0))
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=fs, color=INK)

    def flecha(p0, p1, color=INK2, lw=1.2):
        ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=0))

    def rotulo(x, y, txt, color=INK2, ha="center", va="center", fs=7.5):
        ax.text(x, y, txt, ha=ha, va=va, fontsize=fs, color=color, linespacing=1.15)

    # cadena de aire
    y0, h = 3.85, 0.9
    cm = y0 + h / 2
    caja(0.10, y0, 1.15, h, "Aire\nexterior", "#f4f3f0")
    caja(1.70, y0, 1.15, h, "Mezcla con\nretorno", "#f4f3f0")
    caja(3.30, y0, 1.30, h, "Serpentina\nagua helada", AZUL_CLARO)
    caja(5.05, y0, 1.15, h, "Recalen-\ntador", NARANJA_CLARO)
    caja(6.65, y0, 1.30, h, "Ventilador", "#f4f3f0")
    caja(8.40, y0, 1.90, h, "Zona\n(quirófano, UTI,\ninternación...)", "#f4f3f0", fs=7.5)
    for a, b in ((1.25, 1.70), (2.85, 3.30), (4.60, 5.05), (6.20, 6.65), (7.95, 8.40)):
        flecha((a, cm), (b, cm))
    # retorno
    xz, xm = 9.35, 2.28
    ax.plot([xz, xz, xm], [y0 + h, 5.45, 5.45], color=INK2, lw=1.2)
    flecha((xm, 5.45), (xm, y0 + h))
    rotulo(5.8, 5.55, "retorno", va="bottom")

    # enfriadora
    caja(2.55, 1.45, 2.5, 1.15, "ENFRIADORA (R134a)\nevaporador · compresor\ncondensador · válvula", AZUL_CLARO, fs=7.5)
    flecha((3.85, y0), (3.85, 2.6), color=AZUL, lw=1.4)
    flecha((4.25, 2.6), (4.25, y0), color=AZUL, lw=1.4)
    rotulo(3.72, 3.22, "agua\nhelada", color=AZUL, ha="right")
    rotulo(4.38, 3.22, "$Q_L$", color=AZUL, ha="left", fs=9)
    flecha((1.15, 2.0), (2.55, 2.0), color=AZUL)
    rotulo(1.85, 2.12, "$W_{comp}$", color=AZUL, va="bottom", fs=8.5)
    rotulo(1.85, 1.88, "(electricidad)", color=AZUL, va="top")
    flecha((3.35, 1.45), (3.35, 0.75), color=AZUL)
    rotulo(3.25, 1.10, "$Q_{cond}$ al ambiente\n(hoy se pierde)", color=AZUL, ha="right")

    # caldera
    caja(5.55, 1.45, 1.65, 1.15, "CALDERA\nde gas natural", NARANJA_CLARO)
    flecha((5.75, 2.6), (5.75, y0), color=NARANJA, lw=1.4)
    rotulo(5.88, 3.22, "$Q_{recal}$", color=NARANJA, ha="left", fs=9)
    flecha((5.95, 0.75), (5.95, 1.45), color=NARANJA)
    rotulo(5.85, 1.10, "gas + aire", color=NARANJA, ha="right")
    flecha((6.85, 1.45), (6.85, 0.75), color=INK2)
    rotulo(6.97, 1.10, "gases de\nescape", ha="left")
    # ACS
    caja(8.00, 1.45, 1.35, 1.15, "ACS\n60 °C", NARANJA_CLARO)
    flecha((7.20, 2.0), (8.00, 2.0), color=NARANJA)
    rotulo(7.60, 2.12, "$Q_{ACS}$", color=NARANJA, va="bottom", fs=8.5)
    rotulo(5.2, 0.28, "Azul: circuito de frío y electricidad.   Naranja: circuito de calor y gas.", fs=7.5)
    return _guardar(fig, "fig01_esquema_sistema.png")


# ------------------------------------------------------------------ 2. carta psicrometrica
def fig_psicrometrica(c, resumen):
    P = c["P"]
    caud = ed.caudales(c)
    Tv, Wv = ed.estado_exterior_verano(c)
    r = ed.proceso(c, "G1", caud, Tv, Wv, 1.0, P["q_sol_pico"])
    z = c["Z"]["G1"]
    W_set = ah.w_desde_hr(r["T_r"], z["hr_ver"], P["presion"])

    x0, x1, y0_, y1 = 8.0, 36.0, 5.0, 19.0
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    Ts = np.linspace(x0, x1, 281)
    for rh in (0.2, 0.4, 0.6, 0.8, 1.0):
        W = np.array([ah.w_desde_hr(T, rh, P["presion"]) * 1000 for T in Ts])
        ax.plot(Ts, W, color=GRID if rh < 1 else GRIS, lw=0.9 if rh < 1 else 1.4, zorder=1)
        dentro = np.where((W <= y1 - 0.5) & (W >= y0_ + 0.3))[0]
        if len(dentro):
            j = dentro[-1]
            ax.text(Ts[j] - 0.2, W[j] + 0.25, f"{int(rh * 100)} %", fontsize=7, color=INK2, ha="right", va="bottom", zorder=2)

    A = (Tv, Wv * 1000)
    B = (r["T_r"], W_set * 1000)
    C = (r["T_mix"], r["W_mix"] * 1000)
    D = (r["T_c"], r["W_c"] * 1000)
    E = (r["T_obj"], r["W_c"] * 1000)
    F = (r["T_sup"], r["W_c"] * 1000)
    ax.plot([A[0], B[0]], [A[1], B[1]], color=GRIS, lw=1.0, ls=(0, (3, 3)), zorder=2)
    ax.annotate("", xy=C, xytext=A, arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.4, shrinkA=4, shrinkB=4))
    ax.annotate("", xy=D, xytext=C, arrowprops=dict(arrowstyle="-|>", color=AZUL, lw=2.0, shrinkA=4, shrinkB=4))
    ax.annotate("", xy=E, xytext=D, arrowprops=dict(arrowstyle="-|>", color=NARANJA, lw=2.0, shrinkA=4, shrinkB=4))
    ax.annotate("", xy=F, xytext=E, arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.4, shrinkA=4, shrinkB=4))
    ax.annotate("", xy=B, xytext=F, arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.2, ls=(0, (2, 2)), shrinkA=4, shrinkB=4))
    pts = (("A", A, (7, 3)), ("B", B, (3, -13)), ("C", C, (6, 4)), ("D", D, (-4, 8)), ("E", E, (-3, 8)), ("F", F, (-3, 8)))
    for nom, (x, y), off in pts:
        ax.plot(x, y, "o", ms=6, mfc="white", mec=INK, mew=1.4, zorder=5)
        ax.annotate(nom, (x, y), xytext=off, textcoords="offset points", fontsize=9, fontweight="bold", color=INK, zorder=6)
    clave = (f"A  aire exterior ({coma(A[0])} °C; {coma(A[1], 1)} g/kg)\n"
             f"B  local, consigna ({coma(B[0])} °C; {coma(B[1], 1)} g/kg)\n"
             f"C  mezcla con retorno ({coma(C[0], 1)} °C; {coma(C[1], 1)} g/kg)\n"
             f"D  salida de la serpentina ({coma(D[0], 1)} °C)\n"
             f"E  tras el recalentador ({coma(E[0], 1)} °C)\n"
             f"F  impulsión, tras el ventilador ({coma(F[0], 1)} °C)")
    ax.text(0.015, 0.985, clave, transform=ax.transAxes, ha="left", va="top", fontsize=7.2, color=INK, linespacing=1.35,
            bbox=dict(boxstyle="round,pad=0.35", fc="white", ec=GRID, alpha=0.95), zorder=7)
    ax.text(0.99, 0.03,
            f"Quirófano, verano pico\nSerpentina: {coma(r['Q_coil'])} kW  (sensible {coma(r['Q_coil_sens'])}, latente {coma(r['Q_coil_lat'])})\n"
            f"Recalentamiento: {coma(r['Q_recal'])} kW",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5, color=INK2,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.9), zorder=7)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0_, y1)
    ax.set_xlabel("Temperatura de bulbo seco [°C]")
    ax.set_ylabel("Humedad específica [g de vapor / kg de aire seco]")
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    return _guardar(fig, "fig02_psicrometrica_quirofano.png")


# ------------------------------------------------------------------ 3. diagrama P-h
def fig_ph(c, resumen):
    P = c["P"]
    T_cond = resumen["diseno"]["planta"]["T_cond"]
    r = rf.ciclo(P["T_ev"], T_cond, P["refrigerante"], P["sobrecal"], P["subenf"], P["eta_is"], P["eta_motor"])
    fl = P["refrigerante"]
    Tsat = np.linspace(233.15, 372.0, 220)
    p = np.array([PropsSI("P", "T", t, "Q", 0, fl) for t in Tsat]) / 1e3
    hl = np.array([PropsSI("H", "T", t, "Q", 0, fl) for t in Tsat]) / 1e3
    hv = np.array([PropsSI("H", "T", t, "Q", 1, fl) for t in Tsat]) / 1e3
    fig, ax = plt.subplots(figsize=(7.0, 4.3))
    ax.semilogy(hl, p, color=GRIS, lw=1.4)
    ax.semilogy(hv, p, color=GRIS, lw=1.4)
    pe, pc = r["P_ev"] / 1e3, r["P_c"] / 1e3
    # puntos
    x = {"1": r["h1"], "2": r["h2"], "3": r["h3"], "4": r["h4"], "2s": r["h2s"]}
    ax.plot([x["1"], x["2"]], [pe, pc], color=INK, lw=2.0)
    ax.plot([x["2"], x["3"]], [pc, pc], color=NARANJA, lw=2.0)
    ax.plot([x["3"], x["4"]], [pc, pe], color=INK, lw=2.0)
    ax.plot([x["4"], x["1"]], [pe, pe], color=AZUL, lw=2.0)
    ax.plot([x["1"], x["2s"]], [pe, pc], color=GRIS, lw=1.0, ls=(0, (3, 3)))
    for nom, (hx, py), off in (("1", (x["1"], pe), (6, -13)), ("2", (x["2"], pc), (6, 4)), ("2s", (x["2s"], pc), (-8, 7)),
                               ("3", (x["3"], pc), (-16, 5)), ("4", (x["4"], pe), (-14, -13))):
        ax.plot(hx, py, "o", ms=6, mfc="white", mec=INK, mew=1.4, zorder=5)
        ax.annotate(nom, (hx, py), xytext=off, textcoords="offset points", fontsize=9, fontweight="bold")
    ax.text(0.5 * (x["4"] + x["1"]), pe * 0.8, f"$q_L$ = {coma(r['q_L'], 1)} kJ/kg", color=AZUL, ha="center", fontsize=8)
    ax.text(0.5 * (x["2"] + x["3"]), pc * 1.1, f"$q_H$ = {coma(r['q_H'], 1)} kJ/kg", color=NARANJA, ha="center", fontsize=8)
    ax.text(0.5 * (x["1"] + x["2"]) + 12, np.sqrt(pe * pc) * 0.95, f"$w$ = {coma(r['w'], 1)} kJ/kg", color=INK, ha="left", fontsize=8)
    ax.text(0.02, 0.97, f"{fl}: evaporación a {coma(P['T_ev'])} °C ({coma(pe)} kPa), condensación a {coma(T_cond)} °C ({coma(pc)} kPa)\n"
            f"COP del eje {coma(r['cop_comp'], 2)} · COP eléctrico {coma(r['cop_elec'], 2)} · COP de Carnot {coma(r['cop_carnot'], 2)}",
            transform=ax.transAxes, va="top", fontsize=7.5, color=INK2)
    ax.set_xlabel("Entalpía específica [kJ/kg]")
    ax.set_ylabel("Presión [kPa]")
    ax.set_xlim(100, 520)
    ax.set_ylim(60, 4000)
    ax.grid(color=GRID, lw=0.6, which="both")
    ax.set_axisbelow(True)
    return _guardar(fig, "fig03_diagrama_ph_r134a.png")


# ------------------------------------------------------------------ 4. consumo por uso
def fig_consumo_por_uso(resumen):
    an = resumen["anual"]
    k = resumen["E_gas_PCS"] / an["q_util_total"]
    el = an["elec"]
    filas = [("Ventiladores de las unidades de aire", el["ventiladores"], "e"), ("Compresor de la enfriadora", el["compresor"], "e"),
             ("Recalentamiento", an["q_recal"] * k, "g"), ("Agua caliente sanitaria", an["q_acs"] * k, "g"),
             ("Calefacción del aire", an["q_cal"] * k, "g"), ("Ventiladores del condensador", el["vent_condensador"], "e"),
             ("Bombas de agua helada", el["bombas"], "e")]
    filas.sort(key=lambda f: f[1])
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    for i, (nom, v, t) in enumerate(filas):
        ax.barh(i, v / 1e3, color=AZUL if t == "e" else NARANJA, height=0.62)
        ax.text(v / 1e3 + 12, i, f"{coma(v / 1e3)} MWh  ({coma(v / resumen['E_total'] * 100, 1)} %)", va="center", fontsize=8, color=INK)
    ax.set_yticks(range(len(filas)))
    ax.set_yticklabels([f[0] for f in filas])
    ax.set_xlim(0, max(f[1] for f in filas) / 1e3 * 1.42)
    ax.set_xlabel("Energía final anual [MWh]")
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=AZUL, label="Electricidad"), Patch(color=NARANJA, label="Gas natural (PCS)")], loc="lower right", frameon=False, fontsize=8)
    return _guardar(fig, "fig04_consumo_por_uso.png")


# ------------------------------------------------------------------ 5. perfil mensual
def fig_perfil_mensual(c, resumen):
    an = resumen["anual"]
    meses = c["clima"]["meses"]
    T = c["clima"]["T"]
    frio = [f["Q_L"] / 1e3 for f in an["mensual"]]
    calor = [f["Q_cal"] / 1e3 for f in an["mensual"]]
    x = np.arange(12)
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    ax.bar(x - 0.2, frio, 0.38, color=AZUL, label="Frío entregado por la enfriadora")
    ax.bar(x + 0.2, calor, 0.38, color=NARANJA, label="Calor del aire (recalentamiento y calefacción)")
    ax.set_xticks(x)
    ax.set_xticklabels(meses, fontsize=8)
    for xi, t in zip(x, T):
        ax.text(xi, -0.115, coma(t, 1), transform=ax.get_xaxis_transform(), ha="center", va="top", fontsize=7, color=INK2)
    ax.text(-0.02, -0.115, "T [°C]", transform=ax.transAxes, ha="right", va="top", fontsize=7, color=INK2)
    ax.set_ylabel("Energía [MWh/mes]")
    ax.set_ylim(0, max(frio + calor) * 1.12)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, fontsize=8, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2)
    ax.text(0.0, -0.215, "Debajo de cada mes: temperatura media supuesta (a reemplazar por datos del SMN).", transform=ax.transAxes, fontsize=7, color=INK2)
    return _guardar(fig, "fig05_perfil_mensual.png")


# ------------------------------------------------------------------ 6. sensibilidad
def fig_sensibilidad():
    with open(os.path.join(RAIZ, "informe", "resultados_consumo.json"), encoding="utf-8") as f:
        S = json.load(f)["sensibilidad"]
    S = sorted(S, key=lambda s: -abs(s["delta"]))[:12][::-1]
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    for i, s in enumerate(S):
        col = NARANJA if s["delta"] > 0 else AZUL
        ax.barh(i, s["delta"] * 100, color=col, height=0.6)
        ha = "left" if s["delta"] > 0 else "right"
        ax.text(s["delta"] * 100 + (0.7 if s["delta"] > 0 else -0.7), i, f"{'+' if s['delta'] > 0 else '−'}{coma(abs(s['delta']) * 100, 1)} %",
                va="center", ha=ha, fontsize=8, color=INK)
    ax.axvline(0, color=INK2, lw=0.8)
    ax.set_yticks(range(len(S)))
    ax.set_yticklabels([s["nombre"] for s in S], fontsize=7.5)
    ax.set_xlim(-30, 34)
    ax.set_xlabel("Variación de la energía final anual respecto del caso base [%]")
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=NARANJA, label="Aumenta el consumo"), Patch(color=AZUL, label="Reduce el consumo")], frameon=False, fontsize=8, loc="lower right")
    return _guardar(fig, "fig06_sensibilidad.png")


def main():
    c = supuestos.defaults()
    R = es.resumen(c)
    rutas = [fig_esquema(), fig_psicrometrica(c, R), fig_ph(c, R), fig_consumo_por_uso(R), fig_perfil_mensual(c, R), fig_sensibilidad()]
    for r in rutas:
        print("escrita:", os.path.relpath(r, RAIZ))


if __name__ == "__main__":
    main()
