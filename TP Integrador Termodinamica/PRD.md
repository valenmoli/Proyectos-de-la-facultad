# PRD — TP Integrador de Termodinámica 2026

**Diseño de un sistema energético eficiente para un edificio (hospital)**
Facultad de Ingeniería y Ciencias Agrarias · Ing. Civil · UCA

> **Estado: BORRADOR v0.5 — para revisión. No hay nada construido todavía.**
> Los números técnicos que aparecen abajo son *pendientes de fuente*; no se fija ningún dato de diseño hasta resolver los bloqueos de la sección 0.
>
> **Cambios v0.4 → v0.5:** se recibieron y transcribieron los documentos del hospital de referencia (`datos/referencias_argentina.md`): **consumos estimados por auditoría de tres hospitales argentinos** (informe HCWH, 2021), El Cruce leído del original, y la pista del Austral cerrada (no trae cifras de energía). Se actualizan D5 y los chequeos de la sección 4, se agrega respaldo local a las mejoras de la sección 3 y se cierra la pregunta 11.
>
> **Cambios v0.3 → v0.4:** se recibió y transcribió la **versión completa** del artículo (consumo eléctrico, tabla resumen con supuestos de los autores, contraste con 23 hospitales, bibliografía). Se actualizan B2, B5 y B6, se propone el tamaño del hospital tipo (D4), se corrige el argumento del ACS en la Alt. B (el ACS es una demanda chica frente al calor del condensador) y se agrega el contraste con la intensidad energética anual del artículo a los chequeos de la sección 4.
>
> **Cambios v0.2 → v0.3:** se registra la decisión de ubicar el hospital tipo en Argentina (secciones 0.1 y 0.2), se documenta el acceso a fuentes desde el entorno y se actualizan las preguntas 2 y 10.
>
> **Cambios v0.1 → v0.2:** se recibió el PDF del artículo de Hospitecnia y se transcribió a [`datos/hospitecnia_datos.md`](datos/hospitecnia_datos.md). Se actualizan B2 y B4, se agregan B5 y B6, se amplía el rol de la caldera en la sección 2, se refuerza la Alt. B en la sección 3 y se agrega la pregunta 10. Se creó la estructura de carpetas (`datos/`, `calculo/`, `figuras/`, `informe/`, `presentacion/`).

---

## 0. Estado y bloqueos (leer primero)

| # | Hallazgo | Impacto |
|---|----------|---------|
| B1 | La consigna (PDF, 5 págs.) fue leída completa. | OK |
| B2 | **Resuelto.** El dominio sigue bloqueado en el entorno, pero se adjuntó el PDF de la versión completa (el primero estaba cortado por login). Trae la bibliografía (1) a (16). Las fuentes primarias (manuales y trabajos españoles) no son accesibles desde el entorno. | Datos transcriptos en [`datos/hospitecnia_datos.md`](datos/hospitecnia_datos.md) y [`datos/hospitales_internacionales.csv`](datos/hospitales_internacionales.csv). La fuente citable es el artículo, nombrando la referencia primaria que él cita. |
| B3 | La consigna dice que "podrán utilizarse los datos proporcionados en la consigna", **pero el PDF no trae ningún dato del edificio** (ni superficie, ni camas, ni clima, ni consumos). | Posible documento faltante o dato que dio el docente aparte. Hay que confirmarlo. |
| B4 | **Confirmado:** el artículo es una caracterización genérica (hospitales de España y algunos de Chile, Perú y Portugal), no un edificio concreto, y no trae clima ni consumos de Argentina. | Lo que vamos a diseñar es un *hospital tipo* parametrizado, salvo que ya haya un edificio real asignado. Los datos del artículo son órdenes de magnitud, no valores de diseño. |
| B5 | El artículo tiene **cifras internamente inconsistentes**: gas y gasóleo de Madrid, camas de Coímbra, totales y salto eléctrico de Navarra, porcentajes de Chile, consumo térmico por m² entre filas, y potencia y consumo de ACS. Son 19 casos (E-01 a E-19) con su cálculo en la sección E de `datos/hospitecnia_datos.md`. | No se usan esas cifras. Si se cita alguna en el informe, se aclara la inconsistencia. |
| B6 | **No trae** condiciones interiores ni renovaciones de aire, clima de diseño, refrigerante ni composición del gas (sección F de `datos/hospitecnia_datos.md`). **Sí trae supuestos de conversión de los autores** (sección D4 de los datos): 150 m²/cama, caldera al 90 %, COP 4, 10,8 kWh/m³ de gas sin aclarar si es PCS o PCI, y 6,5 h/día equivalentes de refrigeración. | Hacen falta fuentes complementarias para aire húmedo, refrigeración y combustión. Ver pregunta 10. Los supuestos de los autores son un punto de partida a contrastar, no datos. |

### 0.1 Decisiones tomadas

| # | Decisión | Origen |
|---|----------|--------|
| D1 | El proyecto es un **hospital tipo ubicado en Argentina**, parametrizado con el artículo de Hospitecnia y completado con fuentes locales. | Usuario, 2026-11-03 |
| D2 | Ciudad de referencia: **AMBA (Buenos Aires)**. | Usuario, 2026-11-03 |
| D3 | Las fuentes complementarias las busco yo (clima, normativa, gas natural, refrigerantes). | Interpretación de "una vez tengas esos datos"; **a confirmar** |
| D4 | Hospital tipo de **unos 20.000 m² con 150 m²/cama (unas 130 camas)**, el "hospital de tamaño medio" del propio artículo. | Propuesta mía, confirmada por el usuario, 2026-11-03 |
| D5 | Buscar un **hospital real del AMBA** como **referencia** para contrastar el hospital tipo. Tiene que ser de la **misma magnitud**, no igual: del orden de 10.000 a 50.000 m² y de 60 a 300 camas. Pesa más que tenga datos documentados (superficie, camas, climatización, consumos) que la cercanía exacta al tamaño. No reemplaza al hospital tipo. **Estado:** **El Cruce** (Florencio Varela) leído del documento original: 22.000 m² cubiertos, 140 camas (2010), 157 m²/cama; es de alta complejidad. **Consumos estimados por auditoría** de tres hospitales argentinos (no medidos) en el informe HCWH 2021; el único del AMBA es el Garrahan (259 kWh/m²·año), pero es 6 veces más grande. Ninguno es un hospital del AMBA de unos 20.000 m² con consumo publicado. Detalle en [`datos/referencias_argentina.md`](datos/referencias_argentina.md); otros candidatos de tamaño, sin verificar, en [`datos/hospital_referencia.md`](datos/hospital_referencia.md). | Usuario, 2026-11-03 |
| D6 | **El consumo de energía se calcula, no se copia de las referencias.** Es un resultado del modelo: carga frigorífica, trabajo del compresor y electricidad del chiller, combustible de la caldera y energía anual. El artículo, el informe HCWH y los 23 hospitales solo **contrastan** el resultado. | Usuario, 2026-11-03; coincide con la Consigna 3 |
| D7 | El hospital de referencia se elige entre **Favaloro** (La Matanza) y **Nordelta** (Tigre): el que tenga **más información relevante**; lo que no se tenga **se estima** como supuesto declarado. **Selección provisoria: Favaloro** (La Matanza). Es un **juicio de ponderación y no un conteo**: contando cada fila con algún dato empatan en 7 de 9. La superficie cubierta es la variable que dimensiona el modelo; Favaloro la trae (18.352 m², con otra cifra de más de 20.000 declarada) y ningún documento de Nordelta la trae. La selección se reabre si se confirma la superficie de Nordelta (24.000 m² según una nota de 2018 que no está entre los documentos). De Nordelta se conserva, de forma cualitativa, la recuperación de calor del aire de extracción. Detalle en [`datos/favaloro_nordelta.md`](datos/favaloro_nordelta.md). | Criterio: usuario, 2026-11-03. Selección: mía, a confirmar |

### 0.2 Cómo se adapta el artículo a Argentina

El artículo describe hospitales de España. Para no mezclar climas:

- **Se conserva** lo que depende del uso hospitalario y no del clima: ACS por cama y su temperatura, superficie por cama, combustible dominante (gas natural), y los repartos por uso y la intensidad anual (380 kWh/m²·año en el resumen del artículo; 23 hospitales internacionales entre 120 y 900, mediana 333) como **chequeo** de orden de magnitud. **El ACS es un caso aparte:** los ratios de diseño del artículo (200 a 300 L/cama·día) y sus casos medidos (50 a 55 L/cama·día) difieren de 4 a 6 veces (E-14), así que hay que elegir un valor y justificarlo. El ACS se calcula desde L/cama·día y el salto de temperatura, no desde la fila de 10 W/m² de la tabla del artículo, que es inconsistente con su propio caudal (E-15).
- **Se recalcula** lo que depende del clima. Las cargas de refrigeración y calefacción se obtienen con el modelo de aire húmedo y el clima de diseño local. Los **115 y 90 W/m² del artículo quedan como chequeo, no como entrada.** Motivos: el verano del AMBA es húmedo, con una carga latente importante que un ratio por m² de otro clima no captura, y calcular las cargas desde el balance es justamente lo que pide la Consigna 3 para aire húmedo.
- **Se consigue localmente:** clima de diseño (verano e invierno) y estado muerto; condiciones interiores y renovaciones de aire por zona según la normativa aplicable; PCS y composición del gas natural de red; factor de emisión de la electricidad de red; refrigerantes disponibles y su regulación.
- **Cuando no hay dato citable**, la consigna permite supuestos fundamentados. Cada uno se marca como *supuesto* en `datos/` con su justificación y se reemplaza por el dato citable si aparece.

**Acceso a fuentes desde el entorno (probado el 2026-11-03):** solo responde PyPI y la API de GitHub. Los sitios argentinos probados (SMN, ENARGAS, argentina.gob.ar, Boletín Oficial, energía.gob.ar, IRAM) y NOAA están bloqueados, igual que Hospitecnia. La búsqueda web devuelve fragmentos sin los valores de diseño; ni siquiera pudo dar temperaturas de diseño de Buenos Aires con una fuente confiable. **Dominios que habría que habilitar para cumplir D3:** `ncei.noaa.gov` (datos de ingeniería de la estación Ezeiza), `smn.gob.ar`, `enargas.gob.ar`, `argentina.gob.ar`, `boletinoficial.gob.ar`, `energia.gob.ar`.

**Pistas sin verificar (no usar hasta confirmar con la fuente):** un extracto de búsqueda indica que el límite máximo del PCS del gas natural en la regulación del ENARGAS pasó de 10.200 a 10.700 kcal/m³, y que 9.300 kcal/m³ se usa como referencia de facturación. No hay texto de la resolución a la vista. Dato útil si se confirma: 9.300 kcal/m³ equivalen a 10,82 kWh/m³, casi exactamente los 10,8 kWh/m³ que usa el artículo; si el valor argentino resulta ser PCS, ese supuesto sería utilizable tal cual.

## 1. Problema

Un hospital es un edificio de alta intensidad energética que opera 24/7 y cuya climatización no es de confort sino de proceso: requiere renovación de aire alta, control estricto de temperatura y humedad en zonas críticas (quirófanos, terapia intensiva) y agua caliente / vapor para ACS y esterilización.

**Qué hay que resolver:** definir, modelar y evaluar termodinámicamente el sistema que cubre esas necesidades térmicas, comparar al menos dos configuraciones y proponer mejoras fundadas en la 1.ª y 2.ª ley.

## 2. Tesis de integración (cómo se conectan los 4 temas)

La consigna penaliza tratar los temas por separado ("deberá explicitarse cómo se relacionan"). Propuesta de hilo conductor — **una sola cadena de equipos, cuatro lentes**:

```
Aire exterior ─► [Mezcla con retorno] ─► [Serpentina de enfriamiento y deshumidificación] ─► [Recalentamiento] ─► Zona crítica
 (AIRE HÚMEDO)                              ▲ carga frigorífica                                  ▲ calor
                                            │                                                    │
                                   [Chiller: ciclo de compresión]                      [Caldera a gas natural]
                                      (REFRIGERACIÓN) ─ rechaza Q_H al ambiente           (COMBUSTIÓN)

                         EXERGÍA: balance y destrucción por equipo, con estado muerto = condiciones exteriores
```

- **Aire húmedo →** fija la carga frigorífica (sensible + latente) y el calor de recalentamiento.
- **Refrigeración →** la carga de la serpentina es la capacidad del chiller; de ahí salen W_comp, COP, Q_H.
- **Combustión →** la caldera aporta el recalentamiento, la calefacción de invierno y el ACS. Según el artículo, calefacción y ACS son la mayor parte del consumo térmico y el gas natural es el combustible dominante (73 % en España, 2011). De ahí salen consumo de gas, T de rocío de los gases, CO₂.
- **Exergía →** une todo: dónde se destruye capacidad de hacer trabajo.
- **El punto que lo hace un problema único (no cuatro):** el sistema enfría el aire para deshumidificar y luego lo recalienta con combustible, mientras el chiller *rechaza* al ambiente calor a ~40–55 °C que podría cubrir ese recalentamiento. Es una ineficiencia exergética visible (usar una llama a >1000 °C para subir aire unos pocos grados) y es la base natural de la mejora.

## 3. Alternativas y mejoras a evaluar (Consigna 4)

| | Propuesta | Por qué |
|---|-----------|---------|
| **Alt. A (base)** | Chiller + caldera a gas para recalentamiento y ACS | Configuración convencional; línea de base |
| **Alt. B** | Chiller con **recuperación de calor del condensador** para recalentamiento y precalentamiento de ACS; caldera de respaldo | Ataca la ineficiencia de la sección 2. **Cuidado con el ACS:** es una demanda continua pero chica frente al calor del condensador. Con 55 a 200 L/cama·día, unas 130 camas necesitan entre 16 y 58 kW medios de ACS (de 15 a 60 °C), contra unos 2.500 kW de calor de condensador si la refrigeración es de 2.000 kW (100 W/m² en 20.000 m²) con COP 4. Esos valores son los del artículo, no del hospital tipo. El sumidero principal tendría que ser el recalentamiento. *Hipótesis a verificar con el cálculo.* |
| Opc. C | Caldera de condensación sobre A o B | Variante dentro del módulo de combustión |

Mejoras candidatas (la consigna exige ≥ 2, explicadas desde la Termodinámica; elegir 2–3 que se puedan **cuantificar** con el mismo modelo):
1. Recuperación de calor del condensador (es la Alt. B).
2. Control de exceso de aire / caldera de condensación (menos pérdida en gases, aprovecha calor latente).
3. Recuperación sensible/entálpica del aire de extracción mediante serpentinas de circuito cerrado (evita contaminación cruzada, que en hospital es restricción dura).
4. Mayor temperatura de evaporación / menor *lift* del compresor.

Respaldo local para las mejoras (informe HCWH 2021 sobre hospitales argentinos, `datos/referencias_argentina.md` sección 3): reemplazar splits por VRF con recuperación de calor podría ahorrar hasta 40 % de la energía (Giordano) y 26 % en un laboratorio (CEMAR); un precalentamiento solar de 300 L/día de agua a 50 °C ahorraría más del 80 % de la energía de ese uso. Son estimaciones de los auditores, no mediciones.

## 4. Criterios de éxito (trazabilidad consigna → entregable → chequeo)

| Consigna | Qué exige | Dónde queda | Chequeo de aceptación |
|---|---|---|---|
| 1 | Problema, necesidades, elección de contenidos, esquema, hipótesis | Informe §2–3 | Cada hipótesis con su justificación y fuente |
| 2 | Sistemas y límites, estados, balances, diagramas | Informe §4 + Memoria | Tabla de estados completa (T, P, h, s, ṁ) por equipo |
| 3 | W y COP, capacidad; reacción y consumo; propiedades psicrométricas y cargas S/L; balance exergético y η_ex | Memoria de cálculo | Unidades en todo; ecuación + procedimiento + fuente de cada propiedad |
| 4 | ≥ 2 alternativas, indicadores, focos de pérdida, ventajas/limitaciones, ≥ 2 mejoras | Informe §6 | Tabla comparativa + diagrama de flujo de exergía |
| 5 | Responder las 5 preguntas con resultados | Informe §7 | Cada respuesta cita un número calculado (la consigna prohíbe afirmaciones genéricas) |

**Entregables:** informe técnico 8–12 págs. · memoria de cálculo · representación gráfica (esquema + diagramas termodinámicos) · exposición oral 10–15 min.
**Se evalúa:** aplicación correcta de conceptos, coherencia de cálculos, integración, análisis crítico, fundamentación de decisiones.

### Chequeos termodinámicos automáticos (los corre el código en cada cambio)
- **1.ª ley:** cierra el balance de energía en cada equipo.
- **2.ª ley:** entropía generada ≥ 0 por componente; COP_real < COP_Carnot; Ẋ_dest ≥ 0; ΣẊ_ent = ΣẊ_sal + ΣẊ_dest.
- **Combustión:** balance atómico C, H, O, N; T de rocío de los gases; PCS/PCI contra valor de referencia.
- **Psicrometría:** Q_total = ṁ_a·Δh coincide con Q_sensible + Q_latente; humedades y φ en rango físico.
- **Propiedades:** valores de CoolProp contrastados con 3 puntos de las tablas del libro de la cátedra.
- **Contraste con la fuente (banda de plausibilidad, no validación puntual):** la intensidad energética anual del hospital tipo se compara con los 380 kWh/m²·año del resumen del artículo (mezcla calor útil con electricidad: en energía final son 394 a 400; hay que declarar la base, E-16) y con los 23 hospitales de `datos/hospitales_internacionales.csv` (120 a 900 kWh/m²·año). La potencia frigorífica y la de calefacción se comparan con 100 a 115 y 70 a 90 W/m², que son de España. También con los tres hospitales argentinos auditados por HCWH: **163 a 259 kWh/m²·año** de energía final, estimada (n = 3, dos fuera del AMBA); el del AMBA, el Garrahan, da 259.

## 5. Alcance

**Dentro**
- Punto de diseño de verano (carga máxima) y, si alcanza, uno de invierno.
- Planta térmica del edificio completa a nivel conceptual + **una zona crítica** (quirófano) como caso psicrométrico detallado.
- Comparación Alt. A vs Alt. B con indicadores energéticos, exergéticos y de emisiones.
- **Consumo anual de energía del sistema** (electricidad y combustible), calculado con un método simplificado a partir de los puntos de diseño y contrastado con las referencias (D6). Ver preguntas 12 y 13.

**Fuera (por consigna o por decisión mía, a discutir)**
- Proyecto ejecutivo, planos, presupuesto (la consigna lo excluye).
- Simulación anual horaria.
- **Iluminación, cocina, lavandería, equipos médicos, etc.** El artículo los va a caracterizar, pero no son Termodinámica de los 4 temas. *Mi propuesta: usarlos solo para dimensionar la participación de la climatización en el consumo total y justificar por qué el foco es HVAC + térmico.* Si querés incluir más, ampliamos.

## 6. Restricciones y supuestos
- Informe 8–12 págs.; oral 10–15 min (≈ 10–14 diapositivas).
- Español técnico; SI; cada propiedad con fuente.
- El estado muerto del análisis exergético (T₀, P₀) tiene que ser consistente con el clima elegido.
- Normativa de ventilación hospitalaria (ASHRAE 170 y normativa argentina de Salud) **a relevar y citar**; no fijo valores de memoria.
- Es un trabajo de equipo evaluado también en defensa oral: todo lo que armemos tiene que poder explicarse y defenderse. Voy a incluir una guía de preguntas probables del docente.

## 7. Herramientas (lo que ya existe en el entorno)
| Necesidad | Disponible hoy | Falta (instalable desde PyPI, verificado con `--dry-run`) |
|---|---|---|
| Cálculo | Python 3.13, numpy, pandas | scipy |
| Propiedades de refrigerantes | — | CoolProp |
| Psicrometría | — | psychrolib |
| Gráficos (P-h, carta psicrométrica, Grassmann) | — | matplotlib |
| Informe / memoria | pandoc, LibreOffice, python-docx | — |
| Presentación | python-pptx | — |
| Tests | — | pytest |

**Propuesta de pipeline:** el código de cálculo es la **única fuente de verdad** de los números; el informe y la memoria se generan desde él (Markdown con ecuaciones → pandoc → DOCX con ecuaciones nativas de Word → PDF). Así los valores del informe, la memoria y las diapositivas no pueden contradecirse (criterio "coherencia de los cálculos").

## 8. Plan por hitos (reviso con vos al cierre de cada uno)
| Hito | Contenido | Salida |
|---|---|---|
| **M0** | Aprobar este PRD y resolver bloqueos B2–B4 | Datos del edificio en mano |
| **M1** | Consigna 1: ficha del edificio, necesidades, tabla de hipótesis | `datos/` + borrador §2–3 |
| **M2** | Consigna 2: sistemas, límites, estados, esquema | Esquema + tabla de estados |
| **M3** | Consigna 3: motor de cálculo (refrigeración, aire húmedo, combustión, exergía) + tests | `calculo/` con chequeos verdes. **Verificación independiente:** otro revisor rehace cada cálculo desde cero sin ver mis resultados y se comparan. |
| **M4** | Consigna 4: Alt. A vs B, mejoras, sensibilidades | Tabla comparativa + Grassmann |
| **M5** | Consigna 5: conclusiones ligadas a números | §7 del informe |
| **M6** | Informe, memoria, figuras, diapositivas, guion oral, preguntas de defensa | DOCX + PDF + PPTX |

## 9. Riesgos
| Riesgo | Mitigación |
|---|---|
| Datos del artículo no disponibles / sesgo a otro país (ej. kWh por cama de España) | Resolver B2; si los datos son de otro clima/país, adaptarlos explícitamente y declararlo |
| Pasar de 12 págs. con 4 temas + 2 alternativas | Cuerpo del informe solo con resultados y análisis; desarrollo en la memoria |
| Estado muerto mal elegido arruina el análisis exergético | Fijarlo en M1 y documentarlo |
| Resultados "demasiado lindos" (ej. COP irreal) | Los chequeos de la 2.ª ley son bloqueantes |
| Dependencia de CoolProp si la cátedra exige tablas | Contrastar con tablas del libro (§4) y citar ambas |

## 10. Preguntas abiertas

**Bloqueantes (sin esto no avanzo a M1):**
1. **Resuelto:** versión completa del artículo recibida y transcripta.
2. **Resuelto:** hospital tipo en el AMBA, de unos 20.000 m² y unas 130 camas (D1, D2, D4).
3. **Datos "de la consigna":** ¿el docente pasó otro documento con datos del edificio? ¿Está validado que usemos Hospitecnia como base?

**Asumo lo siguiente salvo que me digas lo contrario:**
4. Alcance de la sección 5 (planta térmica + quirófano como caso detallado, verano como punto de diseño).
5. Alt. A vs B (+ C opcional) y las mejoras de la sección 3.
6. Formato final: informe DOCX + PDF, memoria aparte, diapositivas PPTX. Carpeta `TP Integrador Termodinamica/` en este repo.

**Necesito saber (no bloquean M1):**
7. ¿Cuántos son en el equipo y quién expone?
8. Libro y tablas de la cátedra (Çengel, Moran-Shapiro, otro) y si CoolProp es aceptable como fuente.
9. Fecha de entrega y de exposición. ¿La memoria de cálculo cuenta dentro de las 8–12 págs.?
10. **Fuentes complementarias** (B6, D3): el artículo no trae condiciones de diseño del aire, normativa de ventilación, clima, COP ni rendimiento de caldera. Desde este entorno no puedo alcanzar las fuentes argentinas (sección 0.2). ¿Habilitás los dominios de la sección 0.2, o los pasa la cátedra, o seguimos con supuestos fundamentados y marcados como tales?
11. **Resuelto:** documentos del hospital de referencia recibidos y transcriptos (`datos/referencias_argentina.md`).
12. **Frontera del consumo calculado** (D6). Las referencias miden el edificio entero (iluminación, equipos médicos, cocina, lavandería), pero el TP modela el sistema térmico. Propuesta: **calculamos solo el sistema térmico** (frío, recalentamiento, calefacción, ACS y auxiliares como bombas y ventiladores) y lo comparamos con la parte de climatización y ACS de las referencias, que es la mitad aproximada del total. Alternativa: sumar el resto como un supuesto declarado y comparar totales, lo que agrega incertidumbre que no se calcula. ¿Cuál preferís?
13. **Cómo pasar de los puntos de diseño al consumo anual.** El alcance excluye la simulación horaria. Propuesta: método simple de **3 a 5 condiciones climáticas ponderadas por horas al año** (verano pleno, verano suave, media estación, invierno), que necesita datos de frecuencia del clima del AMBA. Si no los conseguimos, se usa el método del artículo: **horas equivalentes a plena carga**, declaradas como supuesto (1.200 h para refrigeración y 1.556 h para calefacción en su tabla). ¿Estás de acuerdo con empezar por las horas equivalentes y pasar a las condiciones ponderadas si aparece el dato climático?
14. **Resuelto:** documentos de Favaloro y Nordelta recibidos y transcriptos (`datos/favaloro_nordelta.md`). Queda a confirmar la selección de **Favaloro** (D7).
