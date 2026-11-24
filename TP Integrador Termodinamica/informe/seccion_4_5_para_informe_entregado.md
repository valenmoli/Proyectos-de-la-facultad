# Sección 4.5 para el informe entregado (borrador)

Borrador de una sección nueva para el informe que subió el grupo (`TP_Integrador_Hospital_Favaloro`), después de «4.4 Ventajas, limitaciones e impacto ambiental». Respalda la diapositiva 11 («Mejoras de sustentabilidad, en tres familias»). Las cifras salen de nuestro cálculo anual (`informe/informe_tecnico.md`, `informe/memoria_calculo.md` y `calculo/mejoras.py`). El texto a pegar va entre los dos marcadores; lo que sigue son los cambios necesarios en el resto del informe.

<!-- INICIO SECCION -->

## 4.5 Mejoras de sustentabilidad: estimación anual aparte

Las secciones 3 y 4.1 a 4.3 calculan estados de diseño. Las medidas que producen energía o dan sombra necesitan un cálculo anual, así que se hizo una **estimación aparte, simple y de orden de magnitud**: mismo edificio y misma demanda de ACS (unos 43 kW), pero un modelo independiente, con medias mensuales aproximadas de Buenos Aires partidas en día y noche (no los estados de diseño de Ezeiza de la sección 1.4 y la tabla 3), sin cargas parciales y con cargas de diseño propias (frío de 1.987 kW, contra 1.489 kW del informe). **Sus porcentajes no son comparables con los de las secciones anteriores.**

La alternativa A consume 3.021 MWh de energía final por año (1.736 de electricidad y 1.285 de gas sobre PCS, sumados sin ponderar por energía primaria) y emite 895 t de CO₂, con 0,183 kg por kWh PCS de gas y 0,38 t/MWh de electricidad (supuesto; con 0,29 y 0,40 el paquete baja 44,0 % y 40,6 % de CO₂). Es la energía del sistema térmico, no el consumo total del hospital.

| Familia | Medida | Energía | CO₂ | Qué hay que saber |
|-------------|----------------------|-----------|-----------|-------------------------------------------|
| Producir energía limpia | Fotovoltaica de 250 kWp | −11,3 % | −14,4 % | 340 MWh/año (1.700 kWh/m²·año y rendimiento de 0,8: supuestos). Cubre consumo, no lo reduce |
| | Fotovoltaica de 500 kWp | −22,5 % | −28,9 % | 680 MWh/año; 41 % de la azotea (unos 6.117 m² por nivel, con 18.352 m² en tres niveles iguales: supuesto). Supone que otras cargas absorben el excedente. Fuera del paquete |
| | Solar térmico de 300 m² | −8,3 % | −5,1 % | 204 MWh/año de calor solar (251 MWh de gas evitado); cubre el 54 % del ACS en el año (29 % en junio) y la caldera aporta el resto |
| No desperdiciar | B: calor del condensador (agua a 45 °C) | −18,0 % | −9,6 % | Gas de 1.285 a 670 MWh, electricidad +70 MWh; no precalienta el ACS. Es un techo: con 75 % de coincidencia, −13,5 % |
| | Recuperador del aire de extracción | −5,1 % | −2,5 % | −182 MWh de gas (14 % del gas anual), +28 MWh de electricidad |
| | Caldera de condensación | −3,1 % | −1,9 % | Rendimiento sobre PCS de 81,2 a 91,8 % (humos a 45 °C; la M1 de 4.3 supone 50 °C) |
| Pedir menos | Techos y fachadas verdes | −3,7 % | −3,6 % | Supuesto: 20 % menos de calor por la envolvente. Es un techo del efecto |
| | Ventiladores, 20 % menos de presión | −2,5 % | −5,8 % | El CO₂ baja más: se deja de usar electricidad y el calor se repone con gas |
| | Quirófanos al 50 % de noche | −2,0 % | −2,4 % | Evaluar el riesgo; ASHRAE 170 lo admite si no se usan [2] |
| Paquete | B + caldera de condensación + recuperador + solar térmico + ventiladores + quirófanos + 250 kWp | −49,6 % | −41,2 % | No se suman exacto. Con 75 % de coincidencia: −45,5 % y −38,5 %. Sin paneles: −38,4 % y −26,7 % |

Tabla 16. Mejoras respecto de A, evaluadas de a una (estimación anual aparte).

Los paneles cubren consumo y no lo reducen: sin ellos el paquete baja 38,4 % de energía. Este B es otro diseño que el de la sección 4.1 (agua a 45 °C en vez de 35 °C, para cubrir también la calefacción del aire, y sin precalentar el ACS). Las medidas de la sección 4.3 dan menos en el año que en el estado de diseño: el recuperador baja 46 % del gas en invierno y 5,1 % de la energía anual, porque el año promedia todos los meses y suma electricidad y gas; la bomba de calor no se modeló aquí. Los techos y fachadas verdes bajan poco porque el consumo está en el aire y no en la envolvente: se justifican más por comodidad y menor isla de calor. Esta estimación no reemplaza un cálculo anual con datos climáticos horarios y perfiles de uso (conclusión 5): la irradiación es una cota alta (con 1.500 kWh/m²·año, los 250 kWp bajan 9,9 % y no 11,3 %) y el 20 % de los techos verdes no tiene dato propio.

<!-- FIN SECCION -->

---

## Cambios necesarios en el resto del informe (para que no se contradiga)

1. **Índice:** agregar «4.5 Mejoras de sustentabilidad: estimación anual aparte» después de 4.4 (y «Tabla 16» si el índice lista las tablas), y actualizar los números de página.
2. **Conclusión 5 («¿Qué limitaciones tiene el análisis?»):** reemplazar las dos primeras oraciones y la mención de emisiones. Texto completo propuesto: «Es un cálculo en tres estados de diseño, no un consumo anual: para eso harían falta datos climáticos horarios y perfiles de uso; la sección 4.5 agrega una estimación anual aparte, de orden de magnitud, que no los reemplaza. Las superficies, las ganancias internas, la envolvente, el consumo de ACS y la composición del gas son supuestos, y no hay datos medidos del hospital real. Los equipos se modelan a plena carga, sin curvas de carga parcial ni desescarche, y no se evaluaron los costos; las emisiones de la electricidad solo se estimaron en la sección 4.5, con un factor supuesto. Para un diseño de ingeniería harían falta planos y relevamiento de las instalaciones, facturas de electricidad y gas, un año meteorológico típico y catálogos de equipos.»
3. **Resumen:** una oración al final, por ejemplo: «Además, una estimación anual aparte (sección 4.5) ordena otras mejoras de sustentabilidad: el paquete llega, como techo, a casi 50 % menos de energía anual (unos 38 % sin paneles solares); no es comparable con los estados de diseño.»
4. **Tabla 15 (comparación cualitativa):** no hace falta tocarla.
5. **Extensión:** de la página 3 (Resumen) a la 13 (Conclusiones) el informe ocupa unas 11 páginas en el PDF; la 4.5 ocupa cerca de una página con el formato del informe, así que quedaría en unas 12, justo en el tope de la consigna (8 a 12). Si la cátedra cuenta desde la portada, el informe ya ocupaba más. Conviene verificarlo con la paginación real de Word al pegarla.
6. **Referencias:** no se agregan numeradas; la irradiación y el factor de emisión van como «supuesto». Si el grupo prefiere citarlos, habría que cotejar las fuentes (hoy las conocemos por extractos).
7. **Material de respaldo:** el cálculo detallado está en `informe/memoria_calculo.md` (unas 30 páginas), que no es la planilla de Excel del grupo. Si el informe remite a algo, habría que adjuntarla.
