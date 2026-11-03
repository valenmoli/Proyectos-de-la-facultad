# Supuestos y datos de entrada del modelo

*Generado por `calculo/generar_resultados.py` desde `calculo/supuestos.py`. No editar a mano.*

Estado: **DATO** = leido de un documento recibido; **SUPUESTO** = fundamentado pero sin fuente citable todavia; **CONSTANTE** = convencion o propiedad fisica.

| ID | Parametro | Valor | Unidad | Estado | Fuente o justificacion |
|---|---|---|---|---|---|
| E1 | Superficie cubierta total | 18352 | m2 | DATO | Presidencia de la Nacion, presentacion del Hospital Favaloro (datos/favaloro_nordelta.md, FA-03). Otra cifra: mas de 20.000 m2 (FA-04) |
| E2 | Fraccion de la superficie cubierta que se climatiza | 0,85 | - | SUPUESTO | Se climatiza casi todo (las circulaciones reciben aire de transferencia); no se climatizan locales tecnicos, morgue ni depositos. Rango en la sensibilidad: 75 a 95 % |
| E3 | Camas de internacion general | 144 | camas | DATO | Gobierno de la Provincia de Buenos Aires, 28/07/2020 (FA-06). Se interpreta como parte del total del hospital |
| E4 | Camas de terapia intensiva | 14 | camas | DATO | Idem (FA-06) |
| E5 | Cantidad de quirofanos | 6 | quirofanos | DATO | Presentacion de Presidencia (FA-07), cifra de programa |
| E6 | Superficie por quirofano | 42 | m2 | SUPUESTO | Quirofano general de 6 a 7 m de lado |
| E7 | Superficie por cama de terapia intensiva | 24 | m2/cama | SUPUESTO | Box de UTI con circulacion y apoyo |
| E8 | Superficie por cama de internacion general | 28 | m2/cama | SUPUESTO | Habitacion con bano y local de apoyo |
| E9 | Altura libre de los locales | 3 | m | SUPUESTO | Convencion de diseno |
| E10 | Conductancia de la envolvente por m2 de piso expuesto | 0,6 | W/(m2 K) | SUPUESTO | Edificio de tres pisos con 25 % de vidrio: techo, muros y vidrios en conjunto |
| E11 | Ganancia solar en el punto de diseno de verano | 20 | W/m2 | SUPUESTO | Hora pico, zonas expuestas |
| E12 | Ganancia solar media de las 12 h diurnas (anual) | 8 | W/m2 | SUPUESTO | Promedio diurno anual; es 0 de noche |
| E13 | Densidad del aire para convertir caudales | 1,2 | kg/m3 | CONSTANTE | Aire a unos 20 C |
| E14 | Fraccion de las areas generales climatizadas que funciona las 24 h (guardia, diagnostico por imagenes, laboratorio) | 0,35 | - | SUPUESTO | La gacetilla provincial dice que la guardia atiende las 24 h (datos/favaloro_nordelta.md, FA-09); el resto (consultorios, administracion, docencia) funciona de dia |
| C1 | Temperatura de bulbo seco de diseno, verano | 34 | C | SUPUESTO | Conocimiento general sobre Buenos Aires; reemplazar por dato del SMN o ASHRAE |
| C2 | Temperatura de bulbo humedo coincidente, verano | 25 | C | SUPUESTO | Idem |
| C3 | Temperatura de bulbo seco de diseno, invierno | 2 | C | SUPUESTO | Idem |
| C4 | Humedad relativa de diseno, invierno | 0,8 | - | SUPUESTO | Idem |
| C5 | Presion atmosferica | 101325 | Pa | CONSTANTE | Nivel del mar (Buenos Aires esta a unos 25 m: diferencia de 0,3 %) |
| C6 | Amplitud diaria de temperatura (maxima menos minima) | 9 | K | SUPUESTO | Aproximado; se usa para partir cada mes en mitad diurna y nocturna |
| A1 | Temperatura minima del aire de impulsion | 13 | C | CONSTANTE | Limite de confort y de condensacion en difusores |
| A2 | Temperatura maxima del aire de impulsion | 35 | C | CONSTANTE | Limite de calefaccion por aire |
| A3 | Humedad relativa del aire a la salida de la serpentina | 0,95 | - | CONSTANTE | Serpentina de agua helada con aproximacion al saturado |
| A4 | Temperatura exterior bajo la cual rigen las consignas de invierno | 18 | C | SUPUESTO | Criterio de cambio de estacion |
| A5 | Rendimiento total de los ventiladores | 0,6 | - | SUPUESTO | Ventilador, motor y transmision |
| A6 | Temperatura del agua de red (vapor de humidificacion) | 17 | C | SUPUESTO | Igual que la del ACS (S3): media anual aproximada de Buenos Aires |
| A8 | Fraccion de la potencia electrica del ventilador de impulsion que se disipa como calor en el aire | 1 | - | CONSTANTE | Ventilador que aspira despues de la serpentina; con el motor fuera de la corriente seria de 0,85 a 0,95 |
| A7 | Calor latente de vaporizacion del agua (referencia de 0 C) | 2501 | kJ/kg | CONSTANTE | Propiedades del agua |
| R1 | Refrigerante de la enfriadora | R134a | - | SUPUESTO | Enfriadora de tornillo; HFC habitual, propiedades en CoolProp |
| R2 | Temperatura de evaporacion | 3 | C | SUPUESTO | Agua helada 7/12 C con aproximacion del evaporador |
| R3 | Sobrecalentamiento a la salida del evaporador | 5 | K | SUPUESTO | Valor tipico |
| R4 | Subenfriamiento a la salida del condensador | 4 | K | SUPUESTO | Valor tipico |
| R5 | Rendimiento isentropico del compresor | 0,72 | - | SUPUESTO | Compresor de tornillo |
| R6 | Rendimiento del motor electrico del compresor | 0,94 | - | SUPUESTO | Valor tipico |
| R7 | Diferencia entre la temperatura de condensacion y la exterior | 12 | K | SUPUESTO | Condensador enfriado por aire |
| R8 | Temperatura minima de condensacion | 32 | C | SUPUESTO | Control de presion de descarga: el compresor de tornillo necesita una diferencia de presion minima |
| R9 | Potencia de ventiladores del condensador / calor rechazado | 0,025 | - | SUPUESTO | Valor tipico |
| R10 | Salto de temperatura del agua helada | 5 | K | SUPUESTO | Agua helada 7/12 C |
| R11 | Diferencia de presion de las bombas de agua helada | 250000 | Pa | SUPUESTO | Circuito primario y secundario en conjunto (equivale a unos 25 m de columna de agua) |
| R12 | Rendimiento total de las bombas | 0,6 | - | SUPUESTO | Valor tipico |
| B1 | Gas natural: metano | 0,91 | fraccion molar | SUPUESTO | Composicion tipica; verificar con ENARGAS |
| B2 | Gas natural: etano | 0,05 | fraccion molar | SUPUESTO | Idem |
| B3 | Gas natural: propano | 0,01 | fraccion molar | SUPUESTO | Idem |
| B4 | Gas natural: nitrogeno | 0,02 | fraccion molar | SUPUESTO | Idem |
| B5 | Gas natural: dioxido de carbono | 0,01 | fraccion molar | SUPUESTO | Idem |
| B6 | Relacion de aire (1 = estequiometrico) | 1,15 | - | SUPUESTO | 15 % de exceso de aire |
| B7 | Temperatura de los gases de escape | 190 | C | SUPUESTO | Caldera sin condensacion |
| B8 | Temperatura del aire de combustion | 15 | C | SUPUESTO | Sala de calderas. El gas se toma a 25 C, la referencia de las entalpias, y no aporta calor sensible |
| B9 | Perdidas por radiacion y funcionamiento / calor liberado | 0,02 | - | SUPUESTO | Valor tipico |
| B10 | Temperatura de referencia del volumen de gas | 15 | C | CONSTANTE | m3 estandar a 15 C y 101,325 kPa |
| S1 | Consumo de ACS por cama y dia | 100 | L/(cama dia) | SUPUESTO | Entre los casos medidos (50 a 55) y los ratios de diseno (200 a 300) del articulo de Hospitecnia (E-14) |
| S2 | Temperatura del ACS | 60 | C | DATO | Hospitecnia, ref. (7): 55 L/dia y cama a 60 C |
| S3 | Temperatura del agua fria de entrada | 17 | C | SUPUESTO | Media anual aproximada de Buenos Aires |
| S4 | Factor por perdidas de acumulacion y recirculacion | 1,3 | - | SUPUESTO | El articulo muestra 1,6 veces entre su tabla y el calor sensible (datos/hospitecnia_datos.md, seccion E) |

**Zonas termicas** (cada una es un sistema de aire de caudal constante):

| Zona | Nombre | ACH total | ACH aire ext. | q sens. | q lat. | f dia | f noche | T ver | HR ver | T inv | HR min inv | f env | dP vent. | Opera de noche | f dias | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G1 | Quirofanos | 20 | 4 | 60 W/m2 | 10 W/m2 | 0,8 | 0 | 22 C | 55 % | 22 C | 30 % | 0 | 1800 Pa | si | 1 | Condiciones y renovaciones de quirofano segun ASHRAE 170 (valores recordados, a verificar); HR de consigna 55 % = maximo 60 % menos 5 puntos de margen; presion del ventilador de 1.800 Pa por filtro HEPA, dos serpentinas y conductos; ganancias y horarios: supuesto |
| G2 | Terapia intensiva | 6 | 2 | 40 W/m2 | 8 W/m2 | 1 | 1 | 23 C | 55 % | 23 C | 30 % | 0,5 | 1500 Pa | si | 1 | Renovaciones de terapia intensiva segun ASHRAE 170 (valores recordados, a verificar); presion del ventilador de 1.500 Pa (filtro HEPA); ganancias: supuesto |
| G3 | Internacion general | 4 | 2 | 25 W/m2 | 5 W/m2 | 0,9 | 0,7 | 24 C | 55 % | 22 C | 30 % | 1 | 900 Pa | si | 1 | Habitacion de internacion segun ASHRAE 170 (valores recordados, a verificar); ganancias: supuesto |
| G4 | Guardia, diagnostico por imagenes y laboratorio (24 h) | 8 | 2 | 35 W/m2 | 8 W/m2 | 0,9 | 0,5 | 24 C | 60 % | 22 C | 30 % | 1 | 1000 Pa | si | 1 | Funciona las 24 h (la guardia atiende las 24 h segun la gacetilla provincial). 8 renovaciones = promedio ponderado de sala de espera y triage (12, 25 % del area), shock (15, 5 %) e imagenes y laboratorio (6, 70 %), valores de ASHRAE 170 recordados; ganancias: supuesto; HR de consigna 60 % (limite de confort) |
| G5 | Consultorios, administracion y docencia (de dia) | 3 | 1 | 25 W/m2 | 6 W/m2 | 0,9 | 0 | 24 C | 60 % | 22 C | 30 % | 1 | 900 Pa | no | 0,714286 | Funcionan 12 h por dia, de lunes a viernes (5/7 de los dias); renovaciones y ganancias: supuesto; HR de consigna 60 % (limite de confort) |

**Clima mensual aproximado** (SUPUESTO, conocimiento general; reemplazar por datos del SMN):

| Mes | ene | feb | mar | abr | may | jun | jul | ago | sep | oct | nov | dic |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Dias | 31 | 28 | 31 | 30 | 31 | 30 | 31 | 31 | 30 | 31 | 30 | 31 |
| T media [C] | 24,9 | 23,7 | 22 | 18,3 | 14,6 | 11,6 | 10,9 | 12,3 | 14,2 | 17,6 | 20,6 | 23,4 |
| HR media [%] | 66 | 70 | 73 | 75 | 78 | 79 | 77 | 73 | 71 | 70 | 67 | 65 |
