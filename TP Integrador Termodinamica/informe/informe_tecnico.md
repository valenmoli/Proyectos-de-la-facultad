---
title: "Diseño de un sistema energético eficiente para un hospital del AMBA"
subtitle: "TP Integrador de Termodinámica 2026 · Informe técnico · Borrador v0.3"
author: "[Integrantes del equipo: a completar]"
date: "Facultad de Ingeniería y Ciencias Agrarias · Ingeniería Civil · UCA · Noviembre de 2026"
lang: es-AR
---

::: {custom-style="Nota"}
**Cómo leer este borrador.** Explica **qué decidimos, por qué y en qué nos apoyamos**; las ecuaciones y los estados completos están en la memoria de cálculo. Cada dato lleva su nivel de respaldo: **visto** (documento recibido y leído), **cita** (fuente secundaria vista en una búsqueda; falta cotejarla con la original), **propio** (cálculo o criterio nuestro, con su lógica) o **recordado** (de memoria, sin fuente a mano).
:::

# Resumen

Se diseña y evalúa el sistema térmico de un hospital de alta complejidad del AMBA con el tamaño y el programa del Hospital Favaloro (La Matanza: 18.352 m², 158 camas, 6 quirófanos). Es un sistema de aire con enfriadora y caldera de gas, porque quirófanos y áreas críticas exigen aire filtrado, muchas renovaciones y humedad controlada. Para cada dato de partida se explica cómo se obtuvo y en qué se apoya.

El sistema consume **3.021 MWh de energía final por año (165 kWh/m²)**. El hallazgo central es que el aire se enfría para quitarle humedad y se recalienta con gas, mientras la enfriadora tira al ambiente 4.198 MWh de calor por año. Aprovecharlo (alternativa B) baja la energía 18,0 % y las emisiones 9,6 %; el paquete de mejoras de sustentabilidad, 48,1 % y 39,2 %. El análisis exergético muestra que en el verano pico se destruye el 85,6 % de la exergía que entra (la enfriadora y su entorno, el 42,4 %) y que en el momento de máximo recalentamiento la caldera destruye el 57,1 % de lo destruido, con una eficiencia exergética de 12,9 %: se usa una llama de 1.848 °C para subir el aire unos kelvin. Los equipos se eligen con redundancia y se ubican pensando en lo civil (azotea, shafts, ruido, izaje). Lo que no tiene fuente citable está marcado y la sensibilidad muestra cuánto pesa.

# 1. Introducción y objetivos

Un hospital funciona todo el año y todo el día, y su climatización es de **proceso**, no de confort: exige temperatura y humedad controladas, presión positiva y aire exterior filtrado. En el AMBA eso tiene una consecuencia termodinámica concreta: el aire exterior de verano (unos 34 °C con 16,3 g de vapor por kg de aire seco) hay que enfriarlo por debajo de su punto de rocío para quitarle vapor, y a esa temperatura ya no se puede impulsar: hay que **recalentarlo**. Se gasta frío para deshumidificar y combustible para devolver temperatura.

**Objetivo:** definir, modelar y evaluar con la Primera y la Segunda Ley el sistema térmico de un hospital del AMBA y proponer alternativas y mejoras que reduzcan su consumo y su impacto ambiental. Específicamente: respaldar cada dato de partida, elegir y ubicar los equipos, calcular cargas, enfriadora, caldera y consumo anual, calcular dónde se destruye exergía, comparar alternativas y responder con números las cinco preguntas de la consigna.

# 2. El edificio y cómo obtuvimos cada dato

Elegimos un hospital porque es el caso donde refrigeración, combustión, aire húmedo y exergía se necesitan a la vez sobre un mismo sistema, y el **Hospital Dr. René Favaloro (SAMIC)** frente a Nordelta porque es el que trae el dato que dimensiona el modelo: la superficie cubierta. Ningún documento trae datos de climatización ni de consumo del edificio real: el modelo replica su **tamaño y programa**, no sus instalaciones.

| Dato | Valor | Cómo lo obtuvimos | Respaldo |
|----------------|-----------------|-------------------------------------------------|------------------|
| Superficie cubierta | 18.352 m² | Cifra oficial de Presidencia; el intendente habló de «más de 20.000 m²» sin aclarar si es cubierta | Visto [F1, F2] |
| Camas | 144 + 14 = 158 | La gacetilla las atribuye a cuidados progresivos; las tomamos como el total (Presidencia prevé 160 de internación) | Visto [F2, F1]; interpretación nuestra |
| Quirófanos | 6 | Cifra de programa | Visto [F1] |
| Niveles | 3 de 6.117 m² | Presidencia lista tres pisos (1.º guardia, consultorios y diagnóstico; 2.º internación, quirófanos y áreas críticas; 3.º administración y docencia); suponemos tres iguales | Visto [F1] y propio |
| Superficie climatizada | 85 % (15.599 m²) | Casi todo; se excluyen locales técnicos, morgue y depósitos | Propio |
| Quirófano | 42 m² | FGI: al menos 400 ft² (37,2 m²) libres con 6,1 m de lado; sumamos equipamiento fijo (unos 6,5 × 6,5 m) | Cita (FGI) y propio |
| Terapia intensiva | 24 m² por cama | Res. 748/2014: al menos 9 m² por cama de paciente; × 2,7 por apoyo y circulación | Cita (Res. 748/2014) y propio |
| Internación general | 28 m² por cama | Estimación nuestra (habitaciones con baño, office, circulaciones); sin referencia: ±6 m² cambian la energía ±1,6 % | Propio |
| Guardia, imágenes y laboratorio | 35 % de las áreas generales, 24 h | Guardia 24 h según la gacetilla, más imágenes y laboratorio; el resto funciona 12 h de lunes a viernes | Visto [F2] y propio |
| Altura libre | 3 m | Convención de diseño | Propio |

Table: Tabla 1. Datos del edificio, cómo los obtuvimos y en qué nos apoyamos.

**Contraste global.** El Favaloro tiene 116 m² cubiertos por cama, contra 148 del artículo de Hospitecnia [H] y 157 del Hospital El Cruce (visto): es más compacto, una señal para vigilar y no un error de magnitud. **Qué pasa si nos equivocamos:** ±6 m² por cama de internación cambian la energía ±1,6 %; por quirófano, ±1,2 %; por cama de terapia, ±0,3 %; climatizar 95 % o 75 % en vez de 85 %, ±8,0 %; y que la guardia y el diagnóstico ocupen 50 % o 20 % de las áreas generales en vez de 35 %, ±12,8 %. Las áreas de cada zona pesan poco; lo que pesa es **cuánta superficie se climatiza y cuántas horas funciona**.

| Zona | Superficie [m²] | Consigna de verano | Caudal de impulsión [m³/h] | Renovaciones resultantes [1/h] | Funcionamiento |
|------------------------------|-----------|---------------|---------------|---------------|--------------|
| G1 Quirófanos | 252 | 22 °C; 55 % | 15.120 | 20,0 | Continuo |
| G2 Terapia intensiva | 336 | 23 °C; 55 % | 6.048 | 6,0 | Continuo |
| G3 Internación | 4.032 | 24 °C; 55 % | 54.711 | 4,5 | Continuo |
| G4 Guardia, imágenes, laboratorio | 3.843 | 24 °C; 60 % | 92.225 | 8,0 | 24 h |
| G5 Consultorios y administración | 7.136 | 24 °C; 60 % | 96.670 | 4,5 | 12 h, lunes a viernes |

Table: Tabla 2. Zonas térmicas, consignas de verano y caudales. El caudal es el mayor entre el de las renovaciones mínimas y el de la carga sensible, por eso G3 y G5 resultan con más renovaciones que el mínimo (sección 3.2).

# 3. Decisiones de diseño y su respaldo

## 3.1 Temperatura y humedad interiores

**Zonas críticas (G1, G2).** ASHRAE 170 pide para quirófano de 20 a 24 °C y de 20 a 60 % de humedad relativa, con presión positiva y filtro MERV-16 (**cita**: extracto de un adendo visto en una búsqueda), y para habitaciones de pacientes de 21 a 24 °C y hasta 60 % (**cita**: tabla de muestra del capítulo de hospitales del Handbook); un cirujano o un procedimiento pueden pedir otros valores. No pudimos abrir la norma. Elegimos 22 °C para el quirófano y 23 °C para la terapia, con humedad de consigna de **55 %**: el máximo de 60 % menos 5 puntos de margen de control (**propio**). Pesa: con 5 puntos menos en todas las zonas la energía sube +22,7 %.

**Zonas de confort (G3, G4, G5).** Usamos 24 °C y 55 a 60 %. Para respaldarlo usamos la **carta bioclimática de Givoni**, una carta psicrométrica con la zona de confort dibujada (figura 1): 18 a 29 °C, 20 a 80 % de humedad y 4 a 17 g/kg (**cita**: valores de Givoni (1992) que da una herramienta de carta bioclimática, vistos en una búsqueda; falta cotejar con el artículo). Nuestras cinco consignas caen **dentro** de la zona.

![Figura 1. Carta psicrométrica con la zona de confort de Givoni, el clima de cada mes, el estado exterior de diseño y las consignas de verano.](../figuras/fig10_carta_givoni.png){width=10.5cm}

La carta también explica el problema: el clima medio de octubre a abril cae dentro de la zona de confort o muy cerca, pero el **estado exterior de diseño de verano** (34 °C y 16 g/kg) queda fuera, y para llevarlo a las consignas hay que enfriarlo y quitarle vapor; en invierno queda a la izquierda y hay que calentarlo.

## 3.2 Renovaciones por hora: de dónde salen y qué significan

Los quirófanos llevan **20 renovaciones totales por hora, de las cuales 4 son de aire exterior** (ASHRAE 170; **cita**: extracto de un adendo y una guía que la resume; la docente lo confirmó). Cumplen funciones distintas: las 20 mueven el aire por filtros de alta eficiencia, diluyen contaminantes y mantienen la sobrepresión; las 4 de aire exterior aseguran el aire fresco mínimo (olores, gases anestésicos, CO₂) (**propio**: es nuestra explicación). La relación 20/4 = **5** significa que el aire exterior es el 20 % del que se mueve y el 80 % restante se recircula filtrado: solo hay que tratar con las condiciones exteriores un quinto del aire.

Un detalle: un adendo reciente de ASHRAE 170 reconoce que las 20 renovaciones no tienen una justificación científica definitiva, aunque tampoco pudo rechazarlas, y recomienda una evaluación de riesgo antes de cambiarlas (**cita**). Por eso las mantenemos como dato normativo y mostramos su peso: pasar a 15 o 25 cambia la energía −2,3 % y +2,4 %; con 6 de aire exterior en vez de 4, +0,6 %.

**Nuestra comprobación.** Con 60 W/m² de ganancia sensible (supuesto propio), el caudal que haría falta solo por carga es 4.927 m³/h, o sea 6,5 renovaciones por hora; la norma pide 20, 3,1 veces más. **En el quirófano manda la norma, no la carga térmica**, y por eso su consumo por m² es alto.

| Zona | Total / aire exterior | De dónde sale | Respaldo |
|---|---|---|---|
| G1 Quirófanos | 20 / 4 | ASHRAE 170 | Cita y la docente |
| G2 Terapia intensiva | 6 / 2 | ASHRAE 170 | Recordado |
| G3 Internación | 4 / 2 | ASHRAE 170, habitación de pacientes | Cita |
| G4 Guardia, imágenes, laboratorio | 8 / 2 | Promedio ponderado: 25 % sala de espera y triage (12), 5 % shock (15), 70 % imágenes y laboratorio (6) = 0,25·12 + 0,05·15 + 0,70·6 ≈ 8 | Propio con valores recordados |
| G5 Consultorios y administración | 3 / 1 | Supuesto nuestro, sin contrastar con la norma | Propio |

Table: Tabla 3. Renovaciones por hora y su respaldo. En internación (G3) y consultorios (G5) el caudal real sale de la carga sensible y da 4,5 renovaciones por hora.

## 3.3 Clima y agua caliente

**Clima.** Usamos medias mensuales de Buenos Aires partidas en mitad diurna y nocturna (amplitud de 9 K). Las contrastamos con el Observatorio Central del SMN, 1991 a 2020, a través de una página que reproduce la tabla (**cita**): enero 24,9 °C, julio 11,0 °C y diciembre 23,6 °C, contra 24,9, 10,9 y 23,4 °C nuestros. La humedad media anual de esa fuente es de unos 68 % contra 72 % nuestros: usamos algo más de humedad y **sobreestimamos** un poco el consumo (cada 4 puntos son unos 3,6 %). El estado de diseño de verano (**34 °C de bulbo seco y 25 °C de bulbo húmedo**) es un valor habitual que **recordamos** y no pudimos cotejar con ASHRAE.

**Agua caliente.** 100 L por cama y día a 60 °C (red a 17 °C). El artículo de Hospitecnia [H] trae casos medidos de 50 a 55 L (**visto**) y ratios de diseño de 200 a 300 (**visto**), de 4 a 6 veces más: elegimos un valor intermedio y mostramos los extremos, 55 L −6,9 % y 200 L +15,3 %.

## 3.4 Por qué elegimos este sistema

| Decisión | Alternativas | Elegimos y por qué | Respaldo |
|----------------|----------------------|----------------------------------------------|----------------|
| Tipo de sistema de aire | Todo aire con recalentamiento; splits o VRF; fancoils con aire exterior aparte | Todo aire de caudal constante: las zonas críticas necesitan filtrado, muchas renovaciones y control de humedad y de presiones, que un split no da. La auditoría de HCWH encontró en hospitales argentinos splits instalados «porque el aire central no alcanzaba» | Propio; [A] visto |
| Producción de frío | Enfriadora por aire o por agua con torre | Por aire: sin torre no hay consumo de agua, tratamiento ni riesgo de legionela; el COP es algo menor | Propio |
| Redundancia | Sin reserva o N+1 | N+1 (2+1 enfriadoras, 2 calderas al 100 %): un hospital no puede parar la climatización de quirófanos y terapia | Propio |
| Combustible y base | Gas, electricidad o gasoil; caldera o recuperación de calor | Gas natural (hay red en el AMBA y es el combustible dominante en el artículo [H]); caldera como base (A) y recuperación como alternativa B para medir cuánto se gana | Propio; [H] visto |

Table: Tabla 4. Decisiones de diseño del sistema, alternativas consideradas y motivos.

# 4. Equipos y ubicación

**Qué elegimos.**

| Equipo | Qué elegimos | Por qué | Respaldo |
|-------------|--------------------------------------|---------------------------------|----------------|
| Enfriadoras | 3 unidades iguales de tornillo condensadas por aire (2 en servicio y 1 de reserva). Ejemplo: Carrier AquaForce 30XA 1002, R-134a, 988 kW nominales | Cada unidad en servicio debe dar al menos 993,6 kW (la mitad de 1.987 kW); la reserva mantiene el servicio si una falla | Cita (catálogo, búsqueda web) y propio |
| Calderas | 2 calderas de agua caliente a gas de 734 kW cada una (100 % cada una). Ejemplo de condensación: 4 Viessmann Vitocrossal 300 CM3C de 311 kW | Carga de diseño 734 kW = 649 kW de invierno + 86 kW de punta de ACS (el doble de la media, supuesto) | Cita (catálogo) y propio |
| Unidades de tratamiento de aire | 18 unidades: una por quirófano (6 × 2.520 m³/h, con filtro HEPA), una para terapia intensiva (6.048 m³/h) y 11 en cubierta para las demás zonas (hasta 25.000 m³/h cada una) | Las críticas junto a su zona (continuidad, presiones y recorridos cortos); las demás en cubierta, cerca de las enfriadoras | Propio |
| Cañería de agua helada | Principal DN 250 (342 m³/h a 1,93 m/s) y ramal por enfriadora DN 200 | Caudal de la carga con salto de 5 K y velocidad de diseño de 2 m/s | Propio |
| Shafts de aire | 14 shafts de unos 2 m² (21,5 m² verticales en total), apilados en un núcleo técnico | Áreas con 6 m/s en impulsión y 5 m/s en retorno | Propio |

Table: Tabla 5. Equipos elegidos. Los datos de catálogo son **citas de búsquedas web** (no pudimos abrir los catálogos): hay que cotejarlos con el fabricante.

**La enfriadora de ejemplo casi cumple.** La Carrier 30XA 1002 da 988 kW nominales con 288,2 kW de compresores a 35 °C de aire y agua 12/7 °C (la familia va de 267 a 1.682 kW). Dos unidades dan 1.976 kW: **faltan 11,2 kW (0,6 %)**. Es poco, pero no cumple, y no lo tapamos: el catálogo es a 35 °C y nuestro diseño a 34 °C, y la carga de 1.987 kW no incluye el calor de las bombas (hasta 39,6 kW; con él faltarían 50,8 kW, 2,6 %). Lo razonable es **pasar al tamaño siguiente (30XA 1102) y verificar en el catálogo que dé al menos 993,6 kW**; no damos su capacidad porque no está verificada. **Calderas:** la carga de diseño incluye 92 kW de vapor de humidificación, que una caldera de agua caliente **no produce** (hacen falta humidificadores o un generador de vapor); la dejamos completa, del lado seguro. Con la caldera de condensación de ejemplo hacen falta 3 unidades en servicio más 1 de reserva: con una parada quedan 933 kW, suficiente; con 3 en total no alcanza.

## 4.2 Dónde ponerlos

Como ingenieros civiles, la ubicación depende del aire, el ruido, la estructura, el izaje, las cañerías y el mantenimiento. Armamos un esquema con tres niveles iguales de 6.117 m² brutos (5.200 climatizados y 918 de locales técnicos, morgue y depósitos) y ubicamos las zonas según la presentación del hospital (figura 2).

![Figura 2. Corte esquemático con zonas, superficies y equipos, y planta de cubierta con las enfriadoras. Las zonas siguen la presentación del hospital; la distribución en niveles y la planta de cubierta son supuestos nuestros, sin planos.](../figuras/fig08_plano_zonas.png){width=14.5cm}

- **Enfriadoras en la azotea**, junto al núcleo técnico: necesitan aire libre (en un patio rodeado por el edificio recirculan el aire caliente) y el ruido queda por encima del 3.er piso, separado de la internación por una losa. Ocupan 147 m², el 2,4 % de la cubierta de 6.117 m².
- **Carga estructural.** Con un peso supuesto de 12 t por unidad, la carga media sobre su huella es de 2,40 kN/m², 1,20 veces la sobrecarga de referencia de una azotea corriente (2,0 kN/m², **recordada** del CIRSOC 101). La carga bajo los apoyos es mayor: hace falta plataforma o vigas y la verificación del calculista; el peso hay que cambiarlo por el del catálogo.
- **UTAs y shafts.** Las 7 críticas (quirófanos y terapia) van en el cuarto técnico del 2.º piso, junto a su zona; las 11 restantes, en cubierta. Los 264.774 m³/h de impulsión necesitan 21,5 m² de shafts verticales: 14 de unos 2 m² en un núcleo técnico que se apila en los tres niveles.
- **Calderas en un anexo a nivel de calle**: acceso, medidor y regulador de gas, ventilación y chimenea (DN 300) por fuera del edificio. **Izaje:** unidades de 14 m y 12 t a unos 15 m de altura exigen grúa móvil grande y corte de calle; es el costo de la azotea.

**La decisión no es robusta.** Puntuamos azotea y patio a nivel con seis criterios: gana la azotea (3,25 contra 3,05), pero con pesos iguales empatan y si estructura e izaje valen el doble gana el patio (3,38 contra 2,96). Elegimos la azotea por el aire libre y los recorridos cortos hacia las 11 UTAs de cubierta; si el calculista descarta la losa, el patio es la alternativa. Las reservas para solar térmico (300 m²) y fotovoltaica (unos 1.250 m²) caben, pero **no dimensionamos las UTAs ni la sala de calderas**.


# 5. Cálculo y resultados

## 5.1 El método y un caso paso a paso

Cada zona es un sistema de aire de caudal constante. Para cada estado exterior se sigue el aire por la mezcla, la serpentina que enfría y quita vapor, el recalentador y el ventilador (que además lo calienta); de ahí salen la carga frigorífica (sensible y latente) y el calor de recalentamiento. La carga de las serpentinas es la que vence la enfriadora (ciclo de R134a: trabajo, COP, calor rechazado) y el calor de recalentamiento, calefacción y agua caliente se convierte en gas con el rendimiento de la caldera (balance de la reacción y de los gases). Cada mes se parte en una mitad diurna y otra nocturna y se repite el cálculo. **Las ecuaciones y los estados completos están en la memoria.**

**El quirófano en verano pico.** Con el exterior a 34 °C y 25 °C de bulbo húmedo, el aire exterior (A) se mezcla con el de retorno (B) y queda a 24,4 °C (C); la serpentina lo enfría hasta 13,0 °C y le quita vapor (D); el recalentador lo sube a 16,6 °C (E) y el ventilador, que le agrega 2,4 K, lo deja a 19,1 °C (F). La serpentina entrega 79,5 kW (58,8 sensibles y 20,7 latentes) y el recalentador, 18,7 kW. En el punto de diseño todo el edificio recalienta solo 19 kW: **el recalentamiento aparece a carga parcial, y dimensionar su recuperación con el pico subestimaría el potencial**.

![Figura 3. Proceso del aire en el quirófano, verano pico.](../figuras/fig02_psicrometrica_quirofano.png){width=10cm}

## 5.2 Enfriadora y caldera

La capacidad frigorífica de diseño es **1.987 kW** (108 W/m²). El R134a evapora a 3 °C y condensa a 46 °C porque el condensador es enfriado por aire a 34 °C. El COP eléctrico es **3,56**, el 55 % del de Carnot (6,42), y el compresor consume 559 kW. El catálogo de la enfriadora del ejemplo da un COP de 3,43 contando solo los compresores a 35 °C: del mismo orden. Con gas natural y 15 % de exceso de aire, el poder calorífico superior es de 9.196 kcal/m³ y el inferior de 9,656 kWh/m³; los gases salen a 190 °C, por encima de su rocío (56,1 °C), la pérdida es 8,0 % del PCI y la caldera rinde **90,0 % sobre PCI**, igual al 90 % del artículo de Hospitecnia [H] (visto). Cada kWh de gas emite 0,202 kg de CO₂, de la propia reacción.

![Figura 4. Ciclo de compresión de R134a al punto de diseño de verano.](../figuras/fig03_diagrama_ph_r134a.png){width=9cm}

## 5.3 Consumo anual

La energía final es **3.021 MWh por año**: 1.736 de electricidad y 1.285 de gas (por su PCS, unos 120.000 m³), **165 kWh/m²**; suma kWh a kWh, sin ponderar por energía primaria. Las emisiones son 895 t de CO₂ por año (235 del gas y 660 de la electricidad). El factor de la electricidad (0,38 t/MWh, meta de CAMMESA 2023) es el más incierto: otras fuentes dan 0,29 y 0,40, con lo que el paquete de mejoras reduce las emisiones 42,2 % y 38,6 %.

![Figura 5. Consumo anual por uso final.](../figuras/fig04_consumo_por_uso.png){width=11cm}

**Primero**, con los supuestos actuales los ventiladores consumen más que el compresor (28,0 % contra 23,6 %), por ser un sistema todo aire con muchas renovaciones; el orden depende de la presión y el rendimiento supuestos (con 20 % menos de presión el compresor pasa adelante, pero el gas de recalentamiento sube porque el ventilador ya no calienta el aire, y el ahorro neto es de solo 2,5 %). **Segundo**, el recalentamiento es casi la mitad del calor útil de la caldera (511 de 1.044 MWh): el calor del aire es mayor en verano que en invierno (129 MWh en enero contra 46 en julio). **Tercero**, el COP estacional de la planta (3,96) coincide con el COP 4 que supone Hospitecnia [H]; es coincidencia de resultado, no un ajuste.

**Qué tan seguro es el número.** Variando un supuesto por vez, la intensidad queda entre 141 y 202 kWh/m² y año; **eso no es un intervalo de confianza**. Un revisor externo estimó la incertidumbre global en ±15 a 20 % (su estimación, no un cálculo de este modelo). Lo que más mueve el resultado:

| Variación de un supuesto | Energía final [MWh/año] | Diferencia |
|--------------------------------------------------------------|------------------|------------|
| Humedad de consigna de verano 5 puntos menor en todas las zonas | 3.706 | +22,7 % |
| Consultorios y administración funcionan también las 24 h | 3.644 | +20,6 % |
| Sin calor del ventilador en el aire | 3.574 | +18,3 % |
| ACS de 200 L por cama y día (en vez de 100) | 3.483 | +15,3 % |
| Temperatura media mensual +2 K | 3.463 | +14,6 % |
| Cambio de estación (consignas de invierno) bajo 21 °C en vez de 18 °C | 2.589 | −14,3 % |

Table: Tabla 6. Supuestos que más mueven la energía final (caso base: 3.021 MWh). Ganancias internas y envolvente (±30 %) mueven menos de 3 %.

# 6. Exergía: dónde se pierde la capacidad de hacer trabajo

**Qué calculamos y con qué criterio.** Para cada equipo planteamos exergía que entra (F), exergía útil que entrega (P), pérdida al ambiente (L) y exergía destruida (D), con F = P + L + D, en kW. Tomamos como **estado muerto el aire exterior** de cada caso (lo que el ambiente da gratis) y analizamos dos casos con la misma función: el **verano pico** (exterior a 34,0 °C, el que dimensiona la enfriadora) y el **momento del año con más recalentamiento** (diciembre, de noche, exterior a 18,9 °C, con 272 kW de recalentamiento). Entre los dos se ven las dos mitades del sistema. La exergía química del gas es 1,037 veces su PCI, con exergías químicas estándar que **recordamos** y hay que cotejar con el libro de la cátedra. La figura 6 muestra el reparto con sus cifras; el balance por equipo está en la memoria.

![Figura 6. Reparto de la exergía que entra a cada caso entre exergía útil, pérdidas al ambiente y destrucción por grupo de equipos (kW y % de la entrada).](../figuras/fig07_exergia.png){width=12.5cm}

1. **Casi toda la exergía se destruye**: 85,6 % en el verano pico y 95,4 % en el recalentamiento. En climatización es lo esperable: el sistema trabaja con calor y frío a temperaturas cercanas a la del ambiente, que valen poco en exergía.
2. **En el verano pico manda la enfriadora y su entorno.** El compresor con su motor (19,8 %), el condensador, la válvula y el evaporador (22,6 %) destruyen el 42,4 % de lo que entra, y los ventiladores y bombas con sus pérdidas de carga otro 27,3 %. La eficiencia exergética de la enfriadora es de **30,8 %** contando el compresor (26,1 % con ventiladores del condensador y bombas) aunque su COP de 3,56 sea alto: el frío de agua a 9,5 °C con exterior a 34,0 °C vale solo el 8,7 % de su energía en exergía.
3. **En el recalentamiento manda la caldera.** Destruye el 57,1 % de lo destruido y su eficiencia exergética es de **12,9 %**: el 30,2 % del combustible se destruye en la combustión (llama a 1.848 °C) y el 52,5 % al pasar el calor al agua a 80/60 °C. **Se usa una llama de 1.848 °C para subir el aire unos kelvin.** El calor de 32 a 50 °C que la enfriadora rechaza vale poco en exergía, igual que el que pide el recalentamiento: por eso la alternativa B es buena también desde la Segunda Ley.
4. **Hay que leer las eficiencias con cuidado.** La global del verano pico es de 7,4 %, pero en el recalentamiento no se puede definir: el aire sale casi con la misma exergía con que entra. Si se cambia el estado muerto, la destrucción total varía menos de 4,4 % y el equipo que más destruye no cambia, pero los rangos de eficiencia sí.


# 7. Alternativas y mejoras de sustentabilidad

**Alternativa A** (base): enfriadora, caldera de gas y recalentamiento. **Alternativa B:** el recalentamiento y la calefacción del aire se cubren con el **calor del condensador**, que hoy se tira, en lugar de quemar gas. Sale directo del hallazgo central: el calor existe (4.198 MWh por año, unas 8,2 veces el de recalentamiento) y alcanza con agua tibia a 45 °C. **Es honesta:** entregar agua a 45 °C exige condensar a 50 °C, más caliente que los 32 a 41 °C de un condensador por aire, y eso **cuesta trabajo del compresor**. En cada estado del año se elige el mejor entre no recuperar, recuperar solo el sobrecalentamiento de la descarga o poner a condensar el recuperador. B recupera 499 MWh de calor, ahorra 615 MWh de gas y gasta 81 MWh más de electricidad: **la energía baja 18,0 % y las emisiones 9,6 %**. Como el modelo usa estados medios, supone que calor y demanda coinciden dentro de cada estado; si coinciden 75 % o 50 % del tiempo, el ahorro baja a 13,5 % y 8,5 %: es el límite superior realista.

La docente pidió énfasis en mejoras que consuman menos y sean más verdes. Las evaluamos con el mismo modelo, una por vez:

| Medida | Por qué ahorra | Energía final | CO₂ |
|--------------------|------------------------------------------------|----------------|----------------|
| Alternativa B: recuperar el calor del condensador | Aprovecha el calor que se rechaza a 32 a 41 °C (hasta 50 °C cuando recupera) en vez de quemar gas en una llama de 1.848 °C; cuesta trabajo extra del compresor | −18,0 % (544 MWh) | −9,6 % (86 t) |
| M5. Fotovoltaica de 250 kWp | Produce 340 MWh por año (1.360 kWh por kWp) que descuentan electricidad de la red; no depende del resto del sistema | −11,3 % (340 MWh) | −14,4 % (129 t) |
| M2. Solar térmico para el ACS | 300 m² de colectores cubren el 54 % del calor del ACS, una demanda constante de 43 kW medios que el sol atiende bien | −8,3 % (251 MWh) | −5,1 % (46 t) |
| M3. Recuperador del aire de extracción | Precalienta o preenfría el aire exterior con el que sale, sin mezclar las corrientes (circuito de agua, efectividad 0,50); solo trabaja cuando conviene (bypass) | −5,1 % (154 MWh) | −2,5 % (23 t) |
| M1. Caldera de condensación | Los gases salen a 45 °C, por debajo del rocío (56,1 °C): condensa el 47 % del agua formada y recupera su calor latente; el rendimiento sobre PCS pasa de 81,2 a 91,8 % | −3,1 % (94 MWh) | −1,9 % (17 t) |
| M4. Ventiladores con 20 % menos de presión | La potencia del ventilador es proporcional a la presión; pero el calor que ya no cede al aire hay que reponerlo con gas, por eso el ahorro neto es chico | −2,5 % (77 MWh) | −5,8 % (51 t) |
| Paquete B + M1 a M5 | Combinación de todas; no es la suma, porque las medidas se pisan | −48,1 % (1.453 MWh) | −39,2 % (350 t) |

Table: Tabla 7. Mejoras respecto de A (3.021 MWh y 895 t de CO₂ por año).

![Figura 7. Reducción de energía y de emisiones de cada mejora y del paquete.](../figuras/fig09_mejoras.png){width=11cm}

**Cómo leer la tabla.** Las medidas **no se suman**: dependen unas de otras (con B, la caldera de condensación tiene menos calor para entregar). El paquete da 48,1 % menos de energía y 39,2 % menos de emisiones. Las que ahorran gas bajan la energía más que las emisiones, porque el gas emite 0,183 t/MWh y la red 0,38 (cita secundaria); las que ahorran electricidad (fotovoltaica, ventiladores) bajan más las emisiones. **Lo que no conviene priorizar:** aislar la envolvente un 30 % baja solo 2,5 % y reducir las ganancias internas un 30 % (por ejemplo LED), 0,7 %: el consumo está en el aire, no en la envolvente.

**Refrigerante.** El R134a tiene un PCA de 1.430 (**cita**) y la Enmienda de Kigali obliga a reducir los HFC: Argentina depositó su ratificación el 22/11/2019 (en vigor desde el 20/2/2020) y la Resolución 104/2020 puso los HFC bajo licencia de importación (**cita**). Con el modelo de ciclo, el R1234ze(E) (PCA menor que 1, **cita**) da el mismo COP (3,55 contra 3,56) pero 26 % menos capacidad volumétrica, o sea un compresor 35 % más grande, y es ligeramente inflamable (A2L, **recordado**), lo que pesa en un hospital. El R513A (PCA 631, **cita**) no está en la biblioteca que usamos.

**Prioridad propuesta:** (1) **B**, la de mayor ahorro y la única que ataca la ineficiencia central; (2) **fotovoltaica**, por emisiones; (3) **solar térmico** para el ACS; (4) **recuperador del aire de extracción**; (5) **caldera de condensación** y (6) **ventiladores**. Sin costos no se puede ordenar por retorno; la consigna no pide presupuesto.

# 8. Conclusiones

1. **¿La alternativa seleccionada satisface los requerimientos?** Entrega las condiciones de consigna de las cinco zonas por construcción del modelo, con 1.987 kW de frío, 557 kW de calefacción del aire (92 kW más de humidificación) y 43 kW medios de ACS; una enfriadora real casi la cubre con redundancia. Lo que **no** satisface bien es la eficiencia: consume 3.021 MWh y tira 4.198 MWh de calor; B cumple lo mismo con 18,0 % menos de energía.
2. **¿Cuáles son las principales variables que condicionan su desempeño?** La humedad de consigna (5 puntos menos, +22,7 %), los horarios (consultorios 24 h, +20,6 %), el ACS por cama (200 L, +15,3 %) y la temperatura media (±2 K, +14,6 % y −13,7 %). Los parámetros de los equipos mueven menos de 3 % cada uno; el COP depende sobre todo de la temperatura de condensación (3,56 al diseño, 4,94 en el año).
3. **¿Qué procesos presentan mayores pérdidas de energía o destrucción de exergía?** **En energía:** los ventiladores (28,0 % de la energía final), el compresor (23,6 %) y el gas del recalentamiento (20,8 %) son los mayores consumos (el orden de los dos primeros depende de la presión y el rendimiento supuestos de los ventiladores); las pérdidas propiamente dichas son el calor que el condensador rechaza al ambiente (4.198 MWh por año, unas 8,2 veces el calor de recalentamiento), los gases de escape de la caldera (8,0 % del PCI) y la irreversibilidad del compresor. **En exergía:** en el verano pico se destruye el 85,6 % de lo que entra, sobre todo en la enfriadora y su entorno (42,4 %) y en ventiladores y bombas (27,3 %); en el máximo recalentamiento la caldera destruye el 57,1 % del total destruido (eficiencia exergética de 12,9 %), porque calienta aire unos kelvin con una llama de 1.848 °C.
4. **¿Qué modificaciones permitirían mejorar el aprovechamiento de los recursos?** Recuperar el calor del condensador (B: 18,0 % de energía y 9,6 % de CO₂), fotovoltaica (11,3 %), solar térmico (8,3 %), recuperador del aire de extracción (5,1 %), caldera de condensación (3,1 %) y ventiladores de menor presión (2,5 %); el paquete, 48,1 % menos de energía y 39,2 % menos de emisiones. No conviene priorizar la envolvente ni la iluminación.
5. **¿Qué limitaciones presenta el análisis y qué información haría falta?** El resultado se mueve entre 141 y 202 kWh/m² con un supuesto por vez. Faltan datos citables de clima (SMN) y de la norma (ASHRAE 170), que no pudimos abrir; las instalaciones y consumos del hospital real; las curvas de carga parcial y los catálogos completos; los efectos omitidos (economizador, ventiladores de retorno y extracción, caldera a carga parcial, humidificación de invierno); y la coincidencia en el tiempo entre calor disponible y demanda de B. No hay análisis de costos.

# Anexo A. Referencias y su nivel de verificación

| Referencia | Qué se usó | Nivel |
|---|---|---|
| [F1] Presidencia de la Nación, presentación del Hospital SAMIC «Dr. René Favaloro»; [F2] Gobierno de la Provincia de Buenos Aires, gacetilla del 28/07/2020 | Superficie, quirófanos, niveles, camas, guardia 24 h | Visto |
| [H] Gallostra Isern, Sánchez-Vaqué y Túnica Buira, *Caracterización de consumos energéticos y suministros en hospitales*, Hospitecnia, 2022; [A] HCWH y K-CEP, *Energy efficiency and cooling audits in health care facilities in Argentina, China, and the Philippines*, 2021; El Cruce (Medina y Marini, 2010) | ACS, m²/cama, COP y rendimiento de referencia; consumos y hallazgos de tres hospitales argentinos | Visto |
| ASHRAE 170 (adendo de 2025) y Handbook, capítulo de hospitales; FGI Guidelines (quirófano de 400 ft²); Resolución 748/2014 (terapia, 9 m² por cama); Givoni (1992) según Lamberts, Dutra y Pereira | Renovaciones, temperaturas, humedades, superficies, zona de confort | Cita (extractos de búsquedas); no se pudieron abrir |
| SMN, normales 1991-2020 (vía una página que reproduce la tabla); Global Solar Atlas; CAMMESA (meta 2023), Climate Transparency vía Carbon Footprint y Ember | Clima, irradiación, factor de emisión de la electricidad (de 0,29 a 0,40 t/MWh) | Cita (búsquedas) |
| Carrier (enfriadora AquaForce 30XA), Viessmann (Vitocrossal 300 CM3C), Trane y *Consulting-Specifying Engineer* (recuperación de calor del condensador en hospitales), Kigali y Resolución 104/2020 | Equipos de ejemplo, antecedentes de la alternativa B, estado de los HFC | Cita (búsquedas) |
| CoolProp y psychrolib | Propiedades del refrigerante, los gases y el aire húmedo | Visto (código) |

Table: Tabla A1. Fuentes y nivel de verificación. **Las páginas de ASHRAE, SMN, NOAA y otras no se pudieron abrir desde el entorno de trabajo**; todo lo marcado «cita» hay que cotejarlo con la fuente original antes de la entrega.

# Anexo B. Verificación del cálculo

**125 chequeos** (`python -m pytest calculo/tests`): primera ley, segunda ley (COP menor que el de Carnot, destrucción de exergía no negativa, cierre del balance exergético), balance de átomos de la combustión, psicrometría contra CoolProp, reproducción de la tabla de supuestos y que las mejoras den el caso base cuando no se activan. Comprueban la coherencia interna, no que la física sea correcta. El núcleo del modelo se reimplementó de forma independiente (coincidencia dentro de 0,24 %); las mejoras, la exergía y los equipos se revisaron con revisores independientes pero **no** se reimplementaron. Sigue **sin verificar** lo propio y lo recordado.
