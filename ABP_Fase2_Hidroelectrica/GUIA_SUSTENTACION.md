# Guía rápida de sustentación – Fase 2

## Archivos
| Archivo | Contenido |
|---|---|
| `ABP_Fase2_Generacion_Hidroelectrica_ElNino.docx` / `.pdf` | Documento de la Fase 2 (12 páginas, con el código) |
| `generacion_hidro_nino.py` | Programa en Python (menú, condicionales y ciclos) |
| `pseudocodigo_fase2.psc` | Pseudocódigo en PSeInt |

## Cómo ejecutar
1. Abrir una terminal en esta carpeta y escribir `python generacion_hidro_nino.py`.
2. Opción 1 → `R1`, `30`, `500`, `85`, `385`, `240`.
3. Opción 2 tres veces:
   - `CH-1`, `200`, `175`, `0.90`, `290`
   - `CH-2`, `130`, `150`, `0.88`, `165`
   - `CH-3`, `55`, `120`, `0.86`, `60`
4. Opción 4 → debe dar **255,34 GWh, riesgo NORMAL, alerta OPERACIÓN NORMAL**.

## Cómo está hecho el programa (para explicarlo)
1. **Listas**: cada central se guarda en la misma posición de varias listas (`nombres`, `energias`, `estados`...).
2. **while del menú**: repite el menú hasta que se elige la opción 5.
3. **while de validación**: si un dato está fuera de rango, muestra un error y lo vuelve a pedir.
4. **for**: recorre las listas para buscar nombres repetidos, consultar una central y sumar en el reporte.
5. **if / elif / else**: escoge la opción del menú, el estado de la central y el riesgo.
6. **and / or**: se usan en las validaciones y en la alerta.

## Fórmulas
| Cálculo | Fórmula |
|---|---|
| Potencia bruta (MW) | 9,81 × caudal × altura × eficiencia / 1000 |
| Potencia efectiva | la menor entre la potencia bruta y la nominal |
| Energía (GWh) | potencia efectiva × horas / 1000 |
| Factor de planta (%) | potencia efectiva × horas / (potencia nominal × días × 24) × 100 |
| Cobertura (%) | energía total / demanda × 100 |
| Déficit (GWh) | demanda − energía total (si es positivo) |
| Índice de aportes | caudal total / caudal medio |

## Preguntas probables
| Pregunta | Respuesta corta |
|---|---|
| ¿Qué es una central LIMITADA? | Tiene más agua de la que su generador puede convertir; el sobrante se desperdicia. |
| ¿Qué es SUBUTILIZADA? | Su factor de planta es menor que 30 %: genera mucho menos de lo que podría. |
| ¿Cuándo hay El Niño en el programa? | Cuando el caudal total es menor que el 80 % del caudal medio (índice < 0,80). |
| ¿Por qué se usa `.upper()`? | Para que "ch-1" y "CH-1" se consideren el mismo nombre. |
| ¿Qué pasa si escribo una letra en un número? | El programa se detiene; es una limitación que se mejorará en la siguiente fase. |
| ¿Cómo responde al eje problematizador? | El estado de cada central muestra qué instalación tiene problemas. |
