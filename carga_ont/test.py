import requests
import json

#r = requests.get('https://api.github.com/events')

#r = requests.post('https://httpbin.org/post', data = {'key':'value'})

#print(r.text)
'''
payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
payload2= {
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
r = requests.get('https://httpbin.org/get', params=payload2)
print(r.url)
'''

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
print(r.json())
print(type(r.text))
print(type(r.json()))