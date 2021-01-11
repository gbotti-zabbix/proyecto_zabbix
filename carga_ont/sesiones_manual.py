import sys

from requester import requester
from getpass import getpass

def autorizar():
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


#manejo manual de sesion desde CLI
try:
    if sys.argv[1] == "logeo":
        autorizar()
    elif sys.argv[1] == "deslogeo":
        logout()
    else:
        pass
except Exception as e:
    print("No usaste ningun argumento. Las opciones son:\n * \"logeo\" para obtener una ID \n * \"deslogeo\" para borrar un sesion ID")
