// Genera el guion (Markdown) como Word legible para exponer.
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, ShadingType,
  BorderStyle, AlignmentType, LevelFormat, Header, Footer, PageNumber, PageBreak, TabStopType,
} = require("docx");

const SRC = process.argv[2];
const OUT = process.argv[3];
const md = fs.readFileSync(SRC, "utf8").replace(/\r/g, "");
const lines = md.split("\n");

// --- paleta (la del equipo) y tipografía
const NAVY = "12213F", ORANGE_D = "B8461A", ORANGE = "F4A261", INK = "1F2937", MUT = "4A5568";
const GREEN = "0F7B58", BEIGE = "F4F2EB", LINE = "D9D6CC", CUT_BG = "E4E9F2", CUT_TX = "34435E";
const FONT = "Arial";
const PAGE_W = 11906, PAGE_H = 16838, MARGIN = 1134;       // A4, 2 cm
const CONTENT_W = PAGE_W - 2 * MARGIN;                      // 9638 DXA

// --- tiempos medidos (palabras habladas a 130-150 por minuto)
const TIEMPOS = {
  10: "Versión base ≈ 1:00 a 1:10  ·  con todo ≈ 1:20 a 1:35",
  11: "Versión base ≈ 1:45 a 2:00  ·  con todo ≈ 2:30 a 2:50",
  12: "Versión base ≈ 1:00 a 1:10  ·  con todo ≈ 1:25 a 1:40",
};

// --- inline: **negrita**, [corte opcional], resto texto
function runs(text, o = {}) {
  const base = { font: FONT, size: o.size || 22, color: o.color || INK, bold: !!o.bold, italics: !!o.italics };
  const out = [];
  const re = /(\*\*[^*]+\*\*|\[[^\]]{4,}\])/g;
  let last = 0, m;
  const push = (t, extra = {}) => {
    if (!t) return;
    // X_y -> subíndice real (Q_L, W_eje, T_0...)
    const partes = t.split(/([A-Za-zηψωṁ]+_[A-Za-z0-9]+)/g);
    partes.forEach(seg => {
      if (!seg) return;
      const m = /^([A-Za-zηψωṁ]+)_([A-Za-z0-9]+)$/.exec(seg);
      if (m) {
        out.push(new TextRun({ ...base, ...extra, text: m[1] }));
        out.push(new TextRun({ ...base, ...extra, text: m[2], subScript: true }));
      } else out.push(new TextRun({ ...base, ...extra, text: seg }));
    });
  };
  while ((m = re.exec(text))) {
    push(text.slice(last, m.index));
    const tok = m[0];
    if (tok.startsWith("**")) {
      push(tok.slice(2, -2), { bold: true, color: o.boldColor || (o.color ? o.color : NAVY) });
    } else {
      // corte opcional: se muestra entre corchetes y sombreado
      const inner = tok.slice(1, -1);
      const parts = inner.split(/(\*\*[^*]+\*\*)/g);
      push("[", { color: CUT_TX, shading: { type: ShadingType.CLEAR, fill: CUT_BG, color: "auto" } });
      parts.forEach(p => {
        if (!p) return;
        const isB = p.startsWith("**");
        push(isB ? p.slice(2, -2) : p, { color: CUT_TX, italics: true, bold: isB, shading: { type: ShadingType.CLEAR, fill: CUT_BG, color: "auto" } });
      });
      push("]", { color: CUT_TX, shading: { type: ShadingType.CLEAR, fill: CUT_BG, color: "auto" } });
    }
    last = m.index + tok.length;
  }
  push(text.slice(last));
  return out;
}

const border = (c = LINE, sz = 4) => ({ style: BorderStyle.SINGLE, size: sz, color: c });
const cellBorders = { top: border(), bottom: border(), left: border(), right: border() };

// --- bloques
function pBody(text, o = {}) {
  return new Paragraph({
    spacing: { before: o.before ?? 0, after: o.after ?? 120, line: o.line ?? 288 },
    keepNext: !!o.keepNext, indent: o.indent,
    children: runs(text, o),
  });
}
function pSpeech(text) {
  return new Paragraph({ spacing: { before: 0, after: 200, line: 352 }, children: runs(text, { size: 26 }) });
}
function pStage(text) {
  return new Paragraph({
    spacing: { before: 120, after: 160 }, keepNext: true,
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: ORANGE, space: 8 } },
    indent: { left: 200 },
    children: [new TextRun({ font: FONT, size: 22, italics: true, color: MUT, text })],
  });
}
function h1(text, pageBreak = false) {
  return new Paragraph({
    pageBreakBefore: pageBreak, keepNext: true,
    spacing: { before: pageBreak ? 0 : 320, after: 140 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: ORANGE, space: 4 } },
    children: [new TextRun({ font: FONT, size: 32, bold: true, color: NAVY, text })],
  });
}
function h2(text) {
  return new Paragraph({
    keepNext: true, spacing: { before: 260, after: 100 },
    children: [new TextRun({ font: FONT, size: 24, bold: true, color: ORANGE_D, text })],
  });
}
function banner(num, titulo, tiempo) {
  const shade = { type: ShadingType.CLEAR, fill: NAVY, color: "auto" };
  return [
    new Paragraph({
      pageBreakBefore: true, keepNext: true, shading: shade,
      spacing: { before: 0, after: 0 }, indent: { left: 200, right: 200 },
      border: { top: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 10 }, left: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 10 }, right: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 10 } },
      children: [
        new TextRun({ font: FONT, size: 22, bold: true, color: ORANGE, characterSpacing: 40, text: `DIAPOSITIVA ${num}` }),
      ],
    }),
    new Paragraph({
      keepNext: true, shading: shade, spacing: { before: 40, after: 0 }, indent: { left: 200, right: 200 },
      border: { left: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 10 }, right: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 10 } },
      children: [new TextRun({ font: FONT, size: 40, bold: true, color: "FFFFFF", text: titulo })],
    }),
    new Paragraph({
      keepNext: true, shading: shade, spacing: { before: 40, after: 0 }, indent: { left: 200, right: 200 },
      border: { left: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 10 }, right: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 10 } },
      children: [new TextRun({ font: FONT, size: 20, color: "C5CEDF", text: tiempo })],
    }),
    new Paragraph({
      keepNext: true, shading: shade, spacing: { before: 0, after: 220, line: 120, lineRule: "exact" }, indent: { left: 200, right: 200 },
      border: { left: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 10 }, right: { style: BorderStyle.SINGLE, size: 6, color: NAVY, space: 10 } },
      children: [new TextRun({ font: FONT, size: 8, text: " " })],
    }),
  ];
}
function callout(text, o = {}) {
  return new Paragraph({
    spacing: { before: 100, after: 140, line: 300 },
    shading: { type: ShadingType.CLEAR, fill: o.fill || BEIGE, color: "auto" },
    border: { left: { style: BorderStyle.SINGLE, size: 24, color: o.bar || ORANGE_D, space: 8 } },
    indent: { left: 240, right: 120 },
    children: runs(text, { size: 22 }),
  });
}
function bullet(text, level = 0, o = {}) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { before: 0, after: o.after ?? 100, line: 288 }, keepLines: true,
    children: runs(text, { size: o.size || 22 }),
  });
}
function numbered(text, ref, o = {}) {
  return new Paragraph({
    numbering: { reference: ref, level: 0 },
    spacing: { before: o.before ?? 0, after: o.after ?? 100, line: 288 },
    shading: o.card ? { type: ShadingType.CLEAR, fill: BEIGE, color: "auto" } : undefined,
    children: runs(text, { size: o.size || 22 }),
  });
}

// --- tablas
function mdTable(rows, widths, hdrFills) {
  const mk = (cells, ri) => new TableRow({
    cantSplit: true, tableHeader: ri === 0,
    children: cells.map((c, ci) => new TableCell({
      width: { size: widths[ci], type: WidthType.DXA },
      borders: cellBorders,
      margins: { top: 90, bottom: 90, left: 120, right: 120 },
      shading: ri === 0
        ? { type: ShadingType.CLEAR, fill: hdrFills[ci], color: "auto" }
        : (ci === 0 ? { type: ShadingType.CLEAR, fill: BEIGE, color: "auto" } : undefined),
      children: [new Paragraph({
        spacing: { before: 0, after: 0, line: 264 },
        children: ri === 0
          ? [new TextRun({ font: FONT, size: 20, bold: true, color: "FFFFFF", text: c.replace(/\*\*/g, "") })]
          : runs(c, { size: 20, bold: ci === 0 }),
      })],
    })),
  });
  return new Table({
    width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: widths,
    rows: rows.map(mk),
  });
}

// --- armado
const children = [];
// tabla de resumen de las tres diapositivas, después de la portada (se inserta tras el título)
const resumen = [
  ["10", "B: recalentar con el calor que hoy tira el condensador", "Informe entregado (V2, verano húmedo). La hicieron tus compañeros."],
  ["11", "Mejoras de sustentabilidad, en tres familias", "Sección 4.5 del informe (Tabla 16): estimación anual aparte."],
  ["12", "Respuestas a la consigna 5", "Informe entregado. La hicieron tus compañeros."],
];
const resumenTbl = new Table({
  width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: [800, 4400, 4438],
  rows: [
    new TableRow({ tableHeader: true, cantSplit: true, children: ["Nº", "Diapositiva", "De dónde salen las cifras"].map((t, ci) => new TableCell({
      width: { size: [800, 4400, 4438][ci], type: WidthType.DXA }, borders: cellBorders,
      shading: { type: ShadingType.CLEAR, fill: NAVY, color: "auto" }, margins: { top: 90, bottom: 90, left: 120, right: 120 },
      children: [new Paragraph({ children: [new TextRun({ font: FONT, size: 20, bold: true, color: "FFFFFF", text: t })] })],
    })) }),
    ...resumen.map(r => new TableRow({ cantSplit: true, children: r.map((t, ci) => new TableCell({
      width: { size: [800, 4400, 4438][ci], type: WidthType.DXA }, borders: cellBorders,
      shading: ci === 0 ? { type: ShadingType.CLEAR, fill: BEIGE, color: "auto" } : undefined,
      margins: { top: 90, bottom: 90, left: 120, right: 120 },
      children: [new Paragraph({ children: [new TextRun({ font: FONT, size: 21, bold: ci < 2, color: ci === 0 ? ORANGE_D : INK, text: t })] })],
    })) })),
  ],
});

let section = "";
let i = 0;
let titulo = "";

// portada
function portada() {
  children.push(new Paragraph({
    spacing: { before: 0, after: 60 },
    children: [new TextRun({ font: FONT, size: 20, bold: true, color: ORANGE_D, characterSpacing: 40, text: "TP INTEGRADOR DE TERMODINÁMICA 2026 · HOSPITAL FAVALORO" })],
  }));
  children.push(new Paragraph({
    spacing: { before: 0, after: 80 },
    children: [new TextRun({ font: FONT, size: 52, bold: true, color: NAVY, text: titulo })],
  }));
}

while (i < lines.length) {
  const l = lines[i];
  if (l.startsWith("# ")) { titulo = l.slice(2).trim(); portada(); i++; continue; }
  if (l.startsWith("## ")) {
    const h = l.slice(3).trim();
    section = h;
    const ms = /^Diapositiva (\d+): (.*)$/.exec(h);
    if (ms) {
      const t = ms[2].charAt(0).toUpperCase() + ms[2].slice(1);
      children.push(...banner(ms[1], t, TIEMPOS[ms[1]] || ""));
      // leyenda de cortes, una sola vez, en la primera diapositiva
      if (ms[1] === "10") children.push(callout("**Cómo leerlo.** El texto grande es lo que se dice en voz alta. Lo **[sombreado entre corchetes]** se puede cortar si falta tiempo. En negrita van las cifras clave.", { bar: GREEN, fill: "E6F2EC" }));
    } else if (h === "Si te preguntan") {
      children.push(h1("Si te preguntan", true));
    } else if (h === "Glosario") {
      children.push(h1("Glosario", true));
    } else if (h === "Diapositiva 12") {
      children.push(...banner("12", "Respuestas a la consigna 5", TIEMPOS[12]));
    } else if (h.startsWith("Lo que se contradice")) {
      children.push(h1("Lo que se contradice entre tus tres diapositivas", false));
      children.push(pBody("Leer antes de exponer.", { color: ORANGE_D, bold: true, after: 100 }));
    } else if (h === "Si solo recordás cinco cosas") {
      children.push(h1("Si solo recordás cinco cosas", false));
    } else {
      children.push(h1(h, false));
    }
    i++; continue;
  }
  if (!l.trim()) { i++; continue; }

  // tabla markdown
  if (l.trim().startsWith("|")) {
    const rows = [];
    while (i < lines.length && lines[i].trim().startsWith("|")) {
      const cells = lines[i].trim().replace(/^\||\|$/g, "").split("|").map(s => s.trim());
      if (!cells.every(c => /^-+$/.test(c))) rows.push(cells);
      i++;
    }
    let widths, fills;
    if (rows[0][0] === "Tema") { widths = [2300, 3669, 3669]; fills = [NAVY, NAVY, ORANGE_D]; }
    else if (rows[0].length === 3) { widths = [1500, 5538, 2600]; fills = [NAVY, NAVY, NAVY]; }
    else { widths = [2300, 7338]; fills = [NAVY, NAVY]; }
    children.push(mdTable(rows, widths, fills));
    children.push(new Paragraph({ spacing: { before: 0, after: 120 }, children: [] }));
    continue;
  }

  const inSlide = /^Diapositiva \d+/.test(section) || section === "Diapositiva 12";

  // grupo de Q&A: línea que es solo **...**
  if (/^\*\*[^*]+\*\*$/.test(l.trim()) && (section === "Si te preguntan" || section === "Glosario")) {
    children.push(h2(l.trim().slice(2, -2))); i++; continue;
  }
  // indicación escénica
  if (/^\*\(.*\)\*$/.test(l.trim())) { children.push(pStage(l.trim().slice(1, -1))); i++; continue; }

  // los tres puntos iniciales se reemplazan por la tabla de resumen
  if (section === "" && /^- \*\*(10|11|12)\*\*:/.test(l)) {
    if (/^- \*\*10\*\*:/.test(l)) children.push(resumenTbl, new Paragraph({ spacing: { before: 0, after: 120 }, children: [] }));
    i++; continue;
  }
  // listas
  const mb = /^(\s*)- (.*)$/.exec(l);
  if (mb) {
    const lvl = mb[1].length >= 2 ? 1 : 0;
    const inQA = section === "Si te preguntan";
    children.push(bullet(mb[2], lvl, { after: inQA ? 140 : 100, size: inQA ? 22 : 22 }));
    i++; continue;
  }
  const mn = /^(\d+)\. (.*)$/.exec(l);
  if (mn) {
    if (section === "Si solo recordás cinco cosas") {
      children.push(numbered(mn[2], "num-cinco", { card: true, before: 60, after: 60, size: 23 }));
    } else {
      children.push(numbered(mn[2], "num-otras", { after: 100 }));
    }
    i++; continue;
  }

  // párrafo
  if (inSlide) children.push(pSpeech(l));
  else children.push(pBody(l, { size: 22, keepNext: /:\s*$/.test(l) }));
  i++;
}

const doc = new Document({
  creator: "Equipo TP Termodinámica", title: titulo, description: "Guion para la exposición oral",
  styles: { default: { document: { run: { font: FONT, size: 22 } } } },
  numbering: {
    config: [
      { reference: "bullets", levels: [
        { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 460, hanging: 280 } }, run: { color: ORANGE_D } } },
        { level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 920, hanging: 280 } }, run: { color: ORANGE_D } } },
      ] },
      { reference: "num-otras", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 460, hanging: 360 } }, run: { bold: true, color: ORANGE_D } } }] },
      { reference: "num-cinco", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 520, hanging: 400 } }, run: { bold: true, color: ORANGE_D, size: 26 } } }] },
    ],
  },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: 1134, bottom: 1134, left: MARGIN, right: MARGIN, header: 500, footer: 500 } } },
    headers: { default: new Header({ children: [new Paragraph({
      border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 4 } },
      children: [new TextRun({ font: FONT, size: 16, color: "8A8F98", text: "Guion · diapositivas 10 a 12 · TP Integrador de Termodinámica 2026" })],
    })] }) },
    footers: { default: new Footer({ children: [new Paragraph({
      tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_W }],
      children: [
        new TextRun({ font: FONT, size: 16, color: "8A8F98", text: "Borrador para revisar" }),
        new TextRun({ font: FONT, size: 16, color: "8A8F98", children: ["\tPágina ", PageNumber.CURRENT, " de ", PageNumber.TOTAL_PAGES] }),
      ],
    })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log("escrito", OUT, buf.length); });
