#!/usr/bin/python
import mysql.connector
import pickle
from datetime import datetime, date
import json
import re
import sys

def sacar_grupo(grupos):
    tipo = ""
    if "C300"  in grupos:
        Tipo = "C300"
    elif "MA5800" in grupos:
        Tipo = "MA5800"
    elif "ISAM-FX" in grupos:
        Tipo = "ISAM-FX"
    return Tipo


def regex_puerto(nombre):
    Puerto = ""
    match_puerto = re.search("([0-9])[/-]([0-9]{1,2})[/-]([0-9]{1,2})",nombre)
    if match_puerto:
        Puerto = match_puerto.group()
    return Puerto


def regex_etiqueta(nombre):
    pass
    Etiqueta = ""
    match_etiqueta = re.search("(?<=([0-9]) : ).*",nombre)
    if match_etiqueta:
        Etiqueta = match_etiqueta.group()[:-5]
    return Etiqueta


def parseo_ont():

    #Variables de contadores y escritura del pickle
    contador_carga = 0
    contador_error = 0
    lista_tuplas = []
        
    archivo_pickle = "/var/lib/reportes-zabbix/crudos/Merged-Trends-" + str(date.today()) + "_ONT.pickle"
    crudo = "/var/lib/reportes-zabbix/Merged-Trends-" + str(date.today()) + ".ndjson"

    with open(crudo,"r") as crudo:
        crudo = crudo.read().splitlines()
        for linea in crudo:
            #cada linea se pasa de json a dicc
            linea = json.loads(linea)
            if "ONT" in linea["applications"] and "Radio Base" in linea["name"]:
                Tipo = sacar_grupo(linea["groups"])
                Nodo = linea["host"]
                Nombre = linea["name"]
                Puerto = regex_puerto(Nombre)
                Direccion = Nombre[-2:]
                Etiqueta = regex_etiqueta(Nombre)

                #Fecha y hora salen a partir de procesar tiempo
                Tiempo = datetime.fromtimestamp(linea["clock"]).strftime('%Y-%m-%d %H:%M:%S').split()
                #

                #Paso los bits a mega para picos y avg
                Promedio = float(linea["avg"])/1024/1024
                Pico = float(linea['max'])/1024/1024
                #
                if (Direccion == "RX" and Pico < 2500 and Promedio < 2500) or (Direccion == "TX" and Pico < 1250 and Promedio < 1250):
                    tupla = (Tipo, Nodo,Puerto,Direccion, Etiqueta, Tiempo[1],Tiempo[0],Promedio,Pico)
                    lista_tuplas.append(tupla)
                    contador_carga = contador_carga + 1
                else:
                    contador_error = contador_error + 1
                    pass
            else:
                contador_error = contador_error + 1

    #dump en pickle
    with open(archivo_pickle,"wb") as archivo_pickle:
        pickle.dump(lista_tuplas,archivo_pickle)
    
    #printeo descartes, mas adelante voy a gestionarlos en log
    print("{} lineas ingresadas. {} lineas no ingresadas".format(contador_carga,contador_error))


def pusheo_crudos_diarios_ONT():

    print(datetime.now())

    archivo_pickle = "/var/lib/reportes-zabbix/crudos/Merged-Trends-" + str(date.today()) + "_ONT.pickle"
    sql = "INSERT INTO `crudos_diarios_ont` (`tipo`,`nodo`, `puerto`, `direccion`, `etiqueta`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    
    #carga el pickle
    with open (archivo_pickle, 'rb') as lista:
        lista_tuplas = pickle.load(lista)
    #
    
    #coneccion con la BD
    mydb = mysql.connector.connect(host="localhost",user="reportes",password="antel2020",database="reportes_zabbix")
    mycursor = mydb.cursor()
    #

    #pusheo a BD
    mycursor.executemany(sql, lista_tuplas)
    mydb.commit()
    contador_ingresos = mycursor.rowcount
    print("Total Ingresado",contador_ingresos)
    print(datetime.now())


#Menu
if sys.argv[1] == "parseo":
    parseo_ont()
elif sys.argv[1] == "pusheo":
    pusheo_crudos_diarios_ONT()