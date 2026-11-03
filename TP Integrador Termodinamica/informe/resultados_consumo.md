# Resultados de la estimacion de consumos

*Generado por `calculo/generar_resultados.py`. No editar a mano: se regenera con el codigo.*

Hospital modelado: Favaloro (La Matanza), AMBA. Frontera: sistema termico (frio, recalentamiento, calefaccion, humidificacion y agua caliente sanitaria) y sus auxiliares (ventiladores, bombas, ventiladores del condensador). Energia final: electricidad mas gas natural medido por su poder calorifico superior.

## 1. Resultado principal

| Magnitud | Valor |
|---|---|
| Superficie cubierta | 18.352 m2 |
| Superficie climatizada | 15.599 m2 (85 % de la cubierta) |
| Electricidad anual | 1.609 MWh |
| Gas natural anual (PCS) | 1.712 MWh = 160 mil m3 |
| **Energia final anual** | **3.320 MWh** |
| **Intensidad sobre superficie cubierta** | **181 kWh/m2 y anio** (88 electricidad + 93 gas) |
| Intensidad sobre superficie climatizada | 213 kWh/m2 y anio |
| Participacion del gas | 52 % |
| Capacidad frigorifica de diseno | 1.813 kW (99 W/m2 cubierto; 116 W/m2 climatizado) |
| Potencia electrica del compresor al diseno | 510 kW (COP 3,56, condensacion a 46 C) |
| Carga de calefaccion de diseno de invierno (aire) | 771 kW |
| Demanda media de ACS | 43 kW (100 L/cama y dia) |

## 2. Desglose por uso final

| Uso | Energia [MWh/anio] | % del total | kWh/m2 cubierto |
|---|---|---|---|
| Electricidad: compresor de la enfriadora | 678 | 20,4 % | 36,9 |
| Electricidad: ventiladores de las unidades de tratamiento de aire | 767 | 23,1 % | 41,8 |
| Electricidad: ventiladores del condensador | 98 | 3,0 % | 5,4 |
| Electricidad: bombas de agua helada | 66 | 2,0 % | 3,6 |
| Gas: recalentamiento despues de la serpentina | 832 | 25,1 % | 45,3 |
| Gas: calefaccion del aire | 418 | 12,6 % | 22,8 |
| Gas: humidificacion con vapor | 0 | 0,0 % | 0,0 |
| Gas: agua caliente sanitaria | 461 | 13,9 % | 25,1 |
| **Total** | **3.320** | 100 % | **180,9** |

El recalentamiento es el 49 % del calor util que entrega la caldera (676 MWh de 1.390 MWh): el aire se enfria para deshumidificar y luego se recalienta con gas. Es la ineficiencia que la alternativa B (recuperacion de calor del condensador) busca aprovechar; el calor que la enfriadora rechaza en el ano es 3.937 MWh.

Frio entregado en el ano: 3.300 MWh. COP estacional del compresor: 4,87. COP estacional de la planta (compresor, ventiladores del condensador y bombas): 3,92. Horas equivalentes a plena carga de refrigeracion: 1.820 h.

## 3. Por zona

| Zona | Superficie [m2] | Caudal de impulsion [m3/h] | Aire exterior [m3/h] | Serpentina [MWh] | Recalentamiento [MWh] | Calefaccion [MWh] | Ventiladores [MWh] |
|---|---|---|---|---|---|---|---|
| G1 Quirofanos | 252 | 15.120 | 3.024 | 214 | 135 | 36 | 86 |
| G2 Terapia intensiva | 336 | 6.048 | 2.016 | 130 | 21 | 0 | 25 |
| G3 Internacion general | 4.032 | 54.711 | 24.192 | 904 | 223 | 155 | 200 |
| G4 Guardia, diagnostico por imagenes y laboratorio (24 h) | 3.843 | 69.169 | 23.056 | 977 | 212 | 148 | 281 |
| G5 Consultorios, administracion y docencia (de dia) | 7.136 | 96.670 | 21.409 | 1.075 | 85 | 0 | 176 |

## 4. Puntos de diseno

Verano: 34 C de bulbo seco, 25 C de bulbo humedo coincidente, W = 16,26 g/kg, actividad plena y ganancia solar pico. Invierno: 2 C y 80 % de humedad relativa, sin ganancias internas.

| Zona | T mezcla [C] | T salida serpentina [C] | T impulsion [C] | Serpentina [kW] | sensible [kW] | latente [kW] | Recalentamiento [kW] | Invierno: calefaccion [kW] | Invierno: humidificacion [kW] |
|---|---|---|---|---|---|---|---|---|---|
| G1 | 24,4 | 13,0 | 19,1 | 79 | 59 | 21 | 31 | 20 | 4 |
| G2 | 26,7 | 13,4 | 14,3 | 41 | 27 | 14 | 2 | 16 | 3 |
| G3 | 28,4 | 13,0 | 13,0 | 473 | 288 | 185 | 0 | 211 | 30 |
| G4 | 27,4 | 14,1 | 14,1 | 506 | 312 | 194 | 0 | 201 | 29 |
| G5 | 26,2 | 13,0 | 13,0 | 714 | 435 | 279 | 0 | 229 | 27 |
| **Total** | | | | **1.813** | 1.122 | 691 | 33 | 771 | |

## 5. Ciclo de refrigeracion al punto de diseno de verano

Refrigerante R134a, evaporacion a 3 C (326 kPa), condensacion a 46 C (1.190 kPa).

| Estado | Descripcion | T [C] | h [kJ/kg] |
|---|---|---|---|
| 1 | Salida del evaporador (vapor sobrecalentado 5 K) | 8,0 | 404,9 |
| 2s | Salida del compresor, isentropica | | 432,6 |
| 2 | Salida del compresor, real (rendimiento isentropico 0,72) | 64,9 | 443,3 |
| 3 | Salida del condensador (subenfriado 4 K) | 42,0 | 259,4 |
| 4 | Salida de la valvula de expansion (titulo 0,28) | 3,0 | 259,4 |

Efecto frigorifico 145,5 kJ/kg, trabajo de compresion 38,5 kJ/kg, calor rechazado 184,0 kJ/kg. COP sobre el eje 3,78; COP sobre la potencia electrica del compresor 3,56; COP de Carnot entre 3 C y 46 C: 6,42. Caudal de refrigerante al diseno: 12,46 kg/s.

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
| ene | 24,9 | 583 | 157 | 129 | 4,50 |
| feb | 23,7 | 503 | 147 | 108 | 4,65 |
| mar | 22,0 | 368 | 61 | 80 | 4,58 |
| abr | 18,3 | 257 | 85 | 50 | 5,17 |
| may | 14,6 | 135 | 48 | 23 | 5,75 |
| jun | 11,6 | 113 | 67 | 20 | 5,75 |
| jul | 10,9 | 108 | 75 | 19 | 5,75 |
| ago | 12,3 | 126 | 64 | 22 | 5,75 |
| sep | 14,2 | 124 | 47 | 21 | 5,75 |
| oct | 17,6 | 187 | 36 | 35 | 5,31 |
| nov | 20,6 | 290 | 64 | 61 | 4,77 |
| dic | 23,4 | 507 | 164 | 109 | 4,67 |

## 8. Contraste con las referencias

Las referencias miden el edificio completo (iluminacion, equipos medicos, cocina y lavanderia), y este modelo solo el sistema termico. Para comparar, se estima el consumo total equivalente suponiendo que el sistema termico es una fraccion del total, con las participaciones que citan las fuentes del articulo de Hospitecnia.

| Participacion del sistema termico en el total | Fraccion | Total equivalente [kWh/m2 y anio] |
|---|---|---|
| Hospitecnia (10): 45 % climatizacion + 20 % ACS | 65 % | 278 |
| BID (13): 51 % climatizacion + 12 % ventilacion y bombas + 6 % ACS | 69 % | 262 |
| Hospital de Madrid (5): 40 % calefaccion + 20 % refrigeracion + 6 % ventilacion + 7 % ACS | 73 % | 248 |
| Chile (11): 36 % termico x (54 % climatizacion + 30 % agua caliente) + 64 % electrico x (21 % climatizacion + 3 % ACS) | 46 % | 397 |

Con esas participaciones, el consumo total equivalente del edificio queda entre **248 y 397 kWh/m2 y anio**.

| Referencia | kWh/m2 y anio | Observacion |
|---|---|---|
| Garrahan (CABA), HCWH 2021, H-01 | 259 | Edificio completo, estimado por auditoria |
| CEMAR (Rosario), HCWH 2021, H-02 | 211 | Edificio completo, estimado por auditoria |
| Giordano (San Juan), HCWH 2021, H-03 | 163 | Edificio completo, estimado por auditoria |
| Modelo espanol del articulo (Hospitecnia, D-60) | 380 | Calor util mas electricidad |
| Mismo modelo en energia final (Hospitecnia, E-16) | 394 a 400 | Edificio completo |
| 23 hospitales internacionales (Hospitecnia, D-61) | mediana 333; media 387; rango 120 a 900 | Edificio completo |
| **Este modelo, solo sistema termico** | **181** | Equivale a 248 a 397 para el edificio completo |

## 9. Sensibilidad

Cada fila cambia un supuesto y deja los demas en su valor base (3.320 MWh/anio, 181 kWh/m2).

| Variacion | Energia final [MWh/anio] | Diferencia |
|---|---|---|
| Consultorios y administracion tambien funcionan 24 h | 4.408 | +32,8 % |
| Humedad relativa de verano 5 puntos menos (todas las zonas) | 4.079 | +22,9 % |
| ACS por cama: 200 L/dia | 3.782 | +13,9 % |
| Temperatura media mensual +2 K | 3.777 | +13,7 % |
| Temperatura media mensual -2 K | 2.874 | -13,4 % |
| Humedad relativa media -8 puntos | 3.012 | -9,3 % |
| Guardia, diagnostico y laboratorio: 20 % de las areas generales | 3.033 | -8,6 % |
| Guardia, diagnostico y laboratorio: 50 % de las areas generales | 3.607 | +8,6 % |
| Superficie climatizada 75 % | 3.065 | -7,7 % |
| Superficie climatizada 95 % | 3.576 | +7,7 % |
| Aire exterior minimo +25 % | 3.530 | +6,3 % |
| ACS por cama: 55 L/dia | 3.113 | -6,3 % |
| Humedad relativa media +8 puntos | 3.496 | +5,3 % |
| Aire exterior minimo -25 % | 3.205 | -3,5 % |
| Conductancia de la envolvente +30 % | 3.426 | +3,2 % |
| Conductancia de la envolvente -30 % | 3.215 | -3,2 % |
| Quirofanos: 25 renovaciones totales | 3.402 | +2,5 % |
| Quirofanos: 15 renovaciones totales | 3.239 | -2,5 % |
| Rendimiento isentropico 0,65 | 3.395 | +2,2 % |
| Rendimiento isentropico 0,78 | 3.267 | -1,6 % |
| Ganancias internas -30 % | 3.367 | +1,4 % |
| Ganancias internas +30 % | 3.365 | +1,4 % |
| Gases de escape a 230 C | 3.357 | +1,1 % |
| Gases de escape a 160 C | 3.294 | -0,8 % |
| Exceso de aire 30 % (lambda 1,30) | 3.338 | +0,5 % |
| Exceso de aire 5 % (lambda 1,05) | 3.309 | -0,3 % |

Cada variacion por separado mueve el resultado entre 157 y 240 kWh/m2 y anio.

## 10. Chequeos termodinamicos

Los ejecuta `python -m pytest calculo/tests`. Resultado de la ultima corrida: ver la salida de pytest.

- Primera ley: la carga de diseno es la suma de las serpentinas; el calor rechazado es el frio entregado mas el trabajo en el eje.
- Segunda ley: el COP del ciclo y el COP mensual son menores que el de Carnot.
- Combustion: el balance de atomos de C, H, O y N cierra; PCS mayor que PCI; la diferencia es el calor latente del agua formada.
- Aire humedo: la psicrometria coincide con CoolProp dentro de 1,2 %; el balance de entalpia de la corriente de aire cierra.
- Estas verificaciones comprueban la coherencia interna. La verificacion de fondo es la reimplementacion independiente a partir de `calculo/ESPECIFICACION.md`.
