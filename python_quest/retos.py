"""Tipos de retos del juego.

Usamos HERENCIA: la clase base `Reto` define el flujo común (mostrar enunciado,
pedir respuesta, dar XP o quitar vidas) y cada subclase solo redefine CÓMO se
pide y se comprueba la respuesta. Así añadir un tipo nuevo de reto es fácil.
"""

from python_quest.utilidades import normalizar_codigo, pedir_entero, pedir_texto


class Reto:
    """Clase base. No se usa directamente; sirve de plantilla."""

    def __init__(self, enunciado, pista, explicacion, xp=30):
        self.enunciado = enunciado      # Qué se le pide al jugador.
        self.pista = pista              # Se muestra tras el primer fallo.
        self.explicacion = explicacion  # El "porqué" de la respuesta correcta.
        self.xp = xp                    # Recompensa máxima.

    # --- Métodos que las subclases deben redefinir -------------------------
    def mostrar_opciones(self):
        """Muestra información extra (opciones, código...). Opcional."""

    def pedir_respuesta(self):
        raise NotImplementedError  # Obliga a las subclases a implementarlo.

    def es_correcta(self, respuesta):
        raise NotImplementedError

    # --- Flujo común --------------------------------------------------------
    def jugar(self, jugador):
        """Ejecuta el reto. Devuelve True si se superó, False si el jugador murió.

        Cada fallo cuesta una vida y reduce la recompensa de XP, pero el
        jugador puede reintentar mientras siga vivo: equivocarse es parte de
        aprender.
        """
        print(f"\n🧩 RETO: {self.enunciado}")
        self.mostrar_opciones()

        intentos = 0
        while jugador.esta_vivo:
            respuesta = self.pedir_respuesta()
            intentos += 1

            if self.es_correcta(respuesta):
                print("\n  ✅ ¡Correcto!")
                print(f"  📘 {self.explicacion}")
                # Cada fallo previo resta un tercio del XP (mínimo 5 XP).
                recompensa = max(5, self.xp - (intentos - 1) * self.xp // 3)
                jugador.ganar_xp(recompensa)
                return True

            print("\n  ❌ No es correcto.")
            jugador.perder_vida()
            if jugador.esta_vivo:
                print(f"  💡 Pista: {self.pista}")

        return False  # Se acabaron las vidas.


class RetoOpcionMultiple(Reto):
    """El jugador elige una opción numerada."""

    def __init__(self, enunciado, opciones, correcta, pista, explicacion, xp=30):
        # super() llama al constructor de la clase padre para reutilizarlo.
        super().__init__(enunciado, pista, explicacion, xp)
        self.opciones = opciones
        self.correcta = correcta  # Índice (empezando en 1) de la opción buena.

    def mostrar_opciones(self):
        # enumerate() da a la vez el índice y el elemento; start=1 para que
        # el jugador vea 1, 2, 3... en lugar de 0, 1, 2...
        for i, opcion in enumerate(self.opciones, start=1):
            print(f"    {i}) {opcion}")

    def pedir_respuesta(self):
        # pedir_entero ya gestiona letras y números fuera de rango.
        return pedir_entero("  Tu elección: ", 1, len(self.opciones))

    def es_correcta(self, respuesta):
        return respuesta == self.correcta


class RetoCodigo(Reto):
    """El jugador escribe una línea de código. Se aceptan varias formas válidas."""

    def __init__(self, enunciado, respuestas_validas, pista, explicacion, xp=40):
        super().__init__(enunciado, pista, explicacion, xp)
        # Guardamos las respuestas ya normalizadas en un set: buscar en un
        # set es muy rápido y no admite duplicados.
        self.respuestas_validas = {normalizar_codigo(r) for r in respuestas_validas}

    def pedir_respuesta(self):
        return pedir_texto("  >>> ")

    def es_correcta(self, respuesta):
        if not respuesta:  # Una cadena vacía es "falsa" en Python.
            print("  ⚠ No escribiste nada.")
            return False
        return normalizar_codigo(respuesta) in self.respuestas_validas


class RetoPrediccion(Reto):
    """Se muestra un fragmento de código y el jugador predice lo que imprime."""

    def __init__(self, enunciado, codigo, salida_esperada, pista, explicacion, xp=35):
        super().__init__(enunciado, pista, explicacion, xp)
        self.codigo = codigo
        self.salida_esperada = salida_esperada

    def mostrar_opciones(self):
        print("    ┌" + "─" * 40)
        for linea_codigo in self.codigo.splitlines():
            print(f"    │ {linea_codigo}")
        print("    └" + "─" * 40)
        print("    (Escribe la salida exacta; si son varias líneas, sepáralas con espacios)")

    def pedir_respuesta(self):
        return pedir_texto("  Salida: ")

    def es_correcta(self, respuesta):
        # Comparamos ignorando mayúsculas/minúsculas y espacios extra.
        limpia = " ".join(respuesta.lower().split())
        esperada = " ".join(self.salida_esperada.lower().split())
        return limpia == esperada
