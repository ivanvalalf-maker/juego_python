# Guía rápida de sustentación – Fase 2

## Archivos
| Archivo | Contenido |
|---|---|
| `ABP_Fase2_Generacion_Hidroelectrica_ElNino.docx` / `.pdf` | Documento APA 7 completo (Fase 1 corregida + Fase 2) |
| `generacion_hidro_nino.py` | Programa en Python (menú, condicionales y ciclos) |
| `pseudocodigo_fase2.psc` | Pseudocódigo PSeInt de la Fase 2 |

## Cómo ejecutar
1. Abrir una terminal en esta carpeta.
2. `python generacion_hidro_nino.py`
3. Para el Escenario 1: opción 1 → `R1, 30, 500, 2500, 1750, 610, 240`; opción 2 tres veces:
   - `CH-1, 330, 200, 175, 0.90, 290`
   - `CH-2, 195, 130, 150, 0.88, 165`
   - `CH-3, 85, 55, 120, 0.86, 60`
   - opción 4 → debe dar **255,34 GWh, NORMAL, OPERACIÓN NORMAL**.

## Qué explicar (en orden)
1. **Observaciones de la Fase 1** (Tabla 13): se corrigió la autonomía, se reemplazaron las referencias CREG/XM y se probó la validación por central.
2. **Ciclos**: `while` repite el menú y repite cada pregunta hasta recibir un dato válido; `for` recorre la lista de centrales para buscar repetidas, consultar y generar el reporte.
3. **Condicionales**: simple (nombre repetido), doble (limitar potencia), múltiple `if/elif/else` (estado de la central y riesgo), anidada (menú con RN-09), compuesta `and/or` (alerta).
4. **Reglas de negocio** RN-01 a RN-11 (Tabla 15).
5. **Matrices de decisiones** (Tablas 17–19) y **pruebas de escritorio** (Tablas 22–24).

## Preguntas probables
| Pregunta | Respuesta corta |
|---|---|
| ¿Por qué `try/except`? | `int()` y `float()` fallan si se escriben letras; `except ValueError` evita que el programa se cierre. |
| ¿Por qué cambió la autonomía? | Antes usaba el agua turbinada real; en sequía se turbina menos y la autonomía "subía". Ahora usa el agua necesaria para cubrir la demanda. |
| ¿Qué es una central "LIMITADA"? | Su potencia hidráulica supera la nominal; el agua sobrante se vierte sin generar energía. |
| ¿Cómo se relaciona con instalaciones deficientes? | El estado de cada central detecta vertimiento, subutilización (FP < 30 %) y eficiencia baja (η < 0,85). |
