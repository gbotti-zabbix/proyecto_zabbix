#!/usr/bin/python

import os
import csv
import logger
import pickle
import json
import re
import sys


from datetime import datetime, date
from conector import conector
from direcciones import crudozabbix,archivo_pickle_ONT,archivo_pickle_PON, modelos_nodos

#>>>>funcion chequeo existencia archvio<<<<<<<<<<<#
def FileCheck(fn):
    """
    Funcion que perminte chquear la existencia de un archivo, devuelve 1 si existe, loqueo error si no existe.
    """
    try:
        open(fn, "r")
        return 1
    except IOError:
        logger.error (f"Error 23: Archivo no Existe: {fn}")
        return 0
#fin FileCheck(fn)


#>>>>>>funcion parsear inventario telelink<<<<<<<<<<<<<<<#
def f_parsear_inventario (archivo_origen,archivo_destino,archivo_old):
    """ Funcion para parsear el inventario de Telelink, recibe 3 nombres arhivos
        archivo_origen: recibe el path y nombre del archivo a parsear
        archivo_destino: es el nombre del arhivo con que se graban los datos paresados
        arhivo_old: luego de parsear el arhivo lo dejo con otro nombre.
    """
    logger.info ("\n--Se comenzo parseo arhivo--")
    #-- Cargo diccionarios para trabajar con nombres ----
    # debo cargar diccionario de TLK-NOMBRE GESTION
    sql = "SELECT cod_tlk,nom_gestion FROM t_tlk_nombregestion;"
    comentario="Traer nombre gestion"
    dic_gestion={}
    resultado= conector(sql,"select",comentario)
    for x in resultado:
        dic_gestion[x[0]]=[x[1]] 


    

    # debo cargar equivelente - (TIPO NODO)<-->
    sql = "SELECT nro_tlk,modelo,letra_gestion from t_diccionario_nodos_tlk;"
    comentario="Traer tipos nodos"
    dic_nodo={}
    resultado= conector(sql,"select",comentario)
    for x in resultado:
        dic_nodo[x[0]]=[x[1],x[2]] 

    #print (dic_nodo)
    contador=0 # contador de lines de archivo
    with open(archivo_origen,'r') as archivo:
        with open(archivo_destino,"w", newline="") as archivo2:
            wr = csv.writer(archivo2, quoting=csv.QUOTE_ALL)
            archivo = archivo.read().splitlines()
            contador_salto=1 #contador solo para saltar primera línea
            for linea in archivo:
                if contador_salto > 1:
                    linea_parseada = linea.split (";")                          #divido linea a linea por punto y coma
                    #print (linea_parseada)
                    cod_telelink = linea_parseada[0][:10]                       # codigo TLK
                    nro_equipo = linea_parseada[1]                              # nro de equipo TLK completo    
                    if linea_parseada[1][0:2] in dic_nodo: 
                        tipo_equipo = dic_nodo[linea_parseada[1][0:2]][0]
                        letra_nodo = dic_nodo[linea_parseada[1][0:2]][1]
                    else: 
                        tipo_equipo = "Null"
                        letra_nodo = "Null"
                    
                    nro_nodo = linea_parseada[1][2:4]                           #estraigo del numero equipo el nuermo de nodo
                    if cod_telelink in dic_gestion:
                        nombre_gestion= dic_gestion[cod_telelink][0]+"-"+nro_nodo+ letra_nodo
                    else:
                        nombre_gestion = "Null"
                    slot = linea_parseada[1][5:7]                               #estraigo del numero equipo el nuermo de slot 
                    puerto = linea_parseada[1][7:9]                             #estraigo del numero equipo el nuermo de puerto    
                    ont =   linea_parseada[1][9:12]                             #estraigo del numero equipo el nuermo de ont
                    estado = linea_parseada[2]
                    desc_estado = linea_parseada[3].strip()
                    fibra_primaria = linea_parseada[4].strip()
                    linea_parseada[5]=linea_parseada[5].strip()
                    if  linea_parseada[5]=='':
                        par_fibra= "Null"
                    else:
                        par_fibra=int(linea_parseada[5])
                    # Se cheque empresarial, si el campo es I, si tiene VozF, Datos o RBS.
                    # Chequeo si hay empresarial    
                    if linea_parseada[6]=="I":
                        indicador_empresarial = 1
                    else:
                        indicador_empresarial = 0
                    # Chequeo si hay VozF
                    if linea_parseada[7]=="S":
                        indicador_voz = 1
                    else:
                        indicador_voz = 0
                    # Chequeo si hay Datos
                    if linea_parseada[8]=="S":
                        indicador_datos = 1
                    else:
                        indicador_datos =  0
                    # Chequeo si hay RBS
                    if  "MRBS" in linea_parseada[9:18]:
                        indicador_RBS = 1
                    else:
                        indicador_RBS = 0
                    
                    indice_unico = nombre_gestion +  "_" + str(int(slot)) + "/" + str(int (puerto))
                    linea_nueva= [indice_unico,cod_telelink,nro_equipo,tipo_equipo,nombre_gestion,nro_nodo,slot,puerto, ont, estado, desc_estado,fibra_primaria,par_fibra, indicador_empresarial, indicador_voz, indicador_datos, indicador_RBS] 
                    #print (linea_nueva)
                    wr.writerow(linea_nueva)
                contador_salto = contador_salto + 1 #solo elimina la primera linea
    #----------------------------------------------------
                contador = contador+1
    #descomentar para procesar 30 lineas
                #if contador == 30:
                #   break
    #------------------------------------------------------
    logger.info(f'función f_parsear_inventario ejecutada {archivo_destino} con {contador} lineas')
    if FileCheck(archivo_old):
        os.remove(archivo_old)


    os.rename(archivo_origen, archivo_old)
    logger.info( f'Se terminó el parseo del arhivo: {archivo_origen}')
    logger.info(f'Se renombro el arhivo {archivo_origen} en el arhivo {archivo_old} \n')

#---fin f_parsear_inventario---# 


def f_parseo_inventario_RBS(archivo_origen,archivo_destino,archivo_old):
    """Función que recibe el archivo de Radbio Bases DSC y luego lo parsea,
       Recibe el nombre arhivo origen a paresar, el nombre archivo destino
        parseado y como renombrar el archivo original
    """
    logger.info ("\n--Se comenzo parseo arhivo RBS --")
    #-- Cargo diccionarios para trabajar con nombres ----
    # debo cargar diccionario de TLK-NOMBRE GESTION
    sql = "SELECT cod_tlk,nom_gestion FROM t_tlk_nombregestion;"
    comentario="Traer nombre gestion"
    dic_gestion={}
    resultado= conector(sql,"select",comentario)
    for x in resultado:
        dic_gestion[x[0]]=[x[1]] 


    

    # debo cargar equivelente - (TIPO NODO)<-->
    sql = "SELECT nro_tlk,modelo,letra_gestion from t_diccionario_nodos_tlk;"
    comentario="Traer tipos nodos"
    dic_nodo={}
    resultado= conector(sql,"select",comentario)
    for x in resultado:
        dic_nodo[x[0]]=[x[1],x[2]] 

    contador=0 # contador de lines de archivo
    with open(archivo_origen,'r') as archivo:
        with open(archivo_destino,"w", newline="") as archivo2:
            wr = csv.writer(archivo2, quoting=csv.QUOTE_ALL)
            archivo = archivo.read().splitlines()
            contador_salto=1 #contador solo para saltar primera línea
            for linea in archivo:
                if contador_salto > 1:
                    linea_parseada = linea.split (";")                          #divido linea a linea por punto y coma
                    #print (linea_parseada)
                    #----creación campos para la BD---------
                    servicio = linea_parseada[0]
                    nro_equipo= linea_parseada[4]
                    slot = linea_parseada[4][5:7]                               #estraigo del numero equipo el nuermo de slot 
                    puerto = linea_parseada[4][7:9]                             #estraigo del numero equipo el nuermo de puerto    
                    ont =   linea_parseada[4][9:12]                             #estraigo del numero equipo el nuermo de ontslot =
                    estado_ont= linea_parseada[5]
                    fecha_inicio_estado = linea_parseada[6]
                    dias_desde_ultimo_estado = linea_parseada[7]
                    etiqueta = linea_parseada[9]
                    nodo = linea_parseada[11]
                    nodo_slot_puerto_ont = linea_parseada[11]+"-"+slot+"/"+puerto+"/"+ont
                    linea_nueva=[nodo_slot_puerto_ont,servicio,nro_equipo,estado_ont, fecha_inicio_estado,dias_desde_ultimo_estado,etiqueta,nodo, slot, puerto, ont ]
                    #print (linea_nueva)
                    wr.writerow(linea_nueva)
                contador_salto = contador_salto + 1 #solo elimina la primera linea
    #----------------------------------------------------
                contador = contador+1
    #descomentar para procesar 30 lineas
                #if contador == 2:
                #   break
    if FileCheck(archivo_old):
        os.remove(archivo_old)
    os.rename(archivo_origen, archivo_old)
    logger.info( f'Se terminó el parseo del arhivo: {archivo_origen}')
    logger.info(f'Se renombro el arhivo {archivo_origen} en el arhivo {archivo_old} \n')


''' Parseo de Inventario Zabbix'''

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


#Parseo de ONT
def parseo_ont():

    logger.info("Comienza el Parseo de ONTS")
    #Variables de contadores y escritura del pickle
    contador_carga = 0
    contador_error = 0
    lista_tuplas = []

    with open(crudozabbix(),"r") as crudo:
        crudo = crudo.read().splitlines()
        for linea in crudo:
            #cada linea se pasa de json a dicc
            linea = json.loads(linea)
            if "ONT" in linea["applications"] and "Radio Base" in linea["name"]:
                Tipo = sacar_grupo(linea["groups"])
                Nodo = linea["host"]["host"]
                Nombre = linea["name"]
                Puerto = regex_puerto(Nombre,"ONT")
                Direccion = Nombre[-2:]
                Etiqueta = regex_etiqueta(Nombre)

                #Fecha y hora salen a partir de procesar tiempo
                Tiempo = datetime.fromtimestamp(linea["clock"]).strftime('%Y-%m-%d %H:%M:%S').split()
                print(Tiempo)
                #

                #Paso los bits a mega para picos y avg
                Promedio = float(linea["avg"])/1024/1024
                Pico = float(linea['max'])/1024/1024
                #
                if (Direccion == "TX" and Pico < 2500 and Promedio < 2500) or (Direccion == "RX" and Pico < 1250 and Promedio < 1250):
                    tupla = (Tipo, Nodo,Puerto,Direccion, Etiqueta, Tiempo[1],Tiempo[0],Promedio,Pico)
                    lista_tuplas.append(tupla)
                    contador_carga = contador_carga + 1
                else:
                    contador_error = contador_error + 1
                    pass
            else:
                contador_error = contador_error + 1

    #dump en pickle
    with open(archivo_pickle_ONT(),"wb") as archivo_pickle:
        pickle.dump(lista_tuplas,archivo_pickle)
    
    #Logeo Ingresos
    logger.info("Finalizo el Parseo de ONTS")
    logger.info("Datos de ONTs Parseados:{}. Lineas Descartadas {}".format(contador_carga,contador_error))


#Parseo de Puertos PON
def parseo_pon():

    logger.info("Comienza el Parseo de Puertos PON")
    contador_carga = 0
    contador_error = 0
    lista_tuplas = []


    #abro el archivo en read y separo en listas de json, descomentar el basico o el hevy
    with open(crudozabbix(),"r") as crudo:
        #archivo parseado
            crudo = crudo.read().splitlines()
            #

            for linea in crudo:

                #cada linea se pasa de json a dicc
                linea = json.loads(linea)
                #

                #con este if filtro los que no son C300 o MA5800
                if ("C300" in linea["groups"] and "Network interfaces" in linea["applications"]) or ("MA5800" in linea["groups"] and "Network interfaces" in linea["applications"]):

                    Tipo = sacar_grupo(linea["groups"])
                    Nodo = linea["host"]["host"]
                    Nombre = linea["name"]
                    Puerto = regex_puerto(Nombre,"PON")[2:]
                    Direccion = sacar_direccion(Nombre)

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
    
    #Dump en Pickle
    with open(archivo_pickle_PON(),"wb") as archivo_pickle:
        pickle.dump(lista_tuplas,archivo_pickle)

    #Logeo Ingresos
    logger.info("Finalizo el Parseo de PON")
    logger.info("Datos puertos PON Parseados:{}. Lineas Descartadas {}".format(contador_carga,contador_error))







