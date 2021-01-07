import requests
import json

proxies = {"192.168.211.4:80":"http://f030014:brisingr05@proxy.in.iantel.com.uy:80"}

url = "http://192.168.211.4/zabbix/api_jsonrpc.php"
'''
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
'''

payload = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
        "user": "jvignolo",
        "password": "brisingr"
    },
    "id": 1,
    "auth": "null"
}
encabezado = {"Content-Type": "application/json-rpc"}


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