#!/usr/bin/python

import sys
import logger

from requester import requester
from getpass import getpass
from api import usuario, contraseña
""" ###Logeo y deslogeo contra la Zabbix API con user fijo

Importa *usuario* y *contraseña* de **API.pyc** para no tener en texto plano
las credenciales de acceso.

Al autorizar devuelve una llave en formato str utilizada para hacer consultas
a la API.

logaut da de baja estas llaves para que no se acumulen ni queden activadas fuera
de uso.

Contiene las funciones:  
    **autorizar:** Devuelve una string con una API key.  
    **logout:** Da de baja una API key.
"""

def autorizar():
    """***Genera una API Key***

    Cuando se la llama, logea mediante la api el *usuario* API 
    guardado en **api.pyc**. 
    
    Puede solicitarse en la llamada a la funcion que se muestre la key generada.

    Devuelve un string con una API Key.

    **returns:** API Key generada con el *user* API.  
    **rtype:** str.
    """

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
    return llave

def logout(llave):
    """***Da de baja una API Key***

    Cuando se la llama, da de baja la API Key pasada como *llave* en formato
    str.

    La exepcion busca informar de que la key no pudo ser deslogeada o ya habia
    sido dada de baja. *Logger* registra que se deslogeo una Key (sin mostrarla).

    **returns:** Esta funcion no tiene retornos.
    """

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
            logger.info("Deslogeo correcto")
    except Exception as e:
        logger.info("Ocurrio un error al intentar deslogar el id: {}".format(llave))

