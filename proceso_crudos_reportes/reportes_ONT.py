import json
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
    with open("test-heavy.ndjson","r") as crudo:
        crudo = crudo.read().splitlines()
        for linea in crudo:
            linea = json.loads(linea)
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
                #Puerto (que dios me perdone)
                for x in lista_puerto_etiqueta:
                    if Nombre == x[0]:
                        Puerto = x[1]
                #
                #termine de extraer datos

                #creo lista de tuplas para picklear y ademas filtro
                if (Pico < 2500 and Promedio < 2500):
                    tupla = (Tipo,Nodo,Nombre,Puerto,Direccion,Tiempo[1],Tiempo[0],Promedio,Pico)
                    #Test
                    #tupla = (Tipo,Nodo,Nombre,Direccion,Tiempo[1],Tiempo[0],Promedio,Pico)
                    lista_tuplas.append(tupla)
                    contador_carga = contador_carga + 1
                else:
                    contador_error = contador_error + 1
                    pass
        print("{} lineas ingresadas. {} lineas no ingresadas".format(contador_carga,contador_error))
    #Par el fromateo deberia sacar, Tipo, Nodo, Puerto, Nombre, Direccion, Fecha, Hora, Max y AVG
    #Falta
    #Puerto



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

puerto_etiqueta()
parseo_ont()


print(lista_tuplas)
