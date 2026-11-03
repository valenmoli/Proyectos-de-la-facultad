# calculo/

Motor de cálculo en Python (hito **M3**, Consigna 3). Es la **única fuente de verdad** de los números: el informe, la memoria, las figuras y las diapositivas se generan desde acá.

## Módulos previstos
| Módulo | Contenido |
|---|---|
| `refrigeracion` | Ciclo de compresión: capacidad frigorífica, trabajo del compresor, COP, calor rechazado |
| `aire_humedo` | Propiedades psicrométricas, mezcla, serpentina, recalentamiento, cargas sensible y latente |
| `combustion` | Reacción y balance, exceso de aire, energía liberada, consumo de gas, temperatura de rocío de los gases |
| `exergia` | Balance por equipo, destrucción de exergía, eficiencia exergética |
| `tests/` | Chequeos termodinámicos del PRD §4 (1.ª ley, 2.ª ley, balance atómico, psicrometría) |

## Dependencias previstas
`numpy`, `scipy`, `CoolProp`, `psychrolib`, `matplotlib`, `pytest` (instalables desde PyPI).

## Estado
Sin código todavía. Se escribe después de aprobar el [PRD](../PRD.md) y de cerrar los hitos M1 y M2.
