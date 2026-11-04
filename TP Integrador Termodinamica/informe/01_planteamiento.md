# Planteamiento del proyecto

**Borrador v0.1 para revisión.** Corresponde a la Consigna 1 (definición del problema y selección del sistema). Las cifras de consumo están en [`resultados_consumo.md`](resultados_consumo.md) y los supuestos en [`supuestos.md`](supuestos.md); este documento no las repite para no desfasarse.

## 1. El edificio

Se modela un hospital general de agudos de alta complejidad del AMBA, tomando como referencia el **Hospital Dr. René Favaloro (SAMIC), Rafael Castillo, La Matanza**. La elección y sus salvedades están en [`../datos/favaloro_nordelta.md`](../datos/favaloro_nordelta.md).

| Dato | Valor | Estado |
|---|---|---|
| Superficie cubierta | 18.352 m² (otra cifra declarada: más de 20.000 m² de construcción) | Dato |
| Camas | 144 de internación general y 14 de terapia intensiva | Dato (se interpreta como el total) |
| Quirófanos | 6 | Dato de programa |
| Niveles | Tres pisos; quirófanos y áreas críticas en el 2.º; guardia y diagnóstico en el 1.º | Dato |
| Funcionamiento | Guardia las 24 h; internación y áreas críticas continuas | Dato (guardia) y supuesto |
| Ubicación y clima | AMBA, clima templado y húmedo | Supuesto (valores a reemplazar por el SMN) |

## 2. La problemática energética

Un hospital opera todo el año y todo el día, y parte de su climatización no es de confort sino de **proceso**: los quirófanos, la terapia intensiva y las habitaciones requieren temperatura y humedad controladas, presión positiva y una cantidad mínima de aire exterior filtrado. En el clima del AMBA eso tiene una consecuencia termodinámica concreta:

1. El aire exterior de verano es cálido y muy húmedo (el punto de diseño supuesto es de 34 °C con 25 °C de bulbo húmedo, unos 16 g de vapor por kg de aire seco).
2. Para llevarlo a las condiciones de la zona (22 a 24 °C y menos de 60 % de humedad relativa) hay que **enfriarlo por debajo de su punto de rocío**, hasta unos 12 a 13 °C, para condensar el vapor.
3. A esa temperatura el aire ya no sirve para impulsarlo: hay que **recalentarlo** con otra fuente de energía, en este caso la caldera de gas. Se gasta frío para quitar humedad y calor para devolverle temperatura.
4. En las zonas de funcionamiento continuo y con poca carga térmica (quirófanos de noche, terapia intensiva), este recalentamiento ocurre durante gran parte del año.

A eso se suman la demanda de **agua caliente sanitaria** (todo el año), la **calefacción** de invierno y el consumo eléctrico de ventiladores y bombas, que en un sistema de aire con tantas renovaciones es muy relevante.

**Pregunta del proyecto:** ¿cuánta energía consume este sistema, dónde se pierde la mayor parte, y qué configuración o medidas la reducen, medido con la Primera y la Segunda Ley?

Las referencias disponibles son órdenes de magnitud del edificio completo: 163 a 259 kWh/m²·año en tres hospitales argentinos auditados (estimados), 380 a 400 en el modelo español del artículo de Hospitecnia y una mediana de 333 en 23 hospitales internacionales (ver [`../datos/referencias_argentina.md`](../datos/referencias_argentina.md)).

## 3. Necesidades térmicas que el sistema debe satisfacer

| Zona | Superficie [m²] | Condiciones de proyecto | Aire | Funcionamiento |
|---|---|---|---|---|
| G1 Quirófanos (6 salas) | 252 | 22 °C, humedad máx. 55 %, mín. 30 % | 20 renovaciones totales, 4 de aire exterior | Continuo; actividad de día |
| G2 Terapia intensiva (14 camas) | 336 | 23 °C, humedad máx. 55 % | 6 renovaciones, 2 de aire exterior | Continuo |
| G3 Internación general (144 camas) | 4.032 | 24 °C verano, 22 °C invierno, humedad máx. 55 % | 4 renovaciones, 2 de aire exterior | Continuo |
| G4 Guardia, imágenes y laboratorio | 3.843 | 24 °C verano, 22 °C invierno, humedad máx. 60 % | 6 renovaciones, 2 de aire exterior | 24 h |
| G5 Consultorios, administración y docencia | 7.136 | Ídem, humedad máx. 60 % | 3 renovaciones, 1 de aire exterior | De día (12 h) |

Los valores de renovaciones y humedades se toman de ASHRAE 170 **como se recuerdan, y están marcados para verificar** con la norma o con lo que indique la cátedra. Además:

- **Agua caliente sanitaria:** 100 L por cama y día, de 17 a 60 °C, con un factor de pérdidas de 1,3. El valor se eligió entre los casos medidos (50 a 55) y los ratios de diseño (200 a 300) del artículo de Hospitecnia; el efecto de cambiarlo está en la sensibilidad.
- **Calefacción y humidificación** de invierno: se calculan, pero son menores en el AMBA que en los hospitales españoles de referencia.

## 4. Contenidos de Termodinámica elegidos y cómo se integran

Los cuatro contenidos se usan sobre **una sola cadena de equipos**, y cada uno resuelve una parte que el siguiente necesita.

| Contenido | Qué resuelve en este sistema | Resultado que entrega | A quién se lo entrega |
|---|---|---|---|
| **Aire húmedo** | Estados del aire en la mezcla, la serpentina, el recalentamiento y la impulsión; cargas sensible y latente | Carga frigorífica y calor de recalentamiento y calefacción | A la refrigeración (frío) y a la combustión (calor) |
| **Refrigeración** | Ciclo de compresión de la enfriadora: trabajo del compresor, COP, calor rechazado | Electricidad del frío y calor disponible en el condensador | Al balance de energía y a la exergía; el calor del condensador es la base de la alternativa B |
| **Combustión** | Gas natural con exceso de aire: reacción, poder calorífico, rendimiento de la caldera, temperatura de llama | Consumo de gas para recalentar, calefaccionar y producir ACS | Al balance de energía y a la exergía |
| **Exergía** | Dónde se destruye capacidad de hacer trabajo, con el estado muerto en las condiciones exteriores | Destrucción de exergía por equipo y eficiencia exergética | A la comparación de alternativas y mejoras |

**El hilo conductor** es el recalentamiento: el sistema enfría para deshumidificar y luego recalienta quemando gas, mientras la enfriadora **rechaza al ambiente** calor que podría cubrir parte de ese recalentamiento: el refrigerante condensa a 32 a 46 °C según el clima y sale del compresor hasta unos 65 °C, suficiente para llevar aire de unos 13 °C a 20 °C. Es una ineficiencia que se cuantifica con la Primera Ley (energía) y se explica con la Segunda (calentar aire unos pocos grados con una llama que supera los 1.800 °C destruye casi toda la exergía del combustible).

## 5. Esquema conceptual

```
                          RETORNO DE LA ZONA ────────────────┐
                                                             ▼
 AIRE EXTERIOR ──► [MEZCLA] ──► [SERPENTINA DE ──► [RECALENTA-] ──► [HUMIDIFICADOR] ──► ZONA
   (T, W)         (mezcla con     AGUA HELADA]       MIENTO]         (solo invierno)    (quirófano,
                   retorno)       enfría y            ▲                 ▲              UTI, etc.)
                                  deshumidifica       │ Q_recal         │ vapor
                                      │ Q_L           │                 │
                                      ▼               │                 │
                              ┌───────────────┐    ┌──┴─────────────────┴──┐
                              │  ENFRIADORA   │    │   CALDERA DE GAS      │ ◄── gas natural + aire
                              │ (compresión)  │    │   (calefacción, ACS)  │ ──► gases de escape
                              │ 1 evaporador  │    └───────────┬───────────┘
                              │ 2 compresor   │                │ Q_ACS
                              │ 3 condensador │ ──► Q_cond     ▼
                              │ 4 válvula     │   (hoy al    AGUA CALIENTE
                              └───────▲───────┘   ambiente)  SANITARIA 60 °C
                                      │ W_comp (electricidad)
```

**Sistemas de estudio y límites** (volúmenes de control):

| Sistema | Límite | Flujos que cruzan |
|---|---|---|
| Unidad de tratamiento de aire | Mezcla + serpentina + recalentador + humidificador | Aire exterior y retorno (entran), aire de impulsión (sale), agua helada, calor de la caldera, vapor, condensado |
| Enfriadora | Compresor + condensador + válvula + evaporador | Calor del agua helada (entra), electricidad (entra), calor al ambiente (sale) |
| Caldera | Cámara de combustión + intercambiador | Gas y aire (entran), gases de escape (salen), calor útil (sale) |
| Producción de ACS | Acumulación + recirculación | Calor de la caldera, agua fría (entra), agua caliente (sale) |

La **exergía** se evalúa sobre estos mismos sistemas, con el estado muerto en el estado exterior del punto de diseño (temperatura exterior, 101,3 kPa y humedad exterior).

## 6. Condiciones de operación, datos e hipótesis

**Hipótesis de cálculo:**

1. Régimen permanente en cada estado horario (cada mes se parte en una mitad diurna y una nocturna).
2. El aire húmedo es una mezcla de aire seco y vapor, ambos gases ideales, a presión constante de 101,3 kPa.
3. Sistema de aire de **caudal constante** con serpentina y recalentamiento, sin economizador ni recuperación de calor (es la línea de base).
4. El refrigerante realiza un ciclo ideal de compresión de vapor, con compresor adiabático de rendimiento isentrópico constante, expansión isoentálpica y sin pérdidas de presión en los intercambiadores.
5. Combustión completa del gas natural, gases ideales y sin disociación; el aire tiene 21 % de O₂ y 79 % de N₂.
6. Los gases de escape salen a 190 °C, sin condensar.
7. El ventilador de impulsión aspira después de la serpentina y toda su potencia eléctrica se disipa como calor en el aire. No se calculan las pérdidas de distribución de calor y frío (salvo el factor de las de ACS).
8. Frontera: solo el sistema térmico y sus auxiliares. No se incluyen iluminación, equipos médicos, cocina ni lavandería.

**Datos y supuestos:** todos están en [`supuestos.md`](supuestos.md) con su estado (**dato**, **supuesto** o **constante**) y su fuente. Los supuestos sin fuente citable, que son los que más pesan, son: el clima mensual y de diseño, las condiciones y renovaciones por zona (ASHRAE 170 recordado), las ganancias internas, la conductancia de la envolvente, la composición del gas y los rendimientos del compresor y de los ventiladores.

## 7. Alternativas y mejoras a comparar (Consigna 4)

| | Configuración | Qué cambia |
|---|---|---|
| **Alternativa A (línea de base)** | Enfriadora de compresión, caldera de gas, aire de caudal constante con recalentamiento | Es la que se calculó |
| **Alternativa B** | A con **recuperación del calor del condensador** para el recalentamiento | El calor que hoy se rechaza reemplaza parte del gas del recalentamiento |

Mejoras candidatas (la consigna pide al menos dos, explicadas desde la Termodinámica): recuperación de calor del aire de extracción, control del exceso de aire o caldera de condensación, mayor temperatura de evaporación con menor trabajo del compresor, y precalentamiento solar del ACS. El informe HCWH de 2021 aporta estimaciones locales de ahorro (por ejemplo, hasta 40 % con VRF con recuperación de calor en un hospital de San Juan, con base no declarada), que se citan con esa salvedad.

## 8. Estado y pendientes

- **Hecho:** el modelo del sistema A, la estimación del consumo anual con sensibilidad y los chequeos termodinámicos. El modelo fue verificado de forma independiente (dos reimplementaciones y una revisión adversarial; ver [`02_estimacion_consumos.md`](02_estimacion_consumos.md), sección 8). Quedan sin verificar los supuestos de entrada.
- **Falta:** el análisis exergético, la alternativa B y las mejoras, los diagramas (P-h, carta psicrométrica, diagrama de flujo de exergía), el informe y la presentación.
- **Para confirmar con la cátedra o con fuentes:** clima del SMN, valores de ASHRAE 170, composición del gas del ENARGAS y la frontera del consumo (preguntas 12 y 13 del PRD).
