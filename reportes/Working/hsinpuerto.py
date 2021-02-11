import os
import csv
import logger
import pickle
import json
import re
import sys


from datetime import datetime, date
from direcciones import crudozabbix,archivo_pickle_ONT,archivo_pickle_PON, modelos_nodos

#Extraigo grupo de nodos
def sacar_grupo(grupos):
    for tipo in modelos_nodos:
        if tipo in grupos:
            return tipo 


#Regex para extraer nodo/slot/puerto a partir del nombre de la interfaz
def regex_puerto(nombre,tipo):
    Puerto = ""
    if tipo == "PON":
        match_puerto = re.search("([0-9])[/-]([0-9]{1,2})[/-]([0-9]{1,2})",nombre)
    elif tipo == "ONT":
        match_puerto = re.search("([0-9]{1,2})[/-]([0-9]{1,2})[/-]([0-9]{1,2})",nombre)
    if match_puerto:
        Puerto = match_puerto.group()
    return Puerto


#Regex para armado de etiqueta en ONT
def regex_etiqueta(nombre):
    Etiqueta = ""
    match_etiqueta = re.search("(?<=([0-9]) : ).*",nombre)
    if match_etiqueta:
        Etiqueta = match_etiqueta.group()[:-5]
    return Etiqueta


#Regex para formatear direccion
def sacar_direccion(nombre):
    Direccion =  ""
    match_tx = re.search("Bits sent",nombre)
    match_rx = re.search("Bits received",nombre)
    if match_tx:
        Direccion = "TX"
    elif match_rx:
        Direccion = "RX"
    return Direccion


def resultado(archivo):
    contador_carga = 0
    contador_error = 0
    lista_tuplas = []

    with open(archivo,"r") as crudo:
            #archivo parseado
                crudo = crudo.read().splitlines()
                #

                for linea in crudo:

                    #cada linea se pasa de json a dicc
                    linea = json.loads(linea)
                    #

                    #con este if filtro los que no son C300 o MA5800
                    if "MA5800" in linea["groups"] and "Network interfaces" in linea["applications"]:

                        Tipo = sacar_grupo(linea["groups"])
                        Nodo = linea["host"]
                        Nombre = linea["name"]
                        Puerto = regex_puerto(Nombre,"PON")[2:]
                        Direccion = sacar_direccion(Nombre)

                        #Fecha y hora salen a partir de procesar tiempo
                        Tiempo = datetime.fromtimestamp(linea["clock"]).strftime('%Y-%m-%d %H:%M:%S').split()
                        #
                        
                        #Paso los bits a mega para picos y avg
                        Promedio = float(linea["avg"])/1024/1024
                        Pico = float(linea['max'])/1024/1024
                        #
                        #termine de extraer datos

                        #creo lista de tuplas para picklear y ademas filtro
                        if Puerto != "":
                            tupla = ( Tipo, Nodo,Puerto, Nombre, Direccion,Tiempo[1],Tiempo[0],Promedio,Pico)
                            lista_tuplas.append(tupla)
                            contador_carga = contador_carga + 1
                        else:
                            contador_error = contador_error + 1
                            pass
                    else:
                        contador_error = contador_error + 1
        
    #Escribo resultado en TXT
    with open("resultado-27-01-2021check.txt","w") as resultado:
        for linea in lista_tuplas:
            resultado.write("\n")
            resultado.write(str(linea))

resultado("Merged-Trends-2021-01-27.ndjson")