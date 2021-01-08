import requests
import json

from requester import requester

#CHEQUEO SI UNA ONT EXISTE POR KEY O NOMBRE.
#OPCION MARCA COMO BUSCAR (key_,name), PARAMETRO ES LO QUE BUSCAR (la key o nombre especifico)
def ont_check(opcion,parametro,auth):
    ont_check = {
    "jsonrpc": "2.0",
    "method": "item.get",
    "params": {
        "output": ["{}".format(opcion)],
        "search": {
            "{}".format(opcion): "{}".format(parametro)
        },
        "sortfield": "name"
    },
    "auth": "{}".format(auth),
    "id": 1
    }
    chequeo = requester(ont_check)
    if len(chequeo.json()["result"]) < 1:
        print("No se encontro la ONT: {}".format(parametro))
        return 0
    else:
        print(chequeo.json()["result"])
        return 1

#SACAR UN HOST ID ESPECIFICO A PARTIR DEL NOMBRE 
def host_get(nodo,auth):
    host_get = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "filter": {
                "host": [
                    "{}".format(nodo)
                ]
            },
            "output": "hostid"    
        },
        "auth": auth,
        "id": 1
    }
    hostid = requester(host_get)
    if len(hostid.json()["result"]) < 1:
        print("No se encontro el nodo: {}".format(nodo))
    else:
        print(hostid.json()["result"][0]["hostid"])
        return hostid.json()["result"][0]["hostid"]

#SACAR UN INTERFACE ID A PARTIR DE HOST ID
def get_inter_id(hostid,auth):
    interfaceid = {
        "jsonrpc": "2.0",
        "method": "hostinterface.get",
        "params": {
        "output": ["interfaceid","hostid","type"],
            "hostids": "{}".format(hostid),
            "filter": {
                "type": "2"
            }     
        },
        "auth": "{}".format(auth),
        "id": 1
    }
    interfaceid = requester(interfaceid)
    if len(interfaceid.json()["result"]) < 1:
        print("No se encontro el nodo: {}".format(nodo))
    else:
        print(interfaceid.json()["result"][0]["hostid"])
        return interfaceid.json()["result"][0]["hostid"]

#SACAR UN APP ID DE ONT A PARTIR DE HOST ID
def get_app_id():
    '''
    {
        "jsonrpc": "2.0",
        "method": "application.get",
        "params": {
            "output": ["applicationid","hostid","name"],
            "hostids": "11132",
        "filter": {
            "name": ["ONT"]
        }
        },
        "auth": "codigoauthdelogin.json",
        "id": 1
    }
    '''
    pass



get_inter_id("11132","40274b3dc84ece38005a667fd7737fb4")

#host_get("AGUADA-13Z","40274b3dc84ece38005a667fd7737fb4")