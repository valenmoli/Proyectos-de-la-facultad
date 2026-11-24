"""Figura 8: plano simplificado de las zonas con sus m2 y ubicacion de los equipos.

Panel izquierdo: corte esquematico del edificio (cubierta, 3.er, 2.º y 1.er piso). El ancho de cada
bloque es proporcional a su superficie dentro del nivel. Panel derecho: planta de cubierta esquematica y
detalle a escala de la plataforma de las cuatro enfriadoras (3 en servicio + 1 de reserva).

Figura 11: planta tipo a escala del 1.er y del 2.º piso (rectangulo equivalente 4:3, zonas de superficie proporcional a sus m2,
nucleo tecnico del lado de la calle, escala grafica y norte). La geometria sale de equipos.planta_tipo().

Todo numero sale de calculo/equipos.py (que a su vez toma las cargas del modelo); nada se copia a mano.

Uso (desde la carpeta del proyecto):  python -m calculo.figuras_plano
Escribe ../figuras/fig08_plano_zonas.png y ../figuras/fig11_planta_tipo.png respecto de calculo/.
"""
import math
import os
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

from . import equipos
from . import supuestos
from .figuras import AZUL, AZUL_CLARO, GRIS, GRID, INK, INK2, NARANJA, NARANJA_CLARO, SALIDA, coma

# Tabla de color fija por zona (tonos suaves; el azul y el naranja del proyecto quedan para frio y calor).
# Los tonos se ajustaron con el validador de paletas para que los bloques vecinos (G5-G4, G5-G3, G3-G2, G2-G1) se
# distingan tambien con daltonismo (DeltaE >= 15 en vision normal y en deuteranopia). Como son tonos suaves no pasan
# el piso de contraste contra el fondo: por eso cada bloque lleva su rotulo y su borde oscuro (la identidad no depende del color).
COLOR_ZONA = {
    "G1": "#c8aef4",   # quirofanos: violeta suave
    "G2": "#e8857d",   # terapia intensiva: rojo suave
    "G3": "#d3f0e0",   # internacion: verde muy suave
    "G4": "#f1cf72",   # guardia, diagnostico y laboratorio: ambar suave
    "G5": "#98b2dc",   # consultorios, administracion y docencia: azul grisaceo
}
COLOR_NO_CLIM = "#f1f0ec"
COLOR_RESERVA = "#fdf1c0"
NOMBRE_ARCHIVO = "fig08_plano_zonas.png"

# Orden de los bloques de izquierda a derecha en cada nivel (las zonas criticas quedan junto al nucleo tecnico)
ORDEN = {1: ["G5", "G4"], 2: ["G5", "G3", "G2", "G1"], 3: ["G5"]}

# Geometria en pulgadas (el eje cubre toda la figura: 1 unidad de datos = 1 pulgada)
W, H = 7.12, 6.85
GUT_X, XB0, BLOCK_W = 0.80, 0.83, 3.30
XB1 = XB0 + BLOCK_W
Y_CALLE = 1.55
ALT = {1: 1.20, 2: 1.50, 3: 1.00, "cub": 1.05}
FS, FS_CHICO = 7.6, 7.0
XP0, XP1 = 4.82, 6.97            # panel derecho

BARRA_SHAFT = 0.055
ULTIMOS_AVISOS = []
ULTIMOS_TEXTOS = []                # rotulos de la ultima figura 8 (para los tests)


# ------------------------------------------------------------------ utilidades de texto
def _medir(fig, t):
    bb = t.get_window_extent(fig.canvas.get_renderer())
    return bb.width / fig.dpi, bb.height / fig.dpi


def _texto_en_bloque(ax, fig, x0, x1, y0, y1, variantes, fs_lista=(FS, FS_CHICO, 6.6), color=INK, avisos=None, rot_pref=(0, 90)):
    """Centra un rotulo en el bloque. Prueba fuentes de mayor a menor, variantes de texto y rotacion 0 o 90 grados."""
    cx, cy = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    for fs in fs_lista:
        for var in variantes:
            for rot in rot_pref:
                t = ax.text(cx, cy, "\n".join(var), ha="center", va="center", fontsize=fs, color=color, rotation=rot,
                            linespacing=1.15, zorder=6)
                w, h = _medir(fig, t)
                if w <= (x1 - x0) - 0.03 and h <= (y1 - y0) - 0.03:
                    return t
                t.remove()
    if avisos is not None:
        avisos.append(f"rotulo que no entra en su bloque: {variantes[-1]}")
    return ax.text(cx, cy, "\n".join(variantes[-1]), ha="center", va="center", fontsize=fs_lista[-1], color=color, rotation=90, zorder=6)


def _rect(ax, x, y, w, h, fc, ec=INK2, lw=0.6, hatch=None, z=2, ls="-"):
    p = Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, hatch=hatch, zorder=z, ls=ls)
    ax.add_patch(p)
    return p


def _verificar_textos(fig, ax, avisos, ancho=None, alto=None):
    """Detecta rotulos superpuestos o fuera de la figura (ancho y alto en pulgadas; por defecto los de la figura 8)."""
    ancho = W if ancho is None else ancho
    alto = H if alto is None else alto
    r = fig.canvas.get_renderer()
    cajas = []
    for t in ax.texts:
        if not t.get_text().strip():
            continue
        bb = t.get_window_extent(r)
        cajas.append((t.get_text().replace("\n", " / "), bb.x0 / fig.dpi, bb.y0 / fig.dpi, bb.x1 / fig.dpi, bb.y1 / fig.dpi))
    for i, (ti, ax0, ay0, ax1, ay1) in enumerate(cajas):
        if ax0 < -0.001 or ay0 < -0.001 or ax1 > ancho + 0.001 or ay1 > alto + 0.001:
            avisos.append(f"texto fuera de la figura: {ti}")
        for tj, bx0, by0, bx1, by1 in cajas[i + 1:]:
            if min(ax1, bx1) - max(ax0, bx0) > 0.012 and min(ay1, by1) - max(ay0, by0) > 0.012:
                avisos.append(f"textos superpuestos: '{ti}' y '{tj}'")


def _leyenda(ax, fig, items, x0, x1, y_top, paso=0.20):
    """Leyenda en filas que se envuelven. Devuelve la coordenada y de la ultima fila."""
    x, y = x0, y_top
    sw = 0.13
    for kind, fc, ec, hatch, texto in items:
        t = ax.text(0, 0, texto, fontsize=FS_CHICO + 0.2, color=INK, va="center", ha="left")
        w, _h = _medir(fig, t)
        if x + sw + 0.06 + w > x1 and x > x0:
            x, y = x0, y - paso
        if kind == "rect":
            _rect(ax, x, y - sw / 2, sw, sw, fc, ec=ec, lw=0.6, hatch=hatch)
        elif kind == "uta":
            _rect(ax, x, y - sw / 2, sw, sw, fc, ec=INK, lw=0.9)
        t.set_position((x + sw + 0.06, y))
        x += sw + 0.06 + w + 0.22
    return y


# ------------------------------------------------------------------ figura
def fig_plano(c=None, R=None, ruta=None):
    """Genera la figura 8. c: configuracion del modelo; R: equipos.resumen_equipos(c); ruta: archivo de salida."""
    c = c or supuestos.defaults()
    R = R or equipos.resumen_equipos(c)
    niv, enf, cal, ut, hid, sh, az = (R[k] for k in ("niveles", "enfriadoras", "calderas", "utas", "hidraulica", "shafts", "azotea"))
    avisos = []
    plt.rcParams["hatch.linewidth"] = 0.5

    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    s = BLOCK_W / niv["bruta_nivel"]                       # pulgadas por m2
    y_bajo = {1: Y_CALLE}
    y_bajo[2] = y_bajo[1] + ALT[1]
    y_bajo[3] = y_bajo[2] + ALT[2]
    y_cub = y_bajo[3] + ALT[3]                              # losa de cubierta
    y_top = y_cub + ALT["cub"]
    nc_w = niv["niveles"][0]["no_clim"] * s
    x_nc = XB1 - nc_w

    # --- titulos
    ax.text(0.04, H - 0.10, "Corte esquemático", fontsize=9, fontweight="bold", va="top", ha="left")
    ax.text(0.04, H - 0.29, "Ancho de cada bloque proporcional a su superficie", fontsize=FS, color=INK2, va="top", ha="left")
    ax.text(XP0, H - 0.10, "Planta de cubierta", fontsize=9, fontweight="bold", va="top", ha="left")
    ax.text(XP0, H - 0.29, "Sin escala (enfriadoras a escala)", fontsize=FS, color=INK2, va="top", ha="left")

    # --- niveles
    textos_zona = {
        ("G1", 2): [["G1 Quirófanos", "252 m²"]],
        ("G2", 2): [["G2 Terapia intensiva", "336 m²"]],
    }
    for nv in niv["niveles"]:
        n = nv["nivel"]
        y0, y1 = y_bajo[n], y_bajo[n] + ALT[n]
        x = XB0
        por_g = {g: (a, t) for g, a, t in nv["zonas"]}
        for g in ORDEN[n]:
            a, tx = por_g[g]
            w = a * s
            _rect(ax, x, y0, w, ALT[n], COLOR_ZONA[g])
            m2 = f"{coma(a)} m²"
            if g == "G4":
                var = [[f"G4 Guardia, diagnóstico", "y laboratorio (24 h)", m2], [f"G4 Guardia, diagnóstico y laboratorio", m2]]
            elif g == "G5":
                var = [[f"G5 {tx}", m2], [f"G5 {tx} {m2}"], [f"G5 {m2}"]]
            elif g == "G3":
                var = [["G3 Internación general", m2]]
            else:
                var = [[f"{g} {equipos.NOMBRES_ZONA[g]}", m2], [f"{g} {equipos.NOMBRES_ZONA[g]} {m2}"], [f"{g} {m2}"]]
            _texto_en_bloque(ax, fig, x, x + w, y0, y1, var, avisos=avisos)
            x += w
        # locales tecnicos (no climatizados)
        _rect(ax, x_nc, y0, nc_w, ALT[n], COLOR_NO_CLIM, ec=GRIS, hatch="////")
        x_txt = x_nc + BARRA_SHAFT                          # los rotulos van a la derecha de la barra de shafts
        m2nc = f"{coma(nv['no_clim'])} m²"
        zona_txt = (y0, y1)
        if n == 2:
            # cuarto tecnico de las UTAs criticas: 6 de G1 y 1 de G2, a escala de simbolos
            u1 = ut["por_zona"]["G1"]["n"]
            u2 = ut["por_zona"]["G2"]["n"]
            cols, sq, gp = 4, 0.075, 0.02
            ys_top = y1 - 0.08
            xs0 = x_txt + (XB1 - x_txt - (cols * sq + (cols - 1) * gp)) / 2.0
            for i in range(u1 + u2):
                r_, c_ = divmod(i, cols)
                col = COLOR_ZONA["G1"] if i < u1 else COLOR_ZONA["G2"]
                _rect(ax, xs0 + c_ * (sq + gp), ys_top - sq - r_ * (sq + gp), sq, sq, col, ec=INK, lw=0.8, z=5)
            y_txt_top = ys_top - 2 * sq - gp - 0.04
            t = ax.text((x_txt + XB1) / 2.0, y_txt_top, f"UTAs\nG1 ×{u1}\nG2 ×{u2}", ha="center", va="top", fontsize=FS_CHICO, color=INK,
                        linespacing=1.15, zorder=6)
            _texto_en_bloque(ax, fig, x_txt, XB1, y0, y_txt_top - 0.37, [["Locales", "técnicos", m2nc]], avisos=avisos,
                             fs_lista=(FS_CHICO, 6.6))
        else:
            _texto_en_bloque(ax, fig, x_txt, XB1, y0, y1, [["Locales", "técnicos", m2nc]], avisos=avisos, fs_lista=(FS_CHICO, 6.6))
        # nombre del nivel y superficies en el margen izquierdo
        yc = (y0 + y1) / 2.0
        ax.text(GUT_X, yc + 0.17, nv["nombre"], ha="right", va="center", fontsize=8.5, fontweight="bold")
        ax.text(GUT_X, yc - 0.02, f"{coma(nv['clim'])} m²", ha="right", va="center", fontsize=FS, color=INK)
        ax.text(GUT_X, yc - 0.19, "climatizados", ha="right", va="center", fontsize=FS_CHICO, color=INK2)

    # --- cubierta
    _rect(ax, XB0, y_cub, BLOCK_W, ALT["cub"], "#fafaf8", ec=GRIS, lw=0.6, ls=(0, (3, 2)), z=1)
    ax.plot([XB0, XB1], [y_cub, y_cub], color=INK, lw=1.6, zorder=4)
    ax.text(GUT_X, y_cub + ALT["cub"] / 2.0 + 0.08, "Cubierta", ha="right", va="center", fontsize=8.5, fontweight="bold")
    ax.text(GUT_X, y_cub + ALT["cub"] / 2.0 - 0.10, f"{coma(niv['bruta_nivel'])} m²", ha="right", va="center", fontsize=FS, color=INK)
    ax.text(GUT_X, y_cub + ALT["cub"] / 2.0 - 0.27, "brutos", ha="right", va="center", fontsize=FS_CHICO, color=INK2)
    hb = 0.30                                              # altura de los equipos
    yb = y_cub + 0.03
    # reserva solar termica y fotovoltaica (sin dimensionar)
    xr0, wr = XB0 + 0.06, 0.66
    _rect(ax, xr0, yb, wr, 0.16, COLOR_RESERVA, ec=GRIS, hatch="....", z=3)
    ax.text(xr0 + wr / 2.0, yb + 0.30, "Reserva solar\ntérmica y FV", ha="center", va="center", fontsize=FS_CHICO, color=INK2, linespacing=1.15)
    # UTAs de cubierta, por zona
    bw, bg = 0.095, 0.02
    xg = xr0 + wr + 0.16
    uta_cub = {g: r for g, r in ut["por_zona"].items() if not r["critica"]}
    for g, r in uta_cub.items():
        k = r["n"]
        for i in range(k):
            _rect(ax, xg + i * (bw + bg), yb, bw, hb, COLOR_ZONA[g], ec=INK, lw=0.9, z=5)
        wg = k * bw + (k - 1) * bg
        ax.text(xg + wg / 2.0, yb + hb + 0.05, f"{g} ×{k}\n{coma(r['caudal_unidad'])}\nm³/h c/u", ha="center", va="bottom",
                fontsize=FS_CHICO, color=INK, linespacing=1.15)
        xg += wg + 0.17
    # enfriadoras C1 a C4 (C4 de reserva), sobre el nucleo tecnico
    n_t = enf["n_total"]
    cw, cg = 0.17, 0.025
    xc0 = XB1 - n_t * cw - (n_t - 1) * cg - 0.04
    for i in range(n_t):
        reserva = i >= enf["n_serv"]
        _rect(ax, xc0 + i * (cw + cg), yb, cw, hb, AZUL_CLARO if reserva else AZUL, ec=INK, lw=0.9, z=5, hatch="///" if reserva else None)
        ax.text(xc0 + i * (cw + cg) + cw / 2.0, yb + hb / 2.0, f"C{i + 1}", ha="center", va="center", fontsize=FS_CHICO,
                color=INK if reserva else "white", fontweight="bold", zorder=7,
                bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none") if reserva else None)
    ax.text(xc0 + (n_t * cw + (n_t - 1) * cg) / 2.0, yb + hb + 0.05, f"Enfriadoras\n{enf['n_serv']} en servicio\n+ {enf['n_res']} de reserva", ha="center",
            va="bottom", fontsize=FS_CHICO, color=INK, linespacing=1.15)

    # --- shafts (nucleo tecnico): barra rayada de la cubierta al 1.er piso
    n_shafts = sh["n_shafts_agrupados"]
    _rect(ax, x_nc, Y_CALLE, BARRA_SHAFT, y_cub - Y_CALLE, "white", ec=INK, lw=0.7, hatch="////", z=5)
    ax.text(x_nc - 0.085, (y_bajo[3] + y_cub) / 2.0, f"{n_shafts} shafts", rotation=90, ha="center", va="center", fontsize=FS_CHICO,
            color=INK, zorder=6)

    # --- anexo de calderas y chimenea
    xa0, wa, ha_ = XB1 + 0.05, 0.50, 0.58
    _rect(ax, xa0, Y_CALLE, wa, ha_, NARANJA_CLARO, ec=NARANJA, lw=1.3, z=4)
    ax.text(xa0 + wa / 2.0, Y_CALLE + ha_ / 2.0, "Anexo\ncalderas", ha="center", va="center", fontsize=FS_CHICO, color=INK, linespacing=1.15, zorder=6)
    xch = xa0 + 0.26
    y_ch = y_cub + 0.62
    ax.plot([xch, xch], [Y_CALLE + ha_, y_ch], color=NARANJA, lw=2.4, solid_capstyle="butt", zorder=4)
    ax.text(xch, y_ch + 0.04, "Chimenea", ha="center", va="bottom", fontsize=FS_CHICO, color=INK, zorder=6)
    # nivel de calle
    ax.plot([XB0 - 0.04, xa0 + wa + 0.06], [Y_CALLE, Y_CALLE], color=INK, lw=1.4, zorder=4)
    _rect(ax, XB0 - 0.04, Y_CALLE - 0.06, xa0 + wa + 0.10 - XB0, 0.06, "white", ec=GRIS, lw=0, hatch="////", z=1)
    ax.text(GUT_X, Y_CALLE - 0.03, "Nivel de calle", ha="right", va="top", fontsize=FS_CHICO, color=INK2, style="italic")

    # --- planta de cubierta (esquema) --------------------------------------------------------
    ancho_p = XP1 - XP0
    ap = equipos.parametros()["aspecto_planta"]
    Wm = (niv["bruta_nivel"] * ap) ** 0.5                   # m, planta rectangular equivalente
    Hm = niv["bruta_nivel"] / Wm
    k = ancho_p / Wm                                        # pulgadas por metro
    alto_p = Hm * k
    yp1 = y_top
    yp0 = yp1 - alto_p
    _rect(ax, XP0, yp0, ancho_p, alto_p, "#fafaf8", ec=INK, lw=1.0, z=1)
    xnc_p = XP0 + (1.0 - niv["niveles"][0]["no_clim"] / niv["bruta_nivel"]) * ancho_p
    _rect(ax, xnc_p, yp0, XP1 - xnc_p, alto_p, COLOR_NO_CLIM, ec=GRIS, hatch="////", lw=0.5, z=2)
    # shafts: un cuadrado por shaft, color de la zona (sin escala)
    colores = ([COLOR_ZONA["G1"]] * sh["n_shafts_por_grupo"]["G1+G2"] + [COLOR_ZONA["G3"]] * sh["n_shafts_por_grupo"]["G3"]
               + [COLOR_ZONA["G4"]] * sh["n_shafts_por_grupo"]["G4"] + [COLOR_ZONA["G5"]] * sh["n_shafts_por_grupo"]["G5"])
    sq, gp = 0.075, 0.025
    nc_ancho = XP1 - xnc_p
    cols = 2
    xs0 = xnc_p + (nc_ancho - (cols * sq + (cols - 1) * gp)) / 2.0
    ys0 = yp1 - 0.07
    for i, col in enumerate(colores):
        r_, c_ = divmod(i, cols)
        _rect(ax, xs0 + c_ * (sq + gp), ys0 - sq - r_ * (sq + gp), sq, sq, col, ec=INK, lw=0.8, z=5, hatch="////")
    y_shafts_fin = ys0 - (len(colores) // cols) * (sq + gp) - sq
    ax.text(xnc_p + nc_ancho / 2.0, y_shafts_fin - 0.06, f"{n_shafts}\nshafts", ha="center", va="top", fontsize=FS_CHICO, color=INK, linespacing=1.15, zorder=6)
    # chimenea
    y_chim = yp0 + 0.20
    ax.add_patch(Circle((xnc_p + nc_ancho / 2.0, y_chim), 0.065, fc=NARANJA, ec=INK, lw=0.9, zorder=6))
    ax.text(xnc_p - 0.04, y_chim, "Chimenea", ha="right", va="center", fontsize=FS_CHICO, color=INK, zorder=6)
    # enfriadoras a escala: 14 x 3,5 m, una fila por unidad junto al nucleo
    P_ = R["p"]
    cwm, chm, sep = P_["huella_L"] * k, P_["huella_W"] * k, 3.0 * k
    xe0 = xnc_p - 0.10 - cwm
    ye_top = yp1 - 0.10
    for i in range(enf["n_total"]):
        reserva = i >= enf["n_serv"]
        ye = ye_top - chm - i * (chm + sep)
        _rect(ax, xe0, ye, cwm, chm, AZUL_CLARO if reserva else AZUL, ec=INK, lw=0.8, z=5, hatch="///" if reserva else None)
        ax.text(xe0 - 0.04, ye + chm / 2.0, f"C{i + 1}", ha="right", va="center", fontsize=FS_CHICO, color=INK, fontweight="bold", zorder=6)
    # UTAs de cubierta: tres filas por zona (sin escala)
    uw, uh, ug = 0.13, 0.085, 0.035
    xu0 = XP0 + 0.10
    yu = yp1 - 0.10
    ax.text(xu0, yu, "UTAs", ha="left", va="top", fontsize=FS_CHICO, color=INK2)
    yu -= 0.16
    for g, r in uta_cub.items():
        for i in range(r["n"]):
            _rect(ax, xu0 + i * (uw + ug), yu - uh, uw, uh, COLOR_ZONA[g], ec=INK, lw=0.8, z=5)
        ax.text(xu0 + 4 * (uw + ug) + 0.02, yu - uh / 2.0, f"{g} ×{r['n']}", ha="left", va="center", fontsize=FS_CHICO, color=INK)
        yu -= uh + 0.07
    # reservas
    y_res_top = yu - 0.04
    bb_res = dict(boxstyle="square,pad=0.15", fc="white", ec="none", alpha=0.85)
    _rect(ax, XP0 + 0.10, yp0 + 0.10, 1.02, y_res_top - yp0 - 0.10, COLOR_RESERVA, ec=GRIS, hatch="....", lw=0.6, z=3)
    ax.text(XP0 + 0.61, (yp0 + 0.10 + y_res_top) / 2.0, "Reserva\nfotovoltaica", ha="center", va="center", fontsize=FS_CHICO, color=INK, linespacing=1.15,
            zorder=6, bbox=bb_res)
    xs_t0 = XP0 + 1.20
    ys_t1 = ye_top - enf["n_total"] * chm - (enf["n_total"] - 1) * sep - 0.10               # debajo de las enfriadoras
    xs_t1 = xnc_p - 0.10
    _rect(ax, xs_t0, yp0 + 0.38, xs_t1 - xs_t0, ys_t1 - yp0 - 0.38, COLOR_RESERVA, ec=GRIS, hatch="....", lw=0.6, z=3)
    ax.text((xs_t0 + xs_t1) / 2.0, (yp0 + 0.38 + ys_t1) / 2.0, "Reserva\nsolar\ntérmica", ha="center", va="center", fontsize=FS_CHICO, color=INK,
            linespacing=1.15, zorder=6, bbox=bb_res)

    # --- detalle a escala de la plataforma de enfriadoras ----------------------------------------
    y_det = yp0 - 0.30
    ax.text(XP0, y_det, "Enfriadoras (a escala)", fontsize=8.5, fontweight="bold", va="center", ha="left")
    sd = 0.062                                             # pulgadas por metro
    L, Wd = P_["huella_L"], P_["huella_W"]
    xd0 = XP0 + 0.32
    yd_top = y_det - 0.40
    for i in range(enf["n_total"]):
        reserva = i >= enf["n_serv"]
        yd = yd_top - Wd * sd - i * (Wd + 3.0) * sd
        _rect(ax, xd0, yd, L * sd, Wd * sd, AZUL_CLARO if reserva else AZUL, ec=INK, lw=0.9, z=5, hatch="///" if reserva else None)
        ax.text(xd0 + L * sd / 2.0, yd + Wd * sd / 2.0, f"C{i + 1}" + (" (reserva)" if reserva else ""), ha="center", va="center", fontsize=FS,
                color=INK if reserva else "white", fontweight="bold", zorder=7,
                bbox=dict(boxstyle="square,pad=0.15", fc="white", ec="none") if reserva else None)
    yd_bot = yd_top - enf["n_total"] * Wd * sd - (enf["n_total"] - 1) * 3.0 * sd
    # cotas
    ax.annotate("", xy=(xd0, yd_top + 0.09), xytext=(xd0 + L * sd, yd_top + 0.09), arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.8, shrinkA=0, shrinkB=0))
    ax.text(xd0 + L * sd / 2.0, yd_top + 0.12, f"{coma(L)} m", ha="center", va="bottom", fontsize=FS, color=INK)
    ax.annotate("", xy=(xd0 - 0.07, yd_top), xytext=(xd0 - 0.07, yd_top - Wd * sd), arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.8, shrinkA=0, shrinkB=0))
    ax.text(xd0 - 0.10, yd_top - Wd * sd / 2.0, f"{coma(Wd, 1)} m", ha="right", va="center", fontsize=FS, color=INK)
    xs_ = xd0 + L * sd / 2.0
    ax.annotate("", xy=(xs_, yd_top - Wd * sd), xytext=(xs_, yd_top - Wd * sd - 3.0 * sd), arrowprops=dict(arrowstyle="<->", color=INK2, lw=0.8, shrinkA=0, shrinkB=0))
    ax.text(xs_ + 0.05, yd_top - Wd * sd - 1.5 * sd, "s", ha="left", va="center", fontsize=FS, color=INK, style="italic")
    xt = xd0 + L * sd + 0.10
    linea = [f"{enf['n_total']} unidades:", f"{enf['n_serv']} en servicio", f"+ {enf['n_res']} de reserva", f"{coma(L)} × {coma(Wd, 1)} m =", f"{coma(az['A_unidad'])} m² c/u",
             f"{enf['n_total']} × {coma(az['A_unidad'])} m² =", f"{coma(az['A_total'])} m²", f"{coma(P_['peso_op_t'])} t c/u", f"carga {coma(az['q_kN_m2'], 1)} kN/m²",
             "(azotea corriente", f"{coma(az['q_ref'], 1)} kN/m²)"]
    ax.text(xt, yd_top, "\n".join(linea), ha="left", va="top", fontsize=FS_CHICO, color=INK, linespacing=1.3)
    ax.text(xd0, yd_bot - 0.10, "s: separación según fabricante", ha="left", va="top", fontsize=FS_CHICO - 0.4, color=INK2, style="italic")

    # --- notas de ubicacion
    notas = [
        "Enfriadoras en azotea, junto al núcleo técnico: el agua helada baja por sus shafts.",
        "Izaje con grúa móvil desde la calle, del lado del núcleo técnico.",
        "Calderas en anexo a nivel de calle: medidor y regulador de gas, ventilación y chimenea por fuera del edificio.",
    ]
    y_n = yd_bot - 0.40
    cuerpo = "\n".join("• " + textwrap.fill(n, 41, subsequent_indent="  ") for n in notas)
    ax.text(XP0, y_n, cuerpo, ha="left", va="top", fontsize=FS_CHICO, color=INK, linespacing=1.25)

    # --- leyenda al pie
    items = [("rect", COLOR_ZONA[g], INK2, None, f"{g} {equipos.NOMBRES_ZONA[g]}") for g in ("G1", "G2", "G3", "G4", "G5")]
    items += [("rect", COLOR_NO_CLIM, GRIS, "////", "Locales técnicos, morgue y depósitos"),
              ("uta", "white", INK, None, "UTA (color de su zona)"),
              ("rect", AZUL, INK, None, "Enfriadora (rayada: reserva)"),
              ("rect", NARANJA_CLARO, NARANJA, None, "Anexo de calderas (sin escala)"),
              ("rect", "white", INK, "////", "Shaft de aire"),
              ("rect", COLOR_RESERVA, GRIS, "....", "Reserva solar y FV (sin dimensionar)")]
    y_leg = _leyenda(ax, fig, items, 0.06, W - 0.04, 0.90)
    ax.text(0.06, y_leg - 0.20, "Los locales técnicos son la superficie no climatizada de cada nivel (bruta menos climatizada).\n"
            "Superficies de zona: modelo. Distribución en niveles y planta de cubierta: supuesto (ver la memoria, supuestos Q1 a Q4).",
            fontsize=FS_CHICO - 0.4, color=INK2, va="top", ha="left", linespacing=1.3)

    fig.canvas.draw()
    _verificar_textos(fig, ax, avisos)
    ULTIMOS_AVISOS[:] = avisos
    ULTIMOS_TEXTOS[:] = [t.get_text() for t in ax.texts]
    for a in avisos:
        print("AVISO figura 8:", a)

    import os
    if ruta is None:
        os.makedirs(SALIDA, exist_ok=True)
        ruta = os.path.join(SALIDA, NOMBRE_ARCHIVO)
    fig.savefig(ruta, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    return ruta


# ====================================================================================
# Figura 11: planta tipo a escala
# ====================================================================================
NOMBRE_ARCHIVO_PT = "fig11_planta_tipo.png"
PT_W, PT_H = 7.14, 5.70
PT_WP = 3.02                       # ancho del dibujo de cada planta, en pulgadas
PT_X0 = (0.52, 4.08)               # borde oeste de cada planta
PT_YB = 2.05                       # borde sur de las plantas
PT_FS = (7.2, 6.8, 6.4)
PT_FS_N = 6.8                      # tamano de los rotulos sueltos (cotas, accesos, leyenda)
COLOR_CALLE = "#e9e8e4"
ULTIMOS_AVISOS_PT = []
ULTIMOS_TEXTOS_PT = []             # rotulos de la ultima figura 11 (para los tests)
ULTIMAS_AREAS_PT = []              # (nivel, id de bloque, m2 que miden los rectangulos dibujados)
ULTIMA_ESCALA_PT = [None]          # pulgadas por metro del ultimo dibujo


def _costuras(rects):
    """Segmentos compartidos entre rectangulos de un mismo bloque (para ocultar la linea interior de una zona en L)."""
    out = []
    for i, (ax0, ay0, ax1, ay1) in enumerate(rects):
        for (bx0, by0, bx1, by1) in rects[i + 1:]:
            if abs(ay0 - by1) < 1e-9 or abs(ay1 - by0) < 1e-9:
                y = ay0 if abs(ay0 - by1) < 1e-9 else ay1
                x0, x1 = max(ax0, bx0), min(ax1, bx1)
                if x1 - x0 > 1e-9:
                    out.append(((x0, y), (x1, y)))
            if abs(ax0 - bx1) < 1e-9 or abs(ax1 - bx0) < 1e-9:
                x = ax0 if abs(ax0 - bx1) < 1e-9 else ax1
                y0, y1 = max(ay0, by0), min(ay1, by1)
                if y1 - y0 > 1e-9:
                    out.append(((x, y0), (x, y1)))
    return out


def fig_planta_tipo(c=None, R=None, ruta=None):
    """Genera la figura 11. c: configuracion del modelo; R: equipos.resumen_equipos(c); ruta: archivo de salida."""
    c = c or supuestos.defaults()
    R = R or equipos.resumen_equipos(c)
    pl, ut, niv = R["planta"], R["utas"], R["niveles"]
    nuc = pl["nucleo"]
    avisos, areas = [], []
    plt.rcParams["hatch.linewidth"] = 0.5

    fig = plt.figure(figsize=(PT_W, PT_H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, PT_W)
    ax.set_ylim(0, PT_H)
    ax.axis("off")

    Wm, Hm = pl["W"], pl["H"]
    k = PT_WP / Wm                                          # pulgadas por metro (la misma en los dos pisos)
    ULTIMA_ESCALA_PT[0] = k
    yb = PT_YB
    y_top = yb + Hm * k
    flecha = dict(arrowstyle="<->", color=INK2, lw=0.8, shrinkA=0, shrinkB=0)

    ax.text(0.04, PT_H - 0.10, "Planta tipo a escala", fontsize=9.5, fontweight="bold", va="top", ha="left")
    ax.text(0.04, PT_H - 0.31, f"Rectángulo equivalente {'4:3' if abs(pl['aspecto'] - 4.0 / 3.0) < 1e-9 else coma(pl['aspecto'], 2) + ':1'} de {coma(Wm, 1)} × {coma(Hm, 1)} m; la superficie dibujada de cada zona "
            "es proporcional a sus m²", fontsize=PT_FS[0], color=INK2, va="top", ha="left")

    for i, n in enumerate((1, 2)):
        nv = pl["niveles"][n]
        dnv = niv["niveles"][n - 1]
        x0p = PT_X0[i]

        def X(x, x0p=x0p):
            return x0p + x * k

        def Y(y):
            return yb + y * k

        # --- bloques
        for b in nv["bloques"]:
            es_nuc = b["id"] == "NUCLEO"
            for (rx0, ry0, rx1, ry1) in b["rects"]:
                if es_nuc:
                    _rect(ax, X(rx0), Y(ry0), (rx1 - rx0) * k, (ry1 - ry0) * k, COLOR_NO_CLIM, ec=GRIS, lw=0.5, hatch="////", z=2)
                    _rect(ax, X(rx0), Y(ry0), (rx1 - rx0) * k, (ry1 - ry0) * k, "none", ec=INK2, lw=0.9, z=3)
                else:
                    _rect(ax, X(rx0), Y(ry0), (rx1 - rx0) * k, (ry1 - ry0) * k, COLOR_ZONA[b["zona"]], ec=INK2, lw=0.6, z=2)
            for (sx0, sy0), (sx1, sy1) in _costuras(b["rects"]):
                ax.plot([X(sx0), X(sx1)] if abs(sy0 - sy1) < 1e-9 else [X(sx0)] * 2, [Y(sy0)] * 2 if abs(sy0 - sy1) < 1e-9 else [Y(sy0), Y(sy1)],
                        color=COLOR_ZONA[b["zona"]], lw=1.6, solid_capstyle="butt", zorder=2.5)
            # superficie que miden los rectangulos dibujados (pulgadas^2 / escala^2 = m2)
            a_dib = sum(((rx1 - rx0) * k) * ((ry1 - ry0) * k) for (rx0, ry0, rx1, ry1) in b["rects"]) / (k * k)
            areas.append((n, b["id"], a_dib))

        # --- rotulos de zona
        for b in nv["bloques"]:
            if b["id"] == "NUCLEO":
                continue
            rx0, ry0, rx1, ry1 = max(b["rects"], key=lambda r: (r[2] - r[0]) * (r[3] - r[1]))
            m2 = f"{coma(b['area_modelo'])} m²"
            g = b["zona"]
            if b["id"] == "G4":
                var = [["G4 Guardia, diagnóstico", "y laboratorio (24 h)", m2]]
            elif g == "G3":
                var = [[f"G3 {b['nombre']}", m2]]
            elif g == "G5":
                var = [[f"G5 {b['nombre']}", m2], ["G5", b["nombre"], m2], [f"G5 {m2}"]]
            elif g == "G2":
                var = [["G2 Terapia", "intensiva", m2], [f"G2 {m2}"]]
            else:
                var = [[f"{g} {b['nombre']}", m2], [g, b["nombre"], m2], [f"{g} {m2}"]]
            _texto_en_bloque(ax, fig, X(rx0), X(rx1), Y(ry0), Y(ry1), var, fs_lista=PT_FS, avisos=avisos)
        if n == 1:
            g4 = next(b for b in nv["bloques"] if b["id"] == "G4")
            pie = [r for r in g4["rects"] if r[1] < 1e-9]
            if pie:
                rx0, ry0, rx1, ry1 = pie[0]
                _texto_en_bloque(ax, fig, X(rx0), X(rx1), Y(ry0) + 0.20, Y(ry1) - 0.05, [["Guardia"]], fs_lista=PT_FS, avisos=avisos, rot_pref=(0,))

        # --- nucleo tecnico: rotulos, shafts y (2.º piso) UTAs de las zonas criticas
        cx0, cx1 = X(nuc["x0"]), X(nuc["x1"])
        cy0, cy1 = Y(nuc["y0"]), Y(nuc["y1"])
        ccx = (cx0 + cx1) / 2.0
        bb_nuc = dict(boxstyle="square,pad=0.08", fc=COLOR_NO_CLIM, ec="none", alpha=0.92)
        sq = math.sqrt(nuc["area_shaft"]) * k                # lado de un shaft, a escala
        gap = 0.5 * k
        ncol = math.ceil(nuc["n_shafts"] / 2)
        xs0 = cx0 + 0.07
        ys0 = cy0 + 0.17
        for j in range(nuc["n_shafts"]):
            r_, c_ = divmod(j, ncol)
            _rect(ax, xs0 + c_ * (sq + gap), ys0 + r_ * (sq + gap), sq, sq, "white", ec=INK, lw=0.6, hatch="////", z=5)
        w_sh = ncol * sq + (ncol - 1) * gap
        ax.text(xs0 + w_sh + 0.05, ys0 + sq + gap / 2.0, f"{nuc['n_shafts']} shafts", ha="left", va="center", fontsize=PT_FS[1], color=INK, zorder=6, bbox=bb_nuc)
        ax.text(ccx, cy0 + 0.62 if n == 1 else cy0 + 0.50, f"Núcleo técnico\n{coma(nuc['area'])} m²\n{coma(nuc['ancho'], 1)} × {coma(nuc['prof'], 1)} m",
                ha="center", va="center", fontsize=PT_FS[1], color=INK, linespacing=1.15, zorder=6, bbox=bb_nuc)
        if n == 1:
            ax.text(ccx, cy0 + 0.085, "Morgue y depósitos", ha="center", va="center", fontsize=PT_FS[2], color=INK, zorder=6, bbox=bb_nuc)
        else:
            usz, ugp = 0.074, 0.018
            for g in ("G1", "G2"):
                gb = next(b for b in nv["bloques"] if b["id"] == g)
                rx0, _ry0, rx1, _ry1 = gb["rects"][0]
                cnt = nv["utas_criticas"][g]
                cols = 3 if cnt > 1 else 1
                rows = math.ceil(cnt / cols)
                wgrp = cols * usz + (cols - 1) * ugp
                xg0 = (X(rx0) + X(rx1)) / 2.0 - wgrp / 2.0
                ytop = cy1 - 0.025
                for j in range(cnt):
                    r_, c_ = divmod(j, cols)
                    xu = xg0 + c_ * (usz + ugp)
                    yu = ytop - usz - r_ * (usz + ugp)
                    _rect(ax, xu, yu, usz, usz, COLOR_ZONA[g], ec=INK, lw=0.8, z=5)
                    ax.plot([xu + usz / 2.0] * 2, [yu + usz, cy1 + 0.05], color=AZUL, lw=1.2, solid_capstyle="butt", zorder=4)
                y_lbl = ytop - rows * usz - (rows - 1) * ugp - 0.025
                ax.text((X(rx0) + X(rx1)) / 2.0, y_lbl, f"{g} ×{cnt}", ha="center", va="top", fontsize=PT_FS[2], color=INK, zorder=6, bbox=bb_nuc)

        # --- contorno, cotas externas y calle
        _rect(ax, X(0), Y(0), Wm * k, Hm * k, "none", ec=INK, lw=1.3, z=4)
        yd = y_top + 0.14
        ax.annotate("", xy=(X(0), yd), xytext=(X(Wm), yd), arrowprops=flecha)
        for xe in (X(0), X(Wm)):
            ax.plot([xe, xe], [y_top + 0.03, yd + 0.04], color=INK2, lw=0.6, zorder=3)
        ax.text((X(0) + X(Wm)) / 2.0, yd + 0.04, f"{coma(Wm, 1)} m", ha="center", va="bottom", fontsize=PT_FS_N, color=INK)
        xd = x0p - 0.14
        ax.annotate("", xy=(xd, Y(0)), xytext=(xd, Y(Hm)), arrowprops=flecha)
        for ye in (Y(0), Y(Hm)):
            ax.plot([xd - 0.04, x0p - 0.03], [ye, ye], color=INK2, lw=0.6, zorder=3)
        ax.text(xd - 0.04, (Y(0) + Y(Hm)) / 2.0, f"{coma(Hm, 1)} m", ha="right", va="center", fontsize=PT_FS_N, color=INK, rotation=90)
        _rect(ax, X(0), yb - 0.19, Wm * k, 0.15, COLOR_CALLE, ec="none", z=1)
        ax.text(X(Wm) - 0.06, yb - 0.115, "Calle (supuesto)", ha="right", va="center", fontsize=PT_FS_N, color=INK2, style="italic", zorder=6)

        # --- titulo de la planta
        ax.text(x0p, y_top + 0.64, nv["nombre"], ha="left", va="center", fontsize=9.5, fontweight="bold")
        ax.text(x0p, y_top + 0.47, f"{coma(dnv['bruta'])} m² brutos, {coma(dnv['clim'])} m² climatizados", ha="left", va="center", fontsize=PT_FS_N, color=INK2)

        # --- accesos (solo el 1.er piso esta a nivel de calle)
        if n == 1:
            for xm, txt in ((nv["acceso_guardia_x"], "Acceso de guardia"), (nv["ingreso_x"], "Ingreso")):
                ax.annotate("", xy=(X(xm), yb + 0.05), xytext=(X(xm), yb - 0.40), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.1, mutation_scale=7,
                                                                                            shrinkA=0, shrinkB=0), zorder=7)
                ax.text(X(xm), yb - 0.43, txt, ha="center", va="top", fontsize=PT_FS_N, color=INK)

    # --- escala grafica (la misma para los dos pisos), debajo del 2.º piso, y norte, arriba a la derecha
    ys = yb - 0.50
    x_s = PT_X0[1]
    L10 = 10.0 * k
    for j in range(2):
        _rect(ax, x_s + j * L10, ys, L10, 0.06, "white" if j else INK, ec=INK, lw=0.7, z=5)
    for j, t in enumerate(("0", "10", "20 m")):
        ax.text(x_s + j * L10, ys - 0.04, t, ha="center", va="top", fontsize=PT_FS_N, color=INK)
    ax.text(x_s + 2 * L10 + 0.42, ys + 0.03, "Escala gráfica, común a los dos pisos", ha="left", va="center", fontsize=PT_FS_N, color=INK2)
    xn = PT_W - 0.32
    yn0 = y_top + 0.36
    ax.annotate("", xy=(xn, yn0 + 0.36), xytext=(xn, yn0), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4, mutation_scale=10, shrinkA=0, shrinkB=0))
    ax.text(xn, yn0 + 0.39, "N", ha="center", va="bottom", fontsize=9, fontweight="bold", color=INK)
    ax.text(xn - 0.14, yn0 + 0.18, "Norte arriba\n(supuesto)", ha="right", va="center", fontsize=PT_FS_N, color=INK2, linespacing=1.15)

    # --- leyenda y notas
    items = [("rect", COLOR_ZONA[g], INK2, None, f"{g} {equipos.NOMBRES_ZONA[g]}") for g in ("G1", "G2", "G3", "G4", "G5")]
    items += [("rect", COLOR_NO_CLIM, GRIS, "////", "Núcleo técnico: locales técnicos, morgue y depósitos (no climatizado)"),
              ("uta", "white", INK, None, "UTA crítica en el cuarto técnico (sin escala)"),
              ("rect", "white", INK, "////", "Shaft de aire (a escala)")]
    y_leg = _leyenda(ax, fig, items, 0.06, PT_W - 0.04, yb - 0.82)
    notas = [
        f"{nuc['n_shafts']} shafts de {coma(nuc['area_shaft'], 1)} m² ({coma(nuc['area_shafts'])} m² en total, dentro del núcleo; área neta vertical calculada {coma(nuc['area_vertical_neta'], 1)} m²). "
        "La circulación (pasillos y halls) está dentro de la superficie climatizada de cada zona, sin m² propios; la morgue y los depósitos están dentro del núcleo.",
        pl["nota_3er_piso"] + f" ({coma(niv['niveles'][2]['clim'])} m² climatizados.)",
        "Supuestos Q4 a Q9: norte arriba, calle al sur, núcleo técnico en la esquina sudeste y zonas por franjas. Los m² de cada zona son del modelo; "
        "la distribución en planta no sale de planos del edificio real.",
    ]
    cuerpo = "\n".join(textwrap.fill(t, 132, subsequent_indent="  ") for t in notas)
    ax.text(0.06, y_leg - 0.22, cuerpo, fontsize=PT_FS_N - 0.2, color=INK2, va="top", ha="left", linespacing=1.3)

    fig.canvas.draw()
    _verificar_textos(fig, ax, avisos, PT_W, PT_H)
    ULTIMOS_AVISOS_PT[:] = avisos
    ULTIMOS_TEXTOS_PT[:] = [t.get_text() for t in ax.texts]
    ULTIMAS_AREAS_PT[:] = areas
    for a_ in avisos:
        print("AVISO figura 11:", a_)

    if ruta is None:
        os.makedirs(SALIDA, exist_ok=True)
        ruta = os.path.join(SALIDA, NOMBRE_ARCHIVO_PT)
    fig.savefig(ruta, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    return ruta


def main():
    ruta = fig_plano()
    print("escrita:", ruta)
    ruta = fig_planta_tipo()
    print("escrita:", ruta)


if __name__ == "__main__":
    main()
