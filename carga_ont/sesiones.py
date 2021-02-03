#/usr/bin/python

import sys
import logger

from requester import requester
from getpass import getpass
from api import usuario, contraseña

def autorizar():
    autorizar = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": usuario,
        "password": contraseña
    },
    "id": 1
    }
    llave = requester(autorizar)
    llave = llave.json()["result"]
    #si lo piden en la llamada muestra la key
    return llave

def logout(llave):
    logout = {
    "jsonrpc": "2.0",
    "method": "user.logout",
    "params": [],
    "id": 1,
    "auth": llave
    }
    deslogeo = requester(logout)
    try:
        if deslogeo.json()["result"] == True:

            #print("Deslogeo correcto")
            logger.info("Deslogeo correcto")
    except Exception as e:
        #print("Ocurrio un error al intentar deslogar el id: {}".format(llave))
        logger.info("Ocurrio un error al intentar deslogar el id: {}".format(llave))

