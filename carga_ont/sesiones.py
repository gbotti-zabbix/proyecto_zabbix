def autorizar(usuario,contraseña):
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
    print(llave.text)

def logout(llave):
    logout = {
    "jsonrpc": "2.0",
    "method": "user.logout",
    "params": [],
    "id": 1,
    "auth": llave
    }
    deslogeo = requester(logout)
    print(deslogeo.text)

autorizar(input("Ingrese User:\n"),getpass("Ingrese Password:\n"))
logout(input("Ingrese Key a deslogear:\n"))