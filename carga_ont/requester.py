#/usr/bin/python

import requests
import json


url = "http://10.0.0.101/zabbix/api_jsonrpc.php"

encabezado = {"Content-Type": "application/json-rpc"}

def requester(payload):
    r = requests.post(url,headers=encabezado,json=payload)
    return r