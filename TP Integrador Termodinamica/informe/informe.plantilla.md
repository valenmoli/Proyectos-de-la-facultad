---
title: "Diseño de un sistema energético eficiente para un hospital del AMBA"
subtitle: "TP Integrador de Termodinámica 2026 · Informe técnico"
author: "[Integrantes del equipo: a completar]"
date: "Facultad de Ingeniería y Ciencias Agrarias · Ingeniería Civil · UCA · Noviembre de 2026"
lang: es-AR
---

# Resumen

Se diseña y evalúa el sistema térmico de un hospital de alta complejidad del AMBA, con el tamaño y el programa del Hospital Favaloro ({{A_cub}} m², {{camas_tot}} camas, {{n_or}} quirófanos): aire tratado con enfriadora y caldera de gas. Consume **{{E_total_MWh}} MWh de energía final por año ({{i_cub}} kWh/m²)**. El hallazgo central es que el aire se enfría para quitarle humedad y se recalienta con gas, mientras el condensador de la enfriadora tira {{Q_cond_MWh}} MWh de calor por año. Aprovecharlo (alternativa B) baja la energía hasta {{dE_B}} % ({{dE_B75}} % si calor y demanda coinciden el 75 % del tiempo) y las emisiones hasta {{dC_B}} %; sumando las demás mejoras, hasta {{dE_P}} % y {{dC_P}} %. <<RESUMEN_EXERGIA>>

# 1. Introducción y objetivos

Un hospital funciona todo el año y todo el día, y su climatización es de **proceso**, no de confort: exige temperatura y humedad controladas, presión positiva y aire exterior filtrado. En el AMBA eso tiene una consecuencia termodinámica concreta: el aire exterior de verano (unos {{T_ext_ver}} °C con {{W_ext_ver}} g de vapor por kg de aire seco) hay que enfriarlo por debajo de su punto de rocío para quitarle vapor, y a esa temperatura ya no se puede impulsar: hay que **recalentarlo**. Se gasta frío para deshumidificar y combustible para devolver temperatura.

**Objetivo:** modelar y evaluar con la Primera y la Segunda Ley el sistema térmico de un hospital del AMBA y proponer mejoras que reduzcan su consumo y su impacto ambiental: determinar las cargas y el ciclo de frío, el combustible y el CO₂, dónde se destruye exergía, los equipos y su ubicación, y comparar alternativas. Los cuatro temas de la cátedra se usan como una cadena, no por separado:

{{tabla_temas_inf}}

Table: Tabla 1. Los cuatro temas y cómo se conectan en este sistema.

El **hilo conductor**: el aire húmedo fija cuánto frío y cuánto recalentamiento hacen falta; la enfriadora paga ese frío con electricidad y tira calor; la caldera paga el recalentamiento con gas; la exergía muestra que el calor que se tira es justo el que haría falta para recalentar, y de ahí sale la alternativa B. Con esos resultados se eligen y ubican los equipos (sección 6). En el texto, [n] remite a la lista de referencias, el asterisco indica una fuente que solo conocemos por un extracto y «supuesto» marca una decisión nuestra, con su motivo. **Siglas:** AMBA (Área Metropolitana de Buenos Aires), ACS (agua caliente sanitaria), UTA (unidad de tratamiento de aire), COP (coeficiente de desempeño), PCS y PCI (poder calorífico superior e inferior del gas), HCWH (Health Care Without Harm).

# 2. El edificio y sus datos

Elegimos el **Hospital Dr. René Favaloro (SAMIC, La Matanza)** porque, entre los dos candidatos (el Favaloro y el sanatorio de Nordelta), es el único con la superficie cubierta documentada {{R_presidencia}}; El Cruce {{R_elcruce}} sirve de contraste de tamaño. Ningún documento trae datos de climatización ni de consumo del edificio real: replicamos su **tamaño y programa**, no sus instalaciones.

{{tabla_datos_inf}}

Table: Tabla 2. Datos del edificio y cómo los obtuvimos.

El Favaloro tiene {{gross_per_bed}} m² cubiertos por cama, contra {{ref_bed_hospitecnia}} del artículo de Hospitecnia {{R_hospitecnia}} (hospitales españoles) y {{ref_bed_cruce}} de El Cruce {{R_elcruce}}: es algo más compacto, una señal para vigilar. Dividimos el edificio en cinco zonas térmicas según su uso:

{{tabla_zonas_inf}}

Table: Tabla 3. Zonas térmicas: superficie, consigna de verano, renovaciones por hora y su origen. En G3 y G5 el caudal real sale de la carga sensible y es mayor que el mínimo.

Las áreas de cada zona pesan poco (±6 m² por cama de internación cambian la energía ±{{sens_a_gen}} %); pesan más la fracción que se climatiza (±{{sens_f_acond}} %), la que funciona 24 h (±{{sens_g4}} %) y las horas de uso.

# 3. Descripción del sistema y condiciones de diseño

## 3.1 El sistema y por qué lo elegimos

![Figura 1. Esquema del sistema: cadena de aire (A a F son los estados del aire de la figura 3), enfriadora, caldera, agua caliente sanitaria (ACS) y, en verde, la alternativa B.](../figuras/fig01_esquema_sistema.png){width=10.5cm}

Cada zona tiene una unidad de tratamiento de aire de caudal constante: el aire exterior (A) se mezcla con el de retorno (B) y queda en el estado C, la serpentina de agua helada lo enfría y le quita vapor (D), el recalentador lo lleva a la temperatura de impulsión (E) y el ventilador lo impulsa a la zona (F). El agua helada la produce una **enfriadora de R134a** con condensador por aire ($\dot Q_L$ de frío, $\dot W_{comp}$ eléctrico, $\dot Q_{cond}$ rechazado al ambiente). Una **caldera de gas natural** da el recalentamiento, la calefacción de invierno y el ACS. La alternativa B manda el calor del condensador, a 45 °C, al recalentador en lugar de la caldera.

- **Todo aire de caudal constante**: quirófanos y terapia necesitan filtrado, muchas renovaciones y control de humedad y de presiones, que un split no da; en hospitales argentinos, HCWH {{R_hcwh}} encontró equipos de refrigeración de emergencia porque el aire central no alcanzaba.
- **Enfriadora condensada por aire**: sin torre no hay consumo de agua ni riesgo de legionela; el COP es algo menor.
- **Con reserva**: 3+1 enfriadoras y 2 calderas al 100 %, porque un hospital no puede parar quirófanos y terapia (las UTAs críticas no tienen reserva: queda abierto).
- **Gas natural**: hay red en el AMBA y es el combustible dominante en {{R_hospitecnia}}; caldera de base (A) y recuperación de calor (B).

{{tabla_nec_inf}}

Table: Tabla 4. Lo que el sistema tiene que dar: potencia de diseño y energía anual.

## 3.2 Temperatura y humedad: la carta de Givoni

**Quirófano y terapia (G1, G2).** ASHRAE 170 {{R_ashrae170}} pide de 20 a 24 °C y hasta 60 % de humedad relativa en quirófano. Elegimos {{T_G1}} °C para el quirófano y {{T_G2}} °C para la terapia, con humedad de **55 %**: el máximo de 60 % menos 5 puntos de margen de control (supuesto). **Resto (G3, G4, G5).** 24 °C y 55 a 60 %. Lo respaldamos con la **carta bioclimática de Givoni** {{R_givoni}}, una carta psicrométrica (eje horizontal: temperatura de bulbo seco; vertical: humedad específica) con la zona donde la mayoría de la gente está cómoda sin equipos: de 18 a 29 °C, de 20 a 80 % y de 4 a 17 g/kg. Nuestras cinco consignas caen dentro (figura 2); elegimos 24 °C y no 22 °C por estar en su parte media-alta (menos frío que producir).

![Figura 2. Carta psicrométrica con la zona de confort de Givoni, el clima de cada mes, el estado exterior de diseño y las consignas de verano.](../figuras/fig10_carta_givoni.png){width=8.5cm}

La carta muestra además el problema: el clima medio de octubre a abril cae dentro de la zona o muy cerca, pero el **estado exterior de diseño de verano** ({{T_ext_ver}} °C y {{W_ext_ver}} g/kg) queda fuera: hay que enfriarlo, quitarle vapor y recalentarlo.

## 3.3 Renovaciones por hora: de dónde sale el 20/4

Los quirófanos llevan **20 renovaciones totales por hora, de las cuales 4 son de aire exterior** (ASHRAE 170 {{R_ashrae170}}). Las 20 mueven el aire por filtros de alta eficiencia, diluyen contaminantes y mantienen la sobrepresión; las 4 de aire exterior aportan el aire fresco mínimo (olores, gases anestésicos, CO₂); esa explicación es nuestra. La relación 20/4 = **5** significa que el 20 % del aire que se mueve es exterior y el 80 % se recircula filtrado: solo hay que tratar un quinto del aire con las condiciones exteriores.

**Comprobación.** Con {{qs_G1}} W/m² de ganancia sensible (supuesto) y aire de impulsión a 13 °C (9 K bajo la consigna), por carga térmica bastarían {{ach_load_G1}} renovaciones por hora; la norma pide 20, {{ratio_norm_load}} veces más: **en el quirófano manda la norma, no la carga térmica**, y por eso consume mucho por m². Un extracto de un adendo de ASHRAE 170 {{R_ashrae170}} admite que el 20 no tiene una justificación científica definitiva y recomienda evaluar el riesgo antes de cambiarlo; lo mantenemos y mostramos su peso: con 15 o 25 renovaciones la energía cambia {{s_ach15}} % y {{s_ach25}} %.

## 3.4 Clima y agua caliente

**Clima (supuesto).** Medias mensuales aproximadas de Buenos Aires, partidas en mitad diurna y nocturna (amplitud de 9 K). Las contrastamos con el SMN 1991-2020 {{R_smn}} solo en enero ({{T_ene_smn}} contra {{T_ene}} °C), julio ({{T_jul_smn}} contra {{T_jul}} °C) y humedad media ({{HR_smn}} contra {{HR_media}} %: usamos algo más, lo que sobreestima un poco el consumo); los demás meses no se contrastaron. El estado de diseño de verano ({{T_ext_ver}} °C de bulbo seco y {{Tbh_ver}} °C de bulbo húmedo) y el de invierno ({{T_inv_exp}} °C y 80 %) son valores habituales que adoptamos (supuesto).

**Agua caliente.** {{L_cama}} L por cama y día de {{T_red}} a {{T_acs}} °C, más 30 % por pérdidas de acumulación y recirculación (supuesto): {{acs_kW}} kW medios. Hospitecnia {{R_hospitecnia}} da una guía de 55 L y ratios de diseño de 200 a 300 L; un caso de 540 camas de ese artículo da unos 51 L si el consumo se concentra en 4 h y unos 102 L si en 8 h (cálculo propio). Elegimos 100 L (con 55 L la energía cambia {{s_acs55}} % y con 200 L, {{s_acs200}} %).

# 4. Metodología e hipótesis

Para cada zona y cada mes (partido en una mitad diurna y una nocturna) se encadenan los cuatro pasos de la tabla 1: balances de masa y energía del aire húmedo (cargas sensible y latente), ciclo de R134a que vence esa carga, balance de la reacción del gas que alimenta el recalentamiento y el ACS, y balance de exergía $F = P + L + D$ de cada equipo. La energía anual suma 12 meses × 2 mitades (temperatura media del mes ± {{dT_dia}} K), con el COP según la temperatura exterior de cada estado y sin curvas de carga parcial.

**Hipótesis principales.** Régimen permanente en cada estado; aire y vapor como gases ideales a 101,325 kPa; caudal constante con serpentina y recalentamiento, sin economizador; el ventilador disipa toda su potencia como calor en el aire (900 a 1.800 Pa, rendimiento {{eta_vent}}); compresor adiabático de rendimiento isentrópico {{eta_is}}, expansión isoentálpica y evaporación a {{T_ev}} °C; condensación a la temperatura exterior más {{dT_cond}} K (mínimo {{T_cond_min}} °C); combustión completa con {{exceso}} % de exceso de aire, sin disociación, y gases de escape a {{T_gases}} °C; consignas de invierno por debajo de {{T_cambio}} °C. Son supuestos nuestros; su peso está en la memoria.

**Frontera.** Los sistemas de estudio son la UTA, la enfriadora, la caldera y el ACS, cada uno un volumen de control (límites en la memoria), con sus auxiliares (ventiladores y bombas). No se incluyen iluminación, equipos médicos, cocina, lavandería ni esterilización: **los {{E_total_MWh}} MWh no son el consumo total del hospital**. Las ecuaciones, los estados y los datos completos están en la memoria de cálculo.

# 5. Cálculos y resultados

## 5.1 Aire húmedo: el quirófano en verano pico

Con el exterior a {{T_ext_ver}} °C y {{Tbh_ver}} °C de bulbo húmedo, el aire exterior (A) se mezcla con el de retorno (B) y queda a {{T_mix_G1}} °C (C); la serpentina lo enfría hasta {{T_c_G1}} °C y le quita vapor (D); el recalentador lo sube a {{T_obj_G1}} °C (E) y el ventilador, que le agrega {{dT_vent_G1}} K, lo deja a {{T_sup_G1}} °C (F). «Quirófano» son aquí los {{n_or}} quirófanos juntos (zona G1, {{m3h_G1}} m³/h, {{inf_m}} kg/s de aire seco). La carga de la serpentina es el balance de energía del aire más la entalpía del agua que condensa ($h_f = 4{,}186\,T_D$):

$$\dot Q_{serp}=\dot m_a\left[(h_C-h_D)-(\omega_C-\omega_D)\,h_f\right]$$

$$\dot Q_{serp}={{inf_m_m}}\left[({{inf_hC_m}}-{{inf_hD_m}})-({{inf_wC_m}}-{{inf_wD_m}})\cdot {{inf_hf_m}}\right]={{Q_serp_G1_m}}\ \mathrm{kW}$$

$$\dot Q_{lat}=\dot m_a\,(\omega_C-\omega_D)\,h_{fg}={{inf_m_m}}\cdot {{inf_dw_m}}\cdot 2\,501={{Q_lat_G1_m}}\ \mathrm{kW}$$

La carga sensible es entonces {{Q_sens_G1}} kW y el recalentador entrega {{Q_recal_G1}} kW. Las propiedades del aire húmedo salen de psychrolib {{R_coolprop}}.

![Figura 3. Proceso del aire en el quirófano, verano pico.](../figuras/fig02_psicrometrica_quirofano.png){width=7.5cm}

{{tabla_psicro}}

Table: Tabla 5. Estados del aire del quirófano en verano pico (A a F).

Con todo el edificio, la serpentina entrega {{Q_L_dis}} kW en el verano pico, de los cuales el {{inf_lat_pct}} % es latente (tabla 4). En el mismo punto todo el edificio recalienta solo {{Q_recal_ver}} kW: **el recalentamiento aparece a carga parcial**, y dimensionar su recuperación con el pico subestimaría el potencial.

## 5.2 Refrigeración: ciclo de R134a

La enfriadora vence esos {{Q_L_dis}} kW. El R134a evapora a {{T_ev}} °C (agua helada 12/7 °C) y condensa a {{T_cond_dis}} °C, porque el condensador es enfriado por aire a {{T_ext_ver}} °C; usamos un rendimiento isentrópico de {{eta_is}} y un rendimiento del motor de {{eta_motor}} (supuestos de un compresor de tornillo habitual). Los estados 1 a 4 de la tabla 6 se ven en la figura 4 (propiedades con CoolProp {{R_coolprop}}).

{{tabla_ciclo_inf}}

Table: Tabla 6. Estados del ciclo de R134a al punto de diseño de verano.

$$q_L=h_1-h_4={{inf_qL_m}}\ \mathrm{kJ/kg}\qquad w=h_2-h_1={{inf_w_m}}\ \mathrm{kJ/kg}$$

$$COP=\frac{q_L}{w/\eta_{mot}}={{inf_COP_m}}\qquad \dot W=\frac{\dot Q_L}{COP}={{inf_W_m}}\ \mathrm{kW}$$

$$\dot Q_{cond}=\dot Q_L+\eta_{mot}\,\dot W={{Q_L_dis_m}}+{{eta_motor_m}}\cdot {{inf_W_m}}={{inf_Qc_m}}\ \mathrm{kW}$$

El COP es el {{eta_carnot}} % del de Carnot ({{cop_carnot}}) y el catálogo de la enfriadora del ejemplo da {{cop_catalogo}} contando solo los compresores a 35 °C: del mismo orden.

![Figura 4. Ciclo de compresión de R134a al punto de diseño de verano.](../figuras/fig03_diagrama_ph_r134a.png){width=7.5cm}

## 5.3 Combustión: la caldera de gas

El gas de red tiene una composición que suponemos (fracciones molares: metano {{gas_CH4}}, etano {{gas_C2H6}}, propano {{gas_C3H8}}, CO₂ {{gas_CO2}} y N₂ {{gas_N2}}). Para el metano, la reacción con {{exceso}} % de exceso de aire ($\lambda = {{lambda_m}}$) es

$$\mathrm{CH_4}+2{,}30\,(\mathrm{O_2}+3{,}76\,\mathrm{N_2})\;\to\;\mathrm{CO_2}+2\,\mathrm{H_2O}+0{,}30\,\mathrm{O_2}+8{,}65\,\mathrm{N_2}$$

y la memoria balancea la mezcla completa. El gas tiene un poder calorífico superior de {{PCS_kWh}} kWh/m³ ({{PCS_kcal}} kcal/m³) y uno inferior de {{PCI_kWh}} kWh/m³. Los gases salen a {{T_gases}} °C, por encima de su rocío ({{T_rocio}} °C), con una pérdida de {{q_gases}} % del PCI; sumando {{f_rad}} % de pérdidas de la caldera (supuesto):

$$\eta_{PCI}=1-q_{gases}-f_{rad}=1-{{inf_qg4_m}}-{{inf_frad4_m}}={{inf_etaPCI4_m}}\qquad \eta_{PCS}={{eta_PCS_m}}\ \%$$

$$E_{gas}=\frac{Q_{util}}{\eta_{PCS}}=\frac{ {{q_total_MWh_m}} }{ {{inf_etaPCS_m}} }={{E_gas_MWh_m}}\ \mathrm{MWh\ por\ a\tilde{n}o}$$

Son unos {{V_gas_mil}} m³ de gas por año, y cada kWh de PCS emite {{co2_gas_pcs}} kg de CO₂. Hospitecnia {{R_hospitecnia}} usa un rendimiento de 90 % sin aclarar la base: la coincidencia es de resultado.

## 5.4 Consumo anual

La energía final es **{{E_total_MWh}} MWh por año**: {{E_elec_MWh}} de electricidad y {{E_gas_MWh}} de gas (PCS), {{i_cub}} kWh/m² (se suman kWh sin ponderar por energía primaria). Las emisiones son {{co2_t}} t de CO₂ por año ({{co2_gas_t}} del gas y {{co2_elec_t}} de la electricidad, con {{ef_elec}} t/MWh {{R_cammesa}}). Contraste: los {{Q_L_dis_wm2}} W/m² de frío están en el orden de los 100 a 115 W/m² de {{R_hospitecnia}}; los {{i_cub}} kWh/m² del sistema térmico equivalen a 226 a 361 kWh/m² del hospital completo (memoria), por encima de los 163 a 259 kWh/m² estimados para tres hospitales argentinos {{R_hcwh}}: una señal para vigilar, porque el nuestro es todo aire y funciona 24 h.

![Figura 5. Consumo anual por uso final.](../figuras/fig04_consumo_por_uso.png){width=8.5cm}

<<EQUIPOS>>

<<EXERGIA>>

# 8. Alternativas, mejoras y discusión

## 8.1 Alternativas A y B

**A** es la base: enfriadora, caldera de gas y recalentamiento. **B** cubre el recalentamiento y la calefacción del aire con el **calor del condensador**, que hoy se tira: ese calor existe ({{Q_cond_MWh}} MWh por año, {{Q_cond_sobre_recal}} veces el de recalentamiento) y alcanza con agua tibia a {{T_agua_rec}} °C. **Cuesta trabajo:** entregar agua a {{T_agua_rec}} °C exige condensar a {{T_cond_rec}} °C, más caliente que los {{T_cond_min}} a {{T_cond_anual_max}} °C de un condensador por aire; por eso en cada estado del año se elige el mejor entre no recuperar, recuperar solo el sobrecalentamiento de la descarga o condensar en el recuperador. B recupera {{rec_MWh}} MWh de calor, ahorra {{ahorro_gas_B}} MWh de gas y gasta {{extra_elec_B}} MWh más de electricidad. Hay antecedentes: un hospital de Texas calienta con agua a 46 °C de enfriadoras de recuperación de calor en lugar de agua de caldera a 82 °C, y el fabricante informa 80 % menos de gas {{R_trane}}. **Qué proponemos:** dimensionar los equipos con A, porque la planta tiene que cubrir la carga aunque el calor del condensador no coincida con la demanda, y proponer B como primera mejora y, después, las de la tabla 8.

::: {custom-style="Largo"}
{{tabla_ab_inf}}

Table: Tabla 7. Alternativas A y B: indicadores, ventajas y limitaciones.
:::

## 8.2 Mejoras de sustentabilidad

Cada mejora se evaluó con el mismo modelo, una por vez, y se ordenan por ahorro de energía (por CO₂, la fotovoltaica es primera). B y el paquete son el techo: suponen que el calor del condensador y la demanda coinciden.

::: {custom-style="Largo"}
{{tabla_mejoras_inf}}

Table: Tabla 8. Mejoras respecto de A ({{E_total_MWh}} MWh y {{co2_t}} t de CO₂ por año).
:::

Las medidas casi se suman (sueltas ahorran {{sum_ind_MWh}} MWh y el paquete {{pkg_MWh}} MWh), pero el aporte de cada una **depende de las demás**: con B, la caldera de condensación ahorra {{m1_con_b}} MWh y no {{m1_solo}}. **Refrigerante:** el R134a tiene un potencial de calentamiento global de 1.430 (valor de uso corriente; supuesto) y la Enmienda de Kigali obliga a reducir los HFC {{R_kigali}}; con el mismo ciclo y el mismo rendimiento isentrópico supuesto, el R1234ze(E) da el mismo COP ({{cop_ze}} contra {{cop_134}}) con un compresor {{mas_compresor}} % más grande y es ligeramente inflamable (clase A2L; supuesto), lo que pesa en un hospital. Aislar la envolvente 30 % baja la energía solo {{s_ua30}} %, y reducir las ganancias internas 30 % no ahorra: la sube {{s_gi30}} %, porque hay más recalentamiento: el consumo está en el aire, no en la envolvente.

## 8.3 Discusión

- **Qué mueve el resultado.** Cambiando un supuesto por vez, la intensidad queda entre {{sens_min}} y {{sens_max}} kWh/m² por año: la humedad de consigna (5 puntos menos: {{s_hr5}} %), los horarios (consultorios 24 h: {{s_g5_24h}} %), que el ventilador no caliente el aire ({{s_fan}} %), el ACS por cama (200 L: {{s_acs200}} %), la temperatura media (±2 K: {{s_tp2}} % y {{s_tm2}} %) y el cambio de estación a 21 °C ({{s_est21}} %). Es un rango, no un intervalo de confianza.
- **Ventiladores contra compresor.** Los ventiladores consumen más que el compresor ({{pct_vent}} % contra {{pct_comp}} %) por ser un sistema todo aire con muchas renovaciones; el orden depende de la presión y el rendimiento supuestos.
- **El recalentamiento** es casi la mitad del calor útil de la caldera ({{q_recal_MWh}} de {{q_total_MWh}} MWh) y es mayor en verano que en invierno ({{calor_ene}} MWh de calor del aire en enero contra {{calor_jul}} en julio).
- **COP.** El del compresor es {{cop_elec}} al diseño y {{COP_est_comp}} como media anual, porque casi siempre el aire está más frío que a 34 °C; con ventiladores del condensador y bombas, la planta da {{COP_planta}}.

# 9. Conclusiones

1. **¿La alternativa seleccionada satisface los requerimientos?** Seleccionamos A como base de dimensionamiento, con B propuesta como mejora. Sí: la serpentina alcanza las consignas de las cinco zonas, cada zona recibe al menos sus renovaciones mínimas y los equipos de ejemplo cubren {{Q_L_dis}} kW de frío con redundancia (<<CUMPLE_ENF>>, con la capacidad nominal del catálogo {{R_carrier}}; la selección final la confirma el fabricante), {{Q_cal_inv_aire}} kW de calefacción del aire (más {{Q_hum_inv}} kW de vapor) y {{acs_kW}} kW medios de ACS. Lo que no satisface bien es la eficiencia: consume {{E_total_MWh}} MWh y tira {{Q_cond_MWh}} MWh de calor; B cumple lo mismo con hasta {{dE_B}} % menos de energía.
2. **¿Cuáles son las principales variables que condicionan su desempeño?** La humedad de consigna ({{s_hr5}} %), los horarios ({{s_g5_24h}} %), que el ventilador no caliente el aire ({{s_fan}} %), el ACS por cama ({{s_acs200}} %) y la temperatura media ({{s_tp2}} % y {{s_tm2}} %). Termodinámicamente, la humedad del aire exterior ({{W_ext_ver}} g/kg) obliga a deshumidificar y recalentar, y el COP depende de la temperatura de condensación ({{cop_elec}} al diseño y {{COP_est_comp}} como media anual).
3. **¿Qué procesos presentan mayores pérdidas de energía o destrucción de exergía?** <<CONCL3>>
4. **¿Qué modificaciones permitirían mejorar el aprovechamiento de los recursos?** Recuperar el calor del condensador (B: hasta {{dE_B}} % de energía y {{dC_B}} % de CO₂), fotovoltaica ({{dE_M5}} % de energía), solar térmico ({{dE_M2}} %), recuperador del aire de extracción ({{dE_M3}} %) y caldera de condensación ({{dE_M1}} %); el paquete, hasta {{dE_P}} % de energía y {{dC_P}} % de emisiones ({{inf_P75_E}} % y {{inf_P75_C}} % con coincidencia del 75 %; {{inf_PsFV_E}} % y {{inf_PsFV_C}} % sin la fotovoltaica, que cubre consumo y no lo reduce). Sin costos no se puede ordenar por retorno.
5. **¿Qué limitaciones presenta el análisis y qué información haría falta?** El resultado se mueve entre {{sens_min}} y {{sens_max}} kWh/m² con un supuesto por vez. Faltan los consumos y las instalaciones del hospital real, datos de clima (SMN) y de la norma (ASHRAE 170) cotejados con sus originales, las curvas de carga parcial y los efectos omitidos (economizador, ventiladores de retorno, caldera a carga parcial, humidificación de invierno); y para B, la coincidencia entre calor disponible y demanda. Las exergías químicas del gas, el potencial de calentamiento global de los refrigerantes y otras constantes son valores de uso corriente que no cotejamos con una fuente numerada, y las fuentes con asterisco se conocen por extractos. No hay análisis de costos y la distribución en planta es un esquema.

# Referencias

::: {custom-style="Referencias"}
{{lista_referencias}}
:::
