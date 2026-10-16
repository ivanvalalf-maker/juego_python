Algoritmo HidroelectricaNino
  Definir opcion, dias, horas, n, i, conProblema Como Entero
  Definir nivel, caudalMedio, demanda Como Real
  Definir caudal, altura, eficiencia, pNominal, pBruta, pEfectiva, energia, factor Como Real
  Definir energiaTotal, caudalTotal, cobertura, deficit, indiceAportes Como Real
  Definir region, nombre, buscado, estado, riesgo, alerta Como Caracter
  Definir datosListos, repetido, encontrada, nino Como Logico
  Dimension nombres[50], estados[50], energias[50], caudales[50]
  Definir nombres, estados Como Caracter
  Definir energias, caudales Como Real
  n <- 0
  datosListos <- Falso
  opcion <- 0
  Mientras opcion <> 5 Hacer
    Escribir "1.Generales 2.Registrar 3.Consultar 4.Reporte 5.Salir"
    Leer opcion
    Segun opcion Hacer
      1:
        Leer region
        Repetir
          Leer dias
        Hasta Que dias >= 28 Y dias <= 31
        Repetir
          Leer horas
        Hasta Que horas >= 1 Y horas <= dias * 24
        Repetir
          Leer nivel
        Hasta Que nivel >= 0 Y nivel <= 100
        Repetir
          Leer caudalMedio, demanda
        Hasta Que caudalMedio > 0 Y demanda > 0
        datosListos <- Verdadero
      2:
        Si datosListos = Falso Entonces
          Escribir "Primero registre los datos generales"
        SiNo
          Leer nombre
          repetido <- Falso
          Para i <- 1 Hasta n Hacer
            Si nombres[i] = nombre Entonces
              repetido <- Verdadero
            FinSi
          FinPara
          Si repetido Entonces
            Escribir "ERROR: esa central ya existe"
          SiNo
            Repetir
              Leer caudal, altura, eficiencia, pNominal
            Hasta Que caudal > 0 Y altura > 0 Y eficiencia > 0 Y eficiencia <= 1 Y pNominal > 0
            pBruta <- 9.81 * caudal * altura * eficiencia / 1000
            Si pBruta > pNominal Entonces
              pEfectiva <- pNominal
            SiNo
              pEfectiva <- pBruta
            FinSi
            energia <- pEfectiva * horas / 1000
            factor <- pEfectiva * horas / (pNominal * dias * 24) * 100
            Si pBruta > pNominal Entonces
              estado <- "LIMITADA"
            SiNo
              Si factor < 30 Entonces
                estado <- "SUBUTILIZADA"
              SiNo
                Si eficiencia < 0.85 Entonces
                  estado <- "EFICIENCIA BAJA"
                SiNo
                  estado <- "ADECUADA"
                FinSi
              FinSi
            FinSi
            n <- n + 1
            nombres[n] <- nombre
            estados[n] <- estado
            energias[n] <- energia
            caudales[n] <- caudal
          FinSi
        FinSi
      3:
        Leer buscado
        encontrada <- Falso
        Para i <- 1 Hasta n Hacer
          Si nombres[i] = buscado Entonces
            encontrada <- Verdadero
            Escribir energias[i], " GWh ", estados[i]
          FinSi
        FinPara
        Si encontrada = Falso Entonces
          Escribir "No existe una central con ese nombre"
        FinSi
      4:
        energiaTotal <- 0
        caudalTotal <- 0
        conProblema <- 0
        Para i <- 1 Hasta n Hacer
          Escribir nombres[i], " ", energias[i], " GWh ", estados[i]
          energiaTotal <- energiaTotal + energias[i]
          caudalTotal <- caudalTotal + caudales[i]
          Si estados[i] <> "ADECUADA" Entonces
            conProblema <- conProblema + 1
          FinSi
        FinPara
        cobertura <- energiaTotal / demanda * 100
        Si energiaTotal < demanda Entonces
          deficit <- demanda - energiaTotal
        SiNo
          deficit <- 0
        FinSi
        indiceAportes <- caudalTotal / caudalMedio
        nino <- indiceAportes < 0.80
        Si nivel > 70 Y cobertura >= 100 Entonces
          riesgo <- "NORMAL"
        SiNo
          Si nivel > 50 Entonces
            riesgo <- "SEGUIMIENTO"
          SiNo
            Si nivel > 30 Entonces
              riesgo <- "ALERTA"
            SiNo
              riesgo <- "CRITICO"
            FinSi
          FinSi
        FinSi
        Si riesgo = "CRITICO" O (deficit > 0 Y nino) Entonces
          alerta <- "ACTIVAR RESPALDO TERMICO"
        SiNo
          Si deficit > 0 O nino Entonces
            alerta <- "VIGILANCIA"
          SiNo
            alerta <- "OPERACION NORMAL"
          FinSi
        FinSi
        Escribir energiaTotal, cobertura, deficit, riesgo, alerta
      5:
        Escribir "Fin del programa"
      De Otro Modo:
        Escribir "ERROR: opcion no valida"
    FinSegun
  FinMientras
FinAlgoritmo
