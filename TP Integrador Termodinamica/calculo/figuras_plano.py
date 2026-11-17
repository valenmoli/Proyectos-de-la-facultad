"""Figura 8: plano simplificado de las zonas con sus m2 y ubicacion de los equipos.

Panel izquierdo: corte esquematico del edificio (cubierta, 3.er, 2.º y 1.er piso). El ancho de cada
bloque es proporcional a su superficie dentro del nivel. Panel derecho: planta de cubierta esquematica y
detalle a escala de la plataforma de las tres enfriadoras.

Todo numero sale de calculo/equipos.py (que a su vez toma las cargas del modelo); nada se copia a mano.

Uso (desde la carpeta del proyecto):  python -m calculo.figuras_plano
Escribe ../figuras/fig08_plano_zonas.png respecto de calculo/.
"""
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
W, H = 7.12, 6.55
GUT_X, XB0, BLOCK_W = 0.80, 0.83, 3.30
XB1 = XB0 + BLOCK_W
Y_CALLE = 1.25
ALT = {1: 1.20, 2: 1.50, 3: 1.00, "cub": 1.05}
FS, FS_CHICO = 7.6, 7.0
XP0, XP1 = 4.82, 6.97            # panel derecho

BARRA_SHAFT = 0.055
ULTIMOS_AVISOS = []


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


def _verificar_textos(fig, ax, avisos):
    """Detecta rotulos superpuestos o fuera de la figura."""
    r = fig.canvas.get_renderer()
    cajas = []
    for t in ax.texts:
        if not t.get_text().strip():
            continue
        bb = t.get_window_extent(r)
        cajas.append((t.get_text().replace("\n", " / "), bb.x0 / fig.dpi, bb.y0 / fig.dpi, bb.x1 / fig.dpi, bb.y1 / fig.dpi))
    for i, (ti, ax0, ay0, ax1, ay1) in enumerate(cajas):
        if ax0 < -0.001 or ay0 < -0.001 or ax1 > W + 0.001 or ay1 > H + 0.001:
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
    # enfriadoras C1 a C3 (C3 de reserva), sobre el nucleo tecnico
    cw, cg = 0.20, 0.03
    xc0 = XB1 - 3 * cw - 2 * cg - 0.04
    for i in range(enf["n_total"]):
        reserva = i >= enf["n_serv"]
        _rect(ax, xc0 + i * (cw + cg), yb, cw, hb, AZUL_CLARO if reserva else AZUL, ec=INK, lw=0.9, z=5, hatch="///" if reserva else None)
        ax.text(xc0 + i * (cw + cg) + cw / 2.0, yb + hb / 2.0, f"C{i + 1}", ha="center", va="center", fontsize=FS_CHICO,
                color=INK if reserva else "white", fontweight="bold", zorder=7,
                bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none") if reserva else None)
    ax.text(xc0 + (3 * cw + 2 * cg) / 2.0, yb + hb + 0.05, f"Enfriadoras\n{enf['n_serv']} + {enf['n_res']}", ha="center", va="bottom",
            fontsize=FS_CHICO, color=INK, linespacing=1.15)

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
    # enfriadoras a escala: 14 x 3,5 m, tres filas junto al nucleo
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
    ys_t1 = ye_top - 3 * chm - 2 * sep - 0.10               # debajo de las enfriadoras
    xs_t1 = xnc_p - 0.10
    _rect(ax, xs_t0, yp0 + 0.38, xs_t1 - xs_t0, ys_t1 - yp0 - 0.38, COLOR_RESERVA, ec=GRIS, hatch="....", lw=0.6, z=3)
    ax.text((xs_t0 + xs_t1) / 2.0, (yp0 + 0.38 + ys_t1) / 2.0, "Reserva\nsolar\ntérmica", ha="center", va="center", fontsize=FS_CHICO, color=INK,
            linespacing=1.15, zorder=6, bbox=bb_res)

    # --- detalle a escala de la plataforma de enfriadoras ----------------------------------------
    y_det = yp0 - 0.30
    ax.text(XP0, y_det, "Enfriadoras (a escala)", fontsize=8.5, fontweight="bold", va="center", ha="left")
    sd = 0.070                                             # pulgadas por metro
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
    yd_bot = yd_top - 3 * Wd * sd - 2 * 3.0 * sd
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
             f"{coma(P_['peso_op_t'])} t c/u", f"carga {coma(az['q_kN_m2'], 1)} kN/m²", "(azotea corriente", f"{coma(az['q_ref'], 1)} kN/m²)"]
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
            "Superficies de zona: modelo. Distribución en niveles y planta de cubierta: supuesto (tabla de supuestos Q1 a Q4).",
            fontsize=FS_CHICO - 0.4, color=INK2, va="top", ha="left", linespacing=1.3)

    fig.canvas.draw()
    _verificar_textos(fig, ax, avisos)
    ULTIMOS_AVISOS[:] = avisos
    for a in avisos:
        print("AVISO figura 8:", a)

    import os
    if ruta is None:
        os.makedirs(SALIDA, exist_ok=True)
        ruta = os.path.join(SALIDA, NOMBRE_ARCHIVO)
    fig.savefig(ruta, bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    return ruta


def main():
    ruta = fig_plano()
    print("escrita:", ruta)


if __name__ == "__main__":
    main()
