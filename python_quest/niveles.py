"""Contenido pedagógico: historia, teoría y retos de cada nivel.

Separar los DATOS (este archivo) de la LÓGICA (juego.py) hace el juego
escalable: para añadir un Nivel 5 solo hay que crear otra función
`crear_nivel_5()` y añadirla a la lista NIVELES, sin tocar el motor.
"""

from dataclasses import dataclass, field

from python_quest.retos import RetoCodigo, RetoOpcionMultiple, RetoPrediccion


# @dataclass genera automáticamente __init__ y __repr__ a partir de los
# atributos declarados: ideal para clases que solo almacenan datos.
@dataclass
class Nivel:
    numero: int
    titulo: str
    historia: str
    teoria: str
    retos: list = field(default_factory=list)  # Lista vacía nueva por instancia.


# ---------------------------------------------------------------------------
# NIVEL 1 · Variables y tipos de datos
# ---------------------------------------------------------------------------
def crear_nivel_1():
    return Nivel(
        numero=1,
        titulo="La Biblioteca de las Variables",
        historia=(
            "Despiertas en una biblioteca en ruinas. Los libros están vacíos:\n"
            "el Código ha olvidado cómo GUARDAR información. El Bibliotecario\n"
            "Fantasma te pide que restaures la memoria del mundo."
        ),
        teoria=(
            "Una VARIABLE es una caja con nombre que guarda un valor:\n"
            "    edad = 20          # int   → número entero\n"
            "    altura = 1.75      # float → número con decimales\n"
            "    nombre = \"Ana\"     # str   → texto, siempre entre comillas\n"
            "    es_mago = True     # bool  → True o False (con mayúscula)\n"
            "El signo = ASIGNA (guarda), no compara. type(x) te dice el tipo."
        ),
        retos=[
            RetoOpcionMultiple(
                "¿De qué tipo es el valor 3.14?",
                ["int", "float", "str", "bool"],
                correcta=2,
                pista="Fíjate en el punto decimal.",
                explicacion="Los números con parte decimal son de tipo float.",
            ),
            RetoCodigo(
                "Crea una variable llamada 'vidas' que guarde el número entero 3.",
                ["vidas = 3"],
                pista="Formato: nombre = valor  (sin comillas: es un número).",
                explicacion="vidas = 3 guarda el int 3 en la variable 'vidas'.",
            ),
            RetoCodigo(
                "Guarda el texto Merlin en una variable llamada 'heroe'.",
                ['heroe = "Merlin"'],
                pista="Los textos (str) van entre comillas: \"...\" o '...'.",
                explicacion="Sin comillas, Python buscaría una variable llamada Merlin.",
            ),
            RetoPrediccion(
                "¿Qué imprime este código?",
                'x = "5"\ny = "3"\nprint(x + y)',
                "53",
                pista="x e y son str, no int. ¿Qué hace + con textos?",
                explicacion="Con str, + CONCATENA (une) textos: \"5\" + \"3\" = \"53\".",
            ),
            RetoOpcionMultiple(
                "¿Cuál es un valor bool válido en Python?",
                ["true", "\"True\"", "True", "VERDADERO"],
                correcta=3,
                pista="Python distingue mayúsculas; y con comillas sería texto.",
                explicacion="Los booleanos son exactamente True y False, sin comillas.",
            ),
        ],
    )


# ---------------------------------------------------------------------------
# NIVEL 2 · Condicionales
# ---------------------------------------------------------------------------
def crear_nivel_2():
    return Nivel(
        numero=2,
        titulo="El Puente de las Decisiones",
        historia=(
            "Llegas a un puente custodiado por un Troll Lógico. Solo deja pasar\n"
            "a quien sepa tomar DECISIONES. «Si respondes bien, pasas;\n"
            "si no... ya veremos», gruñe."
        ),
        teoria=(
            "Los condicionales ejecutan código SOLO si se cumple una condición:\n"
            "    if oro >= 10:\n"
            "        print(\"Compras la espada\")\n"
            "    elif oro >= 5:\n"
            "        print(\"Compras un escudo\")\n"
            "    else:\n"
            "        print(\"No te alcanza\")\n"
            "Claves: los ':' al final y la SANGRÍA (4 espacios) del bloque.\n"
            "Comparadores: ==  !=  <  >  <=  >=   Lógicos: and  or  not"
        ),
        retos=[
            RetoOpcionMultiple(
                "¿Qué operador COMPARA si dos valores son iguales?",
                ["=", "==", "===", "is equal"],
                correcta=2,
                pista="Uno solo (=) sirve para asignar.",
                explicacion="== compara y devuelve un bool; = asigna un valor.",
            ),
            RetoCodigo(
                "Escribe la primera línea de un if que compruebe si 'vidas' es igual a 0.",
                ["if vidas == 0:", "if 0 == vidas:", "if (vidas == 0):"],
                pista="Formato: if condición:   (no olvides los dos puntos).",
                explicacion="'if vidas == 0:' — la condición usa == y termina en ':'.",
            ),
            RetoPrediccion(
                "¿Qué imprime este código?",
                "oro = 7\nif oro >= 10:\n    print(\"espada\")\nelif oro >= 5:\n"
                "    print(\"escudo\")\nelse:\n    print(\"nada\")",
                "escudo",
                pista="Evalúa las condiciones de arriba abajo; se ejecuta la PRIMERA verdadera.",
                explicacion="7 >= 10 es False; 7 >= 5 es True → se ejecuta el elif.",
            ),
            RetoOpcionMultiple(
                "Si edad = 15, ¿cuánto vale  edad > 12 and edad < 18 ?",
                ["True", "False", "15", "Error"],
                correcta=1,
                pista="'and' es True solo si AMBAS partes son True.",
                explicacion="15 > 12 es True y 15 < 18 es True → True and True = True.",
            ),
        ],
    )


# ---------------------------------------------------------------------------
# NIVEL 3 · Bucles
# ---------------------------------------------------------------------------
def crear_nivel_3():
    return Nivel(
        numero=3,
        titulo="Las Minas del Eterno Retorno",
        historia=(
            "Desciendes a unas minas donde los mineros repiten la misma tarea\n"
            "una y otra vez, a mano. Enséñales a REPETIR con magia y quedarán\n"
            "libres del ciclo eterno."
        ),
        teoria=(
            "for recorre una secuencia un número conocido de veces:\n"
            "    for i in range(3):     # i toma 0, 1, 2  (¡el 3 no se incluye!)\n"
            "        print(i)\n"
            "while repite MIENTRAS la condición sea True:\n"
            "    energia = 3\n"
            "    while energia > 0:\n"
            "        energia = energia - 1   # ¡Si no cambia, bucle infinito!\n"
            "break sale del bucle; continue salta a la siguiente vuelta."
        ),
        retos=[
            RetoOpcionMultiple(
                "¿Qué números genera range(1, 4)?",
                ["1, 2, 3, 4", "1, 2, 3", "0, 1, 2, 3", "4, 3, 2, 1"],
                correcta=2,
                pista="El inicio se incluye, el final NO.",
                explicacion="range(inicio, fin) va de inicio hasta fin-1: 1, 2, 3.",
            ),
            RetoPrediccion(
                "¿Qué imprime este código?",
                "total = 0\nfor n in range(4):\n    total = total + n\nprint(total)",
                "6",
                pista="range(4) da 0, 1, 2, 3. Súmalos.",
                explicacion="0 + 1 + 2 + 3 = 6. El bucle va acumulando en 'total'.",
            ),
            RetoCodigo(
                "Escribe la cabecera de un for que recorra los números del 0 al 4 con la variable i.",
                ["for i in range(5):", "for i in range(0, 5):", "for i in range(0,5,1):"],
                pista="Formato: for variable in range(...):   ¿qué número va para llegar a 4?",
                explicacion="range(5) produce 0, 1, 2, 3, 4 (5 vueltas).",
            ),
            RetoOpcionMultiple(
                "¿Qué le pasa a este bucle?\n    x = 1\n    while x > 0:\n        print(x)",
                ["Se ejecuta 1 vez", "No se ejecuta", "Es un bucle infinito", "Da error de sintaxis"],
                correcta=3,
                pista="¿Cambia x dentro del bucle en algún momento?",
                explicacion="x nunca cambia, así que x > 0 siempre es True: bucle infinito.",
            ),
            RetoPrediccion(
                "¿Qué imprime este código?",
                "for letra in \"py\":\n    print(letra)",
                "p y",
                pista="for también recorre los caracteres de un texto, uno por vuelta.",
                explicacion="Un str es una secuencia: primero imprime 'p' y luego 'y'.",
            ),
        ],
    )


# ---------------------------------------------------------------------------
# NIVEL 4 · Funciones
# ---------------------------------------------------------------------------
def crear_nivel_4():
    return Nivel(
        numero=4,
        titulo="La Torre del Hechizo Reutilizable",
        historia=(
            "En la cima de la torre te espera el Dragón del Código Repetido.\n"
            "Solo un verdadero mago, capaz de crear HECHIZOS REUTILIZABLES\n"
            "(funciones), podrá derrotarlo y despertar al Código."
        ),
        teoria=(
            "Una FUNCIÓN es un bloque de código con nombre que puedes reutilizar:\n"
            "    def curar(vida, pocion):      # def + nombre + parámetros + ':'\n"
            "        nueva = vida + pocion\n"
            "        return nueva              # return DEVUELVE el resultado\n"
            "\n"
            "    resultado = curar(50, 20)     # llamada → resultado vale 70\n"
            "print() solo MUESTRA en pantalla; return ENTREGA el valor a quien llama.\n"
            "Una función sin return devuelve None."
        ),
        retos=[
            RetoOpcionMultiple(
                "¿Qué palabra clave se usa para DEFINIR una función?",
                ["function", "func", "def", "define"],
                correcta=3,
                pista="Es una abreviatura de 'define' de solo 3 letras.",
                explicacion="En Python las funciones se definen con def.",
            ),
            RetoCodigo(
                "Escribe la cabecera de una función llamada 'atacar' que reciba un parámetro 'fuerza'.",
                ["def atacar(fuerza):"],
                pista="Formato: def nombre(parametro):",
                explicacion="def atacar(fuerza): — nombre, paréntesis con parámetros y ':'.",
            ),
            RetoPrediccion(
                "¿Qué imprime este código?",
                "def doble(n):\n    return n * 2\n\nprint(doble(4) + 1)",
                "9",
                pista="Primero se resuelve doble(4); luego se suma 1.",
                explicacion="doble(4) devuelve 8, y 8 + 1 = 9.",
            ),
            RetoPrediccion(
                "¿Qué imprime este código?",
                "def saludar():\n    print(\"hola\")\n\nx = saludar()\nprint(x)",
                "hola None",
                pista="saludar() imprime algo, pero ¿qué DEVUELVE si no tiene return?",
                explicacion="Se imprime 'hola' al llamarla y luego x es None (no hay return).",
                xp=50,
            ),
            RetoCodigo(
                "Dentro de una función, escribe la línea que DEVUELVA la suma de a y b.",
                ["return a + b", "return b + a", "return (a + b)"],
                pista="Usa la palabra clave que entrega el resultado al que llama.",
                explicacion="return a + b calcula la suma y la entrega como resultado.",
                xp=50,
            ),
        ],
    )


# Lista ordenada de "fábricas" de niveles. Guardamos las FUNCIONES (sin
# paréntesis), no los niveles: así cada partida crea niveles nuevos.
NIVELES = [crear_nivel_1, crear_nivel_2, crear_nivel_3, crear_nivel_4]
