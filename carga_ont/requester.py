#/usr/bin/python

import requests
import json

from direcciones import url

encabezado = {"Content-Type": "application/json-rpc"}

def requester(payload):
    r = requests.post(url,headers=encabezado,json=payload)
    return r