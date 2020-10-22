#!/usr/bin/env python
import time
import os
with open ("datos_central.csv","r") as archivo:
    lista = []
    #Cargo el archivo en una lista
    archivo = archivo.read().splitlines()
    #Creo una lista de listas con los valores Nodo y Central TLK
    for x in archivo:
        lista.append(x.split(";"))
        #Uso las listas dentro de lista para llamar a la api por cada nodo"
    for y in lista:
        #para este codigo no use subprocess porque me anulaba los input cuando el valor solicitado era correcto
        os.system("./zhitemfinder.py {} -u jvignolo -p brisingr -a http://10.0.0.101/zabbix/api_jsonrpc.php -e -s Radio".format(y[0]))
        #Meto el sleep para no quebrar el SV
        #time.sleep(2)

#api call
#./zhitemfinder.py CENTENARIO-06Z -u jvignolo -p brisingr -a http://127.0.0.1/zabbix/api_jsonrpc.php -e -s Radio



