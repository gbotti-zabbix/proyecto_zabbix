#/usr/bin/python

import requests
import urllib

proxies = {"http://192.168.211.4":"http://f030014:brisingr05@proxy.in.iantel.com.uy:80"}
proxies2 = {"http": "http://f030014:brisingr05@proxy.in.iantel.com.uy:80","https": "https://f030014:brisingr05@proxy.in.iantel.com.uy:80"}
encabezado = {"Content-Type": "application/json-rpc"}

r = requests.get("http://192.168.211.4/zabbix/api_jsonrpc.php",headers=encabezado,proxies=urllib.request.getproxies())

print(r.status_code)