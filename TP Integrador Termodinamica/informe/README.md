# informe/

Informe técnico y memoria de cálculo (hito **M6**).

## Entregables
- **Informe técnico**: entre 8 y 12 páginas. Introducción, objetivos, descripción del sistema, metodología, cálculos, resultados, discusión y conclusiones.
- **Memoria de cálculo**: desarrollo ordenado de ecuaciones, datos, hipótesis, unidades y resultados. Va separada del informe.

## Cómo se generan
Markdown con ecuaciones, convertido con pandoc a DOCX (ecuaciones nativas de Word) y a PDF vía HTML con MathML impreso con Chromium. Los números se toman de `calculo/` y las figuras de `figuras/`.

## Pendiente de confirmar
Si la memoria de cálculo cuenta dentro de las 8 a 12 páginas (pregunta 9 del [PRD](../PRD.md)). El informe tiene hoy unas 9 páginas con las referencias, así que entra en cualquiera de las dos lecturas.

## Estado
- `informe.plantilla.md` y `memoria_calculo.plantilla.md` son el texto del **informe técnico** (decisiones, motivos y respaldo de cada dato) y de la **memoria de cálculo** (ecuaciones, estados, supuestos), con marcadores `{{valor}}`. `python -m calculo.construir_documentos` los completa con los números del modelo y escribe `informe_tecnico.*` y `memoria_calculo.*` (`.md`, `.docx` y `.pdf`). **No editar los `.md` generados: se editan las plantillas** (y `calculo/texto_equipos.py` y `calculo/texto_exergia.py` para esas secciones).
- `01_planteamiento.md` y `02_estimacion_consumos.md` son los borradores v0.1 previos al rework; `resultados_consumo.*` y `supuestos.md` los genera `calculo/generar_resultados.py`.
- Falta: presentación oral, cotejar con la fuente original todo lo marcado «cita» y reemplazar los supuestos de clima y de ASHRAE 170.
