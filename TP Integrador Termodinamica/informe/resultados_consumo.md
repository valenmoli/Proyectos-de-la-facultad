# Resultados de la estimacion de consumos

*Generado por `calculo/generar_resultados.py`. No editar a mano: se regenera con el codigo.*

Hospital modelado: Favaloro (La Matanza), AMBA. Frontera: sistema termico (frio, recalentamiento, calefaccion, humidificacion y agua caliente sanitaria) y sus auxiliares (ventiladores, bombas, ventiladores del condensador). Energia final: electricidad mas gas natural medido por su poder calorifico superior.

## 1. Resultado principal

| Magnitud | Valor |
|---|---|
| Superficie cubierta | 18.352 m2 |
| Superficie climatizada | 15.599 m2 (85 % de la cubierta) |
| Electricidad anual | 1.736 MWh |
| Gas natural anual (PCS) | 1.285 MWh = 120 mil m3 |
| **Energia final anual** | **3.021 MWh** |
| **Intensidad sobre superficie cubierta** | **165 kWh/m2 y anio** (95 electricidad + 70 gas) |
| Intensidad sobre superficie climatizada | 194 kWh/m2 y anio |
| Participacion del gas | 43 % |
| Capacidad frigorifica de diseno | 1.987 kW (108 W/m2 cubierto; 127 W/m2 climatizado) |
| Potencia electrica del compresor al diseno | 559 kW (COP 3,56, condensacion a 46 C) |
| Carga de calefaccion de diseno de invierno (aire) | 649 kW |
| Demanda media de ACS | 43 kW (100 L/cama y dia) |

## 2. Desglose por uso final

| Uso | Energia [MWh/anio] | % del total | kWh/m2 cubierto |
|---|---|---|---|
| Electricidad: compresor de la enfriadora | 714 | 23,6 % | 38,9 |
| Electricidad: ventiladores de las unidades de tratamiento de aire | 847 | 28,0 % | 46,1 |
| Electricidad: ventiladores del condensador | 105 | 3,5 % | 5,7 |
| Electricidad: bombas de agua helada | 70 | 2,3 % | 3,8 |
| Gas: recalentamiento despues de la serpentina | 629 | 20,8 % | 34,3 |
| Gas: calefaccion del aire | 194 | 6,4 % | 10,6 |
| Gas: humidificacion con vapor | 0 | 0,0 % | 0,0 |
| Gas: agua caliente sanitaria | 461 | 15,3 % | 25,1 |
| **Total** | **3.021** | 100 % | **164,6** |

El recalentamiento es el 49 % del calor util que entrega la caldera (511 MWh de 1.044 MWh): el aire se enfria para deshumidificar y luego se recalienta con gas. Es la ineficiencia que la alternativa B (recuperacion de calor del condensador) busca aprovechar; el calor que la enfriadora rechaza en el ano es 4.198 MWh.

Frio entregado en el ano: 3.526 MWh. COP estacional del compresor: 4,94. COP estacional de la planta (compresor, ventiladores del condensador y bombas): 3,96. Horas equivalentes a plena carga de refrigeracion: 1.775 h.

## 3. Por zona

| Zona | Superficie [m2] | Caudal de impulsion [m3/h] | Aire exterior [m3/h] | Serpentina [MWh] | Recalentamiento [MWh] | Calefaccion [MWh] | Ventiladores [MWh] |
|---|---|---|---|---|---|---|---|
| G1 Quirofanos | 252 | 15.120 | 3.024 | 245 | 89 | 3 | 110 |
| G2 Terapia intensiva | 336 | 6.048 | 2.016 | 150 | 4 | 0 | 37 |
| G3 Internacion general | 4.032 | 54.711 | 24.192 | 972 | 149 | 99 | 200 |
| G4 Guardia, diagnostico por imagenes y laboratorio (24 h) | 3.843 | 92.225 | 23.056 | 1.308 | 264 | 56 | 374 |
| G5 Consultorios, administracion y docencia (de dia) | 7.136 | 96.670 | 21.409 | 850 | 5 | 0 | 126 |

## 4. Puntos de diseno

Verano: 34 C de bulbo seco, 25 C de bulbo humedo coincidente, W = 16,26 g/kg, actividad plena y ganancia solar pico. Invierno: 2 C y 80 % de humedad relativa, sin ganancias internas.

| Zona | T mezcla [C] | T salida serpentina [C] | T impulsion [C] | Serpentina [kW] | sensible [kW] | latente [kW] | Recalentamiento [kW] | Invierno: calefaccion [kW] | Invierno: humidificacion [kW] |
|---|---|---|---|---|---|---|---|---|---|
| G1 | 24,4 | 13,0 | 19,1 | 79 | 59 | 21 | 19 | 8 | 4 |
| G2 | 26,7 | 12,3 | 14,3 | 47 | 30 | 17 | 0 | 12 | 3 |
| G3 | 28,4 | 11,8 | 13,0 | 527 | 311 | 216 | 0 | 189 | 30 |
| G4 | 26,5 | 15,2 | 16,6 | 525 | 355 | 170 | 0 | 159 | 28 |
| G5 | 26,2 | 11,8 | 13,0 | 810 | 475 | 334 | 0 | 189 | 26 |
| **Total** | | | | **1.987** | 1.230 | 758 | 19 | 649 | |

## 5. Ciclo de refrigeracion al punto de diseno de verano

Refrigerante R134a, evaporacion a 3 C (326 kPa), condensacion a 46 C (1.190 kPa).

| Estado | Descripcion | T [C] | h [kJ/kg] |
|---|---|---|---|
| 1 | Salida del evaporador (vapor sobrecalentado 5 K) | 8,0 | 404,9 |
| 2s | Salida del compresor, isentropica | | 432,6 |
| 2 | Salida del compresor, real (rendimiento isentropico 0,72) | 64,9 | 443,3 |
| 3 | Salida del condensador (subenfriado 4 K) | 42,0 | 259,4 |
| 4 | Salida de la valvula de expansion (titulo 0,28) | 3,0 | 259,4 |

Efecto frigorifico 145,5 kJ/kg, trabajo de compresion 38,5 kJ/kg, calor rechazado 184,0 kJ/kg. COP sobre el eje 3,78; COP sobre la potencia electrica del compresor 3,56; COP de Carnot entre 3 C y 46 C: 6,42. Caudal de refrigerante al diseno: 13,66 kg/s.

## 6. Combustion y caldera

Por kmol de gas natural, con relacion de aire 1,15:

| Reactivos | kmol | Productos | kmol |
|---|---|---|---|
| Gas natural | 1,000 | CO2 | 1,050 |
| O2 | 2,352 | H2O | 2,010 |
| N2 del aire | 8,847 | N2 | 8,867 |
| | | O2 | 0,307 |

Aire estequiometrico: 9,738 kmol/kmol de gas. Control de atomos C, H, O y N: cierra.

| Magnitud | Valor |
|---|---|
| Poder calorifico superior | 38,50 MJ/m3 = 9.196 kcal/m3 = 10,695 kWh/m3 (m3 estandar a 15 C) |
| Poder calorifico inferior | 34,76 MJ/m3 = 9,656 kWh/m3 |
| Relacion PCS/PCI | 1,1076 |
| Perdida por gases de escape (190 C) | 8,0 % del PCI |
| **Rendimiento de la caldera** | **90,0 % sobre PCI** (81,2 % sobre PCS) |
| Fraccion molar de agua en los gases | 16,4 % |
| Temperatura de rocio de los gases | 56,1 C (la chimenea a 190 C no condensa) |
| Temperatura de llama adiabatica (sin disociacion) | 1.848 C |
| Gas consumido por kWh util | 0,1151 m3 |

## 7. Perfil mensual

| Mes | T media [C] | Frio entregado [MWh] | Calor de aire [MWh] | Electricidad del compresor [MWh] | COP del compresor |
|---|---|---|---|---|---|
| ene | 24,9 | 595 | 129 | 131 | 4,54 |
| feb | 23,7 | 512 | 120 | 109 | 4,69 |
| mar | 22,0 | 383 | 36 | 82 | 4,65 |
| abr | 18,3 | 264 | 45 | 51 | 5,20 |
| may | 14,6 | 159 | 17 | 28 | 5,75 |
| jun | 11,6 | 139 | 39 | 24 | 5,75 |
| jul | 10,9 | 136 | 46 | 24 | 5,75 |
| ago | 12,3 | 152 | 35 | 26 | 5,75 |
| sep | 14,2 | 149 | 19 | 26 | 5,75 |
| oct | 17,6 | 211 | 9 | 40 | 5,32 |
| nov | 20,6 | 308 | 38 | 63 | 4,85 |
| dic | 23,4 | 519 | 134 | 110 | 4,72 |

## 8. Contraste con las referencias

Las referencias miden el edificio completo (iluminacion, equipos medicos, cocina y lavanderia), y este modelo solo el sistema termico. Para comparar, se estima el consumo total equivalente suponiendo que el sistema termico es una fraccion del total, con las participaciones que citan las fuentes del articulo de Hospitecnia.

| Participacion del sistema termico en el total | Fraccion | Total equivalente [kWh/m2 y anio] |
|---|---|---|
| Hospitecnia (10): 45 % climatizacion + 20 % ACS | 65 % | 253 |
| BID (13): 51 % climatizacion + 12 % ventilacion y bombas + 6 % ACS | 69 % | 239 |
| Hospital de Madrid (5): 40 % calefaccion + 20 % refrigeracion + 6 % ventilacion + 7 % ACS | 73 % | 226 |
| Chile (11): 36 % termico x (54 % climatizacion + 30 % agua caliente) + 64 % electrico x (21 % climatizacion + 3 % ACS) | 46 % | 361 |

Con esas participaciones, el consumo total equivalente del edificio queda entre **226 y 361 kWh/m2 y anio**.

| Referencia | kWh/m2 y anio | Observacion |
|---|---|---|
| Garrahan (CABA), HCWH 2021, H-01 | 259 | Edificio completo, estimado por auditoria |
| CEMAR (Rosario), HCWH 2021, H-02 | 211 | Edificio completo, estimado por auditoria |
| Giordano (San Juan), HCWH 2021, H-03 | 163 | Edificio completo, estimado por auditoria |
| Modelo espanol del articulo (Hospitecnia, D-60) | 380 | Calor util mas electricidad |
| Mismo modelo en energia final (Hospitecnia, E-16) | 394 a 400 | Edificio completo |
| 23 hospitales internacionales (Hospitecnia, D-61) | mediana 333; media 387; rango 120 a 900 | Edificio completo |
| **Este modelo, solo sistema termico** | **165** | Equivale a 226 a 361 para el edificio completo |

## 9. Sensibilidad

Cada fila cambia un supuesto y deja los demas en su valor base (3.021 MWh/anio, 165 kWh/m2).

| Variacion | Energia final [MWh/anio] | Diferencia |
|---|---|---|
| Humedad relativa de verano 5 puntos menos (todas las zonas) | 3.706 | +22,7 % |
| Consultorios y administracion tambien funcionan 24 h | 3.644 | +20,6 % |
| Ventilador sin calor en el aire (sin calor de ventilador) | 3.574 | +18,3 % |
| ACS por cama: 200 L/dia | 3.483 | +15,3 % |
| Temperatura media mensual +2 K | 3.463 | +14,6 % |
| Temperatura media mensual -2 K | 2.608 | -13,7 % |
| Guardia, diagnostico y laboratorio: 50 % de las areas generales | 3.409 | +12,8 % |
| Guardia, diagnostico y laboratorio: 20 % de las areas generales | 2.633 | -12,8 % |
| Humedad relativa media -8 puntos | 2.773 | -8,2 % |
| Superficie climatizada 95 % | 3.263 | +8,0 % |
| Superficie climatizada 75 % | 2.780 | -8,0 % |
| ACS por cama: 55 L/dia | 2.814 | -6,9 % |
| Humedad maxima de verano 60 % en quirofanos, terapia intensiva e internacion | 2.841 | -6,0 % |
| Aire exterior minimo +25 % | 3.180 | +5,3 % |
| Ventiladores: presion +30 % (proxy de ventiladores de retorno) | 3.159 | +4,6 % |
| Humedad relativa media +8 puntos | 3.155 | +4,4 % |
| Caldera con perdidas de ciclado (f_rad 10 %) | 3.147 | +4,2 % |
| Aire exterior minimo -25 % | 2.929 | -3,0 % |
| Conductancia de la envolvente +30 % | 3.102 | +2,7 % |
| Rendimiento isentropico 0,65 | 3.100 | +2,6 % |
| Conductancia de la envolvente -30 % | 2.945 | -2,5 % |
| Quirofanos: 25 renovaciones totales | 3.094 | +2,4 % |
| Consultorios y administracion de lunes a sabado (6/7) | 3.091 | +2,3 % |
| Quirofanos: 15 renovaciones totales | 2.952 | -2,3 % |
| Rendimiento isentropico 0,78 | 2.965 | -1,9 % |
| Gases de escape a 230 C | 3.049 | +0,9 % |
| Ganancias internas -30 % | 3.042 | +0,7 % |
| Gases de escape a 160 C | 3.002 | -0,7 % |
| Ganancias internas +30 % | 3.006 | -0,5 % |
| Exceso de aire 30 % (lambda 1,30) | 3.034 | +0,4 % |
| Exceso de aire 5 % (lambda 1,05) | 3.013 | -0,3 % |

Cada variacion por separado mueve el resultado entre 142 y 202 kWh/m2 y anio.

## 10. Chequeos termodinamicos

Los ejecuta `python -m pytest calculo/tests`. Resultado de la ultima corrida: ver la salida de pytest.

- Primera ley: la carga de diseno es la suma de las serpentinas; el calor rechazado es el frio entregado mas el trabajo en el eje.
- Segunda ley: el COP del ciclo y el COP mensual son menores que el de Carnot.
- Combustion: el balance de atomos de C, H, O y N cierra; PCS mayor que PCI; la diferencia es el calor latente del agua formada.
- Aire humedo: la psicrometria coincide con CoolProp dentro de 1,2 %; el balance de entalpia de la corriente de aire cierra.
- Estas verificaciones comprueban la coherencia interna. La verificacion de fondo es la reimplementacion independiente a partir de `calculo/ESPECIFICACION.md`.
