# 🐍 Python Quest: El Despertar del Código

RPG de texto para consola que enseña Python desde cero mediante retos interactivos.

## Ejecución

```bash
python3 main.py      # Requiere Python 3.8+ (solo biblioteca estándar)
```

## Niveles

| Nivel | Tema | Escenario | Retos |
|---|---|---|---|
| 1 | Variables y tipos (`int`, `float`, `str`, `bool`) | La Biblioteca de las Variables | 5 |
| 2 | Condicionales (`if`, `elif`, `else`) | El Puente de las Decisiones | 4 |
| 3 | Bucles (`for`, `while`) | Las Minas del Eterno Retorno | 5 |
| 4 | Funciones y `return` | La Torre del Hechizo Reutilizable | 5 |

## Mecánicas

| Elemento | Regla |
|---|---|
| Vidas | 3 iniciales; cada respuesta incorrecta resta 1; completar un nivel devuelve 1 |
| XP | Recompensa por reto; cada fallo previo reduce ⅓ (mínimo 5 XP) |
| Rangos | Cada 100 XP: Aprendiz → Iniciado → Hechicero del Código → Archimago Pythonista |
| Pistas | Aparecen tras el primer fallo |
| Tipos de reto | Opción múltiple, escribir código, predecir la salida |

## Estructura

```
main.py                    Punto de entrada
python_quest/
├── utilidades.py          Entrada segura (try/except), formato de pantalla
├── jugador.py             Clase Jugador: vidas, XP, rangos
├── retos.py               Clase base Reto + 3 subclases (herencia)
├── niveles.py             Contenido: historia, teoría y retos (datos)
└── juego.py               Motor: menú, bucle de niveles, resumen final
```

## Cómo añadir un nivel

1. En `python_quest/niveles.py`, crea `crear_nivel_5()` que devuelva un `Nivel(...)`.
2. Añádela al final de la lista `NIVELES`.
3. Actualiza el texto del menú de selección en `juego.py` (`partida()`).
