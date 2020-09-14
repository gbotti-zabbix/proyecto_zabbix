#Traigo datetime para formatear epoch, json para proserar el archivo y re para filtrarlo
import datetime
import json
import re
import mysql.connector
#

#conexion a la BD
mydb = mysql.connector.connect(host="192.168.211.4",user="reportes",password="antel2020",database="diarios_crudos")
mycursor = mydb.cursor()
#

contador = 0
contador_carga = 0
contador_error = 0
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
                Puerto = match_puerto.group()[2:]
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
            Tiempo = datetime.datetime.fromtimestamp(linea["clock"]).strftime('%Y-%m-%d %H:%M:%S').split()
            #

            #Paso los bits a mega para picos y avg
            Promedio = float(linea["avg"])/1024/1024
            Pico = float(linea['max'])/1024/1024
            #
            #termine de extraer datos

            #por ahora printeo para mirar como me estan saliendo los datos, usare return? o vuelco todo a archivo?
            #print("Nodo:", Nodo,"\n","Puerto:", Puerto[2:],"\n","Direccion:", Direccion,"\n","Hora:", Tiempo[1],"\n","Fecha:", Tiempo[0],"\n","Promedio:", Promedio,"\n","Pico:", Pico)
            sql = "INSERT INTO `crudos` (`nodo`, `puerto`, `direccion`, `hora`, `fecha`, `promedio`, `pico`) VALUES ('{}','{}','{}','{}','{}',{},{})".format(Nodo,Puerto,Direccion,Tiempo[1],Tiempo[0],Promedio,Pico)
            if (Pico < 2500 and Promedio < 2500) or (Puerto == "21/1" and Pico < 10000 and Promedio < 10000) or (Puerto == "22/1" and Pico < 10000 and Promedio < 10000):
                mycursor.execute(sql)
                mydb.commit()
                contador_carga = contador_carga + 1
            else:
                contador_error = contador_error + 1
                pass
            #Todas las variables (incluidos los slicing) son str menos menos promedios y picos que son float.
        else:
            contador_error = contador_error + 1
        
        #if contador == 20:
            #break
print("{} lineas ingresadas. {} lineas no ingresadas".format(contador_carga,contador_error))