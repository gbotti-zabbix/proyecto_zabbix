import json
import datetime
import pickle

contador = 0
lista_picos = []
with open("test-heavy.ndjson","r") as archivo:
    archivo = archivo.read().splitlines()
    for linea in archivo:
        linea = json.loads(linea)
        if linea["max"] != 0:
            lista_picos.append(linea['max'])
        #print(linea["host"],linea["name"],datetime.datetime.fromtimestamp(linea["clock"]).strftime('%c'),int(linea["avg"])/1024/1024,int(linea['max'])/1024/1024)
        #contador = contador + 1
    with open("picos","wb") as picos:
        pickle.dump(lista_picos,picos)
print("Lineas Procesadas",len(lista_picos))