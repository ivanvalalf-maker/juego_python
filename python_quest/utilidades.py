"""Funciones auxiliares de entrada/salida.

Centralizar aquí la lectura del teclado permite manejar TODOS los errores de
entrada en un solo lugar, en vez de repetir try/except por todo el código.
"""

import sys
import time

# Constante: en Python se escribe en MAYÚSCULAS por convención para indicar
# que su valor no debería cambiar durante la ejecución.
ANCHO = 64


def linea(caracter="═"):
    """Imprime una línea decorativa del ancho de la pantalla."""
    print(caracter * ANCHO)  # Multiplicar un str por un int lo repite.


def titulo(texto):
    """Imprime un título enmarcado y centrado."""
    linea()
    print(texto.center(ANCHO))  # .center() rellena con espacios a ambos lados.
    linea()


def narrar(texto, pausa=0.0):
    """Muestra texto narrativo; la pausa opcional da ritmo a la historia."""
    print(texto)
    if pausa > 0:
        time.sleep(pausa)


def pedir_texto(mensaje):
    """Lee una línea del usuario de forma segura.

    input() puede lanzar:
      - EOFError: si la entrada se cierra (Ctrl+D / Ctrl+Z, o un archivo vacío).
      - KeyboardInterrupt: si el usuario pulsa Ctrl+C.
    En ambos casos salimos del juego con un mensaje amable en lugar de mostrar
    un traceback que asustaría a un principiante.
    """
    try:
        return input(mensaje).strip()  # .strip() elimina espacios sobrantes.
    except (EOFError, KeyboardInterrupt):
        print("\n\n👋 Has abandonado la aventura. ¡Vuelve pronto, aprendiz!")
        sys.exit(0)


def pedir_entero(mensaje, minimo=None, maximo=None):
    """Pide un número entero y repite hasta que el usuario dé uno válido.

    Aquí está el corazón del manejo de errores: int("abc") lanza ValueError.
    Lo capturamos con try/except y volvemos a preguntar en un bucle while.
    """
    while True:  # Bucle "infinito" que solo termina con return.
        respuesta = pedir_texto(mensaje)
        try:
            numero = int(respuesta)
        except ValueError:
            print(f"  ⚠ '{respuesta}' no es un número entero. Ejemplo válido: 2")
            continue  # Salta al inicio del bucle para preguntar de nuevo.

        # Validamos el rango solo si se especificó (None = sin límite).
        if minimo is not None and numero < minimo:
            print(f"  ⚠ El número debe ser como mínimo {minimo}.")
        elif maximo is not None and numero > maximo:
            print(f"  ⚠ El número debe ser como máximo {maximo}.")
        else:
            return numero


def pausar():
    """Espera a que el jugador pulse Enter para continuar."""
    pedir_texto("\n[Pulsa Enter para continuar...]")


def normalizar_codigo(texto):
    """Normaliza código para compararlo de forma tolerante.

    - Unifica comillas simples y dobles ('hola' == "hola").
    - Elimina TODOS los espacios, así 'x=5' y 'x = 5' se consideran iguales.
    Es una simplificación pedagógica: en Python real los espacios a veces
    importan (p. ej. 'not x' vs 'notx'), pero en estos retos no afecta.
    """
    texto = texto.replace("'", '"')
    return "".join(texto.split())  # split() sin argumentos corta por cualquier espacio.
