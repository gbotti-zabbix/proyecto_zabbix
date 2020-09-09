#Traigo datetime para formatear epoch, json para proserar el archivo y re para filtrarlo
import datetime
import json
import re
#

#abro el archivo en read y separo en listas de json
with open("./proceso_crudos_reportes/test-heavy.ndjson","r") as archivo:
    archivo = archivo.read().splitlines()
    #
    
    for linea in archivo:
        #cada linea se pasa de json a dicc
        linea = json.loads(linea)
        #
        
        #empiezo a extraer los datos
        Nodo = linea["host"]
        #para puerto y direccion preciso regex para estaer lo que quiero de la clave name.
        Puerto = linea["name"]
        Direccion = linea["name"]
        #
        #Fecha y hora salen a partir de procesar tiempo
        Tiempo = datetime.datetime.fromtimestamp(linea["clock"]).strftime('%c').split()
        Fecha = " ".join(Tiempo[0:2])+" "+Tiempo[-1]
        #
        #Paso los bits a mega para picos y avg
        Promedio = int(linea["avg"])/1024/1024
        Pico = int(linea['max'])/1024/1024
        #
        #termine de extraer datos

        #por ahora printeo para mirar como me estan saliendo los datos, usare return? o vuelco todo a archivo?
        print("Nodo:", Nodo,"\n","Puerto:", Puerto,"\n","Direccion:", Direccion,"\n","Hora:", Tiempo[3],"\n","Fecha:", Fecha,"\n","Promedio:", Promedio,"\n","Pico:", Pico)
        break