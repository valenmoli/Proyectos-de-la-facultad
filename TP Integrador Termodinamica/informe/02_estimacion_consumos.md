# Estimación de consumos del sistema térmico

**Borrador v0.1 para revisión.** Hospital base: Favaloro (La Matanza), AMBA. Todas las cifras salen del código (`calculo/`) y se regeneran en [`resultados_consumo.md`](resultados_consumo.md); los supuestos están en [`supuestos.md`](supuestos.md) con su estado (dato, supuesto o constante) y el método completo en [`../calculo/ESPECIFICACION.md`](../calculo/ESPECIFICACION.md).

## 1. Qué se estima y qué no

**Se estima** la energía final que consume el **sistema térmico**: frío, recalentamiento, calefacción, humidificación y agua caliente sanitaria, más sus auxiliares (ventiladores de las unidades de tratamiento de aire, ventiladores del condensador y bombas de agua helada). La energía final es electricidad más gas natural medido por su poder calorífico superior.

**No se incluye** iluminación, equipos médicos, cocina, lavandería ni esterilización. Esa es la frontera acordada por defecto (pregunta 12 del PRD, pendiente de confirmar). Por eso **el resultado no es el consumo total del hospital**: las referencias disponibles sí miden el edificio completo, y la comparación de la sección 5 se hace con esa salvedad.

## 2. Método en una página

1. **Zonas.** El edificio se divide en cinco zonas térmicas según los datos de Favaloro: quirófanos, terapia intensiva, internación general, guardia con diagnóstico y laboratorio (24 h) y consultorios y administración (de día, lunes a viernes). Cada una tiene sus renovaciones de aire, su humedad máxima y sus ganancias internas.
2. **Aire húmedo.** Cada zona se trata como una unidad de caudal constante: se mezcla aire exterior con retorno, una serpentina de agua helada enfría y deshumidifica, un recalentador lleva el aire a la temperatura de impulsión y un ventilador lo impulsa disipando su potencia como calor. Con eso salen la carga frigorífica y el calor de recalentamiento y de calefacción.
3. **Refrigeración.** La carga de las serpentinas es la que debe vencer la enfriadora. Se calcula el ciclo de compresión de R134a (trabajo, COP, calor rechazado) con la temperatura de condensación que impone el clima de cada estado.
4. **Combustión.** El gas natural quema con 15 % de exceso de aire: balance de la reacción, poder calorífico y rendimiento de la caldera por el balance de los gases de escape. El calor que entrega la caldera (recalentamiento, calefacción y ACS) se convierte en consumo de gas.
5. **Año.** Cada mes se parte en una mitad diurna y una nocturna con su temperatura; en cada estado se calculan las cargas y se multiplican por las horas. Se prefirió esto a las horas equivalentes a plena carga porque la ventilación es continua y no se representa bien con un número de horas.
6. **Datos.** El clima mensual y de diseño, las condiciones de ASHRAE 170, las ganancias internas y la envolvente son **supuestos sin fuente citable todavía** (los puse de conocimiento general), marcados como tales y medidos en la sensibilidad.

## 3. Resultado

| Magnitud | Valor |
|---|---|
| **Energía final anual** | **3.021 MWh** |
| **Intensidad** | **165 kWh/m² y año** sobre la superficie cubierta (95 de electricidad y 70 de gas); 194 kWh/m² sobre la climatizada |
| Electricidad | 1.736 MWh |
| Gas natural (PCS) | 1.285 MWh, unos 120.000 m³ |
| Capacidad frigorífica de diseño | 1.987 kW (108 W/m² cubierto) |
| Compresor al diseño | 559 kW, COP 3,56, condensación a 46 °C |
| Carga de la caldera en invierno (aire) | 649 kW, más 43 kW medios de ACS |
| COP estacional de la planta (compresor, ventiladores del condensador y bombas) | 3,96 |

**Dónde se va la energía:**

| Uso | MWh/año | % |
|---|---|---|
| Ventiladores de las unidades de tratamiento de aire | 847 | 28,0 % |
| Compresor de la enfriadora | 714 | 23,6 % |
| Gas del recalentamiento después de la serpentina | 629 | 20,8 % |
| Gas del agua caliente sanitaria | 461 | 15,3 % |
| Gas de la calefacción del aire | 194 | 6,4 % |
| Ventiladores del condensador | 105 | 3,5 % |
| Bombas de agua helada | 70 | 2,3 % |

## 4. Tres cosas que el resultado muestra

1. **Los ventiladores son lo que más energía consume** (28 %), por encima del compresor. El sistema mueve grandes caudales de aire por las renovaciones que exige un hospital (20 en quirófanos, 6 a 8 en áreas críticas) y por las zonas grandes de internación y áreas generales. Es un efecto del tipo de sistema (todo aire), y es candidato a mejora.
2. **El recalentamiento es casi la mitad del calor útil de la caldera** (511 de 1.044 MWh): se gasta frío para deshumidificar y después gas para devolver temperatura. Durante el año la enfriadora rechaza al ambiente 4.198 MWh, unas 8 veces más que el calor de recalentamiento. Eso es lo que la alternativa B (recuperación del calor del condensador) quiere aprovechar. **Dato a no perder:** en el punto de diseño de verano el recalentamiento es de solo 19 kW, porque con carga máxima el aire sale de la serpentina cerca de la temperatura que se necesita; el recalentamiento se concentra a carga parcial y de noche. Dimensionar la recuperación con el pico subestimaría el potencial.
3. **El COP estacional de la planta (3,96) coincide casi exactamente con el COP 4 que supone el artículo de Hospitecnia.** Es una coincidencia de resultado, no un ajuste: el COP sale del ciclo y de las temperaturas de condensación del clima.

## 5. Contraste con las referencias

Las referencias miden el edificio completo y este resultado solo el sistema térmico. Para compararlas se estima el consumo total equivalente suponiendo que el sistema térmico es una fracción del total, con las participaciones que citan las fuentes del artículo de Hospitecnia (de 46 % a 73 %).

| Referencia | kWh/m² y año |
|---|---|
| Tres hospitales argentinos auditados (HCWH 2021, estimados): Garrahan, CEMAR, Giordano | 259, 211, 163 |
| Mediana de 23 hospitales internacionales (rango 120 a 900) | 333 |
| Modelo español del artículo, en energía final | 394 a 400 |
| **Este modelo, solo sistema térmico** | **165** |
| **Equivalente para el edificio completo** (según la participación supuesta) | **226 a 361** |

El resultado queda en la parte alta de los hospitales argentinos auditados y por debajo del modelo español, y es consistente con la mediana internacional. Que esté por encima de los argentinos es esperable: el modelo es un sistema completo de aire con recalentamiento y renovaciones normativas en todas las zonas críticas, mientras que la auditoría de HCWH encontró hospitales subclimatizados con equipos viejos y splits. **Esta comparación es una banda de plausibilidad, no una validación** (tres hospitales estimados, dos fuera del AMBA, y una participación del sistema térmico que varía de 46 a 73 % según la fuente).

## 6. Qué tan seguro es el número

Cada fila cambia un supuesto y deja los demás en su valor base (3.021 MWh, 165 kWh/m²). **Las diez variaciones que más mueven el resultado:**

| Variación | Diferencia |
|---|---|
| Humedad máxima de verano 5 puntos menor en todas las zonas | +22,7 % |
| Consultorios y administración funcionan también las 24 h | +20,6 % |
| Sin calor del ventilador en el aire (lo que omitía la versión anterior) | +18,3 % |
| Agua caliente de 200 L por cama y día (en vez de 100) | +15,3 % |
| Temperatura media mensual +2 K o −2 K | +14,6 % / −13,7 % |
| La guardia y el diagnóstico ocupan el 50 % o el 20 % de las áreas generales | +12,8 % / −12,8 % |
| Humedad relativa media del clima −8 puntos | −8,2 % |
| Superficie climatizada 95 % o 75 % | +8,0 % / −8,0 % |
| Agua caliente de 55 L por cama y día | −6,9 % |
| Humedad máxima de 60 % en quirófanos, terapia intensiva e internación | −6,0 % |

Tomadas de a una, las variaciones mueven el resultado entre 142 y 202 kWh/m² y año. **Eso no es un intervalo de confianza**: las variaciones se combinan y los supuestos no son independientes. Una revisión externa del modelo estimó la incertidumbre global en alrededor de ±15 a 20 %, dominada por la humedad de consigna, los horarios, el aire exterior, el ACS y el clima. Esos cinco puntos son los que más conviene reemplazar por datos citables.

## 7. Qué no incluye el modelo y hacia dónde empujaría

| Omisión | Efecto esperado sobre el consumo |
|---|---|
| Economizador (enfriamiento gratuito con aire exterior). Sin él, el 15 % del frío anual se entrega con el exterior por debajo de 18 °C | Baja unos 2,5 a 4 % |
| Ventiladores de retorno y de extracción, y bombas de agua caliente | Sube unos 3 a 9 % |
| Rendimiento de la caldera a carga parcial (se usa el de plena carga, 90 % sobre PCI) | Sube el gas 6 a 20 % |
| Planta con torre de refrigeración en vez de condensación por aire | Baja unos 3 a 6 % |
| Diversidad de cargas dentro de una zona (se trata cada zona como un solo local) | Sube unos 2 a 6 % |
| ACS de guardia, quirófanos, cocina y personal (solo se cuenta por cama) | Sube unos 2 a 14 % |
| Cocina, lavandería, esterilización y vapor (fuera de la frontera) | No cambia este resultado, pero el gas total del hospital sería mucho mayor |
| Clima de un año típico horario (se usan estados medios por mes) | Cambia en ±5 % con signo incierto |
| Humidificación: la carga de diseño de invierno incluye 92 kW que el cálculo anual nunca usa, porque el promedio mensual de humedad oculta los días secos | Sube algo el consumo real (menos de 0,5 %) |

## 8. Verificación

- **49 chequeos termodinámicos** (`python -m pytest calculo/tests`): primera ley, segunda ley (COP menor que el de Carnot), balance de átomos de la combustión, coincidencia de la psicrometría con CoolProp, y que la tabla de supuestos reproduzca cada valor. Comprueban la coherencia interna; no prueban que la física sea la correcta.
- **Reimplementación independiente.** Dos agentes que no vieron el código reconstruyeron el cálculo desde cero solo con la especificación y la tabla de supuestos, uno con psychrolib y otro con CoolProp. En la primera versión coincidieron conmigo al 0,5 % o mejor en todas las magnitudes salvo una, donde el error era mío: la tabla de supuestos redondeaba a dos decimales y mostraba 0,03 en vez de 0,025 para los ventiladores del condensador. Quedó corregido y cubierto por un chequeo.
- **Revisión adversarial.** Un tercer revisor leyó la especificación y los supuestos, y encontró una omisión física importante, **el calor de los ventiladores**, además de varias incoherencias menores. Se corrigió lo que correspondía y el resto está en la sección 7. Esa corrección redujo el consumo base de 181 a 165 kWh/m².
- **Segunda reimplementación independiente**, sobre la versión corregida, con aislamiento más estricto (cada agente en su propio directorio, sin ver el código ni los resultados). Uno usó psychrolib y coincidió exactamente con el código; el otro usó CoolProp para el aire húmedo y quedó **dentro de 0,24 % en las magnitudes globales y de 0,02 % en la energía final**. Los dos declararon no haber visto nada fuera de la especificación y la tabla de supuestos. Con eso el cálculo queda verificado respecto de la especificación; lo que sigue sin verificar son los **supuestos** de entrada (sección 6).

## 9. Pendientes

- Reemplazar por fuentes citables el clima (SMN o ASHRAE), las renovaciones y humedades (ASHRAE 170 o la norma argentina) y la composición del gas (ENARGAS), y decidir el ACS.
- Confirmar con el usuario la frontera del consumo (pregunta 12) y el método anual (pregunta 13).
- Análisis exergético, alternativa B (recuperación del calor del condensador) y mejoras, con sus diagramas.
- Variantes del modelo base: economizador, caldera a carga parcial y planta con torre.
