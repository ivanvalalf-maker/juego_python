"""Modelo del jugador: guarda su estado (vidas, XP, nivel)."""

# Una clase agrupa DATOS (atributos) y COMPORTAMIENTO (métodos).
# Aunque las clases no se enseñan en los 4 niveles, leer esta te dará
# una primera idea de cómo se organizan programas más grandes.


class Jugador:
    VIDAS_INICIALES = 3
    XP_POR_RANGO = 100  # Cada 100 XP se sube de rango.

    RANGOS = ["Aprendiz", "Iniciado", "Hechicero del Código", "Archimago Pythonista"]

    def __init__(self, nombre):
        """El constructor: se ejecuta al crear un Jugador("Ana")."""
        self.nombre = nombre
        self.vidas = self.VIDAS_INICIALES
        self.xp = 0
        self.nivel_actual = 1
        self.retos_superados = 0
        self.fallos = 0

    @property
    def esta_vivo(self):
        """Propiedad calculada: se usa como atributo (jugador.esta_vivo)."""
        return self.vidas > 0

    @property
    def rango(self):
        """Devuelve el título del jugador según su XP."""
        # División entera (//) para saber cuántos bloques de 100 XP tiene;
        # min() evita salirnos de la lista (IndexError).
        indice = min(self.xp // self.XP_POR_RANGO, len(self.RANGOS) - 1)
        return self.RANGOS[indice]

    def ganar_xp(self, cantidad):
        """Suma XP y avisa si el jugador sube de rango."""
        rango_anterior = self.rango
        self.xp += cantidad
        self.retos_superados += 1
        print(f"  ✨ +{cantidad} XP  (total: {self.xp})")
        if self.rango != rango_anterior:
            print(f"  🎖  ¡Has ascendido a «{self.rango}»!")

    def perder_vida(self):
        """Resta una vida sin bajar de 0."""
        self.vidas = max(0, self.vidas - 1)
        self.fallos += 1
        print(f"  💔 Pierdes una vida. Te quedan: {self.corazones()}")

    def corazones(self):
        """Representación visual de las vidas, p. ej. ❤❤♡."""
        return "❤" * self.vidas + "♡" * (self.VIDAS_INICIALES - self.vidas)

    def estado(self):
        """Texto resumen para la barra de estado."""
        return (f"{self.nombre} [{self.rango}] | Vidas: {self.corazones()} "
                f"| XP: {self.xp} | Nivel: {self.nivel_actual}")
