# PRD — TP Integrador de Termodinámica 2026

**Diseño de un sistema energético eficiente para un edificio (hospital)**
Facultad de Ingeniería y Ciencias Agrarias · Ing. Civil · UCA

> **Estado: BORRADOR v0.3 — para revisión. No hay nada construido todavía.**
> Los números técnicos que aparecen abajo son *pendientes de fuente*; no se fija ningún dato de diseño hasta resolver los bloqueos de la sección 0.
>
> **Cambios v0.2 → v0.3:** se registra la decisión de ubicar el hospital tipo en Argentina (secciones 0.1 y 0.2), se documenta el acceso a fuentes desde el entorno y se actualizan las preguntas 2 y 10.
>
> **Cambios v0.1 → v0.2:** se recibió el PDF del artículo de Hospitecnia y se transcribió a [`datos/hospitecnia_datos.md`](datos/hospitecnia_datos.md). Se actualizan B2 y B4, se agregan B5 y B6, se amplía el rol de la caldera en la sección 2, se refuerza la Alt. B en la sección 3 y se agrega la pregunta 10. Se creó la estructura de carpetas (`datos/`, `calculo/`, `figuras/`, `informe/`, `presentacion/`).

---

## 0. Estado y bloqueos (leer primero)

| # | Hallazgo | Impacto |
|---|----------|---------|
| B1 | La consigna (PDF, 5 págs.) fue leída completa. | OK |
| B2 | **Resuelto en parte.** El dominio sigue bloqueado en el entorno, pero se adjuntó el PDF. **El artículo está cortado por login** al final de la sección de ACS: falta lo que sigue y la bibliografía, así que las citas (1) a (15) no se pueden identificar. | Datos transcriptos en [`datos/hospitecnia_datos.md`](datos/hospitecnia_datos.md). Hay que decidir si alcanza o se consigue el texto completo. |
| B3 | La consigna dice que "podrán utilizarse los datos proporcionados en la consigna", **pero el PDF no trae ningún dato del edificio** (ni superficie, ni camas, ni clima, ni consumos). | Posible documento faltante o dato que dio el docente aparte. Hay que confirmarlo. |
| B4 | **Confirmado:** el artículo es una caracterización genérica (hospitales de España y algunos de Chile, Perú y Portugal), no un edificio concreto, y no trae clima ni consumos de Argentina. | Lo que vamos a diseñar es un *hospital tipo* parametrizado, salvo que ya haya un edificio real asignado. Los datos del artículo son órdenes de magnitud, no valores de diseño. |
| B5 | El artículo tiene **cifras internamente inconsistentes** (gasóleo y gas de Madrid, Coímbra, porcentajes de Chile). Detalle y cálculo en la sección E de `datos/hospitecnia_datos.md`. | No se usan esas cifras. Si se cita alguna en el informe, se aclara la inconsistencia. |
| B6 | **No trae** condiciones interiores y renovaciones de aire, clima de diseño, COP, rendimiento de caldera ni composición del combustible (sección F de `datos/hospitecnia_datos.md`). | Hacen falta fuentes complementarias para los cálculos de aire húmedo, refrigeración y combustión. Ver pregunta 10. |

### 0.1 Decisiones tomadas

| # | Decisión | Origen |
|---|----------|--------|
| D1 | El proyecto es un **hospital tipo ubicado en Argentina**, parametrizado con el artículo de Hospitecnia y completado con fuentes locales. | Usuario, 2026-11-03 |
| D2 | Ciudad de referencia: **AMBA (Buenos Aires)**. | Supuesto mío, **a confirmar** |
| D3 | Las fuentes complementarias las busco yo (clima, normativa, gas natural, refrigerantes). | Interpretación de "una vez tengas esos datos"; **a confirmar** |

### 0.2 Cómo se adapta el artículo a Argentina

El artículo describe hospitales de España. Para no mezclar climas:

- **Se conserva** lo que depende del uso hospitalario y no del clima: ACS por cama y su temperatura, superficie por cama, combustible dominante (gas natural), y los repartos por uso como **chequeo** de orden de magnitud.
- **Se recalcula** lo que depende del clima. Las cargas de refrigeración y calefacción se obtienen con el modelo de aire húmedo y el clima de diseño local. Los **115 y 90 W/m² del artículo quedan como chequeo, no como entrada.** Motivos: el verano del AMBA es húmedo, con una carga latente importante que un ratio por m² de otro clima no captura, y calcular las cargas desde el balance es justamente lo que pide la Consigna 3 para aire húmedo.
- **Se consigue localmente:** clima de diseño (verano e invierno) y estado muerto; condiciones interiores y renovaciones de aire por zona según la normativa aplicable; PCS y composición del gas natural de red; factor de emisión de la electricidad de red; refrigerantes disponibles y su regulación.
- **Cuando no hay dato citable**, la consigna permite supuestos fundamentados. Cada uno se marca como *supuesto* en `datos/` con su justificación y se reemplaza por el dato citable si aparece.

**Acceso a fuentes desde el entorno (probado el 2026-11-03):** solo responde PyPI y la API de GitHub. Los sitios argentinos probados (SMN, ENARGAS, argentina.gob.ar, Boletín Oficial, energía.gob.ar, IRAM) y NOAA están bloqueados, igual que Hospitecnia. La búsqueda web devuelve fragmentos sin los valores de diseño; ni siquiera pudo dar temperaturas de diseño de Buenos Aires con una fuente confiable. **Dominios que habría que habilitar para cumplir D3:** `ncei.noaa.gov` (datos de ingeniería de la estación Ezeiza), `smn.gob.ar`, `enargas.gob.ar`, `argentina.gob.ar`, `boletinoficial.gob.ar`, `energia.gob.ar`.

**Pistas sin verificar (no usar hasta confirmar con la fuente):** un extracto de búsqueda indica que el límite máximo del PCS del gas natural en la regulación del ENARGAS pasó de 10.200 a 10.700 kcal/m³, y que 9.300 kcal/m³ se usa como referencia de facturación. No hay texto de la resolución a la vista.

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
| **Alt. B** | Chiller con **recuperación de calor del condensador** para recalentamiento y precalentamiento de ACS; caldera de respaldo | Ataca la ineficiencia de la sección 2. El ACS es una demanda continua las 24 h (200 a 300 L/cama·día según el artículo) que puede absorber calor del condensador. *Hipótesis a verificar con el cálculo.* |
| Opc. C | Caldera de condensación sobre A o B | Variante dentro del módulo de combustión |

Mejoras candidatas (la consigna exige ≥ 2, explicadas desde la Termodinámica; elegir 2–3 que se puedan **cuantificar** con el mismo modelo):
1. Recuperación de calor del condensador (es la Alt. B).
2. Control de exceso de aire / caldera de condensación (menos pérdida en gases, aprovecha calor latente).
3. Recuperación sensible/entálpica del aire de extracción mediante serpentinas de circuito cerrado (evita contaminación cruzada, que en hospital es restricción dura).
4. Mayor temperatura de evaporación / menor *lift* del compresor.

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

## 5. Alcance

**Dentro**
- Punto de diseño de verano (carga máxima) y, si alcanza, uno de invierno.
- Planta térmica del edificio completa a nivel conceptual + **una zona crítica** (quirófano) como caso psicrométrico detallado.
- Comparación Alt. A vs Alt. B con indicadores energéticos, exergéticos y de emisiones.

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
1. **Artículo:** recibido (PDF de 15 págs.), pero cortado por login. ¿Tenés acceso al texto completo con suscripción, o lo damos por suficiente para esta fuente?
2. **Decidido:** hospital tipo en Argentina (D1). Falta confirmar la ciudad: asumo AMBA (Buenos Aires). ¿Es correcta? La cantidad de camas y la superficie las propongo yo desde los ratios del artículo en el hito M1, salvo que la cátedra fije una.
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
