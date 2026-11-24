# Guion de tu parte: diapositivas 10 a 12

**Borrador para que lo revises.** Está armado con las cifras del **informe que subió el grupo** (`TP_Integrador_Hospital_Favaloro`), que calcula **tres estados de diseño** y no un consumo anual: V1 es el pico de verano seco (33,9 °C), V2 el día húmedo de verano (25,9 °C, 16,8 g/kg) e I el invierno (1,1 °C).

- **Diapositiva 10** (la de tus compañeros, alternativa B): el guion sigue lo que dice esa diapositiva y la sección 4.1 del informe.
- **Diapositiva 11** (la nuestra, `diapositiva_11_mejoras.pptx`): las tres medidas del informe más tres ideas verdes, rotuladas aparte.
- **Diapositiva 12**: todavía no la vi. Mandame una captura y la sumo.

Tiempo: unos 3 min 45 s para la 10 y la 11. Lo que está entre corchetes se puede cortar.

## Antes de exponer

1. **Conclusión 4 del informe**: dice «B: −95 % de gas **en invierno**». Es en **V2 (verano húmedo)**; la sección 4.1 dice que en invierno B no aporta. En la exposición decí siempre «en V2». Conviene avisarle al grupo para que corrijan el texto.
2. **Rótulos**: las diapositivas de tus compañeros muestran «9 ·» y «10 ·» en el rótulo pero el número de página es 10 y 11. La nuestra lleva «10 · MEDIDAS DE MEJORA» para encajar en su serie; si cambian la numeración, se cambia también.
3. **Las ideas verdes no están en el informe.** Los porcentajes con asterisco son de una estimación aparte (modelo anual simple de nuestra memoria). Si el grupo prefiere no mostrar números que no están en el informe, se sacan de la diapositiva y quedan solo las ideas.

## Diapositiva 10: la alternativa B (≈ 1:30)

*(Señalá las tres tarjetas, sin leer el texto chico.)*

Hasta acá vimos cómo funciona el sistema base, la alternativa A, y dónde pierde. Lo más llamativo pasa el día húmedo de verano, el estado que llamamos V2: para sacarle la humedad al aire hay que enfriarlo de más, y después lo recalentamos con la caldera. Son **436 kW de recalentamiento**, el 91 % del calor que entrega la caldera ese día. Y al mismo tiempo, el condensador de la enfriadora **tira 1.418 kW de calor** al ambiente.

Nuestra alternativa B usa ese calor. Le agregamos a la enfriadora un segundo condensador, de agua, en paralelo con el de aire. Entrega agua a 35 °C al recalentador y además precalienta el agua caliente sanitaria. La caldera queda solo para terminar de calentar el ACS hasta 60 °C.

Los números, en V2: el gas baja de 55 a 3 m³ por hora, **95 % menos**, y las emisiones directas de CO₂ pasan de 108 a 6 kilos por hora. ¿Qué cuesta? **19 kW eléctricos más**: para que el agua llegue a 35 °C hay que condensar a 40 °C en lugar de 38, y el COP baja de 4,62 a 4,30. Pero por cada kW eléctrico de más recuperamos **23 kW de calor** que antes se perdía. [Y la exergía que entra al sistema baja de 988 a 484 kW, la mitad, porque dejamos de quemar gas a casi 1.850 °C para calentar aire unos pocos grados.]

Una aclaración: B solo ayuda cuando la enfriadora trabaja. En V1, el pico de verano seco, casi no hay recalentamiento para recuperar (19 kW), y en invierno no aporta. Por eso, para el invierno, evaluamos otras medidas.

## Diapositiva 11: mejoras (≈ 2:15)

*(Primero la fila de arriba, que es del informe; después la verde.)*

Para el invierno calculamos tres medidas con el mismo modelo; están en la tabla 14 del informe.

**M1, caldera de condensación.** Los humos salen por debajo del punto de rocío y se recupera el calor latente del vapor de agua. El rendimiento sube de 89,9 a 99,5 % y el gas baja 10 %. Ojo: la eficiencia exergética no mejora, porque la combustión sigue siendo la misma, con una llama de unos 1.850 °C.

**M2, recuperador de calor del aire expulsado.** Con dos serpentinas y agua, el aire que sale precalienta al que entra, sin mezclarlos. La calefacción baja de 438 a 187 kW y el gas, **46 %**; cuesta unos 10 kW más de ventiladores. Es la que ataca la causa: la cantidad de aire exterior que hay que calentar.

**M3, bomba de calor.** Usa la enfriadora al revés. Con un COP de 3,67 entrega los 438 kW con 119 kW eléctricos y ahorra 50 m³ de gas por hora. Su eficiencia exergética es de **43 %, contra 16 %** de la caldera: es la única que cambia el orden de magnitud. La limitación: pierde capacidad con frío, necesita desescarche y traslada las emisiones a la generación eléctrica, que no evaluamos.

*(Pasá a la franja verde.)*

[Además quisimos sumar tres ideas simples y verdes, que **no están en el modelo del informe**.] **Paneles solares en la azotea**: producen electricidad sin quemar gas. **Solar térmico**: el agua caliente sanitaria es calor de baja temperatura y el sol la entrega sin caldera. **Techos y fachadas verdes**: dan sombra y el agua que evaporan se lleva calor, así que entra menos calor al edificio y baja la temperatura interior.

Los porcentajes con asterisco son una **estimación aparte**, con un modelo anual simple y supuestos nuestros: unos 11 % de la energía anual con 250 kWp de paneles, 8 % con solar térmico y 4 % con techos verdes. **No son comparables** con los de arriba, que son gas en invierno en un estado de diseño. Lo que tienen en común todas es no gastar gas ni electricidad de la red donde alcanza calor de baja temperatura, sol o sombra.

## Diapositiva 12

*(Pendiente: mandame una captura o el texto y la armo en el mismo estilo.)*

## Si te preguntan

- **¿Por qué agua a 35 °C?** Es lo que necesita la serpentina de recalentamiento. Para que llegue a 35 °C hay que condensar a 40 °C como mínimo; mientras más caliente, más trabaja el compresor.
- **¿Por qué B no sirve en invierno?** Porque la enfriadora casi no trabaja, así que el condensador no entrega calor.
- **¿Por qué la caldera de condensación mejora el rendimiento pero no la eficiencia exergética?** Porque entrega el calor a menor temperatura y la irreversibilidad de la combustión queda intacta (16,3 → 14,2 %).
- **¿Y las emisiones de M3?** No se evaluaron las de la generación eléctrica ni los costos; el informe lo dice en las limitaciones.
- **¿Dónde está el cálculo de las ideas verdes?** En nuestra memoria, con un modelo anual simple (3.021 MWh/año de base). No es parte del informe entregado, que calcula tres estados de diseño. Los supuestos principales: azotea de unos 6.100 m², 250 kWp ocupan alrededor de la quinta parte, 300 m² de colectores y 20 % menos de calor por la envolvente en los techos verdes.
- **¿Por qué los techos verdes ahorran poco?** Porque el consumo está en el aire (renovaciones y humedad) y no en la envolvente. Se justifican más por comodidad y menor isla de calor.
- **¿Qué tan seguros son los porcentajes con asterisco?** Son órdenes de magnitud de un modelo con supuestos propios; los de arriba, en cambio, salen del modelo del informe.
