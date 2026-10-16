# ==============================================================
# ABP - Fase 2: Generacion hidroelectrica durante El Nino
# Programa con condicionales y ciclos (registrar, consultar,
# generar reporte). Continuacion del algoritmo de la Fase 1.
# ==============================================================

# ---------- Constantes fisicas y umbrales (no se modifican) ----------
GRAVEDAD = 9.81        # m/s2
DENSIDAD = 1000        # kg/m3
U_NORMAL = 70          # % de volumen util
U_SEGUIM = 50          # %
U_ALERTA = 30          # %
U_COBERTURA = 100      # % de la demanda
U_APORTES = 0.80       # p.u. del caudal medio historico
U_FP_BAJO = 30         # % factor de planta minimo por central
U_EFICIENCIA = 0.85    # eficiencia minima esperada (p.u.)
MAX_CENTRALES = 50


# ---------- Funciones de lectura con validacion ----------
def leer_entero(mensaje, minimo, maximo):
    while True:
        texto = input(mensaje)
        try:
            valor = int(texto)
        except ValueError:
            print("  ERROR: debe escribir un numero entero.")
            continue
        if valor < minimo or valor > maximo:
            print(f"  ERROR: el valor debe estar entre {minimo} y {maximo}.")
        else:
            return valor


def leer_real(mensaje, minimo, maximo):
    while True:
        texto = input(mensaje).replace(",", ".")
        try:
            valor = float(texto)
        except ValueError:
            print("  ERROR: debe escribir un numero.")
            continue
        if valor < minimo or valor > maximo:
            print(f"  ERROR: el valor debe estar entre {minimo} y {maximo}.")
        else:
            return valor


def leer_texto(mensaje):
    texto = input(mensaje).strip()
    while texto == "":
        print("  ERROR: el campo no puede quedar vacio.")
        texto = input(mensaje).strip()
    return texto.upper()


# ---------- Calculos por central ----------
def calcular_central(central, dias_mes, horas_operacion):
    potencia_bruta = (DENSIDAD * GRAVEDAD * central["caudal_turbinado"]
                      * central["altura_neta"] * central["eficiencia"]) / 1000000

    # Regla RN-04: la potencia entregada no puede superar la nominal
    if potencia_bruta > central["potencia_nominal"]:
        potencia_efectiva = central["potencia_nominal"]
        limitada = True
    else:
        potencia_efectiva = potencia_bruta
        limitada = False

    energia = potencia_efectiva * horas_operacion / 1000          # GWh
    factor_planta = energia / (central["potencia_nominal"] * dias_mes * 24 / 1000) * 100

    # Regla RN-05: estado de la instalacion (condicional multiple)
    if limitada:
        estado = "LIMITADA (VIERTE AGUA)"
    elif factor_planta < U_FP_BAJO:
        estado = "SUBUTILIZADA"
    elif central["eficiencia"] < U_EFICIENCIA:
        estado = "EFICIENCIA BAJA"
    else:
        estado = "ADECUADA"

    return potencia_bruta, potencia_efectiva, energia, factor_planta, estado


def clasificar_riesgo(nivel, cobertura):
    # Regla RN-07: condicional anidada (igual a la funcion de la Fase 1)
    if nivel > U_NORMAL and cobertura >= U_COBERTURA:
        categoria = "NORMAL"
    elif nivel > U_SEGUIM:
        categoria = "SEGUIMIENTO"
    elif nivel > U_ALERTA:
        categoria = "ALERTA"
    else:
        categoria = "CRITICO"
    return categoria


# ---------- Opcion 1: registrar datos generales ----------
def registrar_generales():
    print("\n--- DATOS GENERALES DEL SUBSISTEMA ---")
    region = leer_texto("Identificador de la region: ")
    dias = leer_entero("Dias del mes (28 a 31): ", 28, 31)
    # Regla RN-02: las horas no pueden superar las horas del mes
    horas = leer_entero(f"Horas de operacion (1 a {dias * 24}): ", 1, dias * 24)
    vol_util = leer_real("Volumen util del embalse (Mm3): ", 1, 100000)
    # Regla RN-03: el volumen inicial no puede superar el volumen util
    vol_inicial = leer_real(f"Volumen inicial (0 a {vol_util}) (Mm3): ", 0, vol_util)
    caudal_medio = leer_real("Caudal medio historico agregado (m3/s): ", 1, 100000)
    demanda = leer_real("Demanda regional del mes (GWh): ", 1, 100000)
    print("Datos generales registrados.")
    return {"region": region, "dias": dias, "horas": horas,
            "vol_util": vol_util, "vol_inicial": vol_inicial,
            "caudal_medio": caudal_medio, "demanda": demanda}


# ---------- Opcion 2: registrar una central ----------
def registrar_central(centrales):
    # Regla RN-01: maximo 50 centrales
    if len(centrales) >= MAX_CENTRALES:
        print("  ERROR: ya se registro el maximo de centrales.")
        return
    print(f"\n--- REGISTRO DE LA CENTRAL {len(centrales) + 1} ---")
    nombre = leer_texto("Nombre de la central: ")
    # Regla RN-06: no se permiten nombres repetidos (ciclo for de busqueda)
    for c in centrales:
        if c["nombre"] == nombre:
            print("  ERROR: esa central ya esta registrada.")
            return
    central = {
        "nombre": nombre,
        "caudal_afluente": leer_real("Caudal afluente (m3/s): ", 0, 10000),
        "caudal_turbinado": leer_real("Caudal turbinado (m3/s): ", 0.1, 10000),
        "altura_neta": leer_real("Altura neta (m): ", 1, 2000),
        "eficiencia": leer_real("Eficiencia (0.01 a 1): ", 0.01, 1),
        "potencia_nominal": leer_real("Potencia nominal (MW): ", 0.1, 2000),
    }
    centrales.append(central)
    print(f"Central {nombre} registrada. Total: {len(centrales)}")


# ---------- Opcion 3: consultar una central ----------
def consultar_central(centrales, generales):
    nombre = leer_texto("Nombre de la central a consultar: ")
    encontrada = False
    for c in centrales:
        if c["nombre"] == nombre:
            encontrada = True
            pb, pe, e, fp, estado = calcular_central(c, generales["dias"], generales["horas"])
            print(f"  Potencia bruta.....: {pb:.2f} MW")
            print(f"  Potencia efectiva..: {pe:.2f} MW")
            print(f"  Energia del mes....: {e:.2f} GWh")
            print(f"  Factor de planta...: {fp:.1f} %")
            print(f"  Estado.............: {estado}")
    if not encontrada:
        print("  No existe una central con ese nombre.")


# ---------- Opcion 4: generar el reporte del subsistema ----------
def generar_reporte(centrales, g):
    energia_total = 0
    vol_aportes = 0
    vol_turbinado = 0
    caudal_afluente_tot = 0
    energia_maxima = 0
    central_critica = ""
    deficientes = 0

    print("\n=========== REPORTE DEL SUBSISTEMA", g["region"], "===========")
    print(f"{'Central':<10}{'Pe (MW)':>10}{'E (GWh)':>10}{'FP (%)':>9}  Estado")
    for c in centrales:
        pb, pe, e, fp, estado = calcular_central(c, g["dias"], g["horas"])
        print(f"{c['nombre']:<10}{pe:>10.2f}{e:>10.2f}{fp:>9.1f}  {estado}")
        energia_total = energia_total + e
        vol_turbinado = vol_turbinado + c["caudal_turbinado"] * 3600 * g["horas"] / 1000000
        vol_aportes = vol_aportes + c["caudal_afluente"] * 86400 * g["dias"] / 1000000
        caudal_afluente_tot = caudal_afluente_tot + c["caudal_afluente"]
        if e > energia_maxima:
            energia_maxima = e
            central_critica = c["nombre"]
        if estado != "ADECUADA":
            deficientes = deficientes + 1

    # Balance del embalse agregado
    vol_final = g["vol_inicial"] + vol_aportes - vol_turbinado
    if vol_final > g["vol_util"]:
        vol_vertido = vol_final - g["vol_util"]
        vol_final = g["vol_util"]
    else:
        vol_vertido = 0
        if vol_final < 0:
            vol_final = 0

    # Indicadores
    nivel = vol_final / g["vol_util"] * 100
    indice_aportes = caudal_afluente_tot / g["caudal_medio"]
    potencia_instalada = 0
    for c in centrales:
        potencia_instalada = potencia_instalada + c["potencia_nominal"]
    factor_planta = energia_total / (potencia_instalada * g["dias"] * 24 / 1000) * 100
    cobertura = energia_total / g["demanda"] * 100
    if energia_total < g["demanda"]:
        deficit = g["demanda"] - energia_total
    else:
        deficit = 0
    # Autonomia corregida (observacion de la Fase 1): turbinado requerido
    # para cubrir la demanda, no el turbinado real
    if energia_total > 0:
        turbinado_requerido_dia = (vol_turbinado / g["dias"]) * (g["demanda"] / energia_total)
        autonomia = vol_final / turbinado_requerido_dia
    else:
        autonomia = 0
    hay_nino = indice_aportes < U_APORTES

    categoria = clasificar_riesgo(nivel, cobertura)

    # Regla RN-08: alerta operativa con operadores logicos
    if categoria == "CRITICO" or (deficit > 0 and hay_nino):
        alerta = "ACTIVAR RESPALDO TERMICO Y GESTION DE DEMANDA"
    elif deficit > 0 or hay_nino:
        alerta = "VIGILANCIA: PREPARAR RESPALDO"
    else:
        alerta = "OPERACION NORMAL"

    print("-" * 60)
    print(f"Energia generable.....: {energia_total:.2f} GWh")
    print(f"Volumen final.........: {vol_final:.1f} Mm3")
    print(f"Volumen vertido.......: {vol_vertido:.1f} Mm3")
    print(f"Nivel del embalse.....: {nivel:.1f} %")
    print(f"Indice de aportes.....: {indice_aportes:.3f} p.u.")
    print(f"Factor de planta......: {factor_planta:.1f} %")
    print(f"Cobertura de demanda..: {cobertura:.1f} %")
    print(f"Deficit de energia....: {deficit:.2f} GWh")
    print(f"Autonomia del embalse.: {autonomia:.1f} dias")
    print(f"Condicion El Nino.....: {'SI' if hay_nino else 'NO'}")
    print(f"Central de mayor aporte: {central_critica}")
    print(f"Centrales con problema: {deficientes} de {len(centrales)}")
    print(f"Categoria de riesgo...: {categoria}")
    print(f"Alerta operativa......: {alerta}")


# ---------- Programa principal: menu con ciclo while ----------
def main():
    generales = None
    centrales = []
    opcion = 0
    print("ANALISIS DE GENERACION HIDROELECTRICA - FENOMENO DE EL NINO")
    while opcion != 5:
        print("\n1. Registrar datos generales")
        print("2. Registrar central")
        print("3. Consultar central")
        print("4. Generar reporte")
        print("5. Salir")
        opcion = leer_entero("Opcion: ", 1, 5)

        if opcion == 1:
            generales = registrar_generales()
        elif opcion == 2:
            registrar_central(centrales)
        elif opcion == 3 or opcion == 4:
            # Regla RN-09: no se consulta ni reporta sin datos previos
            if generales is None:
                print("  Primero registre los datos generales (opcion 1).")
            elif len(centrales) == 0:
                print("  Primero registre al menos una central (opcion 2).")
            elif opcion == 3:
                consultar_central(centrales, generales)
            else:
                generar_reporte(centrales, generales)
        else:
            print("Fin del programa.")


main()
