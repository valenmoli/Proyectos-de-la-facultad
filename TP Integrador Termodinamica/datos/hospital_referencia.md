# Hospital de referencia en el AMBA

> **Actualización:** se recibieron los documentos de las pistas y se transcribieron en [`referencias_argentina.md`](referencias_argentina.md). El Cruce quedó leído del documento original, el informe de Health Care Without Harm trae **consumos estimados por auditoría de tres hospitales argentinos** (no medidos) (incluido el Garrahan, del AMBA) y el documento del Austral **no trae cifras de energía**. Lo que sigue en este archivo (la tabla de candidatos y las pistas) es el estado previo a esa lectura y se conserva como registro.

**Estado de la tabla de candidatos: SIN VERIFICAR**, salvo El Cruce (ver arriba). Las cifras salen de extractos de búsqueda web, no de abrir la fuente (los dominios están bloqueados desde el entorno). **No entran al modelo** hasta confirmarse con el documento original.

**Criterio (decisión D5 del PRD):** hospital real del AMBA, de la **misma magnitud** que el hospital tipo (10.000 a 50.000 m² y 60 a 300 camas), no igual. Pesa más que los datos estén documentados que la cercanía exacta al tamaño. Se usa para contrastar intensidades (kWh/m², W/m², m²/cama) del hospital tipo, no para reemplazarlo.

> **Actualización posterior:** se recibieron los documentos de Favaloro y Nordelta y se transcribieron en [`favaloro_nordelta.md`](favaloro_nordelta.md). **Cambia la selección:** ninguno de los documentos de Nordelta trae la superficie, y Favaloro resultó tener más datos firmes (superficie oficial, seis quirófanos, distribución por pisos). La selección provisoria pasa de Nordelta a **Favaloro**. La tabla de abajo es el estado previo a esa lectura y se conserva como registro.

## Decisión en curso: Favaloro o Nordelta (D7 del PRD)

**Criterio acordado:** nos quedamos con el que tenga **más información relevante para el modelo**, y lo que falte **se estima** como supuesto declarado. Información relevante es la que fija el tamaño del edificio, las zonas críticas (que son el caso psicrométrico detallado) y el sistema térmico.

**Estado: cifras de extractos de búsqueda, sin verificar.** Se confirman cuando se descarguen las fuentes de abajo.

| Información que necesita el modelo | Favaloro (SAMIC, Rafael Castillo, La Matanza) | Nordelta (Swiss Medical, Tigre) |
|---|---|---|
| Ubicación en el AMBA | Sí, conurbano oeste | Sí, conurbano norte |
| Estado y año | Inaugurado el 28 de julio de 2020 | Abierto en junio de 2025, 5 pisos y 2 subsuelos |
| Superficie cubierta | **18.352 m²**, documento oficial de proyecto (Casa Rosada). Base clara | **24.000 m²** (nota de inicio de obra de 2018). Otra fuente dice **26.000**. Cifra de proyecto, sin total final |
| Camas | **158** al inaugurar (144 de internación general + 14 de terapia intensiva), fuente oficial de la Provincia. El proyecto preveía 160 | **127 habitaciones** de internación clínico-quirúrgica y pediátrica, más terapia intensiva de **18 habitaciones individuales**. No está claro si las 18 están dentro de las 127 |
| m² por cama (calculado) | 116 | 189 (con 127) o 165 (con 145) |
| Quirófanos | Existen, **sin número**. Seis shock rooms, salas de obstetricia | **4 quirófanos** "inteligentes", **2 salas de procedimientos** y un centro quirúrgico de alta complejidad. Quirúrgico y terapia intensiva en el 2.º piso (según el proyecto de 2018) |
| Terapia intensiva | 14 camas | 18 habitaciones, adultos y pediátrica, más unidad coronaria y hemodinamia |
| Climatización y energía | **Nada encontrado** | Un extracto previo de Cronista habla de **recuperadores de calor que reutilizan más del 50 % de la energía del aire extraído**, vidrios de control solar y terrazas verdes. Esta búsqueda no lo reconfirmó. Sin chillers ni consumos |
| Consumo energético | No | No |
| Tipo de fuente | Documento oficial del Estado | Prensa y comunicados de empresas (es privado) |

**Lectura:**
- **Favaloro tiene los números básicos más firmes** (superficie y camas de fuentes oficiales), pero **nada sobre zonas críticas ni sistema térmico**.
- **Nordelta tiene más información relevante para este trabajo**: cuenta quirófanos y habitaciones de terapia intensiva (lo que fija el caso psicrométrico detallado) y menciona recuperación de calor del aire de extracción, que es justo una de nuestras mejoras. Su punto débil es que la superficie y las camas son de proyecto o de prensa y hay dos valores para la superficie (24.000 y 26.000).
- **Selección provisoria: Nordelta**, condicionada a confirmar superficie y camas. **Favaloro queda como respaldo.**
- Ambos encierran el supuesto de 150 m²/cama del hospital tipo (116 y 165 a 189), y ambos son de la misma magnitud que 20.000 m².

**Qué se estimaría** (supuestos declarados) en cualquiera de los dos: el tipo de planta térmica (enfriadora, calderas, unidades de tratamiento de aire), las renovaciones de aire y condiciones interiores por zona, las superficies de cada zona crítica, los horarios de uso y el consumo. El clima es el del AMBA. Lo que se calcula es el consumo (D6).

**Fuentes para confirmar** (descargar y adjuntar; se verifican con el método de siempre):

| Hospital | Documento | Qué confirma |
|---|---|---|
| Nordelta | [Cronista, apertura](https://www.cronista.com/negocios/swiss-medical-inauguro-un-centro-medico-con-tecnologia-de-ultima-generacion-en-nordelta) | Habitaciones, terapia intensiva, quirófanos, recuperadores de calor |
| Nordelta | [La Nación, inicio de obra (2018)](https://www.lanacion.com.ar/economia/negocios/con-una-inversion-de-us80-millones-belocopitt-y-costantini-iniciaron-la-construccion-de-una-clinica-en-nordelta-nid2148786/) | 24.000 m² cubiertos, pisos y subsuelos |
| Nordelta | [Comunicado de Dedalus (PDF)](https://www.dedalus.com/latam/wp-content/uploads/sites/23/2025/07/NP_Dedalus_Hospital-Nordelta-Swiss-Medical.pdf) | Apertura y equipamiento |
| Nordelta | [Ficha de proyecto de Mapei](https://www.mapei.com/ca/fr-ca/projets/project-detail/clinica-swiss-medical-nordelta) | Las fichas de este proveedor suelen traer la superficie; hay que ver si esta la trae |
| Favaloro | [Presentación oficial en Casa Rosada (PDF)](https://www.casarosada.gob.ar/pdf/Acto_Central_-_Hospital_Dr.pdf) | 18.352 m² cubiertos, 160 camas previstas |
| Favaloro | [Gacetilla de la Provincia](https://gba.gob.ar/comunicacion_publica/gacetillas/kicillof_particip%C3%B3_de_la_inauguraci%C3%B3n_del_hospital_doctor_ren%C3%A9) | 144 + 14 camas al inaugurar |

## Resultado en una línea

Hay buenos candidatos **de tamaño y geometría**. **No se encontró ningún hospital del AMBA de esta magnitud con consumo energético real ni datos de climatización publicados** (chillers, calderas, gas). Para eso hay tres pistas que requieren abrir documentos (sección "Pistas de energía").

## Candidatos de tamaño

Ordenados por calidad de la documentación, no por cercanía a 20.000 m². "Base" indica si la fuente aclara que la superficie es cubierta o es de terreno.

| Hospital | Dónde | Superficie | Base | Camas | Fuente (extracto) | Notas |
|---|---|---|---|---|---|---|
| **El Cruce** "Dr. Néstor C. Kirchner" (SAMIC, público) | Florencio Varela | **22.000 m²** sobre 47.000 m² de terreno | **Cubierta** (la fuente separa terreno de cubierta) | **140** (2010) | [Revista Argentina de Salud Pública, dic. 2010](https://rasp.msal.gov.ar/index.php/rasp/article/download/417/349/711) | El mejor documentado: unos 157 m²/cama, casi igual al supuesto de 150. Incluye 1.300 m² de espacios quirúrgicos. Cifras de 2010: después tuvo 171 camas (2015) y una ampliación de +88 camas (Edificio 7, primera etapa de 2.400 m²). Confirmado dos veces por extracto, no abriendo la página. |
| Sanatorio Nordelta (Swiss Medical, privado) | Tigre | 24.000 m² (proyecto 2018); otra fuente dice 26.000 | Cubierta según [La Nación](https://www.lanacion.com.ar/economia/negocios/con-una-inversion-de-us80-millones-belocopitt-y-costantini-iniciaron-la-construccion-de-una-clinica-en-nordelta-nid2148786/) para los 24.000; los 26.000 no aclaran | 127 "habitaciones" (no está claro si son camas) | [Cronista](https://www.cronista.com/negocios/swiss-medical-inauguro-un-centro-medico-con-tecnologia-de-ultima-generacion-en-nordelta) | Terapia intensiva y quirófanos. Menciona recuperadores de calor que reutilizan más del 50 % de la energía del aire extraído. Sin datos de chillers, calderas ni consumo. |
| Hospital Dr. René Favaloro (SAMIC) | Rafael Castillo, La Matanza | 18.352 m² (proyecto) | Cubierta según [Casa Rosada](https://www.casarosada.gob.ar/pdf/Acto_Central_-_Hospital_Dr.pdf) | 158 al inaugurar (144 + 14 de terapia intensiva), según [gba.gob.ar](https://gba.gob.ar/comunicacion_publica/gacetillas/kicillof_particip%C3%B3_de_la_inauguraci%C3%B3n_del_hospital_doctor_ren%C3%A9) | Documento oficial de proyecto | La superficie es de proyecto; no está verificado que coincida con la obra terminada. |
| Hospital Municipal de Alta Complejidad para Adultos | Tigre | 14.800 m² (primera etapa) | Cubierta según [Perfil](https://www.perfil.com/noticias/empresas-y-protagonistas/julio-zamora-anuncio-el-hospital-municipal-mas-grande-de-la-region-14800-m-para-la-salud-en-tigre.phtml) | 150 | Prensa | Estaba en obra en 2023; no consta si está operando. |
| Sanatorio Anchorena Itoiz (UPCN) | Avellaneda | 17.100 m² tras la ampliación | Cubierta según [Minutouno](https://www.minutouno.com/politica/alberto-fernandez/el-presidente-inauguro-un-nuevo-sanatorio-upcn-n5312073) | Sin total; la ampliación suma 84 + 10 | Prensa | Seis quirófanos centrales. |
| Hospital del Bicentenario de Esteban Echeverría | Monte Grande | 22.332 m² | "Construcción" según [La Nación](https://www.lanacion.com.ar/buenos-aires/hospitales-del-bicentenario-los-prometio-el-gobierno-para-2011-y-aun-no-estan-terminados-nid1659104/); no aclarado | 150 previstas; 80 operando en 2020 | Prensa | Cifras de proyecto. |
| Hospital Universitario Austral (privado) | Pilar (borde exterior del AMBA) | 36.000 m² en una página y 45.633 m² en otra, del mismo hospital | No aclarado | 220 a 256 (76 críticas), 15 quirófanos | [Hospital Austral](https://www.hospitalaustral.edu.ar/2025/09/el-hospital-universitario-austral-conmemoro-sus-25-anos-y-reafirmo-su-compromiso-con-la-salud-en-la-argentina/) | Está en el borde superior del rango y de la ciudad. Es el que más probablemente tenga datos de energía (ver abajo). |
| Sanatorio Finochietto | Balvanera, CABA | 16.700 m² (ficha de un proveedor); otras notas dan más de 17.000 y 13.000 | No aclarado | "200" es una suma del buscador (157 habitaciones + 27 de UTI + 16 de neonatología), **no un dato declarado** | [Mapei](https://www.mapei.com/it/en/projects/detail/sanatorio-finochietto-5947) | Seis quirófanos. Las camas no son confiables. |
| Hospital Alemán | Barrio Norte, CABA | Solo la Torre Juncal: 10.070 m² (otro texto, 11.000) | No aclarado | Torre: 104. Hospital: 246 ([IFC](https://disclosures.ifc.org/project-detail/SII/40682/hospital-aleman)), 264 (Wikipedia) o 200 (un proveedor) | Prensa e IFC | No hay superficie total del hospital. La torre tiene certificado EDGE de diseño con 29,05 % de ahorro de energía y sistema VRV (valores de diseño, no consumo). |
| Hospital Británico | Barracas, CABA | El edificio central "ocupa 30.000 m²"; un masterplan de 2014 habla de 64.562 m² cubiertos y 345 camas | Contradictorio | Sin dato firme | [Sitio oficial](https://www.hospitalbritanico.org.ar/centros-medicos/ver/3) | Contrata energía renovable por 5.400 MWh/año para cubrir el 80 % de su demanda eléctrica ([Mercado](https://mercado.com.ar/gestion-sustentable/el-hospital-britanico-cubrira-el-80-de-su-demanda-electrica-con-energia-renovable)). Con la superficie contradictoria no se puede sacar una intensidad. |

Descartados en la búsqueda: Hospital Italiano de Buenos Aires (78.000 m² y 750 a 825 camas, demasiado grande), Hospital Posadas (unos 82.000 m² y 520 camas), Garrahan (587 camas y unos 110.000 m², aunque tiene auditoría energética, ver abajo). Varios hospitales de CABA y del conurbano no tienen superficie publicada en lo que se encontró.

## Pistas de energía (lo más valioso, y todo pendiente de abrir)

Es lo que más pesa para el contraste. Se necesita descargar los documentos, porque desde el entorno no se pueden abrir.

| Pista | Qué podría aportar | Enlace |
|---|---|---|
| **Informe final de Health Care Without Harm**, *Energy efficiency and cooling audits in health care facilities in Argentina, China and the Philippines* (2019 a 2021) | Auditorías energéticas con perfil de consumo, equipos de frío y refrigerantes. El Garrahan figura entre los hospitales argentinos auditados. Otro hospital argentino que se nombra, el Giordano de Albardón, es de San Juan, fuera del AMBA. El informe tiene una sección de Argentina. | [global.noharm.org](https://global.noharm.org/resources/energy-efficiency-and-cooling-audits-health-care-facilities-argentina-china-and) |
| **Informe de Sostenibilidad 2024 del Hospital Universitario Austral** | Indicadores ambientales; el hospital dice haber aplicado criterios de eficiencia a la secuencia de chillers y contratar 60 % de energía solar. Las tablas no se pudieron leer. | [PDF](https://testhua.hospitalaustral.edu.ar/austral/wp-content/uploads/2025/06/Hospital-Universitario-Austral-Informe-Sostenibilidad-2024.pdf) |
| **Hospital Pedro de Elizalde (CABA, 244 camas)** | En 2018 se le encargó una unidad de cogeneración compacta GG 50 (Sokratherm). No se encontró el combustible, la potencia eléctrica ni resultados, ni la superficie. Sería un caso real de combustión y cogeneración en un hospital porteño. | [Sokratherm](https://sokratherm.de/?p=4020) |

## Resultado de las pistas (actualizado)

1. **Informe de Health Care Without Harm:** trae consumos estimados por los auditores (no medidos) de Garrahan, CEMAR y Giordano, con kWh/m²·año, por cama y por paciente. Detalle en `referencias_argentina.md`, secciones 1 y 2.
2. **Nota de El Cruce:** confirma 22.000 m² cubiertos, 140 camas y 50 % de camas críticas (2010). No trae datos de climatización ni de energía.
3. **Documento del Austral:** es un resumen del plan de sostenibilidad, sin kWh, gas, chillers, superficie ni camas. La pista queda cerrada.
4. **Hospital Elizalde (cogeneración):** sin novedades; sigue sin combustible, potencia ni resultados.

Todavía no hay un hospital del AMBA de unos 20.000 m² con consumo real publicado. El informe del proyecto debe declarar esa limitación.
