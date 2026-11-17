---
title: "Memoria de cálculo"
subtitle: "TP Integrador de Termodinámica 2026 · Sistema térmico de un hospital del AMBA · Borrador v0.2"
author: "[Integrantes del equipo: a completar]"
date: "Facultad de Ingeniería y Ciencias Agrarias · Ingeniería Civil · UCA · Noviembre de 2026"
lang: es-AR
---

::: {custom-style="Nota"}
**Para qué sirve esta memoria.** El informe técnico explica las decisiones y sus motivos; acá está el desarrollo ordenado de las ecuaciones, los datos, las hipótesis, las unidades y los resultados, como pide la consigna. Todas las cifras salen del código (`calculo/`) y el documento se regenera con él (`python -m calculo.construir_documentos`). Cada dato lleva su nivel de respaldo: **visto** (documento recibido y leído), **cita** (fuente secundaria vista en una búsqueda; falta cotejar con la fuente original), **propio** (cálculo o criterio nuestro con su lógica) o **recordado** (de memoria, sin fuente a mano).
:::

# 1. Hipótesis y frontera

1. En cada estado considerado el régimen es permanente; cada mes se parte en una mitad diurna y una nocturna.
2. El aire húmedo es una mezcla de aire seco y vapor, ambos gases ideales, a 101,325 kPa.
3. Sistema de caudal constante con serpentina y recalentamiento, sin economizador ni recuperación de calor: es la línea de base (alternativa A).
4. El ventilador de impulsión aspira después de la serpentina y toda su potencia eléctrica se disipa como calor en el aire.
5. El refrigerante cumple un ciclo de compresión de vapor con compresor adiabático de rendimiento isentrópico constante, expansión isoentálpica y sin pérdidas de presión. La evaporación es fija a 3 °C, el COP depende de la temperatura de condensación del estado y no de la carga (no hay curva de carga parcial) y el motor del compresor está fuera de la corriente de refrigerante.
6. Combustión completa del gas natural, gases ideales y sin disociación; el aire tiene 21 % de O₂ y 79 % de N₂; los gases de escape salen a 190 °C sin condensar.
7. **Frontera:** se calcula el sistema térmico y sus auxiliares (ventiladores de las unidades, ventiladores del condensador, bombas de agua helada). No se incluyen iluminación, equipos médicos, cocina, lavandería ni esterilización, por lo que **el resultado no es el consumo total del hospital**. No se modelan economizador, ventiladores de retorno y extracción, bombas de agua caliente ni pérdidas de distribución.

# 2. Aire húmedo

La humedad específica y la entalpía del aire húmedo, por kg de aire seco, son

$$\omega = 0\text{,}622\,\frac{p_v}{P - p_v}, \qquad h = 1\text{,}006\,T + \omega\,(2501 + 1\text{,}86\,T)$$

con $T$ en °C y $h$ en kJ/kg. La mezcla de aire exterior y de retorno conserva entalpía y humedad: $\dot m_a h_{mez} = \dot m_{ae} h_{ext} + \dot m_{ar} h_{ret}$ y la misma relación para $\omega$. La serpentina enfría hasta $T_c$ y deshumidifica hasta $\omega_c$, con el aire a la salida al 95 % de humedad relativa:

$$\dot Q_{serp} = \dot m_a\left[(h_{mez} - h_c) - (\omega_{mez} - \omega_c)\,h_f\right], \qquad \dot Q_{lat} = \dot m_a\,(\omega_{mez} - \omega_c)\,h_{fg}$$

donde $h_f = 4\text{,}186\,T_c$ es la entalpía del condensado y la parte sensible es la diferencia. El recalentador lleva el aire a $T_{obj}$, que es la temperatura de impulsión menos el calentamiento que producirá el ventilador:

$$\dot Q_{rec} = \dot m_a\,c_{p,ah}\,(T_{obj} - T_c), \qquad T_{obj} = T_{imp} - \frac{\dot W_{vent}}{\dot m_a\,c_{p,ah}}, \qquad c_{p,ah} = 1\text{,}006 + 1\text{,}86\,\omega$$

El estado de impulsión sale del balance de la zona. Con la actividad $f_{act}$, la fracción de envolvente expuesta $f_{env}$, la conductancia $U$ por m² de piso expuesto (0,6 W/(m² K)) y la ganancia solar $q_{sol}$ (en W/m², como las ganancias internas de plena actividad $q_s$ y $q_l$):

$$\dot Q_s = A\left[q_s\,f_{act} + f_{env}\,\big(U\,(T_{ext} - T_r) + q_{sol}\big)\right], \qquad \dot Q_l = A\,q_l\,f_{act}$$

$$T_{imp} = T_r - \frac{\dot Q_s}{\dot m_a\,c_{p,ah}}, \qquad \omega_{imp} = \omega_r - \frac{\dot Q_l}{\dot m_a\,h_{fg}}, \qquad \dot W_{vent} = \frac{\dot V\,\Delta p}{\eta_{vent}}$$

con $T_r$ y $\omega_r$ la temperatura y la humedad específica de consigna de la zona (el retorno está en ese estado), $\dot V = \dot m_a/\rho$ y las cargas pasadas a kW al dividir por $\dot m_a\,c_{p,ah}$; $T_{imp}$ queda limitada entre 13 y 35 °C, $h_{fg} = 2501$ kJ/kg, $\eta_{vent} = 0\text{,}60$ y $\rho = 1\text{,}2$ kg/m³. La serpentina lleva el aire a $\omega_c = \omega_{imp}$ con la temperatura de salida que corresponde a la saturación parcial indicada; si esa temperatura supera $T_{obj}$, enfría hasta $T_{obj}$. El caudal de impulsión es el mayor entre el que fijan las renovaciones y el que pide la carga sensible, y el de aire exterior se fija en valor absoluto. En invierno, si el aire sale más seco que la humedad mínima de la zona, se humidifica con vapor.

**Estados del aire en el quirófano, verano pico** (zona G1, 5,04 kg/s de aire seco):

| Estado | Descripción | T [°C] | ω [g/kg] | h [kJ/kg] | HR [%] |
|--------|------------------------------------|------------|------------|--------------|----------|
| A | Aire exterior | 34,0 | 16,26 | 75,9 | 48 |
| B | Local (consigna) | 22,0 | 9,06 | 45,2 | 55 |
| C | Mezcla con retorno | 24,4 | 10,50 | 51,3 | 55 |
| D | Salida de la serpentina | 13,0 | 8,86 | 35,4 | 95 |
| E | Tras el recalentador | 16,6 | 8,86 | 39,2 | 75 |
| F | Impulsión (tras el ventilador) | 19,1 | 8,86 | 41,7 | 64 |

Table: Tabla M1. Estados del aire en el quirófano (A a F). Las diferencias de una décima entre valores se deben al redondeo.

![Figura M0. Proceso del aire en el quirófano, verano pico.](../figuras/fig02_psicrometrica_quirofano.png){width=13cm}

# 3. Refrigeración

Para el ciclo con entalpías $h_1$ a $h_4$ (estados de la tabla M2), por kg de refrigerante:

$$q_L = h_1 - h_4, \qquad w = h_2 - h_1 = \frac{h_{2s} - h_1}{\eta_{is}}, \qquad q_H = h_2 - h_3$$

$$COP_{eje} = \frac{q_L}{w}, \qquad COP_{el} = \frac{q_L}{w/\eta_{mot}}, \qquad COP_{Carnot} = \frac{T_{ev}}{T_{cond} - T_{ev}}$$

$$\dot W_{comp} = \frac{\dot Q_L}{COP_{el}}, \qquad \dot Q_{cond} = \dot Q_L + \eta_{mot}\,\dot W_{comp}$$

El rendimiento del motor es $\eta_{mot} = 0\text{,}94$ y el COP de Carnot usa temperaturas absolutas (K). La temperatura de condensación sigue al clima: $T_{cond} = \max(T_{ext} + 12\ \text{K},\ 32\ °C)$. Los ventiladores del condensador consumen el 2,5 % del calor rechazado y las bombas se calculan con el caudal de agua helada (salto de 5 K), 250 kPa de presión y 0,60 de rendimiento total.

| Estado | Descripción | T [°C] | P [kPa] | h [kJ/kg] |
|--------|--------------------------------------------------|------------|------------|--------------|
| 1 | Salida del evaporador (vapor sobrecalentado 5 K) | 8,0 | 326 | 404,9 |
| 2s | Salida del compresor, isentrópica | – | 1.190 | 432,6 |
| 2 | Salida del compresor, real (rendimiento isentrópico 0,72) | 64,9 | 1.190 | 443,3 |
| 3 | Salida del condensador (subenfriado 4 K) | 42,0 | 1.190 | 259,4 |
| 4 | Salida de la válvula de expansión (título 0,28) | 3,0 | 326 | 259,4 |

Table: Tabla M2. Estados del ciclo de refrigeración al punto de diseño de verano. Las diferencias de una décima entre valores se deben al redondeo.

![Figura M0b. Ciclo de compresión de R134a al punto de diseño de verano.](../figuras/fig03_diagrama_ph_r134a.png){width=12cm}

# 4. Combustión

La reacción por kmol de gas natural, con relación de aire $\lambda$ = 1,15 (el oxígeno estequiométrico es $a_{st}$ = 2,045 kmol y el real, $\lambda\,a_{st}$; coeficientes en kmol, redondeados a tres decimales), es

$$0\text{,}91\,\text{CH}_4 + 0\text{,}05\,\text{C}_2\text{H}_6 + 0\text{,}01\,\text{C}_3\text{H}_8 + 0\text{,}02\,\text{N}_2 + 0\text{,}01\,\text{CO}_2 + 2\text{,}352\left(\text{O}_2 + \tfrac{79}{21}\,\text{N}_2\right) \rightarrow 1\text{,}050\,\text{CO}_2 + 2\text{,}010\,\text{H}_2\text{O} + 8\text{,}867\,\text{N}_2 + 0\text{,}307\,\text{O}_2$$

Los poderes caloríficos salen de las entalpías de formación, con agua líquida en los productos para el superior (PCS) y vapor para el inferior (PCI). El rendimiento de la caldera se calcula por el balance de los gases de escape, y el combustible necesario para entregar un calor útil $Q_{util}$ es

$$\eta = 1 - q_{gases} - f_{rad}, \qquad q_{gases} = \frac{H_{prod}(T_{gases}) - H_{reac}(T_{aire})}{PCI}, \qquad E_{PCS} = \frac{Q_{util}}{\eta}\cdot\frac{PCS}{PCI}$$

donde $H$ son las entalpías sensibles respecto de 25 °C (calores específicos de gas ideal de CoolProp), $T_{aire}$ = 15 °C y $f_{rad}$ = 2,0 % del PCI son las pérdidas por radiación y funcionamiento (supuesto).

| Magnitud | Valor |
|---|---|
| Poder calorífico superior | 9.196 kcal/m³ = 10,695 kWh/m³ (m³ estándar a 15 °C) |
| Poder calorífico inferior | 9,656 kWh/m³ (relación PCS/PCI = 1,108) |
| Pérdida por gases de escape (190 °C) | 8,0 % del PCI |
| Pérdida por radiación y funcionamiento (supuesto) | 2,0 % del PCI |
| **Rendimiento de la caldera** | **90,0 % sobre PCI** (81,2 % sobre PCS) |
| Temperatura de rocío de los gases | 56,1 °C (fracción molar de agua: 16,4 %) |
| Temperatura de llama adiabática teórica (sin disociación) | 1.848 °C |
| Gas por kWh de calor útil | 0,1151 m³ |
| Emisión de CO₂ del gas, de la reacción | 0,202 kg por kWh de PCI (56,2 kg/GJ) |

Table: Tabla M3. Combustión del gas natural y rendimiento de la caldera.

**Caldera de condensación.** Si los gases salen por debajo del punto de rocío, condensa parte del agua formada y se recupera su calor latente. Por kmol de combustible, con entalpías de formación:

$$Q_{util} = PCI + n_{cond}\,L - \sum_i n_i\,\Delta h_i(T_{gases}) + H_{reac} - f_{rad}\,PCI, \qquad n_{cond} = n_{H_2O} - n_{seco}\,\frac{p_{sat}(T_{gases})/P}{1 - p_{sat}(T_{gases})/P}$$

con $L$ = 44.010 kJ/kmol el calor latente del agua a 25 °C. A 45 °C condensan 47 % del agua y el rendimiento sube a 101,6 % sobre PCI (91,8 % sobre PCS).

# 5. ACS y consumo anual

El ACS se calcula desde el consumo por cama, no desde una potencia por m²:

$$\dot Q_{ACS} = \frac{L\cdot N_{camas}\cdot 4\text{,}186\,(T_{ACS} - T_{red})\cdot f_{perd}}{86\,400}$$

con $L$ = 100 L/(cama día), $N_{camas}$ = 158, $T_{ACS}$ = 60 °C, $T_{red}$ = 17 °C, $f_{perd}$ = 1,3, agua de 1 kg/L y resultado en kW (media de las 8.760 h del año; el modelo no calcula el pico).

Cada mes se representa con dos estados de $12\,d_i$ horas ($d_i$ son los días del mes): uno diurno $(T_i + 4\text{,}5\,\text{K})$ y uno nocturno $(T_i - 4\text{,}5\,\text{K})$, con la humedad específica media del mes limitada a la saturación. La estación de cada estado se decide por su temperatura exterior: verano (consignas de verano, con deshumidificación y recalentamiento) si $T \geq$ 18 °C e invierno (consignas de invierno, con calefacción y humidificación) si no, sin histéresis; el resultado es sensible a ese umbral. En cada estado se calculan las cargas de las cinco zonas, la planta de frío con la temperatura exterior del estado y el calor de la caldera, y se multiplican por las horas. Se prefirió este método a las horas equivalentes a plena carga porque la ventilación es continua y un número de horas la representa mal.

![Figura M1. Frío y calor del aire entregados por mes.](../figuras/fig05_perfil_mensual.png){width=14cm}

| Uso final | Energético | MWh/año | % del total | kWh/m² y año |
|--------------------------------------------|--------------|------------|------------|------------|
| Ventiladores de las unidades de tratamiento de aire | Electricidad | 847 | 28,0 % | 46,1 |
| Compresor de la enfriadora | Electricidad | 714 | 23,6 % | 38,9 |
| Recalentamiento después de la serpentina | Gas | 629 | 20,8 % | 34,3 |
| Agua caliente sanitaria | Gas | 461 | 15,3 % | 25,1 |
| Calefacción del aire | Gas | 194 | 6,4 % | 10,6 |
| Ventiladores del condensador | Electricidad | 105 | 3,5 % | 5,7 |
| Bombas de agua helada | Electricidad | 70 | 2,3 % | 3,8 |
| **Total** |  | **3.021** | 100 % | **164,6** |

Table: Tabla M4. Consumo anual por uso final. Los totales pueden diferir en 1 MWh de la suma de las filas por redondeo. La humidificación con vapor no aparece porque, con estados medios mensuales, el aire exterior nunca queda lo bastante seco; en el día de diseño de invierno pediría 92 kW.

La energía final suma electricidad y gas (PCS) kWh a kWh, sin ponderar por energía primaria.

# 6. Sensibilidad

| Variación de un supuesto (los demás quedan en su valor base) | Energía final [MWh/año] | Diferencia |
|--------------------------------------------------------------|----------------|------------|
| Humedad de consigna de verano 5 puntos menor en todas las zonas | 3.706 | +22,7 % |
| Consultorios y administración funcionan también las 24 h | 3.644 | +20,6 % |
| Sin calor del ventilador en el aire | 3.574 | +18,3 % |
| ACS de 200 L por cama y día (en vez de 100) | 3.483 | +15,3 % |
| Temperatura media mensual +2 K | 3.463 | +14,6 % |
| Cambio de estación (consignas de invierno) bajo 21 °C en vez de 18 °C | 2.589 | −14,3 % |
| Temperatura media mensual −2 K | 2.608 | −13,7 % |
| Guardia, diagnóstico y laboratorio: 50 % de las áreas generales | 3.409 | +12,8 % |
| Guardia, diagnóstico y laboratorio: 20 % de las áreas generales | 2.633 | −12,8 % |
| Humedad relativa media del clima −8 puntos | 2.773 | −8,2 % |
| Superficie climatizada 95 % de la cubierta | 3.263 | +8,0 % |
| Superficie climatizada 75 % de la cubierta | 2.780 | −8,0 % |

Table: Tabla M5. Las 12 variaciones que más mueven la energía final (caso base: 3.021 MWh).

![Figura M2. Sensibilidad de la energía final anual.](../figuras/fig06_sensibilidad.png){width=14.5cm}

# 7. Alternativa B y mejoras: modelo

Todas las variantes se calculan con `calculo/mejoras.py`, que repite el cálculo anual con opciones y da exactamente el caso base si no se activa ninguna (lo verifica un test).

- **B, recuperación del calor del condensador.** En cada estado con demanda de recalentamiento y calefacción $\dot Q_{dem}$ y frío en marcha, se elige el mejor entre tres modos: (1) sin recuperar; (2) solo el sobrecalentamiento de la descarga del compresor, sin cambiar la condensación; (3) un condensador de recuperación que condensa a $T_{cond,rec} = T_{agua} + \Delta T_{min}$ = 50 °C, con el compresor funcionando a esa presión. El criterio es el mayor ahorro neto en energía final: $\dot Q_{rec}/\eta_{cald} - \Delta\dot W_{comp} - \Delta\dot W_{vent.cond}$. El calor recuperado es $\dot Q_{rec} = \min(f\,\dot Q_{dem},\ \dot Q_{cond})$ con $f$ la fracción de la demanda que coincide con el calor disponible ($f$ = 1 en el caso central; se prueba 0,75 y 0,5).
- **M1, caldera de condensación:** aplica a la calefacción y el recalentamiento del aire (agua a 50/40 °C); el ACS y el vapor se dejan con el rendimiento base.
- **M2, solar térmico para el ACS:** el calor útil mensual es $A\,\eta_{col}\,H_m\,d_m$ con $H_m$ la irradiación horizontal diaria media del mes, que se calcula con la irradiación extraterrestre de Duffie y Beckman (latitud -34,7°) y un índice de claridad único, $K_t$ = 0,55, calibrado para que la suma anual sea 1.700 kWh/m². Nunca se usa más calor solar que la demanda del mes.
- **M3, recuperador de calor del aire de extracción** con circuito de agua (sin mezcla de corrientes): el aire exterior entra a la mezcla a $T_{oa} = T_{ext} + \varepsilon\,(T_r - T_{ext})$ con $\varepsilon$ = 0,50; tiene bypass y trabaja solo en los estados en que baja el costo de energía, y suma la potencia de ventiladores por su caída de presión.
- **M4, ventiladores:** la presión de diseño de cada zona se multiplica por 0,8; el calor que el ventilador ya no cede al aire lo repone la caldera.
- **M5, fotovoltaica:** energía anual $= kWp \cdot GHI \cdot PR$, descontada de la electricidad del sistema.
- **Emisiones:** CO₂ del gas = energía de PCI por el factor de la reacción (0,202 kg/kWh); CO₂ de la electricidad = energía por el factor de la red (0,38 t/MWh, cita secundaria: es una meta de CAMMESA para 2023).

| Variante | Energía final [MWh] | Electricidad [MWh] | Gas (PCS) [MWh] | CO₂ [t] | Energía | CO₂ |
|----------------------------------|------------|------------|------------|---------|---------|---------|
| A. Caso base | 3.021 | 1.736 | 1.285 | 895 | – | – |
| B. Recuperación del condensador | 2.477 | 1.807 | 670 | 809 | −18,0 % | −9,6 % |
| M1. Caldera de condensación | 2.927 | 1.736 | 1.191 | 877 | −3,1 % | −1,9 % |
| M2. Solar térmico para el ACS | 2.770 | 1.736 | 1.034 | 849 | −8,3 % | −5,1 % |
| M3. Recuperador del aire de extracción | 2.867 | 1.764 | 1.103 | 872 | −5,1 % | −2,5 % |
| M4. Ventiladores, 20 % menos de presión | 2.944 | 1.547 | 1.398 | 843 | −2,5 % | −5,8 % |
| M5. Fotovoltaica | 2.681 | 1.396 | 1.285 | 765 | −11,3 % | −14,4 % |
| Paquete B + M1 a M5 | 1.568 | 1.307 | 261 | 544 | −48,1 % | −39,2 % |

Table: Tabla M6. Resultados de cada variante respecto de la alternativa A.

| ID | Parámetro | Valor | Unidad | Nivel | Respaldo |
|-----|----------------------------|--------|---------|------------|--------------------------------------|
| M1 | Temperatura del agua caliente del recuperador de calor del condensador | 45 | C | SUPUESTO | Serpentina de recalentamiento que lleva aire de unos 13 C a 17-19 C: alcanza con agua tibia. Un caso de hospital con enfriadoras de recuperacion de calor usa agua a 115 F (46 C) en lugar de 180 F de caldera (Trane, caso Baylor Scott & White, via busqueda web) |
| M2 | Diferencia minima entre la condensacion y el agua caliente del recuperador | 5 | K | SUPUESTO | Intercambiador de placas tipico |
| M3 | Temperatura de los gases de escape de la caldera de condensacion | 45 | C | SUPUESTO | Agua de retorno a 40 C y 5 K de aproximacion; por debajo del rocio de los gases (unos 56 C) |
| M4 | Superficie de colectores solares para el ACS | 300 | m2 | SUPUESTO | Unos 5 % de la azotea (6.117 m2 por nivel); tamano que no produce excedentes en verano |
| M5 | Rendimiento medio anual de los colectores solares (sobre irradiacion horizontal) | 0,4 | - | SUPUESTO | Colector plano a 40-60 C con perdidas opticas y termicas; sin dato de catalogo |
| M6 | Irradiacion global horizontal anual | 1700 | kWh/m2 anio | FUENTE SECUNDARIA | Global Solar Atlas, informe de un punto de la provincia de Buenos Aires a unos 300 km (coordenadas -37,16 -59,06), via busqueda web: es una cota alta para la ciudad; a confirmar con globalsolaratlas.info para las coordenadas del hospital |
| M7 | Latitud del hospital | -34,7 | grados | SUPUESTO | La Matanza, Buenos Aires |
| M8 | Potencia fotovoltaica instalada | 250 | kWp | SUPUESTO | Unos 1.250 m2 de paneles (5 m2/kWp) sobre una azotea de 6.117 m2 con equipos |
| M9 | Relacion de rendimiento (performance ratio) de la instalacion fotovoltaica | 0,8 | - | SUPUESTO | Valor habitual de instalaciones nuevas (0,75 a 0,85); sin dato propio |
| M10 | Efectividad del recuperador de calor del aire de extraccion con circuito de agua | 0,5 | - | FUENTE SECUNDARIA | Una comparacion de un fabricante da 45 a 55 % para circuitos de agua con aislacion total entre corrientes (via busqueda web) |
| M11 | Caida de presion adicional del recuperador (cada lado) | 250 | Pa | SUPUESTO | Serpentina de 4 filas en cada corriente |
| M12 | Factor sobre la presion de los ventiladores en la mejora de ventiladores | 0,8 | - | SUPUESTO | Filtros y conductos de menor perdida, ventiladores de velocidad variable |
| M13 | Factor de emision de la electricidad de la red | 0,38 | tCO2/MWh | FUENTE SECUNDARIA | Meta de CAMMESA de 380 kg CO2e/MWh para 2023 (perfil de DitchCarbon, via busqueda web); es una meta y no un dato medido. Otras citas de busquedas: 0,288 t/MWh (Climate Transparency, datos de 2021, via Carbon Footprint) y unos 0,40 t/MWh (Ember, 2022). La Secretaria de Energia publica la serie oficial en datos.gob.ar: reemplazar |
| M14 | Temperatura minima de descarga del compresor para recuperar calor sin subir la condensacion | 50 | C | SUPUESTO | Agua a 45 C mas 5 K de aproximacion |

Table: Tabla M7. Parámetros de las mejoras y su respaldo.

# 8. Exergía: modelo y resultados

## 8.1 Método

Para cada equipo se plantea el esquema combustible–producto–pérdida, $\dot X_F = \dot X_P + \dot X_L + \dot X_D$, en kW. El **estado muerto** es el del aire exterior de cada caso ($T_0$, $\omega_0$, $P_0$ = 101,325 kPa). Exergía de flujo y del calor:

$$\dot X = \dot m\,[(h - h_0) - T_0\,(s - s_0)], \qquad \dot X_Q = \dot Q\,\left(1 - \frac{T_0}{T}\right), \qquad \dot X_D = T_0\,\dot S_{gen}$$

Para el aire húmedo se usa la expresión por kg de aire seco como mezcla de gases ideales, con término térmico $(c_{p,a} + \omega\,c_{p,v})\,T_0\,(T/T_0 - 1 - \ln T/T_0)$ y término de mezcla en función de $\omega$ y $\omega_0$; vale 0 en el estado muerto y es no negativa. La exergía del condensado incluye el término químico respecto del vapor ambiente, $R_v T_0 \ln(p_{sat}(T_0)/p_{v0})$, unos 102 kJ/kg a 34 °C y 48 % de humedad (sin él la destrucción de la serpentina se sobreestimaría casi al doble). La exergía química del gas natural es la de la mezcla ideal, $\sum y_i\,ex_i + R\,T_0 \sum y_i \ln y_i$, con las exergías químicas estándar de Szargut (CH₄ 831.650; C₂H₆ 1.495.840; C₃H₈ 2.154.000; N₂ 720; CO₂ 19.870; O₂ 3.970; H₂O gas 9.500 kJ/kmol): **recordadas, a cotejar con el libro de la cátedra**.

**Eficiencias.** Enfriadora: producto = exergía del frío, $\dot Q_L\,(T_0/T_{cw} - 1)$ con $T_{cw}$ la temperatura media logarítmica del agua helada (9,5 °C); caldera: producto = exergía del calor entregado al agua a 80/60 °C. Para el recalentador y el aire el producto puede ser negativo (se calienta aire que está por debajo del estado muerto): ahí solo se informa la destrucción.

## 8.2 Resultados por equipo

| Exergía [kW] | Verano pico (exterior 34,0 °C): kW | % | Máximo recalentamiento (dic, noche, 18,9 °C): kW | % |
|----------------------------------------------|------------------|--------|--------------------|--------|
| **Exergía que entra** (electricidad más gas) | **854** | 100 | **550** | 100 |
| Exergía útil (aire tratado y ACS) | 63 | 7,4 | 2 | 0,3 |
| Pérdidas al ambiente (condensado, aire del condensador, gases) | 60 | 7,0 | 24 | 4,3 |
| Destruida en: Compresor y motor | 169 | 19,8 | 25 | 4,5 |
| Destruida en: Condensador, válvula y evaporador | 193 | 22,6 | 36 | 6,5 |
| Destruida en: Ventiladores y bombas (con sus pérdidas de carga) | 233 | 27,3 | 105 | 19,1 |
| Destruida en: Mezcla, serpentina y recalentador | 71 | 8,3 | 56 | 10,3 |
| Destruida en: Caldera y ACS | 65 | 7,6 | 303 | 55,1 |
| **Destruida en total** | **731** | **85,6** | **525** | **95,4** |

Table: Tabla M14a. Reparto de la exergía de entrada en los dos casos analizados.


**Verano pico** (exterior a 34,0 °C; entrada 854 kW: 784 de electricidad y 71 de gas). Cierre del balance global: error relativo menor que $10^{-12}$.

| Equipo | F [kW] | P [kW] | L [kW] | D [kW] | % de D | η exergética |
|----------------------------------|---------|---------|---------|---------|---------|-------------|
| Mezcla de aire exterior y retorno | 5,8 | 0,0 | 0,0 | 5,8 | 0,8 | – |
| Serpentina de enfriamiento y deshumidificación | 172,3 | 78,2 | 32,1 | 62,0 | 8,5 | – |
| Recalentador y calefacción (agua 80/60 °C) | 2,0 | -1,2 | 0,0 | 3,2 | 0,4 | – |
| Humidificador de vapor | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | – |
| Ventiladores de impulsión | 122,6 | 73,5 | 0,0 | 49,0 | 6,7 | 60,0 % |
| Pérdidas de carga del aire (filtros, serpentinas, conductos) | 73,5 | -8,4 | 0,0 | 82,0 | 11,2 | – |
| Motor eléctrico del compresor | 558,7 | 525,2 | 0,0 | 33,5 | 4,6 | 94,0 % |
| Compresor (compresión real) | 525,2 | 389,6 | 0,0 | 135,6 | 18,5 | 74,2 % |
| Condensador por aire | 101,8 | 0,0 | 24,2 | 77,6 | 10,6 | – |
| Válvula de expansión | 65,3 | 0,0 | 0,0 | 65,3 | 8,9 | – |
| Evaporador (agua helada / R134a) | 222,5 | 172,3 | 0,0 | 50,2 | 6,9 | 77,5 % |
| Ventiladores del condensador | 62,8 | 0,0 | 0,0 | 62,8 | 8,6 | – |
| Bombas de agua helada | 39,6 | 23,7 | 0,0 | 15,8 | 2,2 | 60,0 % |
| Pérdidas de carga del agua helada | 23,7 | 0,0 | 0,0 | 23,7 | 3,2 | – |
| Caldera de gas natural (combustión y transferencia) | 70,8 | 6,4 | 2,8 | 61,6 | 8,4 | 9,1 % |
| Calentamiento de ACS (intercambiador y acumulación) | 4,5 | 0,4 | 0,8 | 3,3 | 0,4 | 9,5 % |

Table: Tabla M15. Balance exergético por equipo, verano pico.

**Máximo recalentamiento del año** (diciembre, noche; exterior a 18,9 °C; entrada 550 kW: 188 de electricidad y 363 de gas).

| Equipo | F [kW] | P [kW] | L [kW] | D [kW] | % de D | η exergética |
|----------------------------------|---------|---------|---------|---------|---------|-------------|
| Mezcla de aire exterior y retorno | 0,6 | 0,0 | 0,0 | 0,6 | 0,1 | – |
| Serpentina de enfriamiento y deshumidificación | 15,8 | 0,7 | 0,7 | 14,4 | 2,7 | – |
| Recalentador y calefacción (agua 80/60 °C) | 40,4 | -1,0 | 0,0 | 41,4 | 7,9 | – |
| Humidificador de vapor | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | – |
| Ventiladores de impulsión | 82,3 | 49,4 | 0,0 | 32,9 | 6,3 | 60,0 % |
| Pérdidas de carga del aire (filtros, serpentinas, conductos) | 49,4 | 0,5 | 0,0 | 48,8 | 9,3 | – |
| Motor eléctrico del compresor | 82,3 | 77,4 | 0,0 | 4,9 | 0,9 | 94,0 % |
| Compresor (compresión real) | 77,4 | 57,4 | 0,0 | 20,0 | 3,8 | 74,2 % |
| Condensador por aire | 24,6 | 0,0 | 6,1 | 18,5 | 3,5 | – |
| Válvula de expansión | 5,7 | 0,0 | 0,0 | 5,7 | 1,1 | – |
| Evaporador (agua helada / R134a) | 27,1 | 15,8 | 0,0 | 11,4 | 2,2 | 58,1 % |
| Ventiladores del condensador | 13,8 | 0,0 | 0,0 | 13,8 | 2,6 | – |
| Bombas de agua helada | 9,4 | 5,7 | 0,0 | 3,8 | 0,7 | 60,0 % |
| Pérdidas de carga del agua helada | 5,7 | 0,0 | 0,0 | 5,7 | 1,1 | – |
| Caldera de gas natural (combustión y transferencia) | 362,7 | 46,8 | 15,9 | 300,0 | 57,1 | 12,9 % |
| Calentamiento de ACS (intercambiador y acumulación) | 6,4 | 2,0 | 1,2 | 3,1 | 0,6 | 31,8 % |

Table: Tabla M16. Balance exergético por equipo, máximo recalentamiento.

## 8.3 Sensibilidad al estado muerto

Repetición del verano pico con otros estados muertos (el aire exterior queda fijo en 34 °C; la humedad de referencia a $T_0 \neq 34$ °C es la del aire a $T_0$ con la humedad relativa media anual):

| T0 [°C] | D total [kW] | P total [kW] | L total [kW] | η global | η enfriadora | η caldera |
|----------|--------------|--------------|--------------|--------------|----------------|--------------|
| 34,0 | 731 | 63,2 | 60 | 7,4 % | 26,1 % | 9,1 % |
| 25,0 | 714 | 25,2 | 115 | 3,0 % | 16,5 % | 11,4 % |
| 17,5 | 700 | -20,8 | 176 | no definida | 8,5 % | 13,3 % |

Table: Tabla M17. Sensibilidad al estado muerto. Con $T_0$ menor que el aire tratado, el producto del aire pasa a ser negativo y la eficiencia global deja de estar definida.

## 8.4 Supuestos y convenciones

- Circuito de agua caliente 80/60 °C para el recalentador, la calefacción y el ACS (supuesto; el modelo base no lo fija). Agua helada 7/12 °C (coherente con el modelo).
- Efectividad 0,5 del condensador: el aire sale a $T_{ext} + 0{,}5\,(T_{cond} - T_{ext})$; solo reparte la pérdida y la destrucción del condensador, no cambia el total.
- La pérdida del motor del compresor se cuenta como destrucción (calor disipado a una temperatura cercana a $T_0$). **A confirmar con la cátedra**: otra convención la llamaría pérdida.
- Ventiladores y bombas: producto = trabajo de flujo $\dot V\,\Delta p$, que se disipa después en filtros, serpentinas y conductos (fila de pérdidas de carga). Los ventiladores del condensador no tienen producto.
- Limitaciones: la humidificación del modelo base inyecta vapor a 2.676 kJ/kg de forma isotérmica y no conserva la energía exacta (cerca de 0,7 % de la carga de invierno); el modelo no tiene el caudal de aire del condensador, por eso el reparto entre pérdida y destrucción ahí depende de la efectividad supuesta.


# 9. Selección de equipos: cálculos

## 9.1 Enfriadoras

Carga de diseño $\dot Q_L$ = 1.987,2 kW; con 2 unidades en servicio cada una debe dar $\dot Q_L/2$ = 993,6 kW. La Carrier AquaForce 30XA 1002 da 988 kW nominales a 35 °C de aire exterior y agua 12/7 °C, con 288,2 kW de compresores (cita; no se abrió el catálogo). Margen $= 2 \cdot 988 - 1.987,2$ = −11,2 kW (0,6 %). Con el calor de las bombas (39,6 kW) la carga sería 2.027 kW y el faltante, 50,8 kW (2,6 %).

COP de catálogo (compresores solos, 35 °C de aire): 3,43. COP del modelo (compresor solo, 34 °C de aire exterior, condensación a 46 °C): 3,56, 3,7 % por encima. Al mismo aire de 35 °C (condensación a 47 °C) el modelo da 3,45, 0,7 % respecto del catálogo: el 82 % de la diferencia viene de comparar 34 °C con 35 °C. Esa coincidencia a 35 °C no valida el modelo: η_is = 0,72 y η_motor = 0,94 son supuestos, el catálogo incluye pérdidas de aceite, economizador y variador que el modelo no tiene, y la pendiente del COP con la temperatura de la máquina real no está verificada. Ninguno de los dos COP incluye ventiladores del condensador ni bombas.

## 9.2 Calderas

Carga de diseño $= 649 + 86$ = 734 kW (calefacción y humidificación de invierno más la punta de ACS, el doble de la media por supuesto). El vapor de humidificación son 92 kW; sin él, el agua caliente necesita 557 kW. Chimenea: gases de 1.662 m³/h a 190 °C con 8 m/s dan un diámetro de 271 mm, es decir DN 300. Condensación como cota superior: 98 % sobre PCS (catálogo, cita) contra 81,2 % del modelo, hasta 17,1 % menos de gas, solo si el retorno baja del punto de rocío de 56,1 °C.

## 9.3 Unidades de tratamiento de aire

| Unidad | Zona | Caudal [m³/h] | Ubicación | HEPA |
|--------------|--------|--------------|--------------------------------------------------|--------|
| UTA-G1-1 | G1 | 2.520 | cuarto técnico del 2.º piso | sí |
| UTA-G1-2 | G1 | 2.520 | cuarto técnico del 2.º piso | sí |
| UTA-G1-3 | G1 | 2.520 | cuarto técnico del 2.º piso | sí |
| UTA-G1-4 | G1 | 2.520 | cuarto técnico del 2.º piso | sí |
| UTA-G1-5 | G1 | 2.520 | cuarto técnico del 2.º piso | sí |
| UTA-G1-6 | G1 | 2.520 | cuarto técnico del 2.º piso | sí |
| UTA-G2-1 | G2 | 6.048 | cuarto técnico del 2.º piso | sí |
| UTA-G3-1 | G3 | 18.237 | cubierta | no |
| UTA-G3-2 | G3 | 18.237 | cubierta | no |
| UTA-G3-3 | G3 | 18.237 | cubierta | no |
| UTA-G4-1 | G4 | 23.056 | cubierta | no |
| UTA-G4-2 | G4 | 23.056 | cubierta | no |
| UTA-G4-3 | G4 | 23.056 | cubierta | no |
| UTA-G4-4 | G4 | 23.056 | cubierta | no |
| UTA-G5-1 | G5 | 24.167 | cubierta | no |
| UTA-G5-2 | G5 | 24.167 | cubierta | no |
| UTA-G5-3 | G5 | 24.167 | cubierta | no |
| UTA-G5-4 | G5 | 24.167 | cubierta | no |

Table: Tabla M11. Unidades de tratamiento de aire (criterio: una por quirófano y hasta 25.000 m³/h por unidad en las demás zonas).

## 9.4 Hidráulica y conductos

Caudal de agua helada $\dot m_w = \dot Q_L/(c_p \Delta T)$ = 94,9 kg/s (342 m³/h). Diámetro para 2,0 m/s: $D = \sqrt{4\dot V/(\pi v)}$ = 246 mm, por lo que DN 250 con una velocidad real de 1,93 m/s; el ramal por enfriadora, DN 200 (1,51 m/s).

| Zona | Impulsión [m³/h] | A impulsión [m²] | A retorno [m²] | Shaft vertical [m²] | Shafts | Modo |
|-------|------------|------------|-----------|------------|-------|---------------------------------------|
| G1 | 15.120 | 0,70 | 0,67 | 0,31 | 1 | UTA en el nivel: el shaft lleva aire exterior y extracción |
| G2 | 6.048 | 0,28 | 0,22 | 0,21 | 1 | UTA en el nivel: el shaft lleva aire exterior y extracción |
| G3 | 54.711 | 2,53 | 1,70 | 4,23 | 3 | UTA en cubierta: el shaft lleva impulsión y retorno |
| G4 | 92.225 | 4,27 | 3,84 | 8,11 | 5 | UTA en cubierta: el shaft lleva impulsión y retorno |
| G5 | 96.670 | 4,48 | 4,18 | 8,66 | 5 | UTA en cubierta: el shaft lleva impulsión y retorno |
| Total | 264.774 | 12,26 | 10,62 | 21,51 | 14 |  |

Table: Tabla M12. Shafts de aire (impulsión a 6 m/s y retorno a 5 m/s; para las zonas con la UTA en su nivel el shaft vertical lleva solo aire exterior y extracción).

## 9.5 Azotea y ubicación

Huella de 14 × 3,5 = 49 m² por unidad (147 m² en total, 2,4 % de la cubierta). Carga media $q = 12 \cdot 9{,}81 / 49$ = 2,40 kN/m² contra 2,0 kN/m² de referencia (recordada).

| Criterio | Peso | Azotea (1 a 5) | Patio (1 a 5) | Razón |
|--------------------|-------|---------|---------|-------------------------------------------------------|
| Aire libre para el condensador | 20 % | 5 | 2 | En azotea el aire circula sin obstaculos. Un patio tecnico rodeado por el edificio recircula el aire caliente de descarga |
| Ruido hacia internación y terapia intensiva | 20 % | 3 | 2 | En azotea el ruido queda arriba del 3.er piso (administracion y docencia), separado de la internacion por una losa. En el patio a nivel el equipo queda frente a ventanas del 1.er y 2.º piso |
| Carga estructural | 15 % | 2 | 5 | La azotea exige losa y vigas para equipos (ver carga en kN/m2). A nivel el suelo la absorbe sin problema |
| Izaje y montaje | 15 % | 2 | 4 | Unidades de 14 m y 12 t a unos 15 m de altura: grua movil grande y corte de calle. A nivel basta una grua menor para descargar del camion |
| Recorrido de cañerías hacia las UTAs | 15 % | 4 | 2 | 11 de las 18 UTAs estan en cubierta: las canierias horizontales son cortas. Desde un patio a nivel habria que subir todo el agua helada por el nucleo tecnico |
| Acceso para mantenimiento | 15 % | 3 | 4 | Azotea: acceso por escalera o montacargas, proteccion contra caidas, sin camion. Patio: acceso directo, reemplazo de componentes mas facil |

Table: Tabla M13. Matriz de decisión entre azotea y patio a nivel. Puntaje ponderado: azotea 3,25, patio 3,05; con pesos iguales 3,17 en ambos; con estructura e izaje al doble, azotea 2,96 y patio 3,38.

## 9.6 Supuestos de la selección de equipos

::: {custom-style="Largo"}
| ID | Parametro | Valor | Unidad | Estado | Justificacion |
|---|---|---|---|---|---|
| Q1 | Cantidad de niveles del edificio | 3 | niveles | SUPUESTO | datos/favaloro_nordelta.md FA-08 (DATO) lista tres pisos y no menciona planta baja; se toma un edificio de tres niveles |
| Q2 | Superficie bruta de cada nivel | iguales (A_cub / n) | - | SUPUESTO | Sin planos: cada nivel recibe la misma superficie bruta (6.117 m2) y la misma superficie climatizada (5.200 m2) |
| Q3 | El 1.er nivel esta a nivel de calle | 1.er nivel | - | SUPUESTO | Como FA-08 no menciona planta baja, el 1.er piso se toma a nivel de calle; el anexo de calderas se apoya en ese nivel |
| Q4 | Relacion largo/ancho de la planta rectangular equivalente (solo para la figura) | 1,33333 | - | SUPUESTO | Esquema de la planta de cubierta con la misma superficie que un nivel; no hay planos del edificio real |
| Q10 | Enfriadoras en servicio | 2 | unidades | SUPUESTO | Configuracion N+1: 2 en servicio |
| Q11 | Enfriadoras de reserva | 1 | unidades | SUPUESTO | Configuracion N+1: 1 de reserva, 3 unidades iguales |
| Q12 | Enfriadora de ejemplo | Carrier AquaForce 30XA 1002 | - | FUENTE SECUNDARIA | Busqueda web sobre catalogos de Carrier; no se pudo abrir el catalogo. Enfriadora de tornillo condensada por aire |
| Q13 | Capacidad nominal de la enfriadora de ejemplo | 988 | kW | FUENTE SECUNDARIA | Idem Q12. Con aire exterior a 35 C y agua helada 12/7 C |
| Q14 | Potencia absorbida por los compresores de la enfriadora de ejemplo | 288,2 | kW | FUENTE SECUNDARIA | Idem Q12, mismas condiciones nominales. Solo compresores |
| Q15 | Temperatura del aire exterior de la capacidad de catalogo | 35 | C | FUENTE SECUNDARIA | Idem Q12 |
| Q16 | Agua helada de catalogo (entrada / salida del evaporador) | 12 / 7 | C | FUENTE SECUNDARIA | Idem Q12; salto de 5 K, igual al del modelo (R10) |
| Q17 | Capacidad minima de la familia 30XA | 267 | kW | FUENTE SECUNDARIA | Idem Q12 |
| Q18 | Capacidad maxima de la familia 30XA | 1682 | kW | FUENTE SECUNDARIA | Idem Q12 |
| Q19 | Refrigerante de la enfriadora de ejemplo | R-134a | - | FUENTE SECUNDARIA | Idem Q12; coincide con el del modelo (R1) |
| Q20 | Margen de diseno sobre la carga pico (solo informativo) | 0,1 | - | SUPUESTO | Practica habitual de seleccion; el modelo da la carga pico sin margen. No cambia la seleccion base |
| Q21 | Largo de la huella en azotea por enfriadora | 14 | m | SUPUESTO | Sin dimensiones del catalogo; se interpreta como el area reservada por unidad, con espacios de servicio |
| Q22 | Ancho de la huella en azotea por enfriadora | 3,5 | m | SUPUESTO | Idem Q21 |
| Q23 | Peso operativo por enfriadora | 12 | t | SUPUESTO | A confirmar con el catalogo (peso operativo incluye el agua del evaporador y el refrigerante) |
| Q24 | Sobrecarga de referencia de una azotea de uso corriente | 2 | kN/m2 | SUPUESTO | Solo orden de magnitud para comparar. RECORDADO: los reglamentos de cargas dan entre 1 y 5 kN/m2 segun el acceso a la azotea (CIRSOC 101, verificar) |
| Q25 | Aceleracion de la gravedad | 9,81 | m/s2 | CONSTANTE | Para pasar toneladas a kN |
| Q30 | Factor de simultaneidad: punta de ACS / ACS media | 2 | - | SUPUESTO | El modelo da solo el ACS medio (43 kW); el pico no se calcula. Se suma al punto de diseno de invierno (coincidencia conservadora) |
| Q31 | Calderas de agua caliente en servicio (pirotubulares a gas, 100 % cada una) | 1 | unidades | SUPUESTO | Configuracion 2 x 100 % |
| Q32 | Calderas de agua caliente de reserva | 1 | unidades | SUPUESTO | Configuracion 2 x 100 % (N+1), sin marca |
| Q33 | Capacidad maxima por unidad de la caldera de condensacion de ejemplo (Viessmann Vitocrossal 300 CM3C) | 311 | kW | FUENTE SECUNDARIA | Busqueda web; no se pudo abrir el catalogo |
| Q34 | Capacidad minima por unidad de la caldera de ejemplo | 87 | kW | FUENTE SECUNDARIA | Idem Q33; las unidades se pueden poner en cascada |
| Q35 | Rendimiento maximo de la caldera de condensacion | 0,98 | - | FUENTE SECUNDARIA | Idem Q33; sobre PCS y con retorno frio (maximo, no valor de operacion) |
| Q36 | Unidades de reserva de la cascada de condensacion | 1 | unidades | SUPUESTO | Configuracion 3+1: 3 en servicio y 1 de reserva |
| Q37 | Velocidad de los gases en la chimenea | 8 | m/s | SUPUESTO | Quemador con ventilador (tiraje forzado); predimensionamiento |
| Q40 | Caudal maximo por UTA (zonas no criticas) | 25000 | m3/h | SUPUESTO | Criterio de predimensionamiento |
| Q41 | UTAs por quirofano (con filtro HEPA) | 1 | unidades | SUPUESTO | Una UTA por quirofano; cada quirofano es una zona independiente |
| Q42 | UTAs de terapia intensiva (con filtro HEPA) | 1 | unidades | SUPUESTO | Una UTA para la unidad |
| Q50 | Velocidad maxima del agua helada en la canieria principal | 2 | m/s | SUPUESTO | Predimensionamiento |
| Q51 | Serie de diametros nominales disponibles | 150, 200, 250, 300, 350 | mm | CONSTANTE | Serie nominal DN |
| Q52 | Diametro interior de la canieria = DN | ID = DN | - | SUPUESTO | Aproximacion; en tubo de acero el interior real de DN 250 o mayor es algo mayor, asi que la velocidad real es algo menor |
| Q53 | Densidad del agua helada | 1000 | kg/m3 | CONSTANTE | Agua a 7 a 12 C |
| Q54 | Velocidad del aire de impulsion en los shafts | 6 | m/s | SUPUESTO | Predimensionamiento |
| Q55 | Velocidad del aire de retorno en los shafts | 5 | m/s | SUPUESTO | Predimensionamiento |
| Q56 | Caudal de exfiltracion | 0 | m3/h | SUPUESTO | Retorno = impulsion - aire exterior - exfiltracion; con exfiltracion nula todo el aire exterior sale por la extraccion |
| Q57 | Area de un shaft tipo | 2 | m2 | SUPUESTO | Orden de magnitud para contar shafts; es area neta de conducto: el shaft real ocupa mas (aislacion, compuertas cortafuego, acceso) |
| Q60 | Pesos y puntajes de la matriz de decision azotea / patio a nivel | ver MATRIZ_UBICACION | - | SUPUESTO | Juicio de ingenieria, sin ensayo ni calculo de ruido; el resultado se muestra con su sensibilidad a los pesos |

Table: Tabla M14. Supuestos nuevos de la selección y ubicación de equipos, con su estado.
:::


# Anexo. Datos de entrada

La tabla M8 muestra 41 de los 54 parámetros escalares; las tablas M9 y M10, las zonas y el clima. Estado de cada uno: **DATO** (leído de un documento recibido: E1, E3, E4 y E5 son del hospital base y S2 viene del artículo [H]), **SUPUESTO** (fundamentado pero sin fuente citable todavía) o **CONSTANTE** (convención de diseño o propiedad física). La tabla completa, con la justificación de cada uno, está en `informe/supuestos.md`.

::: {custom-style="Largo"}
| ID | Parámetro | Valor | Unidad | Estado |
|------|----------------------------------------------------------|------------|------------|------------|
| E1 | Superficie cubierta total | 18.352 | m² | DATO |
| E2 | Fracción de la superficie cubierta que se climatiza | 0,85 | – | SUPUESTO |
| E3 | Camas de internación general | 144 | camas | DATO |
| E4 | Camas de terapia intensiva | 14 | camas | DATO |
| E5 | Cantidad de quirófanos | 6 | – | DATO |
| E6 | Superficie por quirófano | 42 | m² | SUPUESTO |
| E7 | Superficie por cama de terapia intensiva | 24 | m²/cama | SUPUESTO |
| E8 | Superficie por cama de internación general | 28 | m²/cama | SUPUESTO |
| E9 | Altura libre de los locales | 3 | m | SUPUESTO |
| E10 | Conductancia de la envolvente por m² de piso expuesto | 0,6 | W/(m² K) | SUPUESTO |
| E14 | Fracción de las áreas generales que funciona las 24 h | 0,35 | – | SUPUESTO |
| C1 | Temperatura de bulbo seco de diseño, verano | 34 | °C | SUPUESTO |
| C2 | Temperatura de bulbo húmedo coincidente, verano | 25 | °C | SUPUESTO |
| C3 | Temperatura de bulbo seco de diseño, invierno | 2 | °C | SUPUESTO |
| C4 | Humedad relativa de diseño, invierno | 0,8 | – | SUPUESTO |
| C6 | Amplitud diaria de temperatura | 9 | K | SUPUESTO |
| A1 | Temperatura mínima del aire de impulsión | 13 | °C | CONSTANTE |
| A2 | Temperatura máxima del aire de impulsión | 35 | °C | CONSTANTE |
| A3 | Humedad relativa a la salida de la serpentina | 0,95 | – | CONSTANTE |
| A4 | Temperatura exterior bajo la cual rigen las consignas de invierno | 18 | °C | SUPUESTO |
| A5 | Rendimiento total de los ventiladores | 0,6 | – | SUPUESTO |
| A7 | Calor latente de vaporización del agua | 2.501 | kJ/kg | CONSTANTE |
| A8 | Fracción de la potencia del ventilador que se disipa como calor en el aire | 1 | – | SUPUESTO |
| R1 | Refrigerante | R134a | – | SUPUESTO |
| R2 | Temperatura de evaporación | 3 | °C | SUPUESTO |
| R5 | Rendimiento isentrópico del compresor | 0,72 | – | SUPUESTO |
| R6 | Rendimiento del motor del compresor | 0,94 | – | SUPUESTO |
| R7 | Diferencia entre condensación y temperatura exterior | 12 | K | SUPUESTO |
| R8 | Temperatura mínima de condensación | 32 | °C | SUPUESTO |
| R9 | Potencia de ventiladores del condensador / calor rechazado | 0,025 | – | SUPUESTO |
| R10 | Salto de temperatura del agua helada | 5 | K | SUPUESTO |
| R11 | Diferencia de presión de las bombas de agua helada | 250.000 | Pa | SUPUESTO |
| R12 | Rendimiento total de las bombas | 0,6 | – | SUPUESTO |
| B1 | Gas natural: metano (fracción molar) | 0,91 | – | SUPUESTO |
| B6 | Relación de aire (1 = estequiométrico) | 1,15 | – | SUPUESTO |
| B7 | Temperatura de los gases de escape | 190 | °C | SUPUESTO |
| B9 | Pérdidas por radiación y funcionamiento / calor liberado | 0,02 | – | SUPUESTO |
| S1 | Consumo de ACS por cama y día | 100 | L/(cama día) | SUPUESTO |
| S2 | Temperatura del ACS | 60 | °C | DATO |
| S3 | Temperatura del agua fría de entrada | 17 | °C | SUPUESTO |
| S4 | Factor por pérdidas de acumulación y recirculación | 1,3 | – | SUPUESTO |

Table: Tabla M8. Parámetros principales del modelo.
:::

| Zona | Superficie [m²] | Consigna de verano | Renovaciones mínimas, totales / de aire exterior [1/h] | Caudal de impulsión [m³/h] | Renovaciones resultantes [1/h] | Aire exterior [m³/h] | Funcionamiento |
|--------------------|--------|-----------|--------------|----------|----------|---------|------------------|
| G1 Quirófanos | 252 | 22 °C; 55 % | 20 / 4 | 15.120 | 20,0 | 3.024 | Continuo; actividad de día |
| G2 Terapia intensiva | 336 | 23 °C; 55 % | 6 / 2 | 6.048 | 6,0 | 2.016 | Continuo |
| G3 Internación general | 4.032 | 24 °C; 55 % | 4 / 2 | 54.711 | 4,5 | 24.192 | Continuo |
| G4 Guardia, imágenes y laboratorio | 3.843 | 24 °C; 60 % | 8 / 2 | 92.225 | 8,0 | 23.056 | 24 h |
| G5 Consultorios, administración y docencia | 7.136 | 24 °C; 60 % | 3 / 1 | 96.670 | 4,5 | 21.409 | 12 h, lunes a viernes |

Table: Tabla M9a. Zonas, consignas de verano, renovaciones mínimas (totales / de aire exterior), caudales y funcionamiento.

| Zona | Ganancias internas sensible / latente [W/m²] | Actividad de día / de noche | Consigna de invierno (T; HR mínima) | Fracción de envolvente expuesta | Presión del ventilador [Pa] | Días por semana |
|--------------------------|----------------|------------|----------------|----------|----------|----------|
| G1 Quirófanos | 60 / 10 | 0,8 / 0,0 | 22 °C; 30 % | 0,0 | 1.800 | 7 |
| G2 Terapia intensiva | 40 / 8 | 1,0 / 1,0 | 23 °C; 30 % | 0,5 | 1.500 | 7 |
| G3 Internación general | 25 / 5 | 0,9 / 0,7 | 22 °C; 30 % | 1,0 | 900 | 7 |
| G4 Guardia, imágenes y laboratorio | 35 / 8 | 0,9 / 0,5 | 22 °C; 30 % | 1,0 | 1.000 | 7 |
| G5 Consultorios, administración y docencia | 25 / 6 | 0,9 / 0,0 | 22 °C; 30 % | 1,0 | 900 | 5 |

Table: Tabla M9. Parámetros de las zonas (todos supuestos; las renovaciones están en el informe). La actividad es la fracción de la ganancia interna de plena actividad que hay de día y de noche.

| Mes | ene | feb | mar | abr | may | jun |
|------------------------|------------|------------|------------|------------|------------|------------|
| Días | 31 | 28 | 31 | 30 | 31 | 30 |
| T media [°C] | 24,9 | 23,7 | 22,0 | 18,3 | 14,6 | 11,6 |
| HR media [%] | 66 | 70 | 73 | 75 | 78 | 79 |
| **Mes** | **jul** | **ago** | **sep** | **oct** | **nov** | **dic** |
| Días | 31 | 31 | 30 | 31 | 30 | 31 |
| T media [°C] | 10,9 | 12,3 | 14,2 | 17,6 | 20,6 | 23,4 |
| HR media [%] | 77 | 73 | 71 | 70 | 67 | 65 |

Table: Tabla M10. Clima mensual aproximado, en dos semestres (supuesto de conocimiento general, a reemplazar con datos del SMN).
