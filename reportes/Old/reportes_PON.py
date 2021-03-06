#!/usr/bin/python
import mysql.connector
import pickle
from datetime import datetime, date
import json
import re
import sys

def parsea_crudos(fecha):

    contador_carga = 0
    contador_error = 0
    lista_tuplas = []
    archivo = "/var/lib/reportes-zabbix/Merged-Trends-" + fecha + ".ndjson"
    archivo_pickle = "/var/lib/reportes-zabbix/crudos/Merged-Trends-" + fecha + ".pickle"

    #abro el archivo en read y separo en listas de json, descomentar el basico o el hevy
    with open(archivo,"r") as archivo:
        #archivo parseado
        with open(archivo_pickle,"wb") as archivo2:
            archivo = archivo.read().splitlines()
            #

            for linea in archivo:

                #cada linea se pasa de json a dicc
                linea = json.loads(linea)
                #

                #con este if filtro los que no son C300 o MA5800
                if ("C300" in linea["groups"] and "Network interfaces" in linea["applications"]) or ("MA5800" in linea["groups"] and "Network interfaces" in linea["applications"]):

                    #saco grupo
                    if "C300"  in linea["groups"]:
                        Tipo = "C300"
                    elif "MA5800" in linea["groups"]:
                        Tipo = "MA5800" 
                    #

                    #empiezo a extraer los datos
                    Nodo = linea["host"]
                    #para puerto y direccion preciso regex para estaer lo que quiero de la clave name.
                    Nombre = linea["name"]
                    match_puerto = re.search("([0-9])[/-]([0-9]{1,2})[/-]([0-9]{1,2})",Nombre)
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
                    Tiempo = datetime.fromtimestamp(linea["clock"]).strftime('%Y-%m-%d %H:%M:%S').split()
                    #

                    #Paso los bits a mega para picos y avg
                    Promedio = float(linea["avg"])/1024/1024
                    Pico = float(linea['max'])/1024/1024
                    id_zabbix = str(Nodo + "_" + Puerto + "_" + Direccion)
                    id_tlk = str(Nodo + "_" + Puerto)
                    #
                    #termine de extraer datos

                    #creo lista de tuplas para picklear y ademas filtro
                    if (Direccion == "TX" and Pico < 2500 and Promedio < 2500) or (Direccion == "RX" and Pico < 1250 and Promedio < 1250) or (Puerto == "21/1" and Pico < 10000 and Promedio < 10000) or (Puerto == "22/1" and Pico < 10000 and Promedio < 10000):
                        tupla = (id_zabbix, id_tlk, Tipo, Nodo,Puerto,Direccion,Tiempo[1],Tiempo[0],Promedio,Pico)
                        lista_tuplas.append(tupla)
                        contador_carga = contador_carga + 1
                    else:
                        contador_error = contador_error + 1
                        pass
                else:
                    contador_error = contador_error + 1
            #dump pickle
            pickle.dump(lista_tuplas,archivo2)

    #printeo descartes, mas adelante voy a gestionarlos en log
    print("{} lineas ingresadas. {} lineas no ingresadas".format(contador_carga,contador_error))

def pusheo_crudos_diarios(fecha):

    #variables que uso mas adelante y consulta sql
    print(datetime.now())
    archivo_pickle = "/var/lib/reportes-zabbix/crudos/Merged-Trends-" + fecha + ".pickle"
    contador_insert = 0
    lista_final = []
    contador_final = []
    sql = "INSERT INTO `crudos_diarios` (`id_zabbix`,`id_tlk`,`tipo`,`nodo`, `puerto`, `direccion`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #

    with open (archivo_pickle, 'rb') as lista:
        #carga de lista
        lista_tuplas = pickle.load(lista)
        #

    mydb = mysql.connector.connect(host="localhost",user="reportes",password="antel2020",database="reportes_zabbix")
    mycursor = mydb.cursor()

    for dato in lista_tuplas:
        lista_final.append(dato)
        contador_insert = contador_insert + 1
        if contador_insert == 100000:
            mycursor.executemany(sql, lista_final)
            mydb.commit()
            contador_final.append(mycursor.rowcount)
            contador_insert = 0
            lista_final.clear()

    mycursor.executemany(sql, lista_final)
    mydb.commit()
    contador_final.append(mycursor.rowcount)
    print("Total Ingresado",sum(contador_final))
    print(datetime.now())


#Llamadas a la funcion

if sys.argv[1] == "parseo":
    parsea_crudos(str(date.today()))
elif sys.argv[1] == "pusheo":
    pusheo_crudos_diarios(str(date.today()))
elif sys.argv[1] == "manual":
    opcion = int(input("1-Parsear\n2-Pushear\nCtrl+c para abortar\n"))
    fecha = input("Ingresa una fecha con formato YYYY-MM-DD:\n")
    if opcion == 1:
        parsea_crudos(fecha)
    elif opcion == 2:
        pusheo_crudos_diarios(fecha)
