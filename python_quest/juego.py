"""Motor del juego: menú, bucle principal y finales."""

from python_quest.jugador import Jugador
from python_quest.niveles import NIVELES
from python_quest.utilidades import (linea, narrar, pausar, pedir_entero,
                                     pedir_texto, titulo)


def pedir_nombre():
    """Pide el nombre del jugador; no acepta cadenas vacías."""
    while True:
        nombre = pedir_texto("¿Cuál es tu nombre, aprendiz? ")
        if nombre:
            return nombre[:20]  # Slicing: nos quedamos con 20 caracteres como máximo.
        print("  ⚠ Necesito un nombre para inscribirte en el Gran Libro.")


def mostrar_intro(jugador):
    titulo("PYTHON QUEST: EL DESPERTAR DEL CÓDIGO")
    narrar(f"\nBienvenido/a, {jugador.nombre}.")
    narrar("El reino de Pythonia ha caído en el Sueño del Error. Solo quien")
    narrar("domine el lenguaje de las serpientes podrá despertar al Código.\n")
    narrar(f"Empiezas con {jugador.VIDAS_INICIALES} vidas. Cada error cuesta una;")
    narrar("cada acierto te da XP. ¡Equivocarse también es aprender!")
    pausar()


def jugar_nivel(nivel, jugador):
    """Juega un nivel completo. Devuelve True si el jugador lo supera."""
    jugador.nivel_actual = nivel.numero
    print()
    titulo(f"NIVEL {nivel.numero}: {nivel.titulo.upper()}")
    narrar(nivel.historia + "\n")

    linea("─")
    print("📖 LECCIÓN")
    print(nivel.teoria)
    linea("─")
    pausar()

    for i, reto in enumerate(nivel.retos, start=1):
        print(f"\n— Reto {i}/{len(nivel.retos)} —   {jugador.estado()}")
        if not reto.jugar(jugador):
            return False  # El jugador se quedó sin vidas.

    print(f"\n🏆 ¡Nivel {nivel.numero} superado!")
    # Recompensa: recuperar una vida (sin superar el máximo) por completar el nivel.
    if jugador.vidas < jugador.VIDAS_INICIALES:
        jugador.vidas += 1
        print(f"  💖 Recuperas una vida por tu esfuerzo: {jugador.corazones()}")
    pausar()
    return True


def mostrar_resumen(jugador, victoria):
    print()
    if victoria:
        titulo("🐉 ¡EL CÓDIGO HA DESPERTADO! 🐉")
        narrar("Has derrotado al Dragón del Código Repetido. Pythonia vuelve a vivir.")
    else:
        titulo("💀 GAME OVER 💀")
        narrar("Tus vidas se agotaron... pero cada error te ha enseñado algo.")

    # Tabla de estadísticas finales.
    total = jugador.retos_superados + jugador.fallos
    precision = (jugador.retos_superados / total * 100) if total else 0.0
    print(f"\n  Jugador ........ {jugador.nombre}")
    print(f"  Rango .......... {jugador.rango}")
    print(f"  XP total ....... {jugador.xp}")
    print(f"  Retos superados  {jugador.retos_superados}")
    print(f"  Fallos ......... {jugador.fallos}")
    print(f"  Precisión ...... {precision:.1f} %")  # :.1f → 1 decimal.
    linea()


def partida():
    """Una partida completa, desde el nombre hasta el resumen."""
    jugador = Jugador(pedir_nombre())
    mostrar_intro(jugador)

    print("\n¿Desde qué nivel quieres empezar?")
    print("  1) Variables  2) Condicionales  3) Bucles  4) Funciones")
    inicio = pedir_entero("Nivel: ", 1, len(NIVELES))

    # NIVELES[inicio - 1:] → slicing desde el nivel elegido hasta el final.
    for crear_nivel in NIVELES[inicio - 1:]:
        if not jugar_nivel(crear_nivel(), jugador):
            mostrar_resumen(jugador, victoria=False)
            return
    mostrar_resumen(jugador, victoria=True)


def ejecutar():
    """Bucle exterior: permite jugar varias partidas seguidas."""
    while True:
        partida()
        otra = pedir_texto("\n¿Jugar otra vez? (s/n): ").lower()
        if otra not in ("s", "si", "sí", "y", "yes"):
            print("¡Hasta la próxima, Pythonista! 🐍")
            break
