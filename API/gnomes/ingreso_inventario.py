#!/usr/bin/env python
import subprocess
import time
with open ("datos_central.csv","r") as archivo:
    lista = []
    #Cargo el archivo en una lista
    archivo = archivo.read().splitlines()
    #Creo una lista de listas con los valores Nodo y Central TLK
    for x in archivo:
       	lista.append(x.split(";"))
    	#Uso las listas dentro de lista para llamar a la api por cada nodo"
    for y in lista:
        process = subprocess.run(["./zhostupdater.py","-u","jvignolo","-p","brisingr","-a","http://10.0.0.101/zabbix/api_jsonrpc.php",y[0],"-I","tag={}".format(y[1])],stdout=subprocess.PIPE,universal_newlines=True,)
        #Meto el sleep para no quebrar el SV
        time.sleep(2)

#api call
#./zhostupdater.py -u user -p password -a http://127.0.0.1/zabbix/api_jsonrpc.php NODO -I ITEMDEINVENTARIO="Prueba2"
