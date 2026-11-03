# Especificación del modelo de consumo del sistema térmico

Documento autosuficiente para **reimplementar el cálculo desde cero**. Los valores de entrada están en [`../informe/supuestos.md`](../informe/supuestos.md) (tabla generada). Toda temperatura en °C salvo que se indique, presión 101 325 Pa, humedad específica `W` en kg de vapor por kg de aire seco, entalpía `h` del aire húmedo en kJ por kg de aire seco.

Propiedades: aire húmedo con las fórmulas psicrométricas de ASHRAE Fundamentals (librería `psychrolib` en SI, o equivalente); refrigerante y gases ideales con CoolProp. Se espera coincidencia de los resultados finales dentro de 1 a 2 %.

## 0. Frontera

Sistema térmico de un hospital (frío, recalentamiento, calefacción, humidificación, agua caliente sanitaria) y sus auxiliares (ventiladores de las unidades de tratamiento de aire, ventiladores del condensador, bombas de agua helada). Energía final = electricidad + gas natural medido por su poder calorífico **superior**.

## 1. Superficies

- `A_or = n_or · a_or` (zona G1), `A_uti = camas_uti · a_uti_cama` (G2), `A_gen = camas_gen · a_gen_cama` (G3).
- `A_cond = f_acond · A_cub`. El resto `A_resto = A_cond − A_G1 − A_G2 − A_G3` se reparte: `A_G4 = f_g4_24h · A_resto` (áreas generales que funcionan las 24 h) y `A_G5 = A_resto − A_G4` (áreas generales que funcionan de día).

## 2. Caudales por zona (dimensionamiento, verano pico)

Para cada zona `g` con parámetros `z` (tabla de zonas):

1. Estado de consigna de verano: `T_r = z.t_ver`, `W_r = W(T_r, HR = z.hr_ver)`.
2. Carga sensible pico `Q_s,pico [W] = A · (z.q_s + z.f_env · (UA_m2 · (T_bs_ver − T_r) + q_sol_pico))` (con actividad plena, f_int = 1).
3. Caudal por carga sensible: `m_sens = Q_s,pico / 1000 / (cp_ah(W_r) · (T_r − T_sup_min))` [kg/s de aire seco], con `cp_ah(W) = 1,006 + 1,86·W` kJ/(kg K).
4. Caudal por renovaciones: `m_ach = z.ach_tot · A · h_techo / 3600 · rho_aire`.
5. `m_sup = max(m_ach, m_sens)` (caudal constante todo el año).
6. Aire exterior: `m_oa = min(z.ach_oa · A · h_techo / 3600 · rho_aire, m_sup)`, fijo en valor absoluto.
7. Potencia del ventilador: `P_vent [kW] = (m_sup / rho_aire) · z.dp_vent / 1000 / eta_vent`.

## 3. Tratamiento del aire de una zona para un estado dado

Entradas: estado exterior `(T_out, W_out)`, fracción de actividad `f_int`, ganancia solar `q_sol` [W/m²].

1. **Estación:** verano si `T_out ≥ T_cambio_estacion`, si no invierno.
2. **Consigna:** `T_r = z.t_ver` (verano) o `z.t_inv` (invierno). `W_set = W(T_r, z.hr_ver)`, `W_min = W(T_r, z.hr_min)`. **Humedad del aire de retorno:** `W_ret = W_set` en verano, `W_min` en invierno. El retorno está a `T_r`.
3. **Cargas de la zona [W]:** sensible neta `Q_s = A · (z.q_s · f_int + z.f_env · (UA_m2 · (T_out − T_r) + q_sol))` (positiva = hay que enfriar); latente `Q_l = A · z.q_l · f_int`.
4. **Impulsión requerida:** `T_sup = T_r − Q_s/1000 / (m_sup · cp_ah(W_set))`, acotada a `[T_sup_min, T_sup_max]`. `term_lat = Q_l/1000 / (m_sup · h_fg)`. `W_sup_max = max(W_set − term_lat, 1e-4)` y `W_sup_min = max(W_min − term_lat, 1e-4)`.
5. **Mezcla:** `x = m_oa / m_sup`. `h_mix = x·h(T_out, W_out) + (1−x)·h(T_r, W_ret)`; `W_mix = x·W_out + (1−x)·W_ret`; `T_mix` a partir de `h_mix` y `W_mix`.
6. **Serpentina de enfriamiento:**
   - Si `W_mix > W_sup_max`: deshumidifica. Salida de la serpentina con `W_c = W_sup_max` y saturación parcial `HR_serp`: `T_c` es la temperatura a la que el aire a `HR_serp` tiene humedad `W_c`. Si `T_c > T_sup`, se fija `T_c = T_sup` y `W_c = min(W_sup_max, W(T_sup, HR_serp))`. Si `T_c ≥ T_mix`, no hay enfriamiento (`T_c = T_mix`, `W_c = W_mix`). En otro caso, la serpentina enfría.
   - Si no, y `T_mix > T_sup`: enfriamiento sensible, `T_c = T_sup`, `W_c = W_mix`.
   - Si no: sin enfriamiento.
   - Si enfría: `Q_coil = m_sup · (h_mix − h(T_c, W_c)) − m_sup · (W_mix − W_c) · 4,186 · T_c` [kW] (se resta la entalpía del condensado). Parte latente `Q_lat = m_sup · (W_mix − W_c) · h_fg`; parte sensible = `Q_coil − Q_lat`.
7. **Recalentamiento o calefacción:** si `T_c < T_sup`: `Q = m_sup · cp_ah(W_c) · (T_sup − T_c)`. Es **recalentamiento** si la serpentina enfrió y **calefacción** si no.
8. **Humidificación con vapor (isotérmica):** si `W_c < W_sup_min`: `ΔW = W_sup_min − W_c`, `Q_hum = m_sup · ΔW · (2676 − 4,186·T_agua_red)` [kW] (vapor saturado a 101,3 kPa).

## 4. Planta de frío

Para una carga frigorífica total `Q_L` [kW] (suma de las serpentinas) y una temperatura exterior `T_ext`:

1. `T_cond = max(T_ext + dT_cond, T_cond_min)`.
2. Ciclo con el refrigerante indicado: evaporación a `T_ev` con sobrecalentamiento `sobrecal` a la salida; compresión con rendimiento isentrópico `eta_is`; condensación a `T_cond` con subenfriamiento `subenf`; expansión isoentálpica.
3. `COP_elec = q_L / (w / eta_motor)` con `q_L = h1 − h4` y `w = h2 − h1` por kg de refrigerante.
4. Potencia eléctrica del compresor `W_comp = Q_L / COP_elec`. Calor rechazado `Q_cond = Q_L + W_comp · eta_motor`.
5. Ventiladores del condensador: `W_cond = f_vent_cond · Q_cond`.
6. Bombas: `m_w = Q_L / (4,186 · dT_aguahelada)` kg/s; `W_bomba = (m_w/1000) · dP_bomba / eta_bomba / 1000` kW.

## 5. Combustión y caldera

- Gas natural con la composición molar dada (CH4, C2H6, C3H8, N2, CO2). Aire con 21 % de O2 y 79 % de N2 en moles. Combustión completa, sin disociación. Relación de aire `lambda_aire` (1 = estequiométrico).
- Entalpías de formación a 25 °C [kJ/kmol]: CH4 −74 850; C2H6 −84 680; C3H8 −103 850; CO2 −393 520; H2O(g) −241 820; H2O(l) −285 830.
- **PCS** y **PCI** por kmol de combustible a partir de esas entalpías; en volumen: m³ estándar a 15 °C y 101,325 kPa (gas ideal, R = 8,314462 kJ/(kmol K)).
- **Rendimiento sobre PCI:** `eta = 1 − q_gases − f_rad`, con `q_gases = (H_productos(T_gases) − H_reactivos(T_aire_comb)) / PCI`. Las entalpías son sensibles respecto de 25 °C, por integración del calor específico de gas ideal de cada especie (CoolProp, `CP0MOLAR`). Reactivos: aire (O2 y N2) a `T_aire_comb`; el combustible se toma a 25 °C. Productos: CO2, H2O (vapor), N2 y O2 sobrante a `T_gases`.
- **Temperatura de rocío** de los gases: temperatura de saturación del agua a la presión parcial `y_H2O · 101 325 Pa`.
- **Llama adiabática:** `T` tal que `Σ n_i Δh_i(T) = PCI + H_reactivos`.
- Energía de combustible para entregar `Q_util`: `E_PCI = Q_util / eta`; `E_PCS = E_PCI · (PCS/PCI)`; volumen `E_PCS / PCS[kWh/m³]`.

## 6. Agua caliente sanitaria

`Q_acs [kW] = L_cama_dia · (camas_gen + camas_uti) · 4,186 · (T_acs − T_agua_fria) · f_perd_acs / 86 400` (1 L = 1 kg). Funciona las 8 760 h del año.

## 7. Consumo anual

Para cada mes `i` con `T_i`, `HR_i` y `dias_i`:

1. `W_i = W(T_i, HR_i)` (humedad específica constante en el día).
2. Dos estados por mes, de **12 · dias_i horas** cada uno: **día** con `T = T_i + rango_diario/2`, `f_int = z.f_dia`, `q_sol = q_sol_dia`; **noche** con `T = T_i − rango_diario/2`, `f_int = z.f_noche`, `q_sol = 0`. Las zonas con `opera_noche = no` no funcionan de noche (ni consumen nada).
3. En cada estado y para cada zona que opera: aplicar la sección 3 con `(T, W_i)`. Sumar las serpentinas de todas las zonas del estado: `Q_L`. Aplicar la sección 4 con `T_ext = T`. Todas las potencias (serpentinas, recalentamiento, calefacción, humidificación, ventiladores, compresor, ventiladores del condensador, bombas) se multiplican por las horas del estado y se acumulan.
4. Los ventiladores de las unidades de tratamiento consumen `P_vent` durante las horas en que la zona opera.
5. Calor útil de la caldera = recalentamiento + calefacción + humidificación (de todas las zonas) + ACS anual (sección 6). Combustible con la sección 5.
6. **Energía final** = electricidad total (compresor + ventiladores del condensador + bombas + ventiladores de las unidades) + gas en PCS.

## 8. Puntos de diseño

- **Verano:** `T_out = T_bs_ver`, `W_out = W(T_bs_ver, bulbo húmedo T_bh_ver)`, `f_int = 1` en todas las zonas, `q_sol = q_sol_pico`. `Q_L,diseno` = suma de serpentinas. Planta de frío a `T_ext = T_bs_ver`.
- **Invierno:** `T_out = T_inv`, `W_out = W(T_inv, HR_inv)`, `f_int = 0`, `q_sol = 0`. Carga de la caldera del aire = suma de recalentamiento + calefacción + humidificación.

## 9. Magnitudes a reportar

`Q_L,diseno` [kW]; recalentamiento en verano pico [kW]; carga de la caldera en invierno [kW]; `W_comp` y `COP_elec` y `T_cond` en el diseño; `Q_acs` [kW]; `eta` de la caldera sobre PCI; PCS [kcal/m³ y kWh/m³]; temperatura de rocío y de llama adiabática; por zona: `m_sup`, `m_oa`, serpentina de diseño [kW], serpentina anual [kWh], recalentamiento anual [kWh], calefacción anual [kWh], ventiladores anual [kWh]; anual: compresor, ventiladores del condensador, bombas y ventiladores [kWh]; calor útil (recalentamiento, calefacción, humidificación, ACS) [kWh]; frío entregado [kWh]; gas en PCS [kWh] y [m³]; energía final total [kWh] y [kWh/m² de superficie cubierta].
