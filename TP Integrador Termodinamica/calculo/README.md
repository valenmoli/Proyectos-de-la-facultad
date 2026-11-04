# calculo/

Motor de cálculo en Python (hito **M3**, Consigna 3). Es la **única fuente de verdad** de los números: el informe, la memoria, las figuras y las diapositivas se generan desde acá.

## Módulos
| Módulo | Contenido |
|---|---|
| `aire_humedo` | Propiedades psicrométricas (psychrolib), mezcla, serpentina, cargas sensible y latente |
| `edificio` | Superficies, caudales por zona y tratamiento del aire de cada zona (con calor del ventilador) |
| `refrigeracion` | Ciclo de compresión de R134a: trabajo, COP, calor rechazado; COP según la temperatura exterior |
| `combustion` | Reacción y balance de átomos, PCS y PCI, rendimiento de la caldera, temperatura de rocío y de llama |
| `estimacion` | Puntos de diseño, consumo anual por mes (día y noche), ACS y sensibilidad |
| `supuestos` | Tabla de entradas con su estado (dato, supuesto o constante) |
| `generar_resultados` | Escribe `informe/supuestos.md`, `informe/resultados_consumo.md` y `.json` |
| `figuras` | Genera las seis figuras de `figuras/` |
| `construir_borrador` y `estilo_docx` | Arman `informe/borrador_proyecto` (`.md`, `.docx` con ecuaciones nativas y `.pdf`) desde la plantilla y el modelo |
| `exergia` | **Pendiente.** Balance por equipo, destrucción de exergía, eficiencia exergética |
| `tests/` | 49 chequeos termodinámicos (1.ª ley, 2.ª ley, balance atómico, psicrometría, tabla de supuestos) |

## Uso (desde la carpeta del proyecto)
```
pip install -r calculo/requirements.txt
python -m pytest calculo/tests
python -m calculo.generar_resultados     # tablas y JSON del informe
python -m calculo.figuras                # figuras
python -m calculo.construir_borrador     # borrador del informe (necesita pandoc y Chromium para el PDF)
```

## Estado
Modelo del sistema térmico (alternativa A) verificado de forma independiente. Falta la exergía, la alternativa B y las mejoras. La especificación para reimplementarlo está en [`ESPECIFICACION.md`](ESPECIFICACION.md).
