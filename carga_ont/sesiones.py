import sys

from requester import requester
from getpass import getpass

def autorizar(usuario,contraseña,*args):
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
    if args[0] == "print":
        print(llave)
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
            print("Deslogeo correcto")
    except Exception as e:
        print("Ocurrio un error al intentar deslogar el id: {}".format(llave))    

#manejo manual de sesion
if sys.argv[1] == "logeo":
    autorizar(input("Ingrese User:\n"),getpass("Ingrese Password:\n"),"print")
if sys.argv[1] == "logout":
    logout(input("Ingrese Key a deslogear:\n"))

