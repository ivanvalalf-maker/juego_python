# ABP Fase 2 - Generacion hidroelectrica durante El Nino
GRAVEDAD, DENSIDAD = 9.81, 1000
U_NORMAL, U_SEGUIM, U_ALERTA = 70, 50, 30    # % del volumen util
U_COBERTURA, U_APORTES = 100, 0.80
U_FP_BAJO, U_EFICIENCIA = 30, 0.85
MAX_CENTRALES = 50


def leer_numero(mensaje, minimo, maximo, entero=False):
    while True:                                # repite hasta dato valido
        texto = input(mensaje).replace(",", ".")
        try:
            valor = int(texto) if entero else float(texto)
        except ValueError:
            print("  ERROR: debe escribir un numero.")
            continue
        if minimo <= valor <= maximo:
            return valor
        print(f"  ERROR: el valor debe estar entre {minimo} y {maximo}.")


def leer_texto(mensaje):
    texto = input(mensaje).strip()
    while texto == "":
        print("  ERROR: el campo no puede quedar vacio.")
        texto = input(mensaje).strip()
    return texto.upper()


def calcular_central(c, dias, horas):
    pb = DENSIDAD * GRAVEDAD * c["qt"] * c["h"] * c["ef"] / 1e6   # MW
    if pb > c["pn"]:                           # RN-04
        pe, limitada = c["pn"], True
    else:
        pe, limitada = pb, False
    e = pe * horas / 1000                      # GWh
    fp = e / (c["pn"] * dias * 24 / 1000) * 100
    if limitada:                               # RN-05
        estado = "LIMITADA"
    elif fp < U_FP_BAJO:
        estado = "SUBUTILIZADA"
    elif c["ef"] < U_EFICIENCIA:
        estado = "EFICIENCIA BAJA"
    else:
        estado = "ADECUADA"
    return pe, e, fp, estado


def registrar_generales():
    g = {"region": leer_texto("Region: ")}
    g["dias"] = leer_numero("Dias del mes: ", 28, 31, True)
    g["horas"] = leer_numero("Horas de operacion: ", 1, g["dias"] * 24, True)
    g["vu"] = leer_numero("Volumen util (Mm3): ", 1, 100000)
    g["vi"] = leer_numero("Volumen inicial (Mm3): ", 0, g["vu"])
    g["qmed"] = leer_numero("Caudal medio historico (m3/s): ", 1, 100000)
    g["dem"] = leer_numero("Demanda del mes (GWh): ", 1, 100000)
    return g


def registrar_central(centrales):
    if len(centrales) >= MAX_CENTRALES:        # RN-01
        print("  ERROR: maximo de centrales alcanzado.")
        return
    nombre = leer_texto("Nombre de la central: ")
    for c in centrales:                        # RN-06
        if c["nombre"] == nombre:
            print("  ERROR: esa central ya existe.")
            return
    centrales.append({"nombre": nombre,
        "qa": leer_numero("Caudal afluente (m3/s): ", 0, 10000),
        "qt": leer_numero("Caudal turbinado (m3/s): ", 0.1, 10000),
        "h": leer_numero("Altura neta (m): ", 1, 2000),
        "ef": leer_numero("Eficiencia (0.01-1): ", 0.01, 1),
        "pn": leer_numero("Potencia nominal (MW): ", 0.1, 2000)})


def consultar_central(centrales, g):
    nombre = leer_texto("Central a consultar: ")
    for c in centrales:
        if c["nombre"] == nombre:
            pe, e, fp, estado = calcular_central(c, g["dias"], g["horas"])
            print(f"  Pe={pe:.2f} MW  E={e:.2f} GWh  FP={fp:.1f} %  {estado}")
            return
    print("  No existe una central con ese nombre.")


def generar_reporte(centrales, g):
    et = va = vt = qa = pinst = emax = 0
    critica, malas = "", 0
    for c in centrales:                        # acumula por central
        pe, e, fp, estado = calcular_central(c, g["dias"], g["horas"])
        print(f"  {c['nombre']:<6} {pe:8.2f} MW {e:8.2f} GWh {fp:5.1f} % {estado}")
        et += e
        pinst += c["pn"]
        qa += c["qa"]
        va += c["qa"] * 86400 * g["dias"] / 1e6
        vt += c["qt"] * 3600 * g["horas"] / 1e6
        if e > emax:
            emax, critica = e, c["nombre"]
        if estado != "ADECUADA":
            malas += 1
    vf = g["vi"] + va - vt                     # balance del embalse
    vertido = max(0, vf - g["vu"])
    vf = min(max(vf, 0), g["vu"])
    nivel = vf / g["vu"] * 100
    ia = qa / g["qmed"]
    fp_tot = et / (pinst * g["dias"] * 24 / 1000) * 100
    cob = et / g["dem"] * 100
    deficit = g["dem"] - et if et < g["dem"] else 0
    autonomia = vf / ((vt / g["dias"]) * (g["dem"] / et))   # corregida
    nino = ia < U_APORTES                      # RN-10
    if nivel > U_NORMAL and cob >= U_COBERTURA:   # RN-07
        riesgo = "NORMAL"
    elif nivel > U_SEGUIM:
        riesgo = "SEGUIMIENTO"
    elif nivel > U_ALERTA:
        riesgo = "ALERTA"
    else:
        riesgo = "CRITICO"
    if riesgo == "CRITICO" or (deficit > 0 and nino):   # RN-08
        alerta = "ACTIVAR RESPALDO TERMICO Y GESTION DE DEMANDA"
    elif deficit > 0 or nino:
        alerta = "VIGILANCIA: PREPARAR RESPALDO"
    else:
        alerta = "OPERACION NORMAL"
    print(f"Energia {et:.2f} GWh | Nivel {nivel:.1f} % | Vertido {vertido:.1f} Mm3")
    print(f"IA {ia:.3f} | FP {fp_tot:.1f} % | Cobertura {cob:.1f} % | Deficit {deficit:.2f} GWh")
    print(f"Autonomia {autonomia:.1f} dias | Mayor aporte {critica} | Con problema {malas}")
    print(f"Riesgo: {riesgo} | Alerta: {alerta}")


generales, centrales, opcion = None, [], 0
while opcion != 5:                             # menu principal
    print("\n1.Datos generales 2.Registrar 3.Consultar 4.Reporte 5.Salir")
    opcion = leer_numero("Opcion: ", 1, 5, True)
    if opcion == 1:
        generales = registrar_generales()
    elif opcion == 2:
        registrar_central(centrales)
    elif opcion in (3, 4):
        if generales is None or len(centrales) == 0:   # RN-09
            print("  Registre primero los datos generales y una central.")
        elif opcion == 3:
            consultar_central(centrales, generales)
        else:
            generar_reporte(centrales, generales)
print("Fin del programa.")
