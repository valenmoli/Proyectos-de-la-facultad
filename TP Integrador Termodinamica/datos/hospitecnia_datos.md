# Datos del artículo de Hospitecnia

**Fuente:** *Caracterización de consumos energéticos y suministros en hospitales*. Juan Gallostra Isern (JG Ingenieros), Ángel Sánchez-Vaqué (Hospitecnia) y Josep Túnica Buira (JG Ingenieros S.A.). Hospitecnia, octubre de 2022.
https://hospitecnia.com/instalaciones/caracterizacion-de-consumos-energeticos-y-suministros-en-hospitales/

**Archivos recibidos:** (1) un PDF de 15 páginas, cortado por login; (2) el **PDF de 22 páginas con la versión completa**. En la versión completa el texto y la bibliografía ocupan las págs. 1 a 13; el resto es publicidad y formularios. Esta transcripción cubre la versión completa.

**Estado:** transcripción v0.3. Las secciones A a F (texto de las págs. 1 a 7 del PDF truncado) fueron contrastadas contra el PDF por dos lectores independientes y su aritmética por un auditor: **no se encontró ningún valor, unidad ni cita mal transcripto**, y se corrigieron las ambigüedades y omisiones que marcaron. Las secciones D2 a D5, G y el CSV (agregados de la versión completa) están **pendientes de verificación independiente**.

## Limitaciones de la fuente (leer antes de usar cualquier número)

1. **Fuentes primarias no accesibles.** La versión completa trae la bibliografía (1) a (16) (sección G), pero son manuales y trabajos españoles que no se pueden consultar desde el entorno. Para la consigna ("fuentes de los datos") la fuente citable es el artículo, como fuente secundaria, nombrando la referencia primaria que él mismo cita.
2. **Datos de España** en su gran mayoría (Madrid, Navarra, Barcelona, Castilla-La Mancha), más Chile, Perú y Portugal. **No hay clima ni consumos de Argentina.**
3. El texto dice que los datos "han sido obtenidos e interpolados a partir de la bibliografía consultada" y que no es fácil dar ratios por la gran variabilidad. Son órdenes de magnitud, no valores de diseño.
4. Hay **cifras internamente inconsistentes** (sección E). No se usan.
5. **No trae** condiciones interiores de diseño (T, HR), caudales o renovaciones de aire, clima de diseño, refrigerante ni composición del gas (sección F). **Sí trae supuestos de conversión de los autores** (sección D4): 10,8 kWh/m³ para el gas sin aclarar si es poder calorífico superior o inferior, caldera al 90 %, COP 4 y 6,5 h/día equivalentes de refrigeración.
6. **Base de superficie no aclarada.** El propio artículo advierte (Conceptos generales) que el ratio por superficie casi nunca aclara si usa superficie útil o construida, "por lo que los valores pueden ser bastante diferentes". Afecta a todos los kWh/m².

**Columna "Uso propuesto":** *Modelo* = candidato a entrada del hospital tipo. *Contraste* = sirve para validar que nuestros resultados sean razonables. *Contexto* = para la introducción. *No usar* = inconsistente.

## A. Ratios y superficie

| ID | Dato | Valor | Unidad | Contexto | Cita | Uso propuesto |
|---|---|---|---|---|---|---|
| D-01 | Superficie construida por cama | 60 (años 70) a cerca de 200 (actual) | m²/cama | Evolución histórica; el artículo atribuye la baja de camas a que la estancia media se redujo "a menos de la mitad de tiempo" | — | Modelo |
| D-02 | Superficie por cama, promedio España | 148 | m²/cama | Todos los hospitales de España | (3) | Modelo |
| D-03 | Peso del costo energético | hasta 10 | % de los costos de operación | "Según diversas fuentes" | — | Contexto |
| D-04 | Participación del sector sanitario | 27 | % del consumo del sector servicios | España, 2018; detrás de oficinas y comercio | (9) | Contexto |
| D-05 | Reparto electricidad / combustible | casi a partes iguales | — | "En muchos hospitales": electricidad (alumbrado, fuerza, refrigeración) y GN o gasóleo (calefacción y ACS) | sin cita propia; sigue a una oración que cita (9) | Contexto |

## B. Energía total y repartos

| ID | Dato | Valor | Unidad | Contexto | Cita | Uso propuesto |
|---|---|---|---|---|---|---|
| D-06 | Reparto del consumo | 20 ACS / 35 iluminación / 45 climatización | % | Establecimientos sanitarios; "mismos datos" en (4) | (10), (4) | Contraste |
| D-07 | Energía total anual (térmica + eléctrica) | 225 atlántica / 274 continental / 276 mediterránea | kWh/m² | Hospitales de 101 a 250 camas, España, 2011 | (3) | Contraste |
| D-08 | Hospital de Madrid | 17.957 m², 213 camas, 7 plantas; 7,5 millones kWh/año; 418 kWh/m² | — | Auditoría energética. El gráfico del artículo rotula este hospital como "18.000 m²" y agrupa gasóleo y GN en una sola porción | (5) | Contraste |
| D-08a | Reparto por uso, hospital de Madrid | 40 calefacción / 21 equipamiento / 20 refrigeración / 7 ACS / 6 ventilación / 6 iluminación y otros | % | Suma 100 % | (5) | Contraste |
| D-08b | Reparto por fuente, hospital de Madrid | 54 electricidad / 45 gasóleo / 1 gas natural (cocina) | % | Suma 100 % | (5) | Contraste |
| D-09 | Hospitales de Navarra, 2019 | 46 % de la energía de edificios públicos; 73 millones kWh/año; 44 % electricidad, 51 % GN, 5 % otros; 215 a 415 kWh/m²·año | — | Estudio de Navarra | (6) | Contraste con cautela (E-07) |
| D-10 | Reparto de fuentes en Perú | 66 electricidad / 34 gas natural | % | — | (8) | Contexto |
| D-11 | Hospitales de Chile | 39 hospitales, 34.137 m² y 343 camas promedio; 255 kWh/m²·año; 64 % eléctrico y 36 % térmico | — | — | (11) | Contraste |
| D-11a | Chile, consumo térmico | 30 agua caliente / 54 climatización / 6 central de esterilización / 5 equipos industriales / 5 cocina y otros | % | Suma 100 % | (11) | Contraste |
| D-11b | Chile, consumo eléctrico | 3 ACS / 21 climatización / 25 iluminación / 25 equipos médicos / 14 equipos industriales / 6 oficina / 6 electrodomésticos / 3 otros | % | **Suma 103 %** (ver E-04) | (11) | Contraste con cautela |
| D-12 | Distribución típica según el Banco de Desarrollo de América Latina | 51 climatización / 12 ventilación y bombas / 6 ACS / 14 iluminación / 17 equipos | % | Suma 100 % | (13) | Contraste |
| D-13 | Hospital caso UNED | 410 camas, 71.500 m², interior de la península; 9,8 millones kWh eléctricos y 15,6 millones kWh de GN; 137 y 218 kWh/m²; 40 % electricidad / 60 % GN en energía y 60 % / 40 % en gasto | — | Estudio de casos | (15) | Contraste. Con los kWh del propio renglón el reparto es 38,6 / 61,4, no 40 / 60 |

## C. Energía térmica y combustibles

| ID | Dato | Valor | Unidad | Contexto | Cita | Uso propuesto |
|---|---|---|---|---|---|---|
| D-14 | **Cargas térmicas estándar** | **115 refrigeración / 90 calefacción** | W/m² | "Cargas térmicas estándares". El artículo advierte justo antes que la bibliografía "suele dar información sobre demandas térmicas y medidas de ahorro energético, pero no sobre consumos reales" | (1) | Contraste. Las cargas del hospital tipo se recalculan con el clima local (PRD 0.2); ver E-10 |
| D-15 | Consumo térmico nacional, España 2015 | 791 hospitales, 158.566 camas, 4.200 millones kWh/año; 26.674 kWh/cama y 201 kWh/m² | — | El artículo llama "consumo estimado" a los 4.200 millones e "indicador medio de consumo térmico anual" a los ratios; el carácter térmico del total es inferido del encabezado de la sección | — | Contraste con cautela (E-13) |
| D-16 | Consumo térmico anual | 113 atlántica / 133 continental / 110 mediterránea | kWh/m² | Hospitales de 101 a 250 camas, España, 2011 | (3) | Contraste con cautela (E-13) |
| D-17 | Consumo térmico por cama, Navarra | 20.500 a 29.000 | kWh/cama·año | (12) es el plan de ahorro y eficiencia del Servicio Navarro de Salud de 2013, que detalla los cinco hospitales públicos de la comunidad | (4); detalle en (12) | Contraste |
| D-18 | Combustibles para energía térmica, 2011 | 73 gas natural / 23 gasóleo / 4 otros | % | Suma 100 % | (3) | **Modelo** (combustible: GN) |
| D-19 | Hospital de Madrid, GN 2020 | 127.830 kWh; "71 kWh/m²"; máx. 21.474 kWh en enero; mín. 1.354 kWh en agosto; 18.000 m², 216 camas | — | El artículo escribe las unidades como "kW/h" y "kW/h m²"; aquí se transcriben como kWh | (2) | **No usar** como GN del modelo (E-01) |
| D-20 | Hospital de Madrid, gasóleo | "3,4 millones de litros/año"; máx. 60.000 L en diciembre; mín. 30.000 L en los tres meses de verano | — | Calderas de calefacción y ACS. Es el mismo hospital que D-08 (17.957 m², 213 camas), no el de D-19 | (5) | **No usar** (E-02). El reparto 86 / 14 sirve como orden de magnitud |
| D-20a | Reparto del gasóleo | 86 calefacción / 14 ACS | % | Suma 100 % | (5) | Contraste |
| D-21 | Hospital Vall d'Hebron (Barcelona), 2016 | 22 edificios, 1.100 camas; 88.328 MWh de gas; 80.000 kWh/cama | — | — | — | Contraste con cautela: atípico, unas 3 veces el promedio térmico nacional (E-13) |
| D-22 | Hospitales públicos de Navarra, 2019 | Hospital de Navarra: 15,8 millones kWh, 78.000 m², 202 kWh/m². Virgen del Camino: 10,4 millones kWh, 43.000 m², 240 kWh/m² | — | Consumo de GN | (6) | Contraste |
| D-23 | Hospital de Coímbra, 2010 | 1.600 camas; 38 millones kWh de combustible; "31.457 kWh/cama·año"; 310 kWh/m²·año | — | — | (8) | 310 kWh/m² utilizable; **no usar** la razón por cama ni las 1.600 camas (E-03) |

## D. Agua caliente sanitaria (ACS)

| ID | Dato | Valor | Unidad | Contexto | Cita | Uso propuesto |
|---|---|---|---|---|---|---|
| D-24 | **Consumo y potencia de ACS** | **200 L/cama·día; 6,4 kW/cama de potencia de preparación** | — | Ratios | (1) | **Modelo** el consumo. La potencia contradice la tabla resumen (E-09) |
| D-25 | Consumo de ACS, asociación española de ingeniería hospitalaria | 200 a 300 L/cama·día; 80 % consumido en un período no superior a 4 h | — | — | — | **Modelo** |
| D-26 | Hospital general en Castilla-La Mancha | 540 camas, 96.600 m²; 900 kW de producción de ACS; acumulación total 36.000 L; caudal punta máximo medido 5,5 m³/h | — | — | — | Contraste |
| D-27 | Clínica privada en Madrid | 250 camas; acumulación de ACS 9.000 L; consumo promedio diario "3,0 m³/h" (unidad ambigua, ver E-06) | — | — | — | Contraste con cautela |
| D-28 | Consumo de ACS, hospitales y clínicas | 55 L/día·cama a 60 °C | — | — | (7) | **Modelo** (única que da la temperatura: 60 °C) |
| D-29 | Tendencia del ACS | Disminuyó por menor estancia media (muchos pacientes ingresan "dos o tres días" y esperan a ducharse en su casa), lavado en cama, griferías de bajo caudal, lavamanos de consultas externas solo con agua fría (legionela), lavado de cocina más eficiente y lavandería externalizada | — | Literal: "en los edificios existentes las instalaciones de almacenamiento y distribución de ACS suelen ser muy superiores al consumo real de los edificios" | — | Contexto |

## D2. Consumo eléctrico

| ID | Dato | Valor | Unidad | Contexto | Cita | Uso propuesto |
|---|---|---|---|---|---|---|
| D-30 | Potencia eléctrica simultánea | 75 | W/m² | Hospitales | (1) | Contraste |
| D-31 | Hospital de Madrid, electricidad 2020 | 4,2 millones kWh; 232 kWh/m²·año; 19.354 kWh/cama·año; máx. 588.031 kWh en enero; mín. 141.396 kWh en agosto | — | 18.000 m², 216 camas | (2) | Contraste |
| D-32 | Electricidad anual | 111 atlántica / 141 continental / 166 mediterránea | kWh/m² | Hospitales de 101 a 250 camas, España, 2011 | (3) | Contraste |
| D-33 | Electricidad en Navarra | 97 a 143 (media nacional 139) | kWh/m² | — | (4) | Contraste con cautela (E-08) |
| D-34 | Auditoría de un hospital de Madrid | 17.957 m², 213 camas; electricidad 4,0 millones kWh/año (226 kWh/m²); máx. 419.200 kWh en julio; mín. 279.500 kWh en febrero; promedio cercano a 11.000 kWh/día de lunes a viernes | — | — | (5) | Contraste |
| D-34a | Reparto del consumo eléctrico, misma auditoría | 39 equipos / 38 refrigeración / 12 ventilación / 9 iluminación / 2 ACS y otros | % | Suma 100 % | (5) | Contraste |
| D-35 | Hospitales públicos de Navarra, electricidad 2019 | 313 Hospital de Navarra / 410 Virgen del Camino / 366 Reina Sofía / 286 García Orcoyen | kWh/m² | — | (6), (9) | Contraste con cautela (E-07, E-08) |
| D-36 | Vall d'Hebron, electricidad 2016 | 22.431 MWh; 20.000 kWh/cama·año (1.100 camas) | — | — | — | Contraste |
| D-37 | Consumo eléctrico medio por cama | 29.000 | kWh/cama·año | Según Euroconsult, con datos del Sistema Nacional de Salud | — | Contraste |
| D-38 | Servicio Madrileño de Salud, electricidad 2019 | 140 | kWh/m² | — | — | Contraste |
| D-39 | Coímbra, electricidad 2010 | 19 millones kWh; "15.728 kWh/cama·año"; 155 kWh/m²·año | — | 1.600 camas | (8) | 155 kWh/m² utilizable; la razón por cama no (E-03) |
| D-40 | Hospitales públicos de Navarra, electricidad 2011 | 110 a 140 | kWh/m²·año | — | (12) | Contraste con cautela (E-08) |
| D-41 | Electricidad por cama y día | 31 a 55 (hasta 150 camas); 26 a 65 (hasta 200 camas); 61 (300 camas) | kWh/cama·día | "Muy variable" | (13) | Contraste |
| D-42 | Electricidad por cama según tamaño | Cerca de 20.000 en más de 1.000 camas y en menos de 100 camas; menos de 15.000 entre 100 y 250 camas | kWh/cama·año | Los de 100 a 250 camas son los más eficientes | (14) | Contraste |
| D-43 | Hospital de la Comunidad de Madrid | 600 camas, 59.200 m²; 9,5 millones kWh totales; 161 kWh/m²·año; 15.886 kWh/cama | — | — | (14) | Contraste |
| D-44 | Factores que influyen | Sistema de contratación; hospital todo eléctrico o con combustibles fósiles; fotovoltaica de autoconsumo; la iluminación LED redujo su peso, por lo que "los ratios históricos disponibles suelen ser más altos que la realidad" | — | — | — | Contexto |

## D3. Oxígeno medicinal

Fuera del alcance del TP (la consigna no incluye gases medicinales). Se transcribe por completitud.

| ID | Dato | Valor | Cita | Uso propuesto |
|---|---|---|---|---|
| D-45 | Equivalencia | 1 m³ de oxígeno líquido = 843 m³ de oxígeno gas | — | Fuera de alcance |
| D-46 | Caudal por toma | 10 o 15 L/min (0,6 a 0,9 m³/h), con simultaneidad de 10 a 20 %; paciente covid con altos flujos, 30 a 70 L/min (1,8 a 4,2 m³/h) | — | Fuera de alcance |
| D-47 | Hospital Fundación Alcorcón (Madrid), 2014 | 400 camas, 54.700 m²: 244.838 m³ "de oxígeno líquido" y 31.639 m³ en botellas; 62 % terapia respiratoria, 33 % sedación y anestesia, 5 % pruebas diagnósticas (ver E-11) | — | Fuera de alcance |
| D-48 | Hospital universitario de Ceuta | 252 camas; normal 400 L/día; pico covid 1.900 L/día el 17/2/2021 | — | Fuera de alcance |
| D-49 | Clínicas de JG Ingenieros | 20 m³/cama·mes (164 camas); 24 m³/cama·mes (128 camas) | — | Fuera de alcance |
| D-50 | Clínica Quirón de Zaragoza | 107 camas de hospitalización y 50 especiales; 4.588 m³/mes; 29 m³/cama·mes | — | Fuera de alcance |
| D-51 | Efecto de la pandemia | Consumo de hasta 3 o 4 veces el normal | — | Fuera de alcance |

## D4. Resumen del artículo: potencias y consumos de un hospital medio de unos 20.000 m²

Es la tabla que los autores arman con todo lo anterior. Es la referencia más directa para dimensionar el hospital tipo.

| ID | Suministro | Concepto | Potencia o caudal simultáneo | Consumo anual | Nota | Uso propuesto |
|---|---|---|---|---|---|---|
| R-01 | Térmico | Calefacción, Barcelona | 70 W/m² | 80 kWh/m² | S-1 | Contraste |
| R-02 | Térmico | Calefacción, Madrid | 90 W/m² | 140 kWh/m² | S-1 | Contraste |
| R-03 | Térmico | ACS | 10 W/m² | 40 kWh/m² | ver E-09 | **Modelo** |
| R-04 | Térmico | Refrigeración | 100 W/m² | 120 kWh/m² | S-2 | Contraste |
| R-05 | Gas natural | Calefacción Madrid + ACS | 10,0 L/h·m² | 18 m³/m² | S-3 | Contraste |
| R-06 | Electricidad | Para central frigorífica | 25 W/m² | 30 kWh/m² | S-4 | Contraste |
| R-07 | Electricidad | Para el resto de necesidades | 50 W/m² | 170 kWh/m² | — | Contexto |
| R-08 | Oxígeno | Condición normal | 1,5 L/h·m² | 4,0 m³/m² | — | Fuera de alcance |
| R-09 | Oxígeno | Condición pandemia | 6,0 L/h·m² | 16,0 m³/m² | — | Fuera de alcance |
| R-10 | Agua | Total | 0,27 L/h·m² | 1,2 m³/m² | S-5 | Contexto |
| R-11 | Agua | Caliente | 0,22 L/h·m² | 0,5 m³/m² | S-6 | **Modelo** |

**Supuestos declarados por los autores (notas de la tabla):**

| ID | Supuesto |
|---|---|
| S-1 | Calefacción con dos localizaciones: mediterránea (Barcelona) y continental (Madrid). |
| S-2 | Refrigeración: la potencia instalada es similar en Barcelona (mayor temperatura húmeda) y en Madrid (mayor temperatura seca). Consumo anual con un funcionamiento equivalente de **6,5 h/día durante 6 meses al año**. |
| S-3 | W térmicos de calefacción Madrid + ACS convertidos a m³ de gas con un poder calorífico del gas natural de **10,8 kWh/m³** y **90 % de rendimiento** de los generadores de calor. No se aclara si el poder calorífico es superior o inferior, ni la condición de referencia del m³. |
| S-4 | **COP de 4** para pasar de kW térmicos a kW eléctricos. |
| S-5 | Agua total: **500 L/cama·día** con **150 m²/cama** = 3,3 L/m²·día, repartido en 12 h. |
| S-6 | Agua caliente: **200 L/cama·día** con **150 m²/cama** = 1,3 L/m²·día, repartido en 6 h. |

**Verificación:** recalculé todas las conversiones de la tabla con sus propias notas y coinciden (potencia eléctrica 25 + 50 = 75 W/m², igual que D-30). La tabla es coherente consigo misma; lo discutible son las entradas (E-09, E-10).

## D5. Contraste del artículo con hospitales internacionales

| ID | Dato | Valor | Unidad | Cita | Uso propuesto |
|---|---|---|---|---|---|
| D-60 | Intensidad propuesta por los autores | 180 térmico (calefacción Madrid + ACS) + 200 eléctrico (central de frío + resto) = **380** | kWh/m²·año | — | Contraste |
| D-61 | Promedio de 23 hospitales internacionales | **387** kWh/m²·año; superficie promedio 77.522 m². Los autores concluyen que "valida perfectamente el estudio" | — | (16) | Contraste (ver E-12) |

Los 23 hospitales están en [`hospitales_internacionales.csv`](hospitales_internacionales.csv) (hospital, ubicación, superficie, kWh/m²·año), para que el código los lea directo. Recalculado: promedio 386,8, **mediana 333**, promedio ponderado por superficie 347, rango **120 a 900** kWh/m²·año.

## E. Inconsistencias detectadas en el artículo

Verificadas con cálculo y por un auditor independiente. **No se usan estas cifras sin aclarar.**

| ID | Problema | Cálculo | Lectura probable |
|---|---|---|---|
| E-01 | GN Madrid 2020 (D-19): 127.830 kWh no da 71 kWh/m². | 127.830 / 18.000 = **7,1** kWh/m². Para dar 71 harían falta 1.278.300 kWh, pero entonces el mes máximo (21.474 kWh) quedaría por debajo del promedio mensual (106.525 kWh); con los 12 meses al máximo, el tope anual sería 257.688 kWh = 14,3 kWh/m². | **Lectura más probable: es 7,1, no 71.** Las cifras mensuales son compatibles con 127.830 kWh, y en el hospital de D-08 el GN es solo de cocina (1 % de la energía en D-08b; 127.830 kWh sería 1,7 %). Eso supone que D-19 y D-08 son el mismo hospital (citas (2) y (5), años distintos), lo cual no está confirmado. En cualquier caso **no es el consumo térmico del hospital** (7,1 kWh/m² es 15 a 19 veces menos que D-16) y no debe usarse como "GN del modelo". |
| E-02 | Gasóleo Madrid (D-20): 3,4 millones de litros/año, pero el máximo es de 60.000 L en diciembre. | A unos 10 kWh/L, 3,4 millones de L serían 34 GWh, 4,5 veces la energía total del hospital (7,5 GWh): imposible. Además, 45 % de 7,5 GWh = **3,375 GWh**. El artículo no dice "mensual"; leyendo el máximo como mensual, el tope es 720.000 L/año. | Los litros no pueden ser 3,4 millones. Hay dos lecturas que no se pueden distinguir: 3,4 millones de **kWh**, o 340.000 L (coma corrida). Ninguna cierra del todo con los litros mensuales (360.000 a 630.000 L serían 3,6 a 6,3 GWh, contra 3,375). El mínimo de 30.000 L "para los tres meses de verano" puede ser el total de los tres meses o por mes. No usar; el 86 / 14 sirve como orden de magnitud. |
| E-03 | Coímbra (D-23 y D-39): 1.600 camas no es compatible con las razones por cama. | Térmico: 38e6 / 31.457 = **1.208** camas. Eléctrico: 19e6 / 15.728 = **1.208** camas. Los dos dan además la misma superficie implícita, 122.581 m² (38e6/310 y 19e6/155). | El número de camas (1.600) parece ser el dato erróneo: con 1.208 camas todo es consistente (31.457 × 1.208 reproduce 38 millones kWh). Es una inferencia, no un dato del artículo. Los kWh/m² son utilizables con cautela. |
| E-04 | Chile, consumo eléctrico (D-11b): los porcentajes suman **103 %**. | 3 + 21 + 25 + 25 + 14 + 6 + 6 + 3 = 103 | Poco probable que sea redondeo: con 8 términos el error máximo es +4 puntos y para llegar a +3 haría falta un error medio de +0,375 por ítem. Más probable un error de la fuente o del artículo. Ningún otro reparto del archivo tiene este problema (13 sumas verificadas). |
| E-05 | España térmico 2015 (D-15): 4.200 millones kWh / 158.566 camas = 26.487, el artículo dice 26.674 (0,7 % de diferencia). | — | Redondeo, no una inconsistencia real: el rango 4.150 a 4.250 millones de kWh da 26.172 a 26.803 kWh/cama, que incluye 26.674. |
| E-06 | Clínica de Madrid (D-27): "consumo promedio diario es de 3,0 m³/h". | Una tasa en m³/h no es un consumo diario. Si fueran 3,0 m³/h las 24 h, serían 288 L/cama·día en 250 camas. | Unidad ambigua. 3,0 m³/h son 12 L/h por cama, casi igual al caudal punta medido en D-26 (10,2 L/h por cama), así que probablemente es un caudal punta o de período y no un promedio de 24 h. No usar 288 L/cama·día como consumo diario. |
| E-07 | Navarra (D-09 contra D-22 y D-35): el rango de 215 a 415 kWh/m² de energía total no es compatible con los hospitales que el propio artículo lista. | Hospital de Navarra: GN 202 + electricidad 313 = **515** kWh/m². Virgen del Camino: 240 + 410 = **650** kWh/m². | El rango parece corresponder a un solo tipo de energía o a otra base de superficie. No usarlo como total. |
| E-08 | Electricidad en Navarra: (4) da 97 a 143 kWh/m² y (12) da 110 a 140 en 2011, mientras que (6) y (9) dan 286 a 410 en 2019. | Un salto de 2 a 3 veces en pocos años, sin explicación. | Probablemente cambió la base de superficie (útil o construida) o la fuente. No usar sin aclarar. |
| E-09 | ACS, potencia: (1) da 6,4 kW/cama y la tabla resumen da 10 W/m². | Con 150 m²/cama, 6,4 kW/cama = 42,7 W/m², contra 10 W/m² = 1,5 kW/cama: **4,3 veces menos**. | Las dos son de JG Ingenieros. La tabla coincide con el caso medido de Castilla-La Mancha (1,67 kW/cama, D-26). Para el modelo usar el orden de la tabla y declararlo. |
| E-10 | Refrigeración: el texto da 115 W/m² (D-14) y la tabla 100 W/m² (R-04). | 13 % de diferencia. | La tabla es un resumen redondeado de un hospital medio. Menor. |
| E-11 | Oxígeno, Alcorcón (D-47): "244.838 m³ de oxígeno líquido". | Si fueran m³ líquidos serían 206 millones de m³ de gas (factor 843), absurdo. Como gas son 51 m³/cama·mes, cerca de los otros casos (20 a 29). | Son m³ de gas, mal rotulados. Fuera de alcance. |
| E-12 | Contraste con 23 hospitales (D-61): los autores dicen que 380 contra 387 "valida perfectamente" el estudio. | El promedio es 386,8, pero el rango es 120 a 900 kWh/m²·año, la mediana 333 y el promedio ponderado por superficie 347. | La coincidencia del promedio no valida un valor puntual. Usarlo como banda de plausibilidad. |
| E-13 | Consumo térmico por m² con valores incompatibles entre filas: D-15 da 201 kWh/m² (España 2015) y D-16 da 110 a 133 (2011, 101 a 250 camas). D-15 implica además 132 m²/cama, contra 148 de D-02. D-21 (Vall d'Hebron) da 80.000 kWh/cama de gas. | 201 / 133 = +51 %; 201 / 110 = +83 %. Vall d'Hebron: 80.298 kWh/cama, 3 veces el promedio nacional (26.674); con 148 m²/cama serían unos 540 kWh/m² solo de gas. | Pueden deberse al tamaño, el año y la metodología (y a la base de superficie, Limitación 6), pero el artículo no lo aclara. D-14 a D-21 no son intercambiables como "kWh térmicos por m²" del hospital tipo. Vall d'Hebron es un atípico (22 edificios; posible cogeneración, no confirmado). |
| E-14 | ACS: los ratios de diseño del artículo son 200 a 300 L/cama·día (D-24, D-25), pero sus casos medidos apuntan a unos 50 a 55 L/cama·día. | D-28: 55 L/cama·día a 60 °C. D-26: caudal punta medido de 5,5 m³/h; si fuera el 80 % del consumo en 4 h (D-25), serían 27,5 m³/día = **51 L/cama·día** en 540 camas. Con 200 L/cama·día el caudal punta calculado sería 21,6 m³/h, 3,9 veces el medido. | Los datos medidos y D-28 dan 4 a 6 veces menos que los ratios de diseño. D-24 no indica temperatura; D-28 es la única con 60 °C. El hospital tipo debe elegir un valor, justificarlo y declararlo. |

**Observación (no es una inconsistencia):** el hospital de Castilla-La Mancha (D-26) produce 900 kW de ACS con 540 camas = **1,67 kW/cama**, frente a los **6,4 kW/cama** del ratio estándar (D-24). Es 3,8 veces menos. **Esto es una lectura mía, no del artículo:** el texto dice que las instalaciones de *almacenamiento y distribución* de ACS de los edificios existentes suelen ser muy superiores al consumo real (D-29), y no dice nada de la potencia de producción. Que una potencia medida menor que el ratio sea compatible con ese sobredimensionamiento no está afirmado.

**Observación sobre el ACS (relevante para el modelo):** la tabla da 40 kWh/m²·año con 200 L/cama·día y 150 m²/cama (R-03). El calor sensible para llevar ese caudal de 15 a 60 °C es **25,4 kWh/m²·año** (200 L × 4,18 kJ/kg·K × 45 K / 3.600 / 150 m² × 365). La tabla es 1,6 veces mayor, lo que es coherente con pérdidas de acumulación y recirculación, pero el artículo no lo dice. Para el hospital tipo hay que decidir qué ACS se modela y declararlo.

## F. Lo que el artículo NO da y habrá que conseguir en otra fuente

| Necesidad | Para qué cálculo | Fuente a buscar |
|---|---|---|
| Condiciones de diseño del aire exterior (temperatura de bulbo seco y húmedo, o humedad) y presión, en la ubicación elegida | Aire húmedo; estado muerto de exergía | Servicio Meteorológico Nacional, norma IRAM, o dato de la cátedra |
| Condiciones interiores y renovaciones de aire por zona (quirófano, UCI, habitaciones) | Aire húmedo | ASHRAE 170, normativa argentina de Salud, o dato de la cátedra |
| Refrigerante, temperaturas de evaporación y condensación, rendimiento isentrópico del compresor | Refrigeración | Catálogo de chiller de referencia y tablas de la cátedra |
| Composición del gas natural, PCS y PCI, condición de referencia del m³, exceso de aire. El artículo da 10,8 kWh/m³ y 90 % de rendimiento (S-3) sin aclarar la base | Combustión | ENARGAS o tablas de la cátedra |
| Temperaturas de red de agua fría y de entrega de ACS | ACS y combustión | D-28 da 60 °C; falta la temperatura de entrada |
| Potencia eléctrica de los equipos auxiliares (bombas, ventiladores) | Balance de energía y exergía | Supuesto fundamentado |

## G. Bibliografía del artículo

Las citas del artículo, tal como las lista al final. Son las referencias primarias de las columnas "Cita"; ninguna es accesible desde el entorno.

| N.º | Referencia |
|---|---|
| (1) | JG Ingenieros SA. *Manual de predimensionado. Las instalaciones a palmos.* 2017. |
| (2) | Datos de consumo de un hospital en Madrid (18.000 m² y 216 camas). Sin más datos. |
| (3) | Míguez C.D. de IDEA. *Consumos de energía en hospitales españoles.* Ingeniería hoy. Asociación Española de Ingeniería Hospitalaria. |
| (4) | Factura energética del Servicio Navarro de Salud. 2012. |
| (5) | Pedrajas Boceta J. Trabajo final de máster, Universidad de Comillas. *Auditoría energética de un hospital.* 2017. |
| (6) | *Informe anual de energía 2019.* Gobierno de Navarra. 2020. |
| (7) | IDEA. *Guía técnica. Agua caliente central.* |
| (8) | *Guía de orientación del uso eficiente de la energía y de diagnóstico energético.* Ministerio de Energía y Minas de Perú. |
| (9) | Gómez Cordeiro C. *Análisis de la importancia de la eficiencia energética en los hospitales.* Trabajo fin de grado, Universidad de Cantabria. 2021. |
| (10) | Comunidad de Madrid. *Guía de ahorro y eficiencia energética en hospitales.* |
| (11) | Ministerio de Energía, Gobierno de Chile. *Eficiencia energética.* 2021. |
| (12) | Servicio Navarro de Salud. *Plan de ahorro y eficiencia energética en los centros sanitarios del Servicio Navarro de Salud-Osasunbidea.* 2013. |
| (13) | Banco de Desarrollo de América Latina. *Manual para la evaluación de inversiones en eficiencia energética en el sector de hoteles y hospitales.* |
| (14) | Celis F. y otros. Universidad de Alcalá. *Eficiencia energética y arquitectura hospitalaria en España. Retos y posibilidades.* III Encuentro Latinoamericano y Europeo sobre Edificaciones y Comunidades Sostenibles. 2019. |
| (15) | García Guajardo J. *Casos prácticos de mejora de las infraestructuras y de la eficiencia energética de las instalaciones sanitarias.* Unidades docentes de la Escuela Nacional de Sanidad. UNED. 2013. |
| (16) | Guenter R. y Vittori G. *Sustainable Healthcare Architecture.* Wiley. 2013. |

Las referencias (2) y (7) no se pueden ubicar con certeza: la (2) no trae autor ni título, y los cálculos que se apoyan en ellas deben citarse a través del artículo.
