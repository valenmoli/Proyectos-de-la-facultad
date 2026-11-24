# Presentación oral: estructura propuesta (10 a 15 minutos)

La consigna pide «énfasis en la metodología, los resultados y la justificación de la propuesta». Son **12 diapositivas en unos 13 minutos**, más 4 de reserva (no se proyectan salvo que pregunten). Cada una usa una figura o tabla del informe, para que lo dicho y lo escrito coincidan. Las cifras son las del informe actual; si el modelo cambia, se actualizan con él.

| N.º | Diapositiva | Qué se muestra (informe) | Tiempo | Idea que tiene que quedar |
|---|---|---|---|---|
| 1 | Problema y objetivo | Tabla 1 (los cuatro temas) | 0:45 | En verano se gasta frío para quitar humedad y gas para devolver temperatura; los cuatro temas son una cadena |
| 2 | El edificio y sus datos | Tablas 2 y 3 | 1:00 | Hospital con el tamaño del Favaloro (18.352 m², 158 camas, 6 quirófanos); cada dato con su fuente; no es el consumo total del hospital |
| 3 | Condiciones interiores | Figuras 2 (Givoni) y texto de 20/4 | 1:15 | 24 °C y 55 a 60 % caen dentro de la zona de Givoni; 20/4 renovaciones de ASHRAE 170, y por carga bastarían 6,5: manda la norma |
| 4 | El sistema y por qué | Figura 1 y Tabla 4 | 1:00 | Todo aire, enfriadora por aire, caldera de gas, con reserva; qué tiene que dar: 1.987 kW de frío, 734 kW de calor, 43 kW de ACS |
| 5 | Metodología | Sección 4 | 1:00 | Cuatro pasos encadenados, hipótesis y frontera |
| 6 | Aire húmedo | Figura 3 y Tabla 5 | 1:15 | Quirófano A a F en la carta: serpentina de 79,5 kW (58,8 sensibles y 20,7 latentes), recalentador de 18,7 kW |
| 7 | Refrigeración | Figura 4 y ecuaciones | 1:15 | q_L, w, COP = 3,56 (55 % del de Carnot), compresor de 559 kW, condensador rechaza 2.512 kW |
| 8 | Combustión y consumo anual | Reacción, rendimiento y Figura 5 | 1:15 | η = 90 % sobre PCI; 3.021 MWh por año (165 kWh/m²); ventiladores 28 %, compresor 24 %, recalentamiento 21 % |
| 9 | Equipos y ubicación | Figura 6 | 1:00 | Carrier 30XA 1002, 3 en servicio + 1 de reserva: 2.964 kW con una parada contra 1.987 kW; azotea, shafts, izaje |
| 10 | Exergía | Figura 7 | 1:15 | Se destruye el 86 %; enfriadora y su entorno 42 %; la caldera tiene 13 % de eficiencia exergética: llama de unos 1.850 °C para subir el aire unos kelvin |
| 11 | Alternativas y mejoras | Tablas 7 y 8 | 2:00 | B recupera el calor del condensador (−18 % de energía, −10 % de CO₂); fotovoltaica, solar térmico, recuperador, caldera de condensación; paquete −50 % y −41 % |
| 12 | Conclusiones y límites | Sección 9 | 1:00 | Las cinco respuestas con una cifra cada una; qué falta (datos reales, normas cotejadas, costos) |

**Reserva:** sensibilidad completa (memoria), planta tipo a escala (memoria), matriz azotea contra patio (memoria), exergía por equipo (memoria).

## Diapositivas de propuestas ya armadas

El grupo entregó un informe que calcula **tres estados de diseño** (V1 verano pico, V2 verano húmedo, I invierno), no un consumo anual; las diapositivas 10 y 11 de los compañeros (alternativa B y medidas M1 a M3) coinciden con ese informe. Para la parte de propuestas (diapositivas 10 a 12) se usa:

- la diapositiva 10 de los compañeros (alternativa B en V2);
- `diapositiva_11_mejoras.pptx`: reemplaza su 11 y muestra las tres medidas del informe con sus cifras de invierno, más tres ideas verdes rotuladas como estimación aparte;
- `guion_diapositivas_10_a_12.md`: guion con las cifras del informe, lo que conviene no repetir de él y las preguntas probables.

La primera versión, con cifras del modelo anual propio, quedó en `version_modelo_anual/` como respaldo.

## Preguntas probables y de dónde sale la respuesta

- *¿Por qué 3+1 y no 2+1?* Con 2+1 y la misma unidad faltan 11 kW (0,6 %); 3+1 cumple con una unidad parada pero queda sobredimensionada (informe, sección 6.1).
- *¿De dónde sale el 20/4?* ASHRAE 170 para quirófanos; las 20 mueven y filtran el aire, las 4 son aire fresco; relación 5 (sección 3.3). La fuente es un extracto: hay que tener la norma a mano.
- *¿Por qué el estado muerto es el aire exterior?* Es lo que el ambiente da gratis en cada caso; con otro estado muerto la destrucción total cambia menos de 4,4 % (memoria).
- *¿Qué tan seguro es el número de 3.021 MWh?* Es una estimación con un modelo y supuestos nuestros: varía de 141 a 202 kWh/m² cambiando un supuesto por vez; no es un intervalo de confianza (sección 8.3).
- *¿Por qué B no ahorra todo el gas?* El calor del condensador solo sirve cuando hay frío que producir y recalentamiento que hacer al mismo tiempo; con coincidencia de 75 % o 50 % el ahorro baja a 13,5 % y 8,5 %.
- *¿Qué es la carta de Givoni?* Una carta psicrométrica con la zona de confort sin equipos (18 a 29 °C, 20 a 80 %, 4 a 17 g/kg).

## Pendiente

La fecha de exposición y los integrantes que presentan cada parte no están definidos. Las diapositivas se arman cuando el informe esté aprobado, para no rehacerlas.
