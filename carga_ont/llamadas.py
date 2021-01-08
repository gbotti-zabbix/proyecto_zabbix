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
    for dato in chequeo.json()["result"]:
        print(dato[opcion])


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
            "output": ["hostid","name"]    
        },
        "auth": auth,
        "id": 1
    }
    print(host_get)

#SACAR UN INTERFACE ID A PARTIR DE HOST ID
def get_inter_id():
    '''
    {
        "jsonrpc": "2.0",
        "method": "hostinterface.get",
        "params": {
        "output": ["interfaceid","hostid","type"],
            "hostids": "11132",
            "filter": {
                "type": "2"
            }     
        },
        "auth": "codigoauthdelogin.json",
        "id": 1
    }
    '''
    pass

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


ont_check("name","ONT - GP0801-22024459-PINAZO-MORAN","40274b3dc84ece38005a667fd7737fb4")
ont_check("key_","PONRX[zxAnPonOnuIfRxOctets.ONT17/1/4]","40274b3dc84ece38005a667fd7737fb4")