#/usr/bin/python

import requests
import json

from direcciones_carga_ont import url

encabezado = {"Content-Type": "application/json-rpc"}

def requester(payload):
    r = requests.post(url,headers=encabezado,json=payload)
    return r