Algoritmo MenuHidroelectricaNino
    // Constantes y umbrales de la Fase 1 + dos umbrales nuevos
    Definir U_NORMAL, U_SEGUIM, U_ALERTA, U_COBERTURA, U_APORTES Como Real
    Definir U_FP_BAJO, U_EFICIENCIA Como Real
    Definir opcion, numCentrales, i, diasMes, horasOperacion Como Entero
    Definir volumenInicial, volumenUtil, caudalMedioHistorico, demandaRegional Como Real
    Definir idRegion, nombreNuevo Como Caracter
    Definir hayGenerales, repetida Como Logico
    Dimension nombre[50], qAfl[50], qTur[50], altura[50], efic[50], pNom[50]
    Definir nombre Como Caracter
    Definir qAfl, qTur, altura, efic, pNom Como Real

    U_NORMAL <- 70
    U_SEGUIM <- 50
    U_ALERTA <- 30
    U_COBERTURA <- 100
    U_APORTES <- 0.80
    U_FP_BAJO <- 30
    U_EFICIENCIA <- 0.85
    numCentrales <- 0
    hayGenerales <- Falso
    opcion <- 0

    Mientras opcion <> 5 Hacer
        Escribir "1. Registrar datos generales"
        Escribir "2. Registrar central"
        Escribir "3. Consultar central"
        Escribir "4. Generar reporte"
        Escribir "5. Salir"
        Leer opcion
        Segun opcion Hacer
            1:
                // Bloque Repetir ... Hasta Que de la Fase 1 con RN-02 y RN-03
                LeerDatosGenerales(idRegion, diasMes, horasOperacion, volumenInicial, volumenUtil, caudalMedioHistorico, demandaRegional)
                hayGenerales <- Verdadero
            2:
                Si numCentrales >= 50 Entonces
                    Escribir "ERROR: ya se registro el maximo de centrales"
                SiNo
                    Escribir "Nombre de la central:"
                    Leer nombreNuevo
                    repetida <- Falso
                    Para i <- 1 Hasta numCentrales Con Paso 1 Hacer
                        Si nombre[i] = nombreNuevo Entonces
                            repetida <- Verdadero
                        FinSi
                    FinPara
                    Si repetida Entonces
                        Escribir "ERROR: esa central ya esta registrada"
                    SiNo
                        numCentrales <- numCentrales + 1
                        nombre[numCentrales] <- nombreNuevo
                        LeerDatosCentral(numCentrales, qAfl, qTur, altura, efic, pNom)
                    FinSi
                FinSi
            3, 4:
                Si NO hayGenerales Entonces
                    Escribir "Primero registre los datos generales (opcion 1)"
                SiNo
                    Si numCentrales = 0 Entonces
                        Escribir "Primero registre al menos una central (opcion 2)"
                    SiNo
                        Si opcion = 3 Entonces
                            ConsultarCentral(numCentrales, nombre, qTur, altura, efic, pNom, diasMes, horasOperacion)
                        SiNo
                            // Recorre las centrales con Para y aplica los pasos 5 a 9 de la Fase 1
                            GenerarReporte(numCentrales, nombre, qAfl, qTur, altura, efic, pNom, idRegion, diasMes, horasOperacion, volumenInicial, volumenUtil, caudalMedioHistorico, demandaRegional)
                        FinSi
                    FinSi
                FinSi
            5:
                Escribir "Fin del programa"
            De Otro Modo:
                Escribir "ERROR: opcion no valida"
        FinSegun
    FinMientras
FinAlgoritmo

SubProceso estado <- EstadoCentral(potBruta, potNominal, fp, eficiencia, uFp, uEf)
    Definir estado Como Caracter
    Si potBruta > potNominal Entonces
        estado <- "LIMITADA (VIERTE AGUA)"
    SiNo
        Si fp < uFp Entonces
            estado <- "SUBUTILIZADA"
        SiNo
            Si eficiencia < uEf Entonces
                estado <- "EFICIENCIA BAJA"
            SiNo
                estado <- "ADECUADA"
            FinSi
        FinSi
    FinSi
FinSubProceso

SubProceso alerta <- DeterminarAlerta(categoria, deficit, hayNino)
    Definir alerta Como Caracter
    Si categoria = "CRITICO" O (deficit > 0 Y hayNino) Entonces
        alerta <- "ACTIVAR RESPALDO TERMICO Y GESTION DE DEMANDA"
    SiNo
        Si deficit > 0 O hayNino Entonces
            alerta <- "VIGILANCIA: PREPARAR RESPALDO"
        SiNo
            alerta <- "OPERACION NORMAL"
        FinSi
    FinSi
FinSubProceso
