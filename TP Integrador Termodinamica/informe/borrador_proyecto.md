---
title: "Diseño de un sistema energético eficiente para un hospital del AMBA"
subtitle: "TP Integrador de Termodinámica 2026 · Informe técnico · Borrador v0.1"
author: "[Integrantes del equipo: a completar]"
date: "Facultad de Ingeniería y Ciencias Agrarias · Ingeniería Civil · UCA · Noviembre de 2026"
lang: es-AR
---

::: {custom-style="Nota"}
**Cómo leer este borrador.** Es la versión de trabajo del informe: sirve para ver qué se está armando, no es la entrega. Todas las cifras de cálculo salen del código (`calculo/`) y este documento se regenera con él (`python -m calculo.construir_borrador`). Los recuadros naranjas marcan lo que **falta**; los azules, avisos sobre el origen de los datos. Los valores de entrada marcados como *supuesto* no tienen todavía fuente citable (sección 4.7 y anexo A).
:::

| Sección | Estado | Qué falta |
|---|---|---|
| 1 Introducción, 2 Objetivos | Borrador completo | Revisar redacción |
| 3 Descripción del sistema | Completo con datos del hospital y supuestos declarados | Reemplazar supuestos por fuentes |
| 4 Metodología | Completa salvo exergía | Ecuaciones de exergía por equipo |
| 5 Resultados 5.1 a 5.5 | **Calculados y verificados** (aire húmedo, refrigeración, combustión, consumo anual, sensibilidad) | Datos de clima y normativa citables |
| 5.6 Exergía | **Pendiente** | Todo el análisis |
| 6 Alternativas y mejoras | **Pendiente** (hay una cota superior calculada) | Alternativa B y al menos dos mejoras con números |
| 7 Discusión | Parcial | Comparar alternativas |
| 8 Conclusiones | Preliminares | Responder las cinco preguntas de la Consigna 5 |
| Presentación oral y memoria de cálculo | No iniciadas | |

# Resumen

Se modela el sistema térmico de un hospital general de agudos de alta complejidad del AMBA, con el Hospital Dr. René Favaloro (La Matanza: 18.352 m² cubiertos, 158 camas, 6 quirófanos) como referencia de tamaño y programa. El sistema abarca frío, recalentamiento, calefacción, humidificación y agua caliente sanitaria (ACS), más los ventiladores y bombas que los acompañan. Con aire húmedo, un ciclo de compresión de vapor de R134a y la combustión de gas natural, el modelo estima un consumo anual de **3.021 MWh de energía final (165 kWh/m² y año)**: 1.736 MWh de electricidad y 1.285 MWh de gas natural.

Dos hallazgos ordenan el trabajo. Primero, los ventiladores consumen más que el compresor (28,0 % contra 23,6 % de la energía). Segundo, el sistema enfría el aire para quitarle humedad y después lo recalienta con gas: el recalentamiento es el 49 % del calor útil de la caldera, mientras la enfriadora rechaza al ambiente 4.198 MWh por año, unas 8,2 veces ese calor. Esa ineficiencia es el hilo que une los cuatro contenidos de la materia y la base de la alternativa B (recuperar el calor del condensador).

El resultado depende de supuestos de entrada sin fuente citable todavía (clima, condiciones de ASHRAE 170, ganancias internas): variando uno por vez, la intensidad queda entre 142 y 202 kWh/m² y año. El análisis exergético, la alternativa B y las mejoras están pendientes.

# 1. Introducción

Un hospital opera todo el año y todo el día, y buena parte de su climatización no es de confort sino de **proceso**: los quirófanos, la terapia intensiva y las habitaciones exigen temperatura y humedad controladas, presión positiva y un mínimo de aire exterior filtrado. En el clima templado y húmedo del AMBA esa exigencia tiene una consecuencia termodinámica concreta. El aire exterior de verano (unos 34 °C con 16,3 g de vapor por kg de aire seco) debe enfriarse por debajo de su punto de rocío para condensar vapor, y a esa temperatura ya no puede impulsarse a la zona: hay que **recalentarlo**. Se gasta frío para deshumidificar y combustible para devolver temperatura.

El trabajo diseña y evalúa ese sistema integrando los cuatro contenidos de la materia sobre **una sola cadena de equipos**: el aire húmedo fija la carga frigorífica y el calor de recalentamiento; la refrigeración convierte esa carga en electricidad y en calor rechazado; la combustión convierte el calor de recalentamiento, de calefacción y de ACS en gas natural; y la exergía mide dónde se pierde capacidad de producir trabajo. El caso es un hospital del AMBA con el tamaño y el programa del Hospital Favaloro; los datos que ese hospital no publica (climatización, consumos) se estiman como supuestos declarados.

# 2. Objetivos

**Objetivo general.** Definir, modelar y evaluar con la Primera y la Segunda Ley el sistema térmico de un hospital del AMBA, y proponer configuraciones y mejoras que reduzcan su consumo.

**Objetivos específicos.**

1. Definir el edificio, las zonas térmicas y sus condiciones de proyecto, y declarar cada dato como dato, supuesto o constante.
2. Calcular la carga frigorífica (sensible y latente), el recalentamiento y la calefacción con aire húmedo.
3. Calcular el trabajo, el COP y el calor rechazado de la enfriadora, y el consumo y el rendimiento de la caldera.
4. Estimar el consumo anual de energía final y contrastarlo con hospitales de referencia.
5. Calcular la destrucción de exergía por equipo y comparar al menos dos alternativas y dos mejoras. *(pendiente)*

# 3. Descripción del sistema

## 3.1 El edificio

Se toma como base el **Hospital Dr. René Favaloro (SAMIC), Rafael Castillo, La Matanza**, un Hospital General de Agudos de Alta Complejidad. Ningún documento recibido trae datos de climatización ni de consumo del edificio real [F1, F2], de modo que el modelo es una réplica de su tamaño y programa, no de sus instalaciones.

| Dato | Valor | Estado |
|---|---|---|
| Superficie cubierta | 18.352 m² (otra cifra declarada: más de 20.000 m² de construcción) | Dato [F1, F2] |
| Camas | 144 de internación general y 14 de terapia intensiva (158 en total) | Dato; se interpreta como el total del hospital |
| Quirófanos | 6 | Dato de programa [F1] |
| Niveles | Tres pisos; quirófanos y áreas críticas en el 2.º; guardia y diagnóstico en el 1.º | Dato [F1] |
| Funcionamiento | Guardia las 24 h; internación y áreas críticas continuas | Dato (guardia) y supuesto |
| Superficie climatizada | 85 % de la cubierta (15.599 m²) | Supuesto |
| Clima | AMBA, templado y húmedo | Supuesto (a reemplazar con datos del SMN) |

Table: Tabla 1. Datos del hospital base.

## 3.2 Zonas térmicas

El edificio se divide en cinco zonas, cada una tratada como un sistema de aire de caudal constante con su propia unidad de tratamiento.

| Zona | Superficie [m²] | Consigna de verano | Renovaciones totales / de aire exterior [1/h] | Caudal de impulsión [m³/h] | Aire exterior [m³/h] | Funcionamiento |
|----------------------|---------|------------|--------------|-----------|----------|------------------|
| G1 Quirófanos | 252 | 22 °C; 55 % | 20 / 4 | 15.120 | 3.024 | Continuo; actividad de día |
| G2 Terapia intensiva | 336 | 23 °C; 55 % | 6 / 2 | 6.048 | 2.016 | Continuo |
| G3 Internación general | 4.032 | 24 °C; 55 % | 4 / 2 | 54.711 | 24.192 | Continuo |
| G4 Guardia, imágenes y laboratorio | 3.843 | 24 °C; 60 % | 8 / 2 | 92.225 | 23.056 | 24 h |
| G5 Consultorios, administración y docencia | 7.136 | 24 °C; 60 % | 3 / 1 | 96.670 | 21.409 | 12 h, lunes a viernes |

Table: Tabla 2. Zonas térmicas, consignas de verano y caudales (valores de ASHRAE 170 recordados, a verificar con la norma; ver anexo A).

## 3.3 Esquema del sistema

El aire exterior se mezcla con el retorno, una serpentina de agua helada lo enfría y deshumidifica, un recalentador lleva el aire a la temperatura necesaria y un ventilador lo impulsa a la zona. La enfriadora (compresión de R134a) produce el agua helada y rechaza calor al ambiente; la caldera de gas natural alimenta el recalentamiento, la calefacción de invierno y el ACS.

![Figura 1. Esquema del sistema térmico.](../figuras/fig01_esquema_sistema.png){width=14.5cm}

**Volúmenes de control.** Los balances se plantean sobre cuatro sistemas:

| Sistema | Límite | Flujos que lo cruzan |
|---|---|---|
| Unidad de tratamiento de aire | Mezcla, serpentina, recalentador, humidificador y ventilador | Aire exterior y de retorno (entran), aire de impulsión (sale), agua helada, calor de la caldera, vapor |
| Enfriadora | Compresor, condensador, válvula y evaporador | Calor del agua helada (entra), electricidad (entra), calor al ambiente (sale) |
| Caldera | Cámara de combustión e intercambiador | Gas y aire (entran), gases de escape (salen), calor útil (sale) |
| Producción de ACS | Acumulación y recirculación | Calor de la caldera, agua fría (entra), agua caliente (sale) |

Table: Tabla 3. Sistemas de estudio y sus límites.

## 3.4 Cómo se integran los cuatro contenidos

| Contenido | Qué resuelve | Qué entrega, y a quién |
|---|---|---|
| Aire húmedo | Estados del aire en la mezcla, la serpentina, el recalentador y la impulsión; cargas sensible y latente | Carga frigorífica (a la refrigeración) y calor de recalentamiento y calefacción (a la combustión) |
| Refrigeración | Ciclo de la enfriadora: trabajo, COP, calor rechazado | Electricidad del frío (al balance) y calor del condensador (base de la alternativa B) |
| Combustión | Gas natural con exceso de aire: reacción, poder calorífico, rendimiento, temperatura de llama | Gas para recalentar, calefaccionar y producir ACS (al balance y a la exergía) |
| Exergía | Dónde se destruye capacidad de producir trabajo, con estado muerto en el exterior | Destrucción por equipo, para comparar alternativas y mejoras |

Table: Tabla 4. Integración de los contenidos.

# 4. Metodología

## 4.1 Hipótesis y frontera

1. En cada estado considerado el régimen es permanente; cada mes se parte en una mitad diurna y una nocturna.
2. El aire húmedo es una mezcla de aire seco y vapor, ambos gases ideales, a 101,325 kPa.
3. Sistema de caudal constante con serpentina y recalentamiento, sin economizador ni recuperación de calor: es la línea de base (alternativa A).
4. El ventilador de impulsión aspira después de la serpentina y toda su potencia eléctrica se disipa como calor en el aire.
5. El refrigerante cumple un ciclo de compresión de vapor con compresor adiabático de rendimiento isentrópico constante, expansión isoentálpica y sin pérdidas de presión.
6. Combustión completa del gas natural, gases ideales y sin disociación; el aire tiene 21 % de O₂ y 79 % de N₂; los gases de escape salen a 190 °C sin condensar.
7. **Frontera:** se calcula el sistema térmico y sus auxiliares (ventiladores de las unidades, ventiladores del condensador, bombas de agua helada). No se incluyen iluminación, equipos médicos, cocina, lavandería ni esterilización, por lo que **el resultado no es el consumo total del hospital**. No se modelan economizador, ventiladores de retorno y extracción, bombas de agua caliente ni pérdidas de distribución.

## 4.2 Aire húmedo

La humedad específica y la entalpía del aire húmedo, por kg de aire seco, son

$$\omega = 0\text{,}622\,\frac{p_v}{P - p_v}, \qquad h = 1\text{,}006\,T + \omega\,(2501 + 1\text{,}86\,T)$$

con $T$ en °C y $h$ en kJ/kg. La mezcla de aire exterior y de retorno conserva entalpía y humedad: $\dot m_a h_{mez} = \dot m_{ae} h_{ext} + \dot m_{ar} h_{ret}$ y la misma relación para $\omega$. La serpentina enfría hasta $T_c$ y deshumidifica hasta $\omega_c$, con el aire a la salida al 95 % de humedad relativa:

$$\dot Q_{serp} = \dot m_a\left[(h_{mez} - h_c) - (\omega_{mez} - \omega_c)\,h_f\right], \qquad \dot Q_{lat} = \dot m_a\,(\omega_{mez} - \omega_c)\,h_{fg}$$

donde $h_f = 4\text{,}186\,T_c$ es la entalpía del condensado y la parte sensible es la diferencia. El recalentador lleva el aire a $T_{obj}$, que es la temperatura de impulsión menos el calentamiento que producirá el ventilador:

$$\dot Q_{rec} = \dot m_a\,c_{p,ah}\,(T_{obj} - T_c), \qquad T_{obj} = T_{imp} - \frac{\dot W_{vent}}{\dot m_a\,c_{p,ah}}, \qquad c_{p,ah} = 1\text{,}006 + 1\text{,}86\,\omega$$

El caudal de impulsión es el mayor entre el que fijan las renovaciones y el que pide la carga sensible; el de aire exterior se fija en valor absoluto. En invierno, si el aire sale seco de más, se humidifica con vapor.

## 4.3 Refrigeración

Para el ciclo con entalpías $h_1$ a $h_4$ (estados de la tabla 6), por kg de refrigerante:

$$q_L = h_1 - h_4, \qquad w = h_2 - h_1 = \frac{h_{2s} - h_1}{\eta_{is}}, \qquad q_H = h_2 - h_3$$

$$COP = \frac{q_L}{w/\eta_{mot}}, \qquad \dot W_{comp} = \frac{\dot Q_L}{COP}, \qquad \dot Q_{cond} = \dot Q_L + \eta_{mot}\,\dot W_{comp}, \qquad COP_{Carnot} = \frac{T_{ev}}{T_{cond} - T_{ev}}$$

La temperatura de condensación sigue al clima: $T_{cond} = \max(T_{ext} + 12\ \text{K},\ 32\ °C)$. Los ventiladores del condensador consumen el 2,5 % del calor rechazado y las bombas se calculan con el caudal de agua helada (salto de 5 K) y 250 kPa de presión.

## 4.4 Combustión

La reacción por kmol de gas natural, con relación de aire $\lambda$, es

$$0\text{,}91\,\text{CH}_4 + 0\text{,}05\,\text{C}_2\text{H}_6 + 0\text{,}01\,\text{C}_3\text{H}_8 + 0\text{,}02\,\text{N}_2 + 0\text{,}01\,\text{CO}_2 + \lambda\,a_{st}\left(\text{O}_2 + \tfrac{79}{21}\,\text{N}_2\right) \rightarrow \text{CO}_2 + \text{H}_2\text{O} + \text{N}_2 + \text{O}_2$$

Los poderes caloríficos salen de las entalpías de formación, con agua líquida en los productos para el superior (PCS) y vapor para el inferior (PCI). El rendimiento de la caldera se calcula por el balance de los gases de escape, y el combustible necesario para entregar un calor útil $Q_{util}$ es

$$\eta = 1 - q_{gases} - f_{rad}, \qquad E_{PCS} = \frac{Q_{util}}{\eta}\cdot\frac{PCS}{PCI}$$

El ACS se calcula desde el consumo por cama, no desde una potencia por m²:

$$\dot Q_{ACS} = \frac{L\cdot N_{camas}\cdot 4\text{,}186\,(T_{ACS} - T_{red})\cdot f_{perd}}{86\,400}$$

## 4.5 Consumo anual

Cada mes se representa con dos estados de $12\,d_i$ horas ($d_i$ son los días del mes): uno diurno ($T_i + 4\text{,}5$ K) y uno nocturno ($T_i - 4\text{,}5$ K), con la humedad específica media del mes limitada a la saturación. En cada estado se calculan las cargas de las cinco zonas, la planta de frío con la temperatura exterior del estado y el calor de la caldera, y se multiplican por las horas. Se prefirió este método a las horas equivalentes a plena carga porque la ventilación es continua y un número de horas la representa mal.

## 4.6 Exergía

::: {custom-style="Pendiente"}
**Pendiente.** El análisis usará, para cada equipo, la exergía de flujo $\dot X = \dot m\,[(h - h_0) - T_0\,(s - s_0)]$, la exergía del calor $\dot X_Q = \dot Q\,(1 - T_0/T)$, la destrucción $\dot X_{dest} = T_0\,\dot S_{gen}$ y la eficiencia exergética. Se propone el estado muerto en el estado exterior de diseño (34 °C en verano) y evaluar una temperatura media anual como sensibilidad: **es una decisión a confirmar**, porque cambia la exergía del calor a 60 °C.
:::

## 4.7 Datos y supuestos

El modelo tiene 54 parámetros de entrada: 5 son datos leídos de documentos recibidos, 41 son supuestos fundamentados pero sin fuente citable todavía y 8 son constantes o propiedades físicas. Los supuestos que más pesan son el clima mensual y de diseño, las renovaciones y humedades de ASHRAE 170, las ganancias internas, la conductancia de la envolvente, el consumo de ACS por cama y los horarios. La tabla del anexo A muestra los principales; la completa, con la fuente de cada uno, está en `informe/supuestos.md`.

::: {custom-style="Nota"}
**Origen de las propiedades.** Aire húmedo con las fórmulas de ASHRAE Fundamentals (psychrolib) contrastadas con CoolProp; refrigerante y capacidades caloríficas de gases con CoolProp. Cuando la cátedra indique el libro de tablas, se contrastarán tres puntos contra esas tablas.
:::

# 5. Resultados

## 5.1 Caso detallado: quirófano en el punto de verano pico

El quirófano (zona G1, 5,04 kg/s de aire seco, equivalente a 15.120 m³/h, con 20 % de aire exterior) se calcula con el exterior a 34 °C de bulbo seco y 25 °C de bulbo húmedo y actividad plena. La serpentina entrega 79,5 kW, de los cuales 58,8 kW son sensibles y 20,7 kW latentes; el recalentador aporta 18,7 kW y el ventilador calienta el aire 2,4 K (12,6 kW).

![Figura 2. Proceso del aire en el quirófano, verano pico.](../figuras/fig02_psicrometrica_quirofano.png){width=14.5cm}

| Estado | Descripción | T [°C] | ω [g/kg] | h [kJ/kg] | HR [%] |
|--------|------------------------------------|------------|------------|--------------|----------|
| A | Aire exterior | 34,0 | 16,26 | 75,9 | 48 |
| B | Local (consigna) | 22,0 | 9,06 | 45,2 | 55 |
| C | Mezcla con retorno | 24,4 | 10,50 | 51,3 | 55 |
| D | Salida de la serpentina | 13,0 | 8,86 | 35,4 | 95 |
| E | Tras el recalentador | 16,6 | 8,86 | 39,2 | 75 |
| F | Impulsión (tras el ventilador) | 19,1 | 8,86 | 41,7 | 64 |

Table: Tabla 5. Estados del aire en el quirófano (A a F, figura 2).

En el punto de diseño el recalentamiento del edificio es de solo 19 kW: con carga máxima el aire sale de la serpentina cerca de la temperatura que se necesita. El recalentamiento se concentra a carga parcial y de noche, y **dimensionar su recuperación con el pico subestimaría el potencial**.

## 5.2 Ciclo de refrigeración

Con la suma de las serpentinas, la capacidad frigorífica de diseño es **1.987 kW** (108 W/m² cubierto). El R134a evapora a 3 °C (326 kPa) y condensa a 46 °C (1.190 kPa), porque el condensador es enfriado por aire a 34 °C.

![Figura 3. Ciclo de compresión de R134a al punto de diseño de verano.](../figuras/fig03_diagrama_ph_r134a.png){width=13cm}

| Estado | Descripción | T [°C] | P [kPa] | h [kJ/kg] |
|--------|--------------------------------------------------|------------|------------|--------------|
| 1 | Salida del evaporador (vapor sobrecalentado 5 K) | 8,0 | 326 | 404,9 |
| 2s | Salida del compresor, isentrópica | – | 1.190 | 432,6 |
| 2 | Salida del compresor, real (η_is = 0,72) | 64,9 | 1.190 | 443,3 |
| 3 | Salida del condensador (subenfriado 4 K) | 42,0 | 1.190 | 259,4 |
| 4 | Salida de la válvula de expansión (título 0,28) | 3,0 | 326 | 259,4 |

Table: Tabla 6. Estados del ciclo de refrigeración.

El efecto frigorífico es 145,5 kJ/kg, el trabajo de compresión 38,5 kJ/kg y el calor rechazado 184,0 kJ/kg. El COP sobre el eje es 3,78 y sobre la potencia eléctrica 3,56, contra 6,42 del ciclo de Carnot entre las mismas temperaturas: **el ciclo real alcanza el 55 % del límite de la Segunda Ley**. La potencia eléctrica del compresor al diseño es 559 kW y el caudal de refrigerante, 13,7 kg/s. El compresor descarga a 65 °C: ese nivel de temperatura es lo que hace posible pensar en recuperar calor.

## 5.3 Combustión y caldera

Por kmol de gas natural y con 15 % de exceso de aire, la reacción consume 2,352 kmol de O₂ y 8,847 kmol de N₂ del aire, y produce 1,050 kmol de CO₂, 2,010 kmol de H₂O, 8,867 kmol de N₂ y 0,307 kmol de O₂ sin consumir. El balance de átomos de C, H, O y N cierra.

| Magnitud | Valor |
|---|---|
| Poder calorífico superior | 9.196 kcal/m³ = 10,70 kWh/m³ (m³ estándar a 15 °C) |
| Poder calorífico inferior | 9,66 kWh/m³ (relación PCS/PCI = 1,108) |
| Pérdida por gases de escape (190 °C) | 8,0 % del PCI |
| **Rendimiento de la caldera** | **90,0 % sobre PCI** (81,2 % sobre PCS) |
| Temperatura de rocío de los gases | 56,1 °C (fracción molar de agua: 16,4 %); la chimenea a 190 °C no condensa |
| Temperatura de llama adiabática (sin disociación) | 1.848 °C |
| Gas por kWh de calor útil | 0,1151 m³ |

Table: Tabla 7. Combustión del gas natural y rendimiento de la caldera.

La carga de la caldera en el aire es de 649 kW en el día de diseño de invierno, más 43 kW medios de ACS.

## 5.4 Consumo anual

La energía final anual es **3.021 MWh**: 1.736 MWh de electricidad y 1.285 MWh de gas natural medido por su PCS, unos 120.000 m³. Sobre la superficie cubierta son **165 kWh/m² y año** (95 de electricidad y 70 de gas); sobre la climatizada, 194. El gas es el 43 % de la energía.

| Uso final | Energético | MWh/año | % del total | kWh/m²·año |
|--------------------------------------------|--------------|------------|------------|------------|
| Ventiladores de las unidades de tratamiento de aire | Electricidad | 847 | 28,0 % | 46,1 |
| Compresor de la enfriadora | Electricidad | 714 | 23,6 % | 38,9 |
| Recalentamiento después de la serpentina | Gas | 629 | 20,8 % | 34,3 |
| Agua caliente sanitaria | Gas | 461 | 15,3 % | 25,1 |
| Calefacción del aire | Gas | 194 | 6,4 % | 10,6 |
| Ventiladores del condensador | Electricidad | 105 | 3,5 % | 5,7 |
| Bombas de agua helada | Electricidad | 70 | 2,3 % | 3,8 |
| **Total** |  | **3.021** | 100 % | **164,6** |

Table: Tabla 8. Consumo anual por uso final.

La humidificación con vapor no aparece en la tabla porque el promedio mensual de humedad no la requiere.

![Figura 4. Consumo anual por uso final.](../figuras/fig04_consumo_por_uso.png){width=14cm}

El frío entregado en el año es 3.526 MWh. El COP estacional del compresor es 4,94, mayor que el de diseño (3,56) porque la mayor parte del año la condensación es más baja; el COP estacional de la planta, con los ventiladores del condensador y las bombas, es 3,96. Las horas equivalentes a plena carga de refrigeración son 1.775 h.

![Figura 5. Frío y calor del aire entregados por mes.](../figuras/fig05_perfil_mensual.png){width=14cm}

**El calor del aire es mayor en verano que en invierno**: 129 MWh en enero y 134 MWh en diciembre, contra 46 MWh en julio. Es el recalentamiento posterior a la deshumidificación, no la calefacción, lo que domina el gas del aire. El frío pasa de 595 MWh en enero a 136 MWh en julio y no es cero en invierno porque las ganancias internas y el calor de los ventiladores siguen existiendo y el modelo no incluye economizador (enfriamiento gratuito con aire exterior).

## 5.5 Sensibilidad

Cada fila de la tabla 9 cambia un supuesto y deja los demás en su valor base. Las 12 variaciones que más mueven el resultado son:

| Variación de un supuesto (los demás quedan en su valor base) | Energía final [MWh/año] | Diferencia |
|--------------------------------------------------------------|----------------|------------|
| Humedad máxima de verano 5 puntos menor en todas las zonas | 3.706 | +22,7 % |
| Consultorios y administración funcionan también las 24 h | 3.644 | +20,6 % |
| Sin calor del ventilador en el aire | 3.574 | +18,3 % |
| ACS de 200 L por cama y día (en vez de 100) | 3.483 | +15,3 % |
| Temperatura media mensual +2 K | 3.463 | +14,6 % |
| Temperatura media mensual −2 K | 2.608 | −13,7 % |
| Guardia, diagnóstico y laboratorio: 50 % de las áreas generales | 3.409 | +12,8 % |
| Guardia, diagnóstico y laboratorio: 20 % de las áreas generales | 2.633 | −12,8 % |
| Humedad relativa media del clima −8 puntos | 2.773 | −8,2 % |
| Superficie climatizada 95 % de la cubierta | 3.263 | +8,0 % |
| Superficie climatizada 75 % de la cubierta | 2.780 | −8,0 % |
| ACS de 55 L por cama y día | 2.814 | −6,9 % |

Table: Tabla 9. Sensibilidad de la energía final anual (caso base: 3.021 MWh).

![Figura 6. Sensibilidad de la energía final anual.](../figuras/fig06_sensibilidad.png){width=14.5cm}

Tomadas de a una, las variaciones mueven la intensidad entre 142 y 202 kWh/m² y año. **Eso no es un intervalo de confianza**: las variaciones se combinan y los supuestos no son independientes. Una revisión externa del modelo estimó la incertidumbre global en alrededor de ±15 a 20 %, dominada por la humedad de consigna, los horarios de las zonas, el aire exterior, el ACS y el clima. Son los cinco puntos que más conviene reemplazar por datos citables.

::: {custom-style="Pendiente"}
**Pendiente: 5.6 Análisis exergético.** Falta calcular la destrucción de exergía en la serpentina y la enfriadora (compresor, condensador, válvula), en el recalentador y la caldera, y en los ventiladores, con su eficiencia exergética y un diagrama de flujo de exergía (Grassmann). La hipótesis a poner a prueba: calentar aire unos pocos grados con una llama de 1.848 °C destruye casi toda la exergía del combustible.
:::

# 6. Alternativas y mejoras

::: {custom-style="Pendiente"}
**Pendiente: esta sección todavía no tiene resultados.** Lo que ya está definido y lo que ya se calculó:

**Alternativa A (línea de base):** enfriadora de compresión, caldera de gas y aire de caudal constante con recalentamiento. Es la que se calculó en la sección 5.

**Alternativa B:** igual que A, con **recuperación del calor del condensador** para el recalentamiento. Un recuperador alimentado con el calor que hoy se rechaza reemplazaría parte del gas del recalentamiento. **Cota superior ya calculada:** si el condensador cubriera todo el recalentamiento, se ahorrarían 629 MWh de gas al año (20,8 % de la energía final). No es el resultado de B: faltan la coincidencia en el tiempo entre el recalentamiento y el calor disponible, el nivel de temperatura (el condensador trabaja entre 32 y 46 °C, y el compresor descarga hasta unos 65 °C) y el trabajo extra del compresor si hay que subir la presión de condensación.

**Mejoras candidatas** (la consigna pide al menos dos, explicadas desde la Termodinámica). Hay que elegir dos o tres que se puedan cuantificar con el mismo modelo:
:::

| Mejora | Principio termodinámico | Qué se cuantificaría con el modelo |
|---|---|---|
| Recuperación del calor del condensador (alternativa B) | Aprovechar calor entre 32 y 65 °C que hoy se rechaza, en lugar de quemar gas en una llama de 1.848 °C | Gas evitado y trabajo extra del compresor |
| Control del exceso de aire o caldera de condensación | Menos pérdida en los gases de escape y recuperación del calor latente del agua formada (la temperatura de rocío es 56,1 °C) | Rendimiento de la caldera y gas ahorrado |
| Recuperación de calor del aire de extracción con serpentinas de circuito cerrado | Precalentar o preenfriar el aire exterior con el aire que sale, sin mezclarlos (en un hospital la contaminación cruzada es una restricción dura) | Reducción de la carga de serpentina y de recalentamiento |
| Mayor temperatura de evaporación | Menor salto de presión del compresor, menos trabajo | Reducción de la electricidad del compresor |
| Reducción de la presión y del caudal de los ventiladores en zonas no críticas | Los ventiladores son el 28,0 % de la energía y la potencia crece con el caudal y la presión | Electricidad de ventiladores |

Table: Tabla 10. Mejoras candidatas.

El informe de HCWH sobre hospitales argentinos aporta estimaciones locales de ahorro (por ejemplo, hasta 40 % con VRF con recuperación de calor en un hospital de San Juan), con base no declarada y con la salvedad de que son estimaciones de los auditores [A].

# 7. Discusión

## 7.1 Tres cosas que el resultado muestra

1. **Los ventiladores son lo que más energía consume** (28,0 %, 847 MWh), por encima del compresor (23,6 %). Es un efecto del tipo de sistema (todo aire) y de las renovaciones que exige un hospital: 20 en quirófanos, 6 a 8 en áreas críticas, y zonas grandes de internación y áreas generales.
2. **El recalentamiento es casi la mitad del calor útil de la caldera** (511 de 1.044 MWh). La enfriadora rechaza al ambiente 4.198 MWh por año, unas 8,2 veces el calor de recalentamiento: el calor existe, falta ver si coincide en el tiempo y en temperatura.
3. **El COP estacional de la planta (3,96) coincide casi exactamente con el COP 4 que supone el artículo de Hospitecnia.** Es una coincidencia de resultado, no un ajuste: el COP sale del ciclo y de las temperaturas de condensación del clima.

## 7.2 Contraste con las referencias

Las referencias miden el edificio completo y este resultado solo el sistema térmico. Para compararlas, se estima el consumo total equivalente suponiendo que el sistema térmico es una fracción del total, con las participaciones que citan las fuentes del artículo de Hospitecnia (de 46 % a 73 %): queda entre 226 y 361 kWh/m² y año.

| Referencia | kWh/m²·año | Observación |
|----------------------------------------|--------------------------|----------------------------------|
| Garrahan (CABA), HCWH 2021 | 259 | Edificio completo, estimado por auditoría |
| CEMAR (Rosario), HCWH 2021 | 211 | Edificio completo, estimado por auditoría |
| Giordano (San Juan), HCWH 2021 | 163 | Edificio completo, estimado por auditoría |
| 23 hospitales internacionales (Hospitecnia) | mediana 333; rango 120 a 900 | Edificio completo |
| Modelo español del artículo (Hospitecnia) | 394 a 400 | Energía final, edificio completo |
| **Este modelo, solo sistema térmico** | **165** | Equivale a 226 a 361 para el edificio completo |

Table: Tabla 11. Intensidad energética del modelo y de las referencias.

El resultado queda en la parte alta de los hospitales argentinos auditados y por debajo del modelo español, y es consistente con la mediana internacional. Que supere a los argentinos es esperable: el modelo es un sistema completo de aire con recalentamiento y renovaciones normativas en todas las zonas críticas, mientras que la auditoría de HCWH encontró hospitales subclimatizados, con equipos viejos y splits. **Esta comparación es una banda de plausibilidad, no una validación**: son tres hospitales estimados, dos fuera del AMBA, y la participación del sistema térmico varía entre 46 y 73 % según la fuente.

## 7.3 Qué no incluye el modelo y hacia dónde empujaría

| Omisión | Efecto esperado sobre el consumo |
|---|---|
| Economizador (enfriamiento gratuito con aire exterior) | Baja unos 2,5 a 4 % |
| Ventiladores de retorno y de extracción, y bombas de agua caliente | Sube unos 3 a 9 % |
| Rendimiento de la caldera a carga parcial (se usa el de plena carga, 90 % sobre PCI) | Sube el gas 6 a 20 % |
| Planta con torre de refrigeración en vez de condensación por aire | Baja unos 3 a 6 % |
| Diversidad de cargas dentro de una zona (cada zona es un solo local) | Sube unos 2 a 6 % |
| ACS de guardia, quirófanos, cocina y personal (solo se cuenta por cama) | Sube unos 2 a 14 % |
| Clima de un año típico horario (se usan estados medios por mes) | Cambia en ±5 %, con signo incierto |

Table: Tabla 12. Omisiones del modelo. Los efectos son estimaciones de un revisor externo, no cálculos del modelo.

Cocina, lavandería, esterilización y vapor quedan fuera de la frontera: no cambian este resultado, pero el gas total del hospital sería mucho mayor.

# 8. Conclusiones (preliminares)

::: {custom-style="Pendiente"}
**Pendiente: alinear con la Consigna 5.** La consigna pide responder cinco preguntas con resultados numéricos. El texto exacto de esas preguntas no está en el repositorio, así que las conclusiones de abajo están ordenadas por tema y se reordenarán cuando se confirmen. Las que dependen de la exergía y de las alternativas no se pueden cerrar todavía.
:::

1. **Consumo.** El sistema térmico del hospital consume **3.021 MWh de energía final por año (165 kWh/m²)**: 1.736 MWh de electricidad y 1.285 MWh de gas. Para el edificio completo equivale a 226 a 361 kWh/m², dentro de la banda de las referencias.
2. **Dónde se va la energía.** El 28,0 % se consume en los ventiladores de las unidades de aire y el 23,6 % en el compresor; el gas del recalentamiento es el 20,8 %.
3. **Refrigeración.** La capacidad de diseño es 1.987 kW y el COP de diseño es 3,56, el 55 % del COP de Carnot (6,42); el COP estacional del compresor es 4,94.
4. **Combustión.** La caldera rinde 90,0 % sobre PCI. Los gases salen a 190 °C, por encima del rocío (56,1 °C), así que no se aprovecha el calor latente: es una mejora posible.
5. **Integración.** El hilo conductor es el recalentamiento: 511 MWh de calor útil que hoy se produce con gas mientras la enfriadora rechaza 4.198 MWh. La cota superior del ahorro de gas es 629 MWh al año. **Pendiente de cuantificar:** alternativa B, mejoras y exergía.
6. **Incertidumbre.** El resultado se mueve entre 142 y 202 kWh/m² con un supuesto por vez, y la incertidumbre global se estima en ±15 a 20 %. Antes de la entrega hay que reemplazar por fuentes citables el clima, las condiciones y renovaciones de ASHRAE 170, la composición del gas y el ACS.

# Anexo A. Supuestos principales

La tabla muestra 29 de los 54 parámetros, con su estado: **DATO** (leído de un documento recibido), **SUPUESTO** (fundamentado pero sin fuente citable todavía) o **CONSTANTE** (convención o propiedad física). La tabla completa, con la justificación de cada uno, está en `informe/supuestos.md`.

::: {custom-style="Largo"}
| ID | Parámetro | Valor | Unidad | Estado |
|------|----------------------------------------------------------|------------|------------|------------|
| E1 | Superficie cubierta total | 18352 | m² | DATO |
| E2 | Fracción de la superficie cubierta que se climatiza | 0,85 | – | SUPUESTO |
| E3 | Camas de internación general | 144 | camas | DATO |
| E4 | Camas de terapia intensiva | 14 | camas | DATO |
| E5 | Cantidad de quirófanos | 6 | – | DATO |
| E10 | Conductancia de la envolvente por m² de piso expuesto | 0,6 | W/(m² K) | SUPUESTO |
| E14 | Fracción de las áreas generales que funciona las 24 h | 0,35 | – | SUPUESTO |
| C1 | Temperatura de bulbo seco de diseño, verano | 34 | °C | SUPUESTO |
| C2 | Temperatura de bulbo húmedo coincidente, verano | 25 | °C | SUPUESTO |
| C3 | Temperatura de bulbo seco de diseño, invierno | 2 | °C | SUPUESTO |
| C4 | Humedad relativa de diseño, invierno | 0,8 | – | SUPUESTO |
| C6 | Amplitud diaria de temperatura | 9 | K | SUPUESTO |
| A1 | Temperatura mínima del aire de impulsión | 13 | °C | CONSTANTE |
| A3 | Humedad relativa a la salida de la serpentina | 0,95 | – | CONSTANTE |
| A5 | Rendimiento total de los ventiladores | 0,6 | – | SUPUESTO |
| A8 | Fracción de la potencia del ventilador que se disipa como calor en el aire | 1 | – | CONSTANTE |
| R1 | Refrigerante | R134a | – | SUPUESTO |
| R2 | Temperatura de evaporación | 3 | °C | SUPUESTO |
| R5 | Rendimiento isentrópico del compresor | 0,72 | – | SUPUESTO |
| R6 | Rendimiento del motor del compresor | 0,94 | – | SUPUESTO |
| R7 | Diferencia entre condensación y temperatura exterior | 12 | K | SUPUESTO |
| R8 | Temperatura mínima de condensación | 32 | °C | SUPUESTO |
| B1 | Gas natural: metano (fracción molar) | 0,91 | – | SUPUESTO |
| B6 | Relación de aire (1 = estequiométrico) | 1,15 | – | SUPUESTO |
| B7 | Temperatura de los gases de escape | 190 | °C | SUPUESTO |
| S1 | Consumo de ACS por cama y día | 100 | L/(cama día) | SUPUESTO |
| S2 | Temperatura del ACS | 60 | °C | DATO |
| S3 | Temperatura del agua fría de entrada | 17 | °C | SUPUESTO |
| S4 | Factor por pérdidas de acumulación y recirculación | 1,3 | – | SUPUESTO |

Table: Tabla A1. Parámetros principales del modelo.
:::

# Anexo B. Fuentes

- **[F1]** Presidencia de la Nación. Presentación *Inicio de la puesta en marcha. Hospital SAMIC «Dr. René Favaloro»*. Diapositivas, sin fecha explícita.
- **[F2]** Gobierno de la Provincia de Buenos Aires. *Kicillof participó de la inauguración del Hospital Doctor René Favaloro en La Matanza*. 28 de julio de 2020.
- **[A]** Health Care Without Harm y Kigali Cooling Efficiency Program. *Energy efficiency and cooling audits in health care facilities in Argentina, China, and the Philippines. Final project report*. Marzo de 2021.
- **[H]** Gallostra Isern, J., Sánchez-Vaqué, Á. y Túnica Buira, J. *Caracterización de consumos energéticos y suministros en hospitales*. Hospitecnia, octubre de 2022.
- Propiedades del refrigerante y de los gases: CoolProp. Aire húmedo: psychrolib (fórmulas de ASHRAE Fundamentals).
- Condiciones interiores y renovaciones: ASHRAE 170, **valores recordados y a verificar con la norma**.
- Clima de diseño y mensual: **sin fuente citable todavía** (a reemplazar con datos del SMN).

# Anexo C. Verificación del cálculo

- **49 chequeos termodinámicos** (`python -m pytest calculo/tests`): primera ley, segunda ley (COP menor que el de Carnot), balance de átomos de la combustión, coincidencia de la psicrometría con CoolProp y reproducción de la tabla de supuestos. Comprueban la coherencia interna; no prueban que la física sea la correcta.
- **Reimplementación independiente.** Agentes que no vieron el código reconstruyeron el cálculo solo con la especificación y la tabla de supuestos. En la primera versión coincidieron al 0,5 % o mejor salvo un defecto de la tabla de supuestos (redondeo de un parámetro), ya corregido. En la versión actual, uno coincidió exactamente y otro, con otra librería de aire húmedo, quedó dentro de 0,24 % en las magnitudes globales y de 0,02 % en la energía final.
- **Revisión adversarial.** Un tercer revisor encontró una omisión física importante, el calor de los ventiladores, que se corrigió y redujo el consumo base de 181 a 165 kWh/m².
- Lo que sigue **sin verificar** son los supuestos de entrada, no el cálculo.
