#!/usr/bin/python
import mysql.connector
import pickle
from datetime import datetime, date
import json
import re
import sys


lista_tuplas = []
lista_puerto_etiqueta = []

def parseo_ont():
    contador_carga = 0
    contador_error = 0
    crudo = "/var/lib/reportes-zabbix/Merged-Trends-" + str(date.today()) + ".ndjson"
    archivo_pickle = "/var/lib/reportes-zabbix/Merged-Trends-ONT-" + str(date.today()) + ".pickle"
    #abro el archivo en read y separo en listas de json
    with open(crudo,"r") as crudo:
        #archivo parseado
        with open(archivo_pickle,"wb") as archivo_pickle:
            crudo = crudo.read().splitlines()
            #
            
            for linea in crudo:
                #cada linea se pasa de json a dicc
                linea = json.loads(linea)
                #

                #Arranca parseo
                if "ONT" in linea["applications"]:
                    #Tipo
                    if "C300"  in linea["groups"]:
                        Tipo = "C300"
                    elif "MA5800" in linea["groups"]:
                        Tipo = "MA5800"
                    #
                    #Nodo
                    Nodo = linea["host"]
                    #
                    #Nombre
                    Nombre = linea["name"][13:-5]
                    #
                    #Direccion
                    Direccion = linea["name"][-2:]
                    #
                    #Fecha y hora salen a partir de procesar tiempo
                    Tiempo = datetime.fromtimestamp(linea["clock"]).strftime('%Y-%m-%d %H:%M:%S').split()
                    #
                    #Paso los bits a mega para picos y avg
                    Promedio = float(linea["avg"])/1024/1024
                    Pico = float(linea['max'])/1024/1024
                    #
                    #Puerto (que dios me perdone), lista_puerto_etiqueta viene de la funcion puerto_etiqueta
                    for x in lista_puerto_etiqueta:
                        if Nombre == x[0]:
                            Puerto = x[1]
                    #
                    #termine de extraer datos

                    #creo lista de tuplas para picklear y ademas filtro
                    if (Pico < 2500 and Promedio < 2500):
                        tupla = (Tipo,Nodo,Puerto,Nombre,Direccion,Tiempo[1],Tiempo[0],Promedio,Pico)
                        lista_tuplas.append(tupla)
                        contador_carga = contador_carga + 1
                    else:
                        contador_error = contador_error + 1
                        pass
            pickle.dump(lista_tuplas,archivo_pickle)
    print("{} lineas ingresadas. {} lineas no ingresadas".format(contador_carga,contador_error))

def puerto_etiqueta():
    with open ("datos_puertos_RBS","r") as puertos_RBS:
        puertos_RBS = puertos_RBS.readlines()
        for x in puertos_RBS:
            Key = x.split(":")[4]
            Nombre = x.split(":")[5][13:-6]
            match_puerto = re.search("ONT([0-9]{1}|[0-9]{2})[/-]([0-9]{1}|[0-9]{2})",Key)
            if match_puerto:
                Puerto = match_puerto.group()[3:]
                Tupla = (Nombre,Puerto)
                lista_puerto_etiqueta.append(Tupla)

def pusheo_crudos_diarios():
    print(datetime.now())
    archivo_pickle = "/var/lib/reportes-zabbix/Merged-Trends-ONT-" + str(date.today()) + ".pickle"
    contador_insert = 0
    lista_final = []
    contador_final = []
    sql = "INSERT INTO `crudos_diarios` (`tipo`,`nodo`, `puerto`, `nombre`, `direccion`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    with open (archivo_pickle, 'rb') as lista:
        #carga de lista
        lista_tuplas = pickle.load(lista)
        #
    mydb = mysql.connector.connect(host="localhost",user="reportes",password="antel2020",database="reportes_zabbix")
    mycursor = mydb.cursor()

    for dato in lista_tuplas:
        lista_final.append(dato)
        contador_insert = contador_insert + 1
        if contador_insert == 10000:
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

def extractor_puertos():
    pass

#Llamadas a la funcion
if sys.argv[1] == "parseo":
    puerto_etiqueta()
    parseo_ont()
elif sys.argv[1] == "pusheo":
    pusheo_crudos_diarios()
elif sys.argv[1] == "extractor":
    extractor_puertos()

puerto_etiqueta()
parseo_ont()