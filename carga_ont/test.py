import requests
import json

url = "http://10.0.0.101/zabbix/api_jsonrpc.php"
payload= {
    "jsonrpc": "2.0",
    "method": "item.get",
    "params": {
        "output": ["name","key_"],
        "search": {
            "key_": "PONRX[zxAnPonOnuIfRxOctets.ONT17/1/4]"
        },
        "sortfield": "name"
    },
    "auth": "23f8f52facd8cfc607d92862d38d669a",
    "id": 1
}
encabezado = {"Content-Type": "application/json-rpc"}

r = requests.post(url,headers=encabezado,json=payload)

print(r.status_code)
print(r.text)
print(r.json()["result"][0])
print(r.json()["result"][0]["name"])
nombre = r.json()["result"][0]["name"]



print(type(r.text))
print(type(r.json()))
print(type(r.json()["result"][0]))
print(type(r.json()["result"][0]["name"]))

testeo = "ONT - GP0801-22024459-PINAZO-MORAN - RX"

if testeo == nombre:
    print("Tal Cual")