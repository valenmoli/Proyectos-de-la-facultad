"""Da formato al DOCX que genera pandoc: pagina A4, tipografia, tablas, epigrafes, avisos y pie de pagina."""
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

TINTA, TINTA2 = RGBColor(0x0B, 0x0B, 0x0B), RGBColor(0x52, 0x51, 0x4E)
TITULO = RGBColor(0x1F, 0x3A, 0x5F)
FUENTE = "Calibri"


def _fuente(estilo, tam=None, negrita=None, cursiva=None, color=None, nombre=FUENTE):
    f = estilo.font
    f.name = nombre
    rpr = estilo.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), nombre)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rf.get(qn(a)) is not None:
            del rf.attrib[qn(a)]
    if tam:
        f.size = Pt(tam)
    if negrita is not None:
        f.bold = negrita
    if cursiva is not None:
        f.italic = cursiva
    if color is not None:
        f.color.rgb = color


def _sombra_y_borde(estilo, relleno, borde):
    ppr = estilo.element.get_or_add_pPr()
    for tag in ("w:pBdr", "w:shd"):
        viejo = ppr.find(qn(tag))
        if viejo is not None:
            ppr.remove(viejo)
    pbdr = OxmlElement("w:pBdr")
    izq = OxmlElement("w:left")
    for k, v in (("w:val", "single"), ("w:sz", "24"), ("w:space", "6"), ("w:color", borde)):
        izq.set(qn(k), v)
    pbdr.append(izq)
    shd = OxmlElement("w:shd")
    for k, v in (("w:val", "clear"), ("w:color", "auto"), ("w:fill", relleno)):
        shd.set(qn(k), v)
    ppr.append(pbdr)
    ppr.append(shd)


def _estilos(doc):
    st = {s.name: s for s in doc.styles}
    for nom in ("Normal", "Body Text", "First Paragraph", "Compact", "Block Text"):
        if nom in st:
            _fuente(st[nom], 10.5, color=TINTA)
            pf = st[nom].paragraph_format
            pf.space_before = Pt(0)
            pf.space_after = Pt(6)
            pf.line_spacing = 1.12
            pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if "Compact" in st:
        st["Compact"].paragraph_format.space_after = Pt(2)
    cab = {"Heading 1": (15, 16, 6), "Heading 2": (12, 12, 4), "Heading 3": (10.5, 9, 3)}
    for nom, (tam, antes, desp) in cab.items():
        if nom in st:
            _fuente(st[nom], tam, negrita=True, cursiva=False, color=TITULO)
            st[nom].paragraph_format.space_before = Pt(antes)
            st[nom].paragraph_format.space_after = Pt(desp)
            st[nom].paragraph_format.keep_with_next = True
    if "Title" in st:
        _fuente(st["Title"], 22, negrita=True, color=TITULO)
        st["Title"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        st["Title"].paragraph_format.space_after = Pt(4)
    if "Subtitle" in st:
        _fuente(st["Subtitle"], 12.5, negrita=False, cursiva=False, color=TINTA2)
        st["Subtitle"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for nom in ("Author", "Date"):
        if nom in st:
            _fuente(st[nom], 10.5, color=TINTA2)
            st[nom].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            st[nom].paragraph_format.space_after = Pt(2)
    if "Table Caption" in st:
        _fuente(st["Table Caption"], 9, negrita=True, cursiva=False, color=TINTA)
        st["Table Caption"].paragraph_format.keep_with_next = True
        st["Table Caption"].paragraph_format.space_before = Pt(8)
        st["Table Caption"].paragraph_format.space_after = Pt(3)
    if "Image Caption" in st:
        _fuente(st["Image Caption"], 8.5, negrita=False, cursiva=True, color=TINTA2)
        st["Image Caption"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        st["Image Caption"].paragraph_format.space_after = Pt(10)
    for nom in ("Captioned Figure", "Figure"):
        if nom in st:
            st[nom].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            st[nom].paragraph_format.keep_with_next = True
            st[nom].paragraph_format.space_before = Pt(6)
            st[nom].paragraph_format.space_after = Pt(2)
    if "Verbatim Char" in st:
        _fuente(st["Verbatim Char"], 8.5, nombre="Consolas")
    if "Pendiente" in st:
        _fuente(st["Pendiente"], 10, color=TINTA)
        _sombra_y_borde(st["Pendiente"], "FDEFE3", "EB6834")
        st["Pendiente"].paragraph_format.space_after = Pt(6)
        st["Pendiente"].paragraph_format.left_indent = Cm(0.25)
    if "Nota" in st:
        _fuente(st["Nota"], 9.5, color=TINTA)
        _sombra_y_borde(st["Nota"], "E8F1FC", "2A78D6")
        st["Nota"].paragraph_format.space_after = Pt(6)
        st["Nota"].paragraph_format.left_indent = Cm(0.25)


def _borde_celda_tabla(tbl):
    tblpr = tbl._tbl.tblPr
    for tag in ("w:tblBorders", "w:tblCellMar", "w:tblLayout"):
        v = tblpr.find(qn(tag))
        if v is not None:
            tblpr.remove(v)
    b = OxmlElement("w:tblBorders")
    for lado, sz, color in (("top", "8", "52514E"), ("bottom", "8", "52514E"), ("insideH", "4", "D9D8D3")):
        e = OxmlElement(f"w:{lado}")
        for k, v in (("w:val", "single"), ("w:sz", sz), ("w:space", "0"), ("w:color", color)):
            e.set(qn(k), v)
        b.append(e)
    tblpr.append(b)
    m = OxmlElement("w:tblCellMar")
    for lado, w in (("top", "35"), ("left", "70"), ("bottom", "35"), ("right", "70")):
        e = OxmlElement(f"w:{lado}")
        e.set(qn("w:w"), w)
        e.set(qn("w:type"), "dxa")
        m.append(e)
    tblpr.append(m)


def _tablas(doc):
    for tbl in doc.tables:
        _borde_celda_tabla(tbl)
        for i, fila in enumerate(tbl.rows):
            trpr = fila._tr.get_or_add_trPr()
            cs = OxmlElement("w:cantSplit")
            trpr.append(cs)
            if i == 0:
                th = OxmlElement("w:tblHeader")
                trpr.append(th)
            for celda in fila.cells:
                if i == 0:
                    tcpr = celda._tc.get_or_add_tcPr()
                    shd = OxmlElement("w:shd")
                    for k, v in (("w:val", "clear"), ("w:color", "auto"), ("w:fill", "EEF3FA")):
                        shd.set(qn(k), v)
                    tcpr.append(shd)
                for p in celda.paragraphs:
                    if len(tbl.rows) <= 14 and i < len(tbl.rows) - 1:
                        p.paragraph_format.keep_with_next = True
                    p.paragraph_format.space_after = Pt(0)
                    p.paragraph_format.space_before = Pt(0)
                    p.paragraph_format.line_spacing = 1.0
                    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for r in p.runs:
                        r.font.size = Pt(8.5)
                        r.font.name = FUENTE
                        if i == 0:
                            r.font.bold = True


def _pie(doc):
    sec = doc.sections[0]
    p = sec.footer.paragraphs[0] if sec.footer.paragraphs else sec.footer.add_paragraph()
    p.text = ""
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Borrador v0.1 · TP Integrador de Termodinámica 2026 · Página ")
    r.font.size = Pt(8)
    r.font.color.rgb = TINTA2
    r2 = p.add_run()
    r2.font.size = Pt(8)
    r2.font.color.rgb = TINTA2
    for tipo, txt in (("begin", None), (None, "PAGE"), ("separate", None), (None, "\u200b1"), ("end", None)):
        if tipo:
            e = OxmlElement("w:fldChar")
            e.set(qn("w:fldCharType"), tipo)
        elif txt == "PAGE":
            e = OxmlElement("w:instrText")
            e.set(qn("xml:space"), "preserve")
            e.text = txt
        else:
            e = OxmlElement("w:t")
            e.text = "1"
        r2._r.append(e)


def aplicar(ruta):
    doc = Document(ruta)
    for s in doc.sections:
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)
        s.left_margin = s.right_margin = Cm(2.2)
        s.top_margin, s.bottom_margin = Cm(2.0), Cm(2.0)
    _estilos(doc)
    _tablas(doc)
    _pie(doc)
    doc.save(ruta)
