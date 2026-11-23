---
title: "Diseño de un sistema energético eficiente para un hospital del AMBA"
subtitle: "TP Integrador de Termodinámica 2026 · Informe técnico"
author: "[Integrantes del equipo: a completar]"
date: "Facultad de Ingeniería y Ciencias Agrarias · Ingeniería Civil · UCA · Noviembre de 2026"
lang: es-AR
---

# Resumen

Se diseña y evalúa el sistema térmico de un hospital de alta complejidad del AMBA, con el tamaño y el programa del Hospital Favaloro ({{A_cub}} m², {{camas_tot}} camas, {{n_or}} quirófanos): un sistema de aire con enfriadora y caldera de gas. Consume **{{E_total_MWh}} MWh de energía final por año ({{i_cub}} kWh/m²)**. El hallazgo central es que el aire se enfría para quitarle humedad y se recalienta con gas, mientras el condensador de la enfriadora tira {{Q_cond_MWh}} MWh de calor por año. Aprovechar ese calor (alternativa B) baja la energía {{dE_B}} % y las emisiones {{dC_B}} %; sumando las demás mejoras, {{dE_P}} % y {{dC_P}} %. <<RESUMEN_EXERGIA>>

# 1. Introducción y objetivos

Un hospital funciona todo el año y todo el día, y su climatización es de **proceso**, no de confort: exige temperatura y humedad controladas, presión positiva y aire exterior filtrado. En el AMBA eso tiene una consecuencia termodinámica concreta: el aire exterior de verano (unos {{T_ext_ver}} °C con {{W_ext_ver}} g de vapor por kg de aire seco) hay que enfriarlo por debajo de su punto de rocío para quitarle vapor, y a esa temperatura ya no se puede impulsar: hay que **recalentarlo**. Se gasta frío para deshumidificar y combustible para devolver temperatura.

**Objetivo:** modelar y evaluar con la Primera y la Segunda Ley el sistema térmico de un hospital del AMBA, elegir y ubicar sus equipos, comparar alternativas y proponer mejoras que reduzcan su consumo y su impacto ambiental. Los cuatro temas de la cátedra se usan como una cadena, no por separado:

{{tabla_temas_inf}}

Table: Tabla 1. Los cuatro temas y cómo se conectan en este sistema.

El **hilo conductor**: el aire húmedo fija cuánto frío y cuánto recalentamiento hacen falta; la enfriadora paga ese frío con electricidad y tira calor; la caldera paga el recalentamiento con gas; la exergía muestra que el calor que se tira es justo el que haría falta para recalentar, y de ahí sale la alternativa B. En el texto, [n] remite a la lista de referencias, el asterisco indica una fuente que solo conocemos por un extracto (hay que cotejarla con el original) y «supuesto» marca una decisión nuestra, con su motivo.

# 2. El edificio y sus datos

Elegimos el **Hospital Dr. René Favaloro (SAMIC, La Matanza)** porque es el hospital del AMBA que trae el dato que dimensiona el modelo, la superficie cubierta {{R_presidencia}}. Ningún documento trae datos de climatización ni de consumo del edificio real: replicamos su **tamaño y programa**, no sus instalaciones. Cada dato y su origen:

{{tabla_datos_inf}}

Table: Tabla 2. Datos del edificio y cómo los obtuvimos.

El Favaloro tiene {{gross_per_bed}} m² cubiertos por cama, contra {{ref_bed_hospitecnia}} del artículo de Hospitecnia {{R_hospitecnia}} (hospitales españoles) y {{ref_bed_cruce}} de El Cruce {{R_elcruce}}: es algo más compacto, una señal para vigilar y no un error de magnitud. Dividimos el edificio en cinco zonas térmicas según su uso:

{{tabla_zonas_inf}}

Table: Tabla 3. Zonas térmicas: superficie, consigna de verano, renovaciones por hora y su origen. En G3 y G5 el caudal real sale de la carga sensible y es mayor que el mínimo.

Las áreas de cada zona pesan poco (±6 m² por cama de internación cambian la energía ±{{sens_a_gen}} %); lo que pesa es cuánta superficie se climatiza y cuántas horas funciona (memoria de cálculo).

# 3. Descripción del sistema y condiciones de diseño

## 3.1 El sistema y por qué lo elegimos

![Figura 1. Esquema del sistema: cadena de aire (A a F son los estados del aire de la figura 3), enfriadora, caldera, agua caliente sanitaria (ACS) y, en verde, la alternativa B.](../figuras/fig01_esquema_sistema.png){width=11.5cm}

Cada zona tiene una unidad de tratamiento de aire de caudal constante: el aire exterior (A) se mezcla con el de retorno (C), la serpentina de agua helada lo enfría y le quita vapor (D), el recalentador lo lleva a la temperatura de impulsión (E) y el ventilador lo impulsa a la zona (F). El agua helada la produce una **enfriadora de R134a** con condensador por aire ($\dot Q_L$ de frío, $\dot W_{comp}$ eléctrico, $\dot Q_{cond}$ rechazado al ambiente). Una **caldera de gas natural** da el recalentamiento, la calefacción de invierno y el ACS. La alternativa B manda el calor del condensador, a 45 °C, al recalentador en lugar de la caldera.

- **Todo aire de caudal constante**, porque quirófanos y terapia necesitan filtrado, muchas renovaciones y control de humedad y de presiones, que un split no da; la auditoría de HCWH {{R_hcwh}} encontró en hospitales argentinos splits instalados «porque el aire central no alcanzaba».
- **Enfriadora condensada por aire**: sin torre no hay consumo de agua, tratamiento ni riesgo de legionela; el COP es algo menor.
- **Con reserva**: 3+1 enfriadoras y 2 calderas al 100 %, porque un hospital no puede parar la climatización de quirófanos y terapia.
- **Gas natural**: hay red en el AMBA y es el combustible dominante en {{R_hospitecnia}}; la caldera es la base (A) y la recuperación de calor, la alternativa (B).

Lo que el sistema tiene que dar, con los cálculos de las secciones siguientes:

{{tabla_nec_inf}}

Table: Tabla 4. Necesidades térmicas del edificio: potencia de diseño y energía anual.

## 3.2 Temperatura y humedad: la carta de Givoni

**Quirófano y terapia (G1, G2).** ASHRAE 170 {{R_ashrae170}} pide de 20 a 24 °C y hasta 60 % de humedad relativa en quirófano. Elegimos {{T_G1}} °C para el quirófano y {{T_G2}} °C para la terapia, con humedad de consigna de **55 %**: el máximo de 60 % menos 5 puntos de margen de control (supuesto). **Resto de las zonas (G3, G4, G5).** 24 °C y 55 a 60 %. Para respaldarlo usamos la **carta bioclimática de Givoni** {{R_givoni}}, una carta psicrométrica (eje horizontal: temperatura de bulbo seco; vertical: humedad específica) con la zona donde la mayoría de la gente está cómoda sin equipos: de 18 a 29 °C, de 20 a 80 % de humedad y de 4 a 17 g/kg. Nuestras cinco consignas caen dentro de la zona (figura 2); elegimos 24 °C y no 22 °C por estar en su parte media-alta (menos frío que producir).

![Figura 2. Carta psicrométrica con la zona de confort de Givoni, el clima de cada mes, el estado exterior de diseño y las consignas de verano.](../figuras/fig10_carta_givoni.png){width=9cm}

La carta también muestra el problema: el clima medio de octubre a abril cae dentro de la zona o muy cerca, pero el **estado exterior de diseño de verano** ({{T_ext_ver}} °C y {{W_ext_ver}} g/kg) queda fuera. Para llevarlo a las consignas hay que enfriarlo, quitarle vapor y recalentarlo; en invierno queda a la izquierda y hay que calentarlo.

## 3.3 Renovaciones por hora: de dónde sale el 20/4

Los quirófanos llevan **20 renovaciones totales por hora, de las cuales 4 son de aire exterior** (ASHRAE 170 {{R_ashrae170}}). Cumplen funciones distintas: las 20 mueven el aire por filtros de alta eficiencia, diluyen contaminantes y mantienen la sobrepresión; las 4 de aire exterior aportan el aire fresco mínimo (olores, gases anestésicos, CO₂); esa explicación es nuestra. La relación 20/4 = **5** significa que el aire exterior es el 20 % del que se mueve y el 80 % se recircula filtrado: solo hay que tratar con las condiciones exteriores un quinto del aire.

**Comprobación.** Con {{qs_G1}} W/m² de ganancia sensible (supuesto), por carga térmica bastarían {{ach_load_G1}} renovaciones por hora; la norma pide 20, {{ratio_norm_load}} veces más. **En el quirófano manda la norma, no la carga térmica**, y por eso su consumo por m² es alto. Un adendo de ASHRAE 170 admite que el 20 no tiene una justificación científica definitiva y recomienda evaluar el riesgo antes de cambiarlo {{R_ashrae170}}; lo mantenemos y mostramos su peso: con 15 o 25 renovaciones la energía cambia {{s_ach15}} % y {{s_ach25}} %. Para las demás zonas, la tabla 3 indica el origen de cada valor.

## 3.4 Clima y agua caliente

**Clima.** Medias mensuales de Buenos Aires partidas en mitad diurna y nocturna (amplitud de 9 K), contrastadas con el SMN 1991-2020 {{R_smn}}: enero {{T_ene_smn}} °C y julio {{T_jul_smn}} °C contra {{T_ene}} y {{T_jul}} °C nuestros; la humedad media de esa fuente es {{HR_smn}} % contra {{HR_media}} % nuestros (usamos algo más de humedad, lo que sobreestima un poco el consumo). El estado de diseño de verano, {{T_ext_ver}} °C de bulbo seco y {{Tbh_ver}} °C de bulbo húmedo, es un valor habitual de diseño (supuesto).

**Agua caliente.** {{L_cama}} L por cama y día de {{T_red}} a {{T_acs}} °C, más 30 % por pérdidas de acumulación y recirculación (supuesto): {{acs_kW}} kW medios. Hospitecnia {{R_hospitecnia}} da una guía de 55 L, un caso de 540 camas que sale en unos 51 L y ratios de diseño de 200 a 300 L; elegimos un valor intermedio (con 55 L la energía cambia {{s_acs55}} % y con 200 L, {{s_acs200}} %).

# 4. Metodología e hipótesis

Para cada zona y cada mes (partido en una mitad diurna y una nocturna) se siguen cuatro pasos encadenados, que son los cuatro temas:

1. **Aire húmedo:** balances de masa (vapor) y de energía en la mezcla, la serpentina, el recalentador y el ventilador; dan las cargas sensible y latente.
2. **Refrigeración:** ciclo de compresión de R134a que vence la carga de las serpentinas; da el trabajo, el COP y el calor rechazado.
3. **Combustión:** balance de la reacción del gas natural con exceso de aire; da el rendimiento de la caldera y el consumo de gas.
4. **Exergía:** balance $F = P + L + D$ de cada equipo; da dónde se destruye capacidad de hacer trabajo.

**Hipótesis principales.** Régimen permanente en cada estado; aire y vapor como gases ideales a 101,325 kPa; sistema de caudal constante con serpentina y recalentamiento, sin economizador; el ventilador disipa toda su potencia como calor en el aire; ciclo de compresión de vapor con compresor adiabático de rendimiento isentrópico {{eta_is}}, expansión isoentálpica y evaporación fija a {{T_ev}} °C; combustión completa con {{exceso}} % de exceso de aire, sin disociación, y gases de escape a {{T_gases}} °C.

**Frontera.** Se calcula el sistema térmico y sus auxiliares (ventiladores de las unidades y del condensador, bombas de agua helada). No se incluyen iluminación, equipos médicos, cocina, lavandería ni esterilización: **los {{E_total_MWh}} MWh no son el consumo total del hospital** y no se pueden comparar sin más con el consumo de hospitales completos. Las ecuaciones, los estados y los datos completos están en la memoria de cálculo.

# 5. Cálculos y resultados

## 5.1 Aire húmedo: el quirófano en verano pico

Con el exterior a {{T_ext_ver}} °C y {{Tbh_ver}} °C de bulbo húmedo, el aire exterior (A) se mezcla con el de retorno (B) y queda a {{T_mix_G1}} °C (C); la serpentina lo enfría hasta {{T_c_G1}} °C y le quita vapor (D); el recalentador lo sube a {{T_obj_G1}} °C (E) y el ventilador, que le agrega {{dT_vent_G1}} K, lo deja a {{T_sup_G1}} °C (F). «Quirófano» son aquí los {{n_or}} quirófanos juntos (zona G1, {{m3h_G1}} m³/h, {{inf_m}} kg/s de aire seco). La carga de la serpentina es el balance de energía del aire más la entalpía del agua que condensa ($h_f = 4{,}186\,T_D$):

$$\dot Q_{serp}=\dot m_a\left[(h_C-h_D)-(\omega_C-\omega_D)\,h_f\right]={{inf_m_m}}\left[({{inf_hC_m}}-{{inf_hD_m}})-({{inf_wC_m}}-{{inf_wD_m}})\cdot {{inf_hf_m}}\right]={{Q_serp_G1_m}}\ \mathrm{kW}$$

$$\dot Q_{lat}=\dot m_a\,(\omega_C-\omega_D)\,h_{fg}={{inf_m_m}}\cdot {{inf_dw_m}}\cdot 2\,501={{Q_lat_G1_m}}\ \mathrm{kW}\qquad \dot Q_{sens}={{Q_sens_G1_m}}\ \mathrm{kW}\qquad \dot Q_{recal}={{Q_recal_G1_m}}\ \mathrm{kW}$$

![Figura 3. Proceso del aire en el quirófano, verano pico.](../figuras/fig02_psicrometrica_quirofano.png){width=8cm}

{{tabla_psicro}}

Table: Tabla 5. Estados del aire del quirófano en verano pico (A a F).

Con todo el edificio, la serpentina entrega {{Q_L_dis}} kW en el verano pico, de los cuales el {{inf_lat_pct}} % es latente (tabla 4). En el mismo punto todo el edificio recalienta solo {{Q_recal_ver}} kW: **el recalentamiento aparece a carga parcial**, y dimensionar su recuperación con el pico subestimaría el potencial.

## 5.2 Refrigeración: ciclo de R134a

La enfriadora vence esos {{Q_L_dis}} kW. El R134a evapora a {{T_ev}} °C (agua helada 12/7 °C) y condensa a {{T_cond_dis}} °C, porque el condensador es enfriado por aire a {{T_ext_ver}} °C; usamos un rendimiento isentrópico de {{eta_is}} y un rendimiento del motor de {{eta_motor}} (supuestos de un compresor de tornillo habitual). Los estados 1 a 4 de la tabla 6 se ven en la figura 4.

{{tabla_ciclo}}

Table: Tabla 6. Estados del ciclo de R134a al punto de diseño de verano.

$$q_L=h_1-h_4={{inf_qL_m}}\ \mathrm{kJ/kg}\qquad w=h_2-h_1={{inf_w_m}}\ \mathrm{kJ/kg}\qquad COP=\frac{q_L}{w/\eta_{mot}}={{inf_COP_m}}\qquad \dot W=\frac{\dot Q_L}{COP}={{inf_W_m}}\ \mathrm{kW}$$

$$\dot Q_{cond}=\dot Q_L+\eta_{mot}\,\dot W={{Q_L_dis_m}}+{{eta_motor_m}}\cdot {{inf_W_m}}={{inf_Qc_m}}\ \mathrm{kW}$$

El COP es el {{eta_carnot}} % del de Carnot ({{cop_carnot}}) y el catálogo de la enfriadora del ejemplo da {{cop_catalogo}} contando solo los compresores a 35 °C: del mismo orden.

![Figura 4. Ciclo de compresión de R134a al punto de diseño de verano.](../figuras/fig03_diagrama_ph_r134a.png){width=8cm}

## 5.3 Combustión: la caldera de gas

El gas de red tiene una composición que suponemos (fracciones molares: metano {{gas_CH4}}, etano {{gas_C2H6}}, propano {{gas_C3H8}}, CO₂ {{gas_CO2}} y N₂ {{gas_N2}}). Para el metano, la reacción con {{exceso}} % de exceso de aire ($\lambda = {{lambda_m}}$) es

$$\mathrm{CH_4}+2{,}30\,(\mathrm{O_2}+3{,}76\,\mathrm{N_2})\;\to\;\mathrm{CO_2}+2\,\mathrm{H_2O}+0{,}30\,\mathrm{O_2}+8{,}65\,\mathrm{N_2}$$

y la memoria balancea la mezcla completa. El gas tiene un poder calorífico superior de {{PCS_kWh}} kWh/m³ ({{PCS_kcal}} kcal/m³) y uno inferior de {{PCI_kWh}} kWh/m³. Los gases salen a {{T_gases}} °C, por encima de su rocío ({{T_rocio}} °C), con una pérdida de {{q_gases}} % del PCI; sumando {{f_rad}} % de pérdidas de la caldera (supuesto):

$$\eta_{PCI}=1-q_{gases}-f_{rad}=1-0{,}080-0{,}020={{eta_PCI}}\ \%\ \Rightarrow\ \eta_{PCS}={{eta_PCS}}\ \%\qquad E_{gas}=\frac{Q_{util}}{\eta_{PCS}}=\frac{ {{q_total_MWh_m}} }{ {{inf_etaPCS_m}} }={{E_gas_MWh_m}}\ \mathrm{MWh/a\tilde{n}o}$$

Son unos {{V_gas_mil}} m³ de gas por año. Cada kWh de PCS emite {{co2_gas_pcs}} kg de CO₂, de la propia reacción. Hospitecnia {{R_hospitecnia}} usa un rendimiento de 90 % sin aclarar la base, así que la coincidencia es de resultado y no una comparación directa.

## 5.4 Consumo anual

La energía final es **{{E_total_MWh}} MWh por año**: {{E_elec_MWh}} de electricidad y {{E_gas_MWh}} de gas (PCS), {{i_cub}} kWh/m² (se suman kWh sin ponderar por energía primaria). Las emisiones son {{co2_t}} t de CO₂ por año ({{co2_gas_t}} del gas y {{co2_elec_t}} de la electricidad, con {{ef_elec}} t/MWh {{R_cammesa}}; otras fuentes dan 0,29 y 0,40).

![Figura 5. Consumo anual por uso final.](../figuras/fig04_consumo_por_uso.png){width=9cm}

<<EQUIPOS>>

<<EXERGIA>>

# 8. Alternativas, mejoras y discusión

## 8.1 Alternativas A y B

**A** es la base: enfriadora, caldera de gas y recalentamiento. **B** cubre el recalentamiento y la calefacción del aire con el **calor del condensador**, que hoy se tira. Nace del hallazgo central: ese calor existe ({{Q_cond_MWh}} MWh por año, {{Q_cond_sobre_recal}} veces el de recalentamiento) y alcanza con agua tibia a {{T_agua_rec}} °C. **Tiene un costo:** entregar agua a {{T_agua_rec}} °C exige condensar a {{T_cond_rec}} °C, más caliente que los {{T_cond_min}} a {{T_cond_anual_max}} °C de un condensador por aire, y eso aumenta el trabajo del compresor; por eso en cada estado del año se elige el mejor entre no recuperar, recuperar solo el sobrecalentamiento de la descarga o condensar en el recuperador. B recupera {{rec_MWh}} MWh de calor, ahorra {{ahorro_gas_B}} MWh de gas y gasta {{extra_elec_B}} MWh más de electricidad. Hay antecedentes: un hospital de Texas calienta con agua a 46 °C de enfriadoras de recuperación de calor en lugar de agua de caldera a 82 °C, y el fabricante informa 80 % menos de gas {{R_trane}}.

{{tabla_ab_inf}}

Table: Tabla 7. Alternativas A y B: indicadores, ventajas y limitaciones.

## 8.2 Mejoras de sustentabilidad

Cada mejora se evaluó con el mismo modelo, una por vez; la tabla ordena por ahorro de energía (por CO₂, la fotovoltaica es primera).

{{tabla_mejoras_inf}}

Table: Tabla 8. Mejoras respecto de A ({{E_total_MWh}} MWh y {{co2_t}} t de CO₂ por año).

Las medidas casi se suman en el total (sueltas ahorran {{sum_ind_MWh}} MWh y el paquete {{pkg_MWh}} MWh), pero con B la caldera de condensación ahorra {{m1_con_b}} MWh en vez de {{m1_solo}}: el aporte de cada una **depende de las demás**. **Refrigerante:** el R134a tiene un potencial de calentamiento global de 1.430 y la Enmienda de Kigali obliga a reducir los HFC {{R_kigali}}; con el mismo ciclo, el R1234ze(E) da el mismo COP ({{cop_ze}} contra {{cop_134}}) con un compresor {{mas_compresor}} % más grande y es ligeramente inflamable, lo que pesa en un hospital. Aislar la envolvente 30 % o reducir las ganancias internas 30 % ahorran menos de 3 %: el consumo está en el aire, no en la envolvente.

## 8.3 Discusión

- **Qué mueve el resultado.** Cambiando un supuesto por vez, la intensidad queda entre {{sens_min}} y {{sens_max}} kWh/m² por año: la humedad de consigna (5 puntos menos: {{s_hr5}} %), los horarios (consultorios 24 h: {{s_g5_24h}} %), el ACS por cama (200 L: {{s_acs200}} %) y la temperatura media (±2 K: {{s_tp2}} % y {{s_tm2}} %). Eso es un rango, no un intervalo de confianza.
- **Ventiladores contra compresor.** Los ventiladores consumen más que el compresor ({{pct_vent}} % contra {{pct_comp}} %) por ser un sistema todo aire con muchas renovaciones; el orden depende de la presión y el rendimiento supuestos.
- **El recalentamiento** es casi la mitad del calor útil de la caldera ({{q_recal_MWh}} de {{q_total_MWh}} MWh), y es mayor en verano que en invierno ({{calor_ene}} MWh de calor del aire en enero contra {{calor_jul}} en julio).
- **COP.** El del compresor es {{cop_elec}} al diseño y {{COP_est_comp}} como media anual, porque casi siempre el aire está más frío que a 34 °C; con ventiladores del condensador y bombas, la planta da {{COP_planta}}.

# 9. Conclusiones

1. **¿La alternativa seleccionada satisface los requerimientos?** Sí: la serpentina alcanza las consignas de las cinco zonas, cada zona recibe al menos sus renovaciones mínimas, y los equipos elegidos cubren {{Q_L_dis}} kW de frío con redundancia (<<CUMPLE_ENF>>), {{Q_cal_inv_aire}} kW de calefacción del aire (más {{Q_hum_inv}} kW de humidificación, que necesita vapor) y {{acs_kW}} kW medios de ACS. Lo que no satisface bien es la eficiencia: consume {{E_total_MWh}} MWh y tira {{Q_cond_MWh}} MWh de calor; B cumple lo mismo con {{dE_B}} % menos de energía.
2. **¿Cuáles son las principales variables que condicionan su desempeño?** La humedad de consigna ({{s_hr5}} %), los horarios ({{s_g5_24h}} %), el ACS por cama ({{s_acs200}} %) y la temperatura media ({{s_tp2}} % y {{s_tm2}} %). Termodinámicamente, la humedad del aire exterior ({{W_ext_ver}} g/kg) obliga a deshumidificar y recalentar, y el COP depende de la temperatura de condensación ({{cop_elec}} al diseño y {{COP_est_comp}} como media anual).
3. **¿Qué procesos presentan mayores pérdidas de energía o destrucción de exergía?** <<CONCL3>>
4. **¿Qué modificaciones permitirían mejorar el aprovechamiento de los recursos?** Recuperar el calor del condensador (B: {{dE_B}} % de energía y {{dC_B}} % de CO₂), fotovoltaica ({{dE_M5}} %), solar térmico ({{dE_M2}} %), recuperador del aire de extracción ({{dE_M3}} %) y caldera de condensación ({{dE_M1}} %); el paquete completo, {{dE_P}} % menos de energía y {{dC_P}} % menos de emisiones. Sin costos no se puede ordenar por retorno; la consigna no pide presupuesto.
5. **¿Qué limitaciones presenta el análisis y qué información haría falta?** El resultado se mueve entre {{sens_min}} y {{sens_max}} kWh/m² con un supuesto por vez. Faltan los consumos y las instalaciones del hospital real, datos citables de clima (SMN) y de la norma (ASHRAE 170) cotejados con sus originales, las curvas de carga parcial de los equipos y los efectos omitidos (economizador, ventiladores de retorno, caldera a carga parcial, humidificación de invierno); y para B, la coincidencia en el tiempo entre calor disponible y demanda. Las exergías químicas del gas son valores de uso corriente que hay que cotejar con el libro de la cátedra. No hay análisis de costos, y la distribución en planta es un esquema.

# Referencias

{{lista_referencias}}
