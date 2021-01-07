import requests
import json

from direcciones import url
from llamadas import host_get 

host_get("Tuviega")

'''
r = requests.post(url,proxies=proxies,headers=encabezado,json=payload)

print(r.status_code)
#print(r.text)
#print(r.json()["result"][0])
#print(r.json()["result"][0]["name"])
#nombre = r.json()["result"][0]["name"]

#print(type(r.text))
#print(type(r.json()))
#print(type(r.json()["result"][0]))
#print(type(r.json()["result"][0]["name"]))

#testeo = "ONT - GP0801-22024459-PINAZO-MORAN - RX"

#if testeo == nombre:
    #print("Tal Cual")
'''