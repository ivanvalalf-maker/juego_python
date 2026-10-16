# ABP Fase 2 - Generacion hidroelectrica durante El Nino
# Programa con menu, condicionales y ciclos

# Constantes
GRAVEDAD = 9.81
MAX_CENTRALES = 50

# Listas donde se guardan las centrales
nombres = []
potencias = []
energias = []
factores = []
estados = []
caudales = []

datos_listos = False
opcion = 0

while opcion != 5:
    print("")
    print("1. Registrar datos generales")
    print("2. Registrar central")
    print("3. Consultar central")
    print("4. Generar reporte")
    print("5. Salir")
    opcion = int(input("Opcion: "))
    while opcion < 1 or opcion > 5:
        print("ERROR: la opcion debe estar entre 1 y 5")
        opcion = int(input("Opcion: "))

    if opcion == 1:
        region = input("Nombre de la region: ")
        dias = int(input("Dias del mes (28 a 31): "))
        while dias < 28 or dias > 31:
            print("ERROR: los dias deben estar entre 28 y 31")
            dias = int(input("Dias del mes (28 a 31): "))
        horas = int(input("Horas de operacion en el mes: "))
        while horas < 1 or horas > dias * 24:
            print("ERROR: las horas deben estar entre 1 y", dias * 24)
            horas = int(input("Horas de operacion en el mes: "))
        nivel = float(input("Nivel del embalse (0 a 100 %): "))
        while nivel < 0 or nivel > 100:
            print("ERROR: el nivel debe estar entre 0 y 100")
            nivel = float(input("Nivel del embalse (0 a 100 %): "))
        caudal_medio = float(input("Caudal medio historico (m3/s): "))
        while caudal_medio <= 0:
            print("ERROR: el caudal medio debe ser mayor que 0")
            caudal_medio = float(input("Caudal medio historico (m3/s): "))
        demanda = float(input("Demanda del mes (GWh): "))
        while demanda <= 0:
            print("ERROR: la demanda debe ser mayor que 0")
            demanda = float(input("Demanda del mes (GWh): "))
        datos_listos = True
        print("Datos generales registrados")

    elif opcion == 2:
        if datos_listos == False:
            print("Primero registre los datos generales (opcion 1)")
        elif len(nombres) >= MAX_CENTRALES:
            print("ERROR: ya hay", MAX_CENTRALES, "centrales registradas")
        else:
            nombre = input("Nombre de la central: ").upper()
            repetido = False
            for i in range(len(nombres)):
                if nombres[i] == nombre:
                    repetido = True
            if repetido == True:
                print("ERROR: esa central ya existe")
            else:
                caudal = float(input("Caudal turbinado (m3/s): "))
                while caudal <= 0:
                    print("ERROR: el caudal debe ser mayor que 0")
                    caudal = float(input("Caudal turbinado (m3/s): "))
                altura = float(input("Altura neta (m): "))
                while altura <= 0:
                    print("ERROR: la altura debe ser mayor que 0")
                    altura = float(input("Altura neta (m): "))
                eficiencia = float(input("Eficiencia (0 a 1): "))
                while eficiencia <= 0 or eficiencia > 1:
                    print("ERROR: la eficiencia debe estar entre 0 y 1")
                    eficiencia = float(input("Eficiencia (0 a 1): "))
                p_nominal = float(input("Potencia nominal (MW): "))
                while p_nominal <= 0:
                    print("ERROR: la potencia nominal debe ser mayor que 0")
                    p_nominal = float(input("Potencia nominal (MW): "))

                # Calculos de la central
                p_bruta = GRAVEDAD * caudal * altura * eficiencia / 1000   # MW
                if p_bruta > p_nominal:
                    p_efectiva = p_nominal
                else:
                    p_efectiva = p_bruta
                energia = p_efectiva * horas / 1000                       # GWh
                factor = p_efectiva * horas / (p_nominal * dias * 24) * 100

                # Estado de la instalacion
                if p_bruta > p_nominal:
                    estado = "LIMITADA"
                elif factor < 30:
                    estado = "SUBUTILIZADA"
                elif eficiencia < 0.85:
                    estado = "EFICIENCIA BAJA"
                else:
                    estado = "ADECUADA"

                nombres.append(nombre)
                caudales.append(caudal)
                potencias.append(p_efectiva)
                energias.append(energia)
                factores.append(factor)
                estados.append(estado)
                print("Central", nombre, "registrada:", estado)

    elif opcion == 3:
        if len(nombres) == 0:
            print("No hay centrales registradas")
        else:
            buscado = input("Nombre de la central a consultar: ").upper()
            encontrada = False
            for i in range(len(nombres)):
                if nombres[i] == buscado:
                    encontrada = True
                    print("Potencia efectiva:", round(potencias[i], 2), "MW")
                    print("Energia del mes:", round(energias[i], 2), "GWh")
                    print("Factor de planta:", round(factores[i], 1), "%")
                    print("Estado:", estados[i])
            if encontrada == False:
                print("No existe una central con ese nombre")

    elif opcion == 4:
        if len(nombres) == 0:
            print("No hay centrales registradas")
        else:
            energia_total = 0
            caudal_total = 0
            con_problema = 0
            print("REPORTE DE LA REGION", region)
            for i in range(len(nombres)):
                print(nombres[i], round(energias[i], 2), "GWh", estados[i])
                energia_total = energia_total + energias[i]
                caudal_total = caudal_total + caudales[i]
                if estados[i] != "ADECUADA":
                    con_problema = con_problema + 1

            cobertura = energia_total / demanda * 100
            if energia_total < demanda:
                deficit = demanda - energia_total
            else:
                deficit = 0
            indice_aportes = caudal_total / caudal_medio
            if indice_aportes < 0.80:
                nino = True
            else:
                nino = False

            # Clasificacion del riesgo
            if nivel > 70 and cobertura >= 100:
                riesgo = "NORMAL"
            elif nivel > 50:
                riesgo = "SEGUIMIENTO"
            elif nivel > 30:
                riesgo = "ALERTA"
            else:
                riesgo = "CRITICO"

            # Alerta operativa
            if riesgo == "CRITICO" or (deficit > 0 and nino == True):
                alerta = "ACTIVAR RESPALDO TERMICO"
            elif deficit > 0 or nino == True:
                alerta = "VIGILANCIA"
            else:
                alerta = "OPERACION NORMAL"

            print("Energia total:", round(energia_total, 2), "GWh")
            print("Cobertura de la demanda:", round(cobertura, 1), "%")
            print("Deficit:", round(deficit, 2), "GWh")
            print("Indice de aportes:", round(indice_aportes, 2))
            print("Centrales con problema:", con_problema, "de", len(nombres))
            print("Riesgo:", riesgo)
            print("Alerta:", alerta)

print("Fin del programa")
