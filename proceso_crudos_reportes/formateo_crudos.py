#Traigo datetime para formatear epoch, json para proserar el archivo y re para filtrarlo
import datetime
import json
import re
#

contador = 0
#abro el archivo en read y separo en listas de json, descomentar el basico o el hevy
#with open("./proceso_crudos_reportes/test","r") as archivo:
with open("./proceso_crudos_reportes/test-heavy.ndjson","r") as archivo:
    archivo = archivo.read().splitlines()
    #
    
    for linea in archivo:
        contador = contador + 1

        #cada linea se pasa de json a dicc
        linea = json.loads(linea)
        #

        #con este if filtro los que no son C300 o MA5800
        if "C300" in linea["groups"] or "MA5800" in linea["groups"]:

            #empiezo a extraer los datos
            Nodo = linea["host"]
            #para puerto y direccion preciso regex para estaer lo que quiero de la clave name.
            Nombre = linea["name"]
            match_puerto = re.search("[0-9][/-]([0-9]{1}|[0-9]{2})[/-]([0-9]{1}|[0-9]{2})",Nombre)
            match_tx = re.search("Bits sent",Nombre)
            match_rx = re.search("Bits received",Nombre)
            if match_puerto:
                Puerto = match_puerto.group()
            else:
                pass
            #a direccion la cargo con nuestra nomenclatura
            if match_tx:
                Direccion = "TX"
            elif match_rx:
                Direccion = "RX"
            else:
                pass
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
            #Todas las variables (incluidos los slicing) son str menos menos promedios y picos que son float.
        else:
            print("No entraste en el if que querias")
        
        if contador == 20:
            break