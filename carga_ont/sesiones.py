from requester import requester
from getpass import getpass

def autorizar(usuario,contraseña,opcion):
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
    #opcion 1 printea una llave, la opcion 2 solo la retorna
    if opcion == 1:
        print(llave)
    if opcion == 2:
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

def sesiones(opcion):
    if opcion == "autorizar":
        autorizar(input("Ingrese User:\n"),getpass("Ingrese Password:\n"),1)
    elif opcion == "logout":
        logout(input("Ingrese Key a deslogear:\n"))

sesiones("autorizar")
sesiones("logout")