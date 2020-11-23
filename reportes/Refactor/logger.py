import direcciones
from datetime import datetime, date, timedelta

def error(mensaje):
    with open(direcciones.file_log,"a") as log:
        tipo = "ERROR"
        hora = datetime.now()
        logeo = tipo + " " + str(hora) + " " + mensaje + "\n"
        log.write(logeo)

def info(mensaje):
    with open(file_log,"a") as log:
        tipo = "INFO"
        hora = datetime.now()
        logeo = tipo + " " + str(hora) + " " + mensaje + "\n"
        log.write(logeo)



error("Tuvieja")
info("Tutia")

