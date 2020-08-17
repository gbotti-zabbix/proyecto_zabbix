import json
import datetime


with open("test","r") as archivo:
    archivo = archivo.read().splitlines()
    for linea in archivo:
        linea = json.loads(linea)
        print(linea["host"],linea["name"],datetime.datetime.fromtimestamp(linea["clock"]).strftime('%c'),int(linea["avg"])/1024/1024,int(linea['max'])/1024/1024)