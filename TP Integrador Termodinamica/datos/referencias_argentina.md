# Referencias de hospitales argentinos con datos documentados

**Estado:** transcripción v0.2, **verificada** por dos lectores independientes de los PDFs y un auditor aritmético. **Todas las cifras de los gráficos 3, 4 y 5, de la tabla del anexo, de la sección 3 y de El Cruce coinciden con los documentos**, y la afirmación de que el documento del Austral no trae cifras de energía fue confirmada leyendo sus 6 páginas. Se corrigieron números de página, citas no literales y rótulos, y se agregaron las advertencias del auditor. Reemplaza las pistas de [`hospital_referencia.md`](hospital_referencia.md) con datos leídos del documento original.

## Fuentes (archivos recibidos)

| ID | Fuente | Qué es |
|---|---|---|
| **A** | Health Care Without Harm (HCWH), con fondos del Kigali Cooling Efficiency Program (K-CEP). *Energy efficiency and cooling audits in health care facilities in Argentina, China, and the Philippines. Final project report.* Marzo de 2021. 79 págs. | Informe final de auditorías energéticas y de refrigeración. Argentina: págs. 20 a 27 y anexo págs. 54 a 62 (Fase 1, auditoría: 54 a 58; Fase 2, proyecto piloto: 59 a 62). |
| **B** | Medina A. y Marini J.E. *Hospital El Cruce "Dr. Néstor Carlos Kirchner": alta complejidad en red.* (el título original trae la errata "compejidad"; aquí se corrige) Revista Argentina de Salud Pública, Vol. 1, N.º 5, diciembre de 2010, págs. 46 a 48 (sección "noticias"). Medina era Director Ejecutivo y Marini Director Médico Asistencial. | Nota institucional del propio hospital. |
| **C** | Hospital Universitario Austral. *Plan de Sostenibilidad* (archivo "Informe de Sostenibilidad 2024"). 6 págs. | Resumen del plan ESG. **No trae cifras de energía** (sección 5). |
| **D** | HCWH. *Sample Terms of Reference for Energy and Cooling Audits at Health Care Facilities.* Versión 1, marzo de 2021. 3 págs. | Modelo de pliego para contratar auditorías. Útil como lista de datos que se piden (nivel de complejidad, áreas total y cubierta, camas, personal, consumos). No trae datos de hospitales. |

## 1. Intensidad energética de tres hospitales argentinos (fuente A)

Auditorías de julio a octubre de 2019. Energía anual total, **estimada** por el equipo consultor con la información disponible (el informe habla de electricidad, gas natural y energía total; el gasoil de los generadores se desglosa explícitamente solo en el Giordano, pág. 55). El informe aclara que faltaban datos medidos confiables de los últimos tres años, que no se pudo separar el consumo de refrigeración, y que el indicador por cama **no es representativo** para CEMAR (atiende casi solo pacientes ambulatorios).

| ID | Hospital | Ubicación | Tipo | Camas | Superficie cubierta | Pacientes/año | kWh/m²·año | kWh/cama·año | kWh/paciente·año |
|---|---|---|---|---|---|---|---|---|---|
| **H-01** | Prof. Dr. J. P. Garrahan | Ciudad de Buenos Aires | Terciario (alta complejidad), pediátrico | 534 | 120.000 m² | más de 600.000 | **259** | 58.185 | 52 |
| **H-02** | CEMAR (Centro de Especialidades Médicas Ambulatorias de Rosario "M. H. Zuasnábar", con la Maternidad Martin) | Rosario, Santa Fe | Secundario (media complejidad), casi todo ambulatorio | 42 | casi 20.000 m² | unos 185.000 | **211** | 99.215 | 22 |
| **H-03** | Dr. José María Giordano | Albardón, San Juan | Secundario (media complejidad) | 51 | 4.970 m² | unos 90.000 (91.686 en el anexo) | **163** | 15.837 | 9 |

Valores leídos de los gráficos 3, 4 y 5 (págs. 21 y 22). Superficies, camas y pacientes, del texto de las págs. 20 y 21. Garrahan: 534 camas según el informe (una búsqueda web mencionó 500 y 587, sin verificar). Antigüedad: Garrahan inaugurado en 1987, Giordano en 2014, CEMAR en 1999 (la Maternidad Martin se anexó en 2006).

**Chequeo de coherencia (mío):** para cada hospital, superficie × kWh/m², camas × kWh/cama y pacientes × kWh/paciente dan la misma energía anual dentro de 4 %: Garrahan 31,1 GWh, CEMAR 4,2 GWh, Giordano 0,81 GWh. Por superficie y por cama coinciden dentro de 1,3 %; la diferencia mayor está en kWh/paciente, que el informe redondea a enteros (en CEMAR da 22,5 y el informe dice 22; en el Giordano da 8,8 con los 91.686 pacientes del anexo y el informe dice 9). Las cifras de los gráficos son coherentes con el texto.

**Qué sirve para el hospital tipo (AMBA, unos 20.000 m²):**
- **Garrahan** es el único del AMBA, pero es 6 veces más grande y es un hospital pediátrico de alta complejidad. Es la única intensidad en el clima de Buenos Aires, y es **estimada**, no medida.
- **CEMAR** tiene la misma superficie (casi 20.000 m²) y un clima parecido (Rosario), pero es ambulatorio: 476 m²/cama contra 150 del hospital tipo.
- **Giordano** está en San Juan (clima árido) y es 4 veces más chico. Sirve por el desglose de la sección 2.

## 2. Desglose de un caso: Hospital Giordano (fuente A, anexo págs. 54 a 56, 58 y 60 a 61)

Promedios 2016 a 2018. **No había datos de gas** porque el medidor no funcionaba: el consumo de gas se calculó según el clima, los usuarios y la eficiencia de los equipos usados (traducción mía de la pág. 55; estimado, no medido).

| ID | Energía | kWh/año | kWh/cama·año | kWh/paciente·año | kWh/m²·año | kgCO₂/año |
|---|---|---|---|---|---|---|
| H-03a | Electricidad | 495.643 | 9.718 | 5,4 | 100 | 237.909 |
| H-03b | Gas natural (estimado) | 309.351 | 6.066 | 3,4 | 62 | 148.489 |
| H-03c | Gasoil (generadores) | 2.716 | 53 | 0 | 0,5 | 1.303 |
| H-03d | **Total** | **807.710** | **15.837** | **9** | **163** | **387.701** |

Participaciones (calculadas): electricidad 61,4 %, gas natural 38,3 %, gasoil 0,3 %. Las sumas del informe cierran. Datos del texto (pág. 56): el gas se usa para calentar agua, cocinar y en estufas, y **no se usa para aire acondicionado en instalaciones termomecánicas**. Las págs. 22 a 23 agregan que en los tres hospitales el gas sirve para calefacción general y que en uno de ellos también se usa en verano en equipos fan coil. La electricidad se usa para iluminación, confort térmico y equipos y es muy sensible a la temperatura (la demanda sube al alejarse de 25 °C).

Otros datos del anexo:
- **Camas del Giordano:** 51, de las cuales 27 son de adultos y 24 pediátricas (pág. 54).
- **Emisiones normalizadas** (pág. 55): 7.602 kgCO₂/cama·año, 4 kgCO₂/paciente·año y 78 kgCO₂/m²·año. Ver la advertencia de abajo.
- **Costos** (pág. 56, facturas de diciembre de 2018): electricidad a 0,09 USD/kWh, unos 42.000 USD al año; gasoil, casi 230 USD; **no hay datos de costo del gas natural**.
- **Gasoil por año** (gráfico 2, pág. 56): 230, 238 y 303 L, o 2.433, 2.512 y 3.203 kWh (2016 a 2018). Creciente desde 2016. El promedio coincide con los 2.716 kWh de la tabla.
- **Potencial solar:** el informe dice que llega a "7 kWh per day during the summer" en San Juan (pág. 58) y a "6-7 kWh per day" en los tres hospitales (pág. 24). **No aclara la unidad**; probablemente es radiación en kWh/m² por día, pero eso es una inferencia mía. No usar sin aclararlo, porque 7 kWh por día de producción para una instalación de 10 kWp sería unas diez veces menos de lo esperable (unos 7 kWh por kWp instalado).
- **Vida útil de los splits:** "después de 3 años ya necesitan ser reemplazados" (pág. 54).

**Advertencia sobre las emisiones:** el informe usa el **mismo factor, 0,48 kgCO₂/kWh**, para electricidad, gas natural y gasoil (237.909 / 495.643 = 148.489 / 309.351 = 0,48). Ese valor es un factor de red eléctrica; para el gas natural es bastante más alto que el valor típico (alrededor de 0,2 kgCO₂/kWh, dato de conocimiento general que habría que citar con fuente si se usa) y para el gasoil también queda alto. **No usar las emisiones de gas del informe.**

## 3. Hallazgos técnicos del informe, útiles para alternativas y mejoras (fuente A)

Estos puntos sirven para la Consigna 4 (alternativas y mejoras), con su página.

| Hallazgo | Dónde |
|---|---|
| Equipos de refrigeración viejos e ineficientes; muchos de categorías de eficiencia C y D, instalados como solución de emergencia porque el aire central no alcanzaba; muchos usan **R22** | p. 22 |
| Sistemas inadecuados en áreas especiales: el equipo no permite el recambio de aire necesario ni la limpieza completa | pp. 22 a 23 |
| Aislación de cañerías dañada, y envolvente con aislación térmica insuficiente | p. 23 |
| Diseño arquitectónico: claraboyas = **6,62 % de la superficie del techo** en Giordano; gran fachada vidriada al norte en CEMAR; gran superficie de contacto con el exterior en Garrahan | p. 23 |
| En áreas especiales, el ventilador de inyección de los filtros HEPA debe funcionar de forma permanente: si el aire deja de circular, se tardan **24 a 36 horas** en recuperar la asepsia para operar | p. 24 |
| Reemplazar los splits por **VRF con recuperación de calor** en habitaciones y por bomba de calor en consultorios, más recambio de equipos en áreas especiales, podría ahorrar **hasta 40 %** de la energía (Giordano). **La base del porcentaje no está declarada**: si fuera sobre la energía total (807.710 kWh) serían 323 MWh/año, es decir el 65 % de la electricidad del hospital, y el gas no se reemplaza con VRF; si fuera sobre la electricidad, serían el 24,5 % del total. Además el informe dice que el consumo de climatización no se pudo separar | p. 58 |
| En el laboratorio de CEMAR, cambiar los equipos por VRF reduciría el consumo **26 %** | p. 26 |
| Solar térmico: con una demanda diaria de 300 L de agua a 50 °C, un precalentamiento solar podría ahorrar **más del 80 %** de la energía anual de ese uso | p. 58 |
| Fotovoltaica de 10 kWp instalada en Giordano en marzo de 2021. **Sola ahorra 3,75 %**; junto con las claraboyas mejoradas (protección vegetal y films reflectivos), el ahorro potencial llega a **10 %**. El informe estima además 50.000 USD de inversión y un potencial de 50 a 60 kWp | pp. 26 y 27; 60 y 61 |
| Los sistemas de medición de varios hospitales no permiten separar el consumo de refrigeración, y faltaban datos de años anteriores (la pág. 4 lo dice de los hospitales de los tres países, no solo de Argentina) | p. 4 y p. 21 |

## 4. Hospital El Cruce, Florencio Varela (fuente B)

Nota del propio hospital, diciembre de 2010.

| ID | Dato | Valor | Cita textual o contexto |
|---|---|---|---|
| E-01 | Terreno | 47.000 m² | "superficie total de terreno de 47.000 m²" |
| E-02 | **Superficie cubierta** | **22.000 m²** | "de los cuales 22.000 son cubiertos" |
| E-03 | Desglose de lo cubierto | 1.300 m² espacios quirúrgicos; 1.980 m² servicios de diagnóstico; 862 m² laboratorio | Suman 4.142 m², el 19 % de lo cubierto |
| E-04 | **Camas** | **140** | "Dispone de 140 camas, el 50% de ellas para internación especializada en Unidad de Terapia Intensiva, Unidad Coronaria y Recuperación Cardiovascular" |
| E-05 | Superficie por cama | 157 m²/cama (calculado) | Casi igual al supuesto de 150 del hospital tipo |
| E-06 | Camas críticas | 70 (50 % de 140, calculado) | Es un hospital de alta complejidad: más intensivo que un hospital general |
| E-07 | Ubicación | Florencio Varela, segundo cordón del conurbano sur | Atiende a unos 1.800.000 habitantes de cuatro distritos |
| E-08 | Inversión | 120 millones de pesos | Estado nacional. El documento no fecha la inversión; solo la nota es de diciembre de 2010 |
| E-09 | Otras instalaciones | Helipuerto de operación diurna y nocturna; sistema de emergencias y generadores | Sin datos de climatización ni de energía |

**Límites:** son cifras de **2010**. Después el hospital se amplió (otras fuentes, sin verificar, hablan de 171 camas en 2015 y de una ampliación de +88 camas). La nota **no trae ningún dato de climatización ni de consumo**.

## 5. Hospital Universitario Austral (fuente C)

El documento recibido es un resumen del plan de sostenibilidad ESG. **No trae kWh, m³ de gas, chillers ni superficie ni camas.** Lo único energético: "programa de eficiencia energética con luminarias LED, 60 % de energía renovable solar, y búsqueda de financiamiento para energía solar propia" (ODS 7), medición anual de la huella de carbono y objetivo de emisiones netas cero para 2050. El documento no aclara de qué es el 60 % (energía consumida, capacidad), y el mismo 60 % aparece para las mujeres en puestos de liderazgo. **No sirve para consumos.** La pista de los kWh queda cerrada con este documento; si existe otro informe con tablas, no es éste.

## 6. Cómo entra al proyecto

- **Banda de contraste local, estimada por auditoría:** 163 a 259 kWh/m²·año de energía final en tres hospitales argentinos (n = 3, estimados, dos de ellos fuera del AMBA). Está por debajo de los 380 a 400 del modelo español del artículo (Garrahan es 65 % de 397, que es el punto medio de 394 a 400 en energía final, y 68 % de 380, que mezcla calor útil con electricidad; hay que declarar la base, ver E-16 de `hospitecnia_datos.md`) y de la mediana de 333 de los 23 hospitales internacionales. Se usa como **banda de plausibilidad**, no como valor de diseño.
- **Hospital de referencia de tamaño y geometría:** El Cruce (22.000 m² cubiertos, 140 camas, 157 m²/cama), con la salvedad de que es de alta complejidad y las cifras son de 2010.
- **Hospital de referencia de energía:** Garrahan, con la salvedad de su tamaño (6 veces) y su perfil pediátrico de alta complejidad.
- **Ninguno es un hospital del AMBA de unos 20.000 m² con consumo real publicado.** Esa combinación no se encontró; el informe del proyecto debe declararlo.
