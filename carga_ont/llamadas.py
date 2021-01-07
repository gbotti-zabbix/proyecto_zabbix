import requests
import json

from direcciones import url
from getpass import getpass

encabezado = {"Content-Type": "application/json-rpc"}

def requester(payload):
    r = requests.post(url,headers=encabezado,json=payload)
    return r

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

def host_get(nodo,auth):
    #SACAR UN HOST ID ESPECIFICO A PARTIR DEL NOMBRE 
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


def unused():
    #SACAR UN INTERFACE ID A PARTIR DE HOST ID
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

    #SACAR UN APP ID DE ONT A PARTIR DE HOST ID
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

    #CONSULTAR ITEM POR NOMBRE Y KEY
    #POR KEY
    #KEY TAMBIEN ME DEJA HACER BUSQUEDAS MAS JUSTADAS COMO DIRECCIONES O TIPOS DE ITEM
    '''
    {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": ["name","key_"],
            "search": {
                "key_": "PONRX[zxAnPonOnuIfRxOctets.ONT17/1/4]"
            },
            "sortfield": "name"
        },
        "auth": "codigoauthdelogin.json",
        "id": 1
    }
    '''
    #POR NOMBRE
    '''
    {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": ["name","key_"],
            "search": {
                "name": "ONT - GP0801-22024459-PINAZO-MORAN - RX"
            },
            "sortfield": "name"
        },
        "auth": "23f8f52facd8cfc607d92862d38d669a",
        "id": 1
    }
    '''