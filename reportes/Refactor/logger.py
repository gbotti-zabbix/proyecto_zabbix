<<<<<<< HEAD
import direcciones

=======
from direcciones import file_log
>>>>>>> 8fdc4c050faada466dcb02c21a7494b29fa8fca3
from datetime import datetime, date, timedelta

def error(mensaje):
    with open(file_log,"a") as log:
        tipo = "ERROR"
        hora = datetime.now()
        logeo = tipo + " " + str(hora) + " " + mensaje + "\n"
        log.write(logeo)

def info(mensaje):
    with open(direcciones.file_log,"a") as log:
        tipo = "INFO"
        hora = datetime.now()
        logeo = tipo + " " + str(hora) + " " + mensaje + "\n"
        log.write(logeo)
