# Datos del artículo de Hospitecnia

**Fuente:** *Caracterización de consumos energéticos y suministros en hospitales*. Juan Gallostra Isern (JG Ingenieros), Ángel Sánchez-Vaqué (Hospitecnia) y Josep Túnica Buira (JG Ingenieros S.A.). Hospitecnia, octubre de 2022.
https://hospitecnia.com/instalaciones/caracterizacion-de-consumos-energeticos-y-suministros-en-hospitales/

**Archivo recibido:** PDF de 15 páginas impreso desde el navegador. El contenido útil está en las págs. 1 a 7; las págs. 8 a 15 son publicidad, menús y patrocinadores.

**Estado:** transcripción v0.1, **pendiente de verificación independiente** contra el PDF.

## Limitaciones de la fuente (leer antes de usar cualquier número)

1. **Artículo cortado.** Termina en la sección de ACS con "Para poder seguir leyendo este artículo debe iniciar sesión o darse de alta en el portal". El propio texto dice que la bibliografía está "al final del informe", y no está. **Las citas (1) a (15) no se pueden identificar.** Para la consigna ("fuentes de los datos") la fuente citable es el artículo mismo, como fuente secundaria.
2. **Datos de España** en su gran mayoría (Madrid, Navarra, Barcelona, Castilla-La Mancha), más Chile, Perú y Portugal. **No hay clima ni consumos de Argentina.**
3. El texto dice que los datos "han sido obtenidos e interpolados a partir de la bibliografía consultada" y que no es fácil dar ratios por la gran variabilidad. Son órdenes de magnitud, no valores de diseño.
4. Hay **cifras internamente inconsistentes** (sección E). No se usan.
5. **No trae** lo necesario para los cálculos termodinámicos: condiciones interiores de diseño (T, HR), caudales o renovaciones de aire, COP o capacidad de chillers, rendimiento de calderas, ni composición del combustible (sección F).

**Columna "Uso propuesto":** *Modelo* = candidato a entrada del hospital tipo. *Contraste* = sirve para validar que nuestros resultados sean razonables. *Contexto* = para la introducción. *No usar* = inconsistente.

## A. Ratios y superficie

| ID | Dato | Valor | Unidad | Contexto | Cita | Uso propuesto |
|---|---|---|---|---|---|---|
| D-01 | Superficie construida por cama | 60 (años 70) a cerca de 200 (actual) | m²/cama | Evolución histórica | — | Modelo |
| D-02 | Superficie por cama, promedio España | 148 | m²/cama | Todos los hospitales de España | (3) | Modelo |
| D-03 | Peso del costo energético | hasta 10 | % de los costos de operación | "Según diversas fuentes" | — | Contexto |
| D-04 | Participación del sector sanitario | 27 | % del consumo del sector servicios | España, 2018; detrás de oficinas y comercio | (9) | Contexto |
| D-05 | Reparto electricidad / combustible | casi a partes iguales | — | "En muchos hospitales": electricidad (alumbrado, fuerza, refrigeración) y GN o gasóleo (calefacción y ACS) | párrafo de (9) | Contexto |

## B. Energía total y repartos

| ID | Dato | Valor | Unidad | Contexto | Cita | Uso propuesto |
|---|---|---|---|---|---|---|
| D-06 | Reparto del consumo | 20 ACS / 35 iluminación / 45 climatización | % | Establecimientos sanitarios; "mismos datos" en (4) | (10), (4) | Contraste |
| D-07 | Energía total anual (térmica + eléctrica) | 225 atlántica / 274 continental / 276 mediterránea | kWh/m² | Hospitales de 101 a 250 camas, España, 2011 | (3) | Contraste |
| D-08 | Hospital de Madrid | 17.957 m², 213 camas, 7 plantas; 7,5 millones kWh/año; 418 kWh/m² | — | Auditoría energética | (5) | Contraste |
| D-08a | Reparto por uso, hospital de Madrid | 40 calefacción / 21 equipamiento / 20 refrigeración / 7 ACS / 6 ventilación / 6 iluminación y otros | % | Suma 100 % | (5) | Contraste |
| D-08b | Reparto por fuente, hospital de Madrid | 54 electricidad / 45 gasóleo / 1 gas natural (cocina) | % | Suma 100 % | (5) | Contraste |
| D-09 | Hospitales de Navarra, 2019 | 46 % de la energía de edificios públicos; 73 millones kWh/año; 44 % electricidad, 51 % GN, 5 % otros; 215 a 415 kWh/m²·año | — | Estudio de Navarra | (6) | Contraste |
| D-10 | Reparto de fuentes en Perú | 66 electricidad / 34 gas natural | % | — | (8) | Contexto |
| D-11 | Hospitales de Chile | 39 hospitales, 34.137 m² y 343 camas promedio; 255 kWh/m²·año; 64 % eléctrico y 36 % térmico | — | — | (11) | Contraste |
| D-11a | Chile, consumo térmico | 30 agua caliente / 54 climatización / 6 central de esterilización / 5 equipos industriales / 5 cocina y otros | % | Suma 100 % | (11) | Contraste |
| D-11b | Chile, consumo eléctrico | 3 ACS / 21 climatización / 25 iluminación / 25 equipos médicos / 14 equipos industriales / 6 oficina / 6 electrodomésticos / 3 otros | % | **Suma 103 %** (ver E-04) | (11) | Contraste con cautela |
| D-12 | Distribución típica según el Banco de Desarrollo de América Latina | 51 climatización / 12 ventilación y bombas / 6 ACS / 14 iluminación / 17 equipos | % | Suma 100 % | (13) | Contraste |
| D-13 | Hospital caso UNED | 410 camas, 71.500 m², interior de la península; 9,8 millones kWh eléctricos y 15,6 millones kWh de GN; 137 y 218 kWh/m²; 40 % electricidad / 60 % GN en energía y 60 % / 40 % en gasto | — | Estudio de casos | (15) | Contraste |

## C. Energía térmica y combustibles

| ID | Dato | Valor | Unidad | Contexto | Cita | Uso propuesto |
|---|---|---|---|---|---|---|
| D-14 | **Cargas térmicas estándar** | **115 refrigeración / 90 calefacción** | W/m² | "Cargas térmicas estándares" | (1) | **Modelo** |
| D-15 | Consumo térmico nacional, España 2015 | 791 hospitales, 158.566 camas, 4.200 millones kWh/año; 26.674 kWh/cama y 201 kWh/m² | — | Indicador medio anual | — | Contraste |
| D-16 | Consumo térmico anual | 113 atlántica / 133 continental / 110 mediterránea | kWh/m² | Hospitales de 101 a 250 camas, España, 2011 | (3) | Contraste |
| D-17 | Consumo térmico por cama, Navarra | 20.500 a 29.000 | kWh/cama·año | — | (4); detalle en (12) | Contraste |
| D-18 | Combustibles para energía térmica, 2011 | 73 gas natural / 23 gasóleo / 4 otros | % | Suma 100 % | (3) | **Modelo** (combustible: GN) |
| D-19 | Hospital de Madrid, GN 2020 | 127.830 kWh; "71 kWh/m²"; máx. 21.474 kWh en enero; mín. 1.354 kWh en agosto; 18.000 m², 216 camas | — | — | (2) | **No usar** (E-01) |
| D-20 | Hospital de Madrid, gasóleo | "3,4 millones de litros/año"; máx. 60.000 L en diciembre; mín. 30.000 L en los tres meses de verano | — | Calderas de calefacción y ACS | (5) | **No usar los litros** (E-02) |
| D-20a | Reparto del gasóleo | 86 calefacción / 14 ACS | % | Suma 100 % | (5) | Contraste |
| D-21 | Hospital Vall d'Hebron (Barcelona), 2016 | 22 edificios, 1.100 camas; 88.328 MWh de gas; 80.000 kWh/cama | — | — | — | Contraste |
| D-22 | Hospitales públicos de Navarra, 2019 | Hospital de Navarra: 15,8 millones kWh, 78.000 m², 202 kWh/m². Virgen del Camino: 10,4 millones kWh, 43.000 m², 240 kWh/m² | — | Consumo de GN | (6) | Contraste |
| D-23 | Hospital de Coímbra, 2010 | 1.600 camas; 38 millones kWh de combustible; "31.457 kWh/cama·año"; 310 kWh/m²·año | — | — | (8) | **No usar** (E-03) |

## D. Agua caliente sanitaria (ACS)

| ID | Dato | Valor | Unidad | Contexto | Cita | Uso propuesto |
|---|---|---|---|---|---|---|
| D-24 | **Consumo y potencia de ACS** | **200 L/cama·día; 6,4 kW/cama de potencia de preparación** | — | Ratios | (1) | **Modelo** |
| D-25 | Consumo de ACS, asociación española de ingeniería hospitalaria | 200 a 300 L/cama·día; 80 % consumido en un período no superior a 4 h | — | — | — | **Modelo** |
| D-26 | Hospital general en Castilla-La Mancha | 540 camas, 96.600 m²; 900 kW de producción de ACS; acumulación total 36.000 L; caudal punta máximo medido 5,5 m³/h | — | — | — | Contraste |
| D-27 | Clínica privada en Madrid | 250 camas; acumulación de ACS 9.000 L; consumo promedio diario "3,0 m³/h" (unidad ambigua, ver E-06) | — | — | — | Contraste con cautela |
| D-28 | Consumo de ACS, hospitales y clínicas | 55 L/día·cama a 60 °C | — | — | (7) | **Modelo** (única que da la temperatura: 60 °C) |
| D-29 | Tendencia del ACS | Disminuyó por menor estancia media, lavado en cama, griferías de bajo caudal, lavamanos solo con agua fría (legionela), lavado de cocina más eficiente y lavandería externalizada | — | "Las instalaciones de ACS suelen ser muy superiores al consumo real" | — | Contexto |

## E. Inconsistencias detectadas en el artículo

Verificadas con cálculo, ver la sesión de trabajo. **No se usan estas cifras sin aclarar.**

| ID | Problema | Cálculo | Lectura probable |
|---|---|---|---|
| E-01 | GN Madrid 2020 (D-19): 127.830 kWh no da 71 kWh/m². | 127.830 / 18.000 = **7,1** kWh/m². Para dar 71 harían falta 1.278.300 kWh, pero entonces el mes máximo (21.474 kWh) quedaría por debajo del promedio mensual (106.525 kWh). | Los valores mensuales cuadran con 127.830 kWh, y "71" sería un error por 7,1. |
| E-02 | Gasóleo Madrid (D-20): 3,4 millones de litros/año, pero el máximo mensual es de 60.000 L. | Tope posible con los 12 meses al máximo: 720.000 L/año. Además, 45 % de 7,5 GWh = **3,375 GWh**. | "3,4 millones" parece ser 3,4 millones de **kWh**, no de litros. Las proporciones 86 / 14 siguen siendo usables. |
| E-03 | Coímbra (D-23): 38 millones kWh con 1.600 camas no da 31.457 kWh/cama. | 38e6 / 1.600 = **23.750** kWh/cama; 31.457 × 1.600 = 50,3 millones kWh. Con 310 kWh/m² el área implícita es 122.581 m² (76,6 m²/cama). | Dos de los tres números no son consistentes entre sí. |
| E-04 | Chile, consumo eléctrico (D-11b): los porcentajes suman **103 %**. | 3 + 21 + 25 + 25 + 14 + 6 + 6 + 3 = 103 | Redondeos o un error de transcripción de la fuente. |
| E-05 | España térmico 2015 (D-15): 4.200 millones kWh / 158.566 camas = 26.487, el artículo dice 26.674 (0,7 % de diferencia). | — | Menor; probablemente el total estimado está redondeado. |
| E-06 | Clínica de Madrid (D-27): "consumo promedio diario es de 3,0 m³/h". | Una tasa en m³/h no es un consumo diario. Si fueran 3,0 m³/h las 24 h, serían 288 L/cama·día en 250 camas. | Unidad ambigua. |

**Observación (no es una inconsistencia):** el hospital de Castilla-La Mancha (D-26) produce 900 kW de ACS con 540 camas = **1,67 kW/cama**, frente a los **6,4 kW/cama** del ratio estándar (D-24). Es 3,8 veces menos, y coincide con lo que dice el texto: las instalaciones existentes suelen estar sobredimensionadas respecto del consumo real.

## F. Lo que el artículo NO da y habrá que conseguir en otra fuente

| Necesidad | Para qué cálculo | Fuente a buscar |
|---|---|---|
| Condiciones de diseño del aire exterior (temperatura de bulbo seco y húmedo, o humedad) y presión, en la ubicación elegida | Aire húmedo; estado muerto de exergía | Servicio Meteorológico Nacional, norma IRAM, o dato de la cátedra |
| Condiciones interiores y renovaciones de aire por zona (quirófano, UCI, habitaciones) | Aire húmedo | ASHRAE 170, normativa argentina de Salud, o dato de la cátedra |
| Refrigerante, temperaturas de evaporación y condensación, rendimiento isentrópico del compresor | Refrigeración | Catálogo de chiller de referencia y tablas de la cátedra |
| Composición del gas natural, PCI/PCS, exceso de aire, rendimiento de caldera | Combustión | ENARGAS o tablas de la cátedra |
| Temperaturas de red de agua fría y de entrega de ACS | ACS y combustión | D-28 da 60 °C; falta la temperatura de entrada |
| Potencia eléctrica de los equipos auxiliares (bombas, ventiladores) | Balance de energía y exergía | Supuesto fundamentado |
