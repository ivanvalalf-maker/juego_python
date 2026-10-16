Algoritmo HidroelectricaNino
  Definir opcion, n, i, dias, horas Como Entero
  Definir vu, vi, qmed, dem Como Real
  Definir hayGen, repetida Como Logico
  Definir nomNuevo Como Caracter
  Dimension nom[50], qa[50], qt[50], h[50], ef[50], pn[50]
  Definir nom Como Caracter
  Definir qa, qt, h, ef, pn Como Real
  n <- 0
  hayGen <- Falso
  opcion <- 0
  Mientras opcion <> 5 Hacer
    Escribir "1.Generales 2.Registrar 3.Consultar 4.Reporte 5.Salir"
    Leer opcion
    Segun opcion Hacer
      1:
        Repetir
          Leer dias, horas, vu, vi, qmed, dem
        Hasta Que dias>=28 Y dias<=31 Y horas>=1 Y horas<=24*dias Y vu>0 Y vi>=0 Y vi<=vu Y qmed>0 Y dem>0
        hayGen <- Verdadero
      2:
        Si n >= 50 Entonces
          Escribir "ERROR: maximo de centrales"
        SiNo
          Leer nomNuevo
          repetida <- Falso
          Para i <- 1 Hasta n Hacer
            Si nom[i] = nomNuevo Entonces
              repetida <- Verdadero
            FinSi
          FinPara
          Si repetida Entonces
            Escribir "ERROR: central repetida"
          SiNo
            n <- n + 1
            nom[n] <- nomNuevo
            Repetir
              Leer qa[n], qt[n], h[n], ef[n], pn[n]
            Hasta Que qa[n]>=0 Y qt[n]>0 Y h[n]>0 Y ef[n]>0 Y ef[n]<=1 Y pn[n]>0
          FinSi
        FinSi
      3, 4:
        Si NO hayGen O n = 0 Entonces
          Escribir "Registre datos generales y una central"
        SiNo
          Si opcion = 3 Entonces
            ConsultarCentral(n, nom, qt, h, ef, pn, dias, horas)
          SiNo
            GenerarReporte(n, nom, qa, qt, h, ef, pn, dias, horas, vu, vi, qmed, dem)
          FinSi
        FinSi
      5:
        Escribir "Fin del programa"
      De Otro Modo:
        Escribir "ERROR: opcion no valida"
    FinSegun
  FinMientras
FinAlgoritmo

SubProceso GenerarReporte(n, nom, qa, qt, h, ef, pn, dias, horas, vu, vi, qmed, dem)
  Definir i Como Entero
  Definir pb, pe, e, et, va, vt, qat, pinst, vf, nivel, ia, cob, deficit, aut Como Real
  Definir riesgo, alerta Como Caracter
  et <- 0; va <- 0; vt <- 0; qat <- 0; pinst <- 0
  Para i <- 1 Hasta n Hacer
    pb <- 1000 * 9.81 * qt[i] * h[i] * ef[i] / 1000000
    Si pb > pn[i] Entonces
      pe <- pn[i]
    SiNo
      pe <- pb
    FinSi
    e <- pe * horas / 1000
    Escribir nom[i], " ", e, " GWh ", EstadoCentral(pb, pn[i], e, ef[i], dias)
    et <- et + e
    pinst <- pinst + pn[i]
    qat <- qat + qa[i]
    va <- va + qa[i] * 86400 * dias / 1000000
    vt <- vt + qt[i] * 3600 * horas / 1000000
  FinPara
  vf <- vi + va - vt
  Si vf > vu Entonces
    vf <- vu
  SiNo
    Si vf < 0 Entonces
      vf <- 0
    FinSi
  FinSi
  nivel <- vf / vu * 100
  ia <- qat / qmed
  cob <- et / dem * 100
  Si et < dem Entonces
    deficit <- dem - et
  SiNo
    deficit <- 0
  FinSi
  aut <- vf / ((vt / dias) * (dem / et))
  Si nivel > 70 Y cob >= 100 Entonces
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
  Si riesgo = "CRITICO" O (deficit > 0 Y ia < 0.8) Entonces
    alerta <- "ACTIVAR RESPALDO TERMICO"
  SiNo
    Si deficit > 0 O ia < 0.8 Entonces
      alerta <- "VIGILANCIA"
    SiNo
      alerta <- "OPERACION NORMAL"
    FinSi
  FinSi
  Escribir et, nivel, ia, cob, deficit, aut, riesgo, alerta
FinSubProceso

SubProceso estado <- EstadoCentral(pb, pn, e, ef, dias)
  Definir estado Como Caracter
  Definir fp Como Real
  fp <- e / (pn * dias * 24 / 1000) * 100
  Si pb > pn Entonces
    estado <- "LIMITADA"
  SiNo
    Si fp < 30 Entonces
      estado <- "SUBUTILIZADA"
    SiNo
      Si ef < 0.85 Entonces
        estado <- "EFICIENCIA BAJA"
      SiNo
        estado <- "ADECUADA"
      FinSi
    FinSi
  FinSi
FinSubProceso
