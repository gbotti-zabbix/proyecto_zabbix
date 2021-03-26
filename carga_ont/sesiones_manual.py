#!/usr/bin/python

import sys

from requester import requester
from getpass import getpass
""" ###Logeo y deslogeo contra la Zabbix API manual

Al autorizar devuelve una llave en formato str utilizada para hacer consultas
a la API. Utiliza el *usuario* y *contraseña* solicitado al llamar *autorizar()*.

*logaut()* da de baja estas llaves para que no se acumulen ni queden activadas fuera
de uso. Debe pasarse la llave a deslogear en formato str.

Para llamar a la funcion *autorizar()* se debe ejcutar el script con el argumento de sistema logeo.  
Para dar de baja una key se debe ejcutar el script con el argumento de sistema deslogeo.  
**Ej: CLI: .~\proyecto_zabbix\carga_ont\sesiones_manual.py logeo**

Contiene las funciones:  
    **autorizar:** Devuelve una string con una API key.  
    **logout:** Da de baja una API key.
"""

def autorizar():
    """***Genera una API Key***

    Solicita un *usuario* y *contraseña* de Zabbix en formato string. 
    Este user debe tener definido en zabbix permisos para ulitlizar la API.

    Devuelve un string con una API Key.

    **param user:** Usuario de zabbix en formato string.  
    **type user:** input(str)

    **param password:** Password de zabbix en formato string.  
    **type password:** input(str)

    **returns:** API Key generada con el user API.  
    **rtype:** str.
    """
    autorizar = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": input("Ingrese User:\n"),
        "password": getpass("Ingrese Password:\n")
    },
    "id": 1
    }
    llave = requester(autorizar)
    llave = llave.json()["result"]
    print(llave)

def logout():
    """***Da de baja una API Key***

    Cuando se la llama, solicita la Key a bajar en formato string.

    La exepcion busca informar de que la key no pudo ser deslogeada o ya habia
    sido dada de baja. Se imprime en pantalla si el deslogeo fue correcto.

    **param user:** API Key a deslogear en formato string.  
    **type user:** input(str)

    **returns:** Esta funcion no tiene retornos.
    """

    llave = input("Ingrese Key a deslogear:\n")
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
            print("Deslogeo correcto")
    except Exception as e:
        print("Ocurrio un error al intentar deslogar el id: {}".format(llave))    


""" ##Menu con argumentos de sistema

Para llamar a la funcion logeo se debe ejcutar el script con el argumento de sistema logeo.
Para dar de baja una key se debe ejcutar el script con el argumento de sistema deslogeo.
**Ej: CLI: .~\proyecto_zabbix\carga_ont\sesiones_manual.py logeo**

La exepcion informa que ninguna opcion pasada es correcta.
"""
try:
    if sys.argv[1] == "logeo":
        autorizar()
    elif sys.argv[1] == "deslogeo":
        logout()
    else:
        pass
except Exception as e:
    print("No usaste ningun argumento. Las opciones son:\n * \"logeo\" para obtener una ID \n * \"deslogeo\" para borrar un sesion ID")
