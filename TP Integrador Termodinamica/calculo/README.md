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
| `mejoras` | Alternativa B y mejoras de sustentabilidad (caldera de condensación, solar térmico, fotovoltaica, recuperador del aire de extracción, ventiladores, quirófanos de noche, refrigerantes) con emisiones de CO₂ |
| `exergia` | Balance exergético por equipo en dos estados (verano pico y máximo recalentamiento) y sensibilidad al estado muerto |
| `equipos` | Selección de enfriadoras, calderas, UTAs, hidráulica, shafts, azotea y niveles; matriz de ubicación |
| `supuestos` | Tabla de entradas con su estado (dato, supuesto o constante) |
| `generar_resultados` | Escribe `informe/supuestos.md`, `informe/resultados_consumo.md` y `.json` |
| `figuras`, `figuras_mejoras`, `figuras_exergia`, `figuras_plano` | Generan las figuras de `figuras/` |
| `construir_documentos`, `texto_equipos`, `texto_exergia`, `estilo_docx` | Arman el informe técnico y la memoria de cálculo (`.md`, `.docx` con ecuaciones nativas y `.pdf`) desde las plantillas y el modelo |
| `tests/` | Chequeos termodinámicos (1.ª ley, 2.ª ley, balance atómico, psicrometría, exergía, equipos, mejoras) |

## Uso (desde la carpeta del proyecto)
```
pip install -r calculo/requirements.txt
python -m pytest calculo/tests
python -m calculo.generar_resultados     # tablas y JSON del informe
python -m calculo.figuras                # figuras 1 a 6 (también figuras_mejoras, figuras_exergia, figuras_plano)
python -m calculo.construir_documentos   # informe técnico y memoria de cálculo (necesita pandoc y Chromium para el PDF)
```

## Estado
Modelo del sistema térmico (alternativa A) verificado de forma independiente; la alternativa B, las mejoras, la exergía y los equipos tienen revisiones internas independientes pero no reimplementación. La especificación para reimplementarlo está en [`ESPECIFICACION.md`](ESPECIFICACION.md).
