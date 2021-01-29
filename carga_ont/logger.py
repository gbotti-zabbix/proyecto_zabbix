#!/usr/bin/python

from datetime import datetime, date, timedelta

file_log = "/var/log/carga_ont/ont.log"

def error(mensaje):
    with open(file_log,"a") as log:
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
