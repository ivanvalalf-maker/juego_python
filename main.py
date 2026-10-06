"""Punto de entrada de Python Quest: El Despertar del Código.

Ejecuta:  python main.py
"""

# Importamos solo la función principal: el resto del juego vive en el paquete
# `python_quest`. Separar el "arranque" de la lógica es una buena práctica.
from python_quest.juego import ejecutar

# Este bloque solo se ejecuta si el archivo se lanza directamente
# (y no si otro módulo lo importa). Es un patrón estándar en Python.
if __name__ == "__main__":
    ejecutar()
