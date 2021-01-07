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

def sesion_manual(opcion):
    if opcion == "autorizar":
        autorizar(input("Ingrese User:\n"),getpass("Ingrese Password:\n"),"print")
    elif opcion == "logout":
        logout(input("Ingrese Key a deslogear:\n"))

#manejo manual de sesion desde CLI
if sys.argv[1] == "logeo":
    sesion_manual("autorizar")
if sys.argv[1] == "deslogeo":
    sesion_manual("logout")
if range(sys.argv) > 1:
    print("No usaste ningun argumento. Las opciones son:\n * \"logeo\" para obtener una ID \n \"deslogeo\" para borrar un sesion ID")