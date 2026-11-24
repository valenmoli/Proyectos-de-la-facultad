# Sección 4.5 para el informe entregado (borrador)

Borrador de una sección nueva para el informe que subió el grupo (`TP_Integrador_Hospital_Favaloro`), después de «4.4 Ventajas, limitaciones e impacto ambiental». Respalda la diapositiva 11 («Mejoras de sustentabilidad, en tres familias»). Las cifras salen de nuestro cálculo anual (`informe/informe_tecnico.md`, `informe/memoria_calculo.md` y `calculo/mejoras.py`). El texto a pegar va entre los dos marcadores; lo que sigue son los cambios necesarios en el resto del informe.

<!-- INICIO SECCION -->

## 4.5 Mejoras de sustentabilidad: estimación anual aparte

Las secciones 3 y 4.1 a 4.3 calculan tres estados de diseño. Las medidas que producen energía o dan sombra necesitan un cálculo anual, así que se hizo una **estimación aparte, simple y de orden de magnitud**: mismo edificio y misma demanda de ACS (unos 43 kW), pero un modelo independiente, con medias mensuales aproximadas de Buenos Aires partidas en día y noche (no los valores de ASHRAE para Ezeiza de la sección 3), sin cargas parciales y con cargas de diseño propias (frío de 1.987 kW, contra 1.489 kW en la sección 3). **Sus porcentajes no son comparables con los de las secciones anteriores.**

La alternativa A consume 3.021 MWh de energía final por año (1.736 de electricidad y 1.285 de gas sobre PCS, sumados sin ponderar por energía primaria) y emite 895 t de CO₂, con 0,183 kg/kWh de gas y 0,38 t/MWh de electricidad (supuesto; con 0,29 y 0,40 el paquete baja 44,0 % y 40,6 % de CO₂). Es la energía del sistema térmico, no el consumo total del hospital.

| Familia | Medida | Energía | CO₂ | Qué hay que saber |
|-------------|----------------------|-----------|-----------|-------------------------------------------|
| Producir energía limpia | Fotovoltaica de 250 kWp | −11,3 % | −14,4 % | 340 MWh/año (1.700 kWh/m²·año y rendimiento de 0,8: supuestos). Cubre consumo, no lo reduce |
| | Fotovoltaica de 500 kWp | −22,5 % | −28,9 % | 680 MWh/año; 41 % de la azotea (6.117 m² por nivel). Supone que otras cargas absorben el excedente. Fuera del paquete |
| | Solar térmico de 300 m² | −8,3 % | −5,1 % | 251 MWh/año; cubre el 54 % del ACS en el año (29 % en junio) y la caldera completa |
| No desperdiciar | B: calor del condensador (agua a 45 °C) | −18,0 % | −9,6 % | Gas de 1.285 a 670 MWh, electricidad +70 MWh. Es un techo: con 75 % de coincidencia, −13,5 % |
| | Recuperador del aire de extracción | −5,1 % | −2,5 % | −182 MWh de gas, +28 MWh de electricidad |
| | Caldera de condensación | −3,1 % | −1,9 % | Rendimiento sobre PCS de 81,2 a 91,8 % |
| Pedir menos | Techos y fachadas verdes | −3,7 % | −3,6 % | Supuesto: 20 % menos de calor por la envolvente. Es un techo del efecto |
| | Ventiladores, 20 % menos de presión | −2,5 % | −5,8 % | El CO₂ baja más: se deja de usar electricidad y el calor se repone con gas |
| | Quirófanos al 50 % de noche | −2,0 % | −2,4 % | Evaluar el riesgo; ASHRAE 170 lo admite si no se usan [2] |
| Paquete | B + caldera de condensación + recuperador + solar térmico + ventiladores + quirófanos + 250 kWp | −49,6 % | −41,2 % | No se suman exacto. Con 75 % de coincidencia: −45,5 % y −38,5 %. Sin paneles: −38,4 % y −26,7 % |

Tabla 16. Mejoras respecto de A, evaluadas de a una (estimación anual aparte).

Los paneles cubren consumo y no lo reducen: sin ellos el paquete baja 38,4 % de energía. Este B es otro diseño que el de la sección 4.1 (agua a 45 °C en vez de 35 °C, para cubrir también la calefacción del aire). Las medidas de la sección 4.3 dan menos en el año que en el estado de diseño: el recuperador baja 46 % del gas en invierno y 5,1 % de la energía anual, porque el año promedia todos los meses y suma electricidad y gas; la bomba de calor no se modeló aquí. Los techos y fachadas verdes bajan poco porque el consumo está en el aire y no en la envolvente: se justifican más por comodidad y menor isla de calor. Esta estimación no reemplaza la simulación con clima horario que falta (conclusión 5): la irradiación es una cota alta (con 1.500 kWh/m²·año, los 250 kWp bajan 9,9 % y no 11,3 %) y el 20 % de los techos verdes no tiene dato propio.

<!-- FIN SECCION -->

---

## Cambios necesarios en el resto del informe (para que no se contradiga)

1. **Índice:** agregar «4.5 Mejoras de sustentabilidad: estimación anual aparte».
2. **Conclusión 5 («¿Qué limitaciones tiene el análisis?»):** hoy dice «Es un cálculo en tres estados de diseño, no un consumo anual» y «no se evaluaron las emisiones de la electricidad ni los costos». Sugerencia: «Es un cálculo en tres estados de diseño; la sección 4.5 agrega una estimación anual aparte, de orden de magnitud, sin clima horario ni cargas parciales, con las emisiones de la electricidad a un factor supuesto. No se evaluaron los costos.»
3. **Resumen:** una oración al final, por ejemplo: «Además, una estimación anual aparte (sección 4.5) ordena las mejoras de sustentabilidad: el paquete llega hasta casi 50 % menos de energía anual.»
4. **Tabla 15 (comparación cualitativa):** no hace falta tocarla. Si quieren, puede decir «Ver también la tabla 16» en el pie.
5. **Extensión:** el cuerpo del informe (de la portada a las conclusiones, sin referencias ni anexo) hoy ocupa unas 11 páginas contando el resumen; la sección ocupa cerca de una página, así que queda en unas 12. La consigna pide entre 8 y 12. Conviene chequearlo al pegarla en Word.
6. **Referencias:** no se agregan numeradas; los valores de irradiación y factor de emisión van como «supuesto» en el texto. Si el grupo prefiere citarlos, habría que cotejar las fuentes (hoy las conocemos por extractos).
7. **Material de respaldo:** el cálculo detallado está en `informe/memoria_calculo.md` (unas 30 páginas), que no es la planilla de Excel del grupo. Si el grupo quiere que el informe remita a algo, habría que adjuntarla como anexo o memoria complementaria.
