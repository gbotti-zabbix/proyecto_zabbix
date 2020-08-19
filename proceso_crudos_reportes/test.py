import json
import datetime

contador = 0
with open("./proceso_crudos_reportes/test-heavy.ndjson","r") as archivo:
    archivo = archivo.read().splitlines()
    for linea in archivo:
        linea = json.loads(linea)
        print(linea["host"],linea["name"],datetime.datetime.fromtimestamp(linea["clock"]).strftime('%c'),int(linea["avg"])/1024/1024,int(linea['max'])/1024/1024)
        contador = contador + 1
print("Lineas Procesadas",contador)