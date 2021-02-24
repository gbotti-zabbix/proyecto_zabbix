#!/usr/bin/python

from direcciones import file_log
from datetime import datetime, date, timedelta
""" Logeo de scripts

Este script permite logear en el archivo seteado en file_log mensajes, hora de ejcucion 
y marcar la entrada como ERROR o INFO.

Todas las funciones requieren que se las llame pasando el string del mensaje. Dependiendo
del flag que buscamos para la entrada en el log, llamamos a info o error.

Para cambiar el archivo donde logear, modificar file_log en direcciones.py

Contiene las funciones:
    * error - Ingresa una entrada a file log, al final del archivo, con ERROR HORA Y FECHA MENSAJE
    * info - Ingresa una entrada a file log, al final del archivo, con INFO HORA Y FECHA MENSAJE
"""

def error(mensaje):
    """ Ingresa un ERROR a el archivo file_log

    :param mensaje: El mensaje a marcar como ERROR en el file_log
    :type mensaje: str

    :returns: no hay retorno. Escribe en file_log.
    """
    with open(file_log,"a") as log:
        tipo = "ERROR"
        hora = datetime.now()
        logeo = tipo + " " + str(hora) + " " + mensaje + "\n"
        log.write(logeo)

def info(mensaje):
    """ Ingresa un INFO a el archivo file_log

    :param mensaje: El mensaje a marcar como INFO en el file_log
    :type mensaje: str

    :returns: no hay retorno. Escribe en file_log.
    """
    with open(file_log,"a") as log:
        tipo = "INFO"
        hora = datetime.now()
        logeo = tipo + " " + str(hora) + " " + mensaje + "\n"
        log.write(logeo)
