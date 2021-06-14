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

""" ###Script que parsea crudos de Zabbix y Telelink

Toma archivos ndjson desde Zabbix y csv desde telelink/gestion, los parsea en un formato util para cargarlo a la base de datos
y los guarda en archivos pickle para zabbix y csv para Telelink.

Importar **pickle** y **json** es esencial para parsear Zabbix.

Si se queire cambiar el nombre de los crudos a buscar o el nombre con el que se guardaran los crudos
se debe editar las variables/funciones importadas desde **direcciones**.

Tambien se importa *modelos_nodos* para procesar los vendors de distinta forma, de necesitar diferenciar
nuevos modelos, editar esta variable en direcciones.

Contiene las funciones:
    **FileCheck** - Chequea que el archivo crudo a parsear exista.  
    **f_parsear_inventario** - Parsea el archivo crudo de TLK para pushearlo a la BD. Puertos PON.  
    **f_parseo_inventario_RBS** - Parsea el archivo crudo de gestion para pushearlo a la BD. RBS en ONT.  
    **sacar_grupo** -  Revisa a que el valor a parsear corresponda a un nodo deseado.  
    **regex_puerto** -  Extrae el numero de puerto en el formato deseado, a partir de una string.  
    **regex_etiqueta** -  Extrae la etiqueta de puerto en el formato deseado, a partir de una string.  
    **sacar_direccion** -  Traduce Bit Sent/Recieved a TX o RX segun corresponda.  
    **metodo** - Parametro utilizado por los orquestadores, define crudozabbix dependiendo el parametro en
    formato string que se le pase.  
    **parseo_ont** - Parsea el archivo crudo de Merged-Trends para pushearlo a la BD. Vuelva los datos en un .pickle.
    Solo en ONTs.  
    **parseo_pon** - Parsea el archivo crudo de Merged-Trends para pushearlo a la BD. Vuelva los datos en un .pickle.
    Solo puertos PON/Uplink.
"""

def FileCheck(fn):
    """***Chequea la existencia de un archivo***

    Se pasa un directorio en formato string y chequea que exista. 
    Logea un error si no lo encuentra.

    **param fn:** Directorio a chequear.  
    **type fn:** str

    **returns:** Returna 0 o 1 dependiendo si lo encontro o no respectivamente.  
    **rtype:** int
    """
    try:
        open(fn, "r")
        return 1
    except IOError:
        logger.error (f"Error 23: Archivo no Existe: {fn}")
        return 0


"""##Parseo TLK/Gestion"""

def f_parsear_inventario (archivo_origen,archivo_destino,archivo_old):
    """***Funcion para parsear el inventario de Telelink, recibe 3 nombres arhivos***

    **param archivo_origen:** recibe el path y nombre del archivo a parsear.  
    **type archivo_origen:** str

    **param archivo_origen:** archivo_destino: es el nombre del arhivo con que se graban los datos paresados.  
    **type archivo_origen:** str

    **param archivo_origen:** arhivo_old: luego de parsear el arhivo lo dejo con otro nombre.  
    **type archivo_origen:** str
    """
    
    logger.info ("\n--Se comenzo parseo arhivo--")
    #**Debo cargar diccionario de TLK-NOMBRE GESTION**
    sql = "SELECT cod_tlk,nom_gestion FROM t_tlk_nombregestion;"
    comentario="Traer nombre gestion"
    #**Cargo diccionarios para trabajar con nombres.** 
    dic_gestion={}
    resultado= conector(sql,"select",comentario)
    for x in resultado:
        dic_gestion[x[0]]=[x[1]] 


    #***Debo cargar equivelente - (TIPO NODO)<-->***
    sql = "SELECT nro_tlk,modelo,letra_gestion from t_diccionario_nodos_tlk;"
    comentario="Traer tipos nodos"
    dic_nodo={}
    resultado= conector(sql,"select",comentario)
    for x in resultado:
        dic_nodo[x[0]]=[x[1],x[2]] 

    linea_valida=0
    #**contador de lines de archivo**
    contador=0 
    with open(archivo_origen,'r') as archivo:
        with open(archivo_destino,"w", newline="") as archivo2:
            wr = csv.writer(archivo2, quoting=csv.QUOTE_ALL)
            archivo = archivo.read().splitlines()
            #**contador solo para saltar primera línea.**
            contador_salto=1 
            for linea in archivo:
                if contador_salto > 1:
                    #**divido linea a linea por punto y coma**
                    linea_parseada = linea.split (";")   
                    #**codigo TLK**                       
                    cod_telelink = linea_parseada[0][:10]                       
                    central_valida = str(linea_parseada[0][10])
                    if central_valida == "M":
                        linea_valida = 1
                    else:
                        linea_valida = 0
                    #**nro de equipo TLK completo.**    
                    nro_equipo = linea_parseada[1]
                    if linea_parseada[1][0:2] in dic_nodo: 
                        tipo_equipo = dic_nodo[linea_parseada[1][0:2]][0]
                        letra_nodo = dic_nodo[linea_parseada[1][0:2]][1]
                    else: 
                        tipo_equipo = "Null"
                        letra_nodo = "Null"
                    
                    #**Extraigo del numero equipo el nuermo de nodo**
                    nro_nodo = linea_parseada[1][2:4]
                    if cod_telelink in dic_gestion:
                        nombre_gestion= dic_gestion[cod_telelink][0]+"-"+nro_nodo+ letra_nodo
                    else:
                        nombre_gestion = "Null"
                    #**Extraigo del numero equipo el nuermo de slot.**
                    slot = linea_parseada[1][5:7]
                    #**Extraigo del numero equipo el nuermo de puerto.**                               
                    puerto = linea_parseada[1][7:9] 
                    #**Extraigo del numero equipo el nuermo de ont.**                                
                    ont =   linea_parseada[1][9:12]                             
                    estado = linea_parseada[2]
                    desc_estado = linea_parseada[3].strip()
                    fibra_primaria = linea_parseada[4].strip()
                    linea_parseada[5]=linea_parseada[5].strip()
                    if  linea_parseada[5]=='':
                        par_fibra= "Null"
                    else:
                        par_fibra=int(linea_parseada[5])
                    #**Se cheque empresarial, si el campo es I, si tiene VozF, Datos o RBS.**
                    #**Chequeo si hay empresarial.**    
                    if linea_parseada[6]=="I":
                        indicador_empresarial = 1
                    else:
                        indicador_empresarial = 0
                    #**Chequeo si hay VozF**
                    if linea_parseada[7]=="S":
                        indicador_voz = 1
                    else:
                        indicador_voz = 0
                    #**Chequeo si hay Datos**
                    if linea_parseada[8]=="S":
                        indicador_datos = 1
                    else:
                        indicador_datos =  0
                    #**Chequeo si hay RBS**
                    if  "MRBS" in linea_parseada[9:18]:
                        indicador_RBS = 1
                    else:
                        indicador_RBS = 0
                    
                    indice_unico = nombre_gestion +  "_" + str(int(slot)) + "/" + str(int (puerto))
                    if (linea_valida == 1):
                        linea_nueva= [indice_unico,cod_telelink,nro_equipo,tipo_equipo,nombre_gestion,nro_nodo,slot,puerto, ont, estado, desc_estado,fibra_primaria,par_fibra, indicador_empresarial, indicador_voz, indicador_datos, indicador_RBS] 
                        wr.writerow(linea_nueva)
                #**solo elimina la primera linea**
                contador_salto = contador_salto + 1
                contador = contador+1

    logger.info(f'función f_parsear_inventario ejecutada {archivo_destino} con {contador} lineas')
    if FileCheck(archivo_old):
        os.remove(archivo_old)


    os.rename(archivo_origen, archivo_old)
    logger.info( f'Se terminó el parseo del arhivo: {archivo_origen}')
    logger.info(f'Se renombro el arhivo {archivo_origen} en el arhivo {archivo_old} \n')


def f_parseo_inventario_RBS(archivo_origen,archivo_destino,archivo_old):
    """***Función que recibe el archivo de Radbio Bases DSC y luego lo parsea***
        
    El archivo se transfiere de Ritaf todas las semanas.
    
    **param archivo_origen:** nombre con direccion absoluta del archivo origen de Radio Bases DSC.  
    **type archivo_origen:** str 

    **param archivo_destino:** nombre con direccion absoluta del archivo destino, como será guardado los datos parseados.  
    **type archivo_origen:** str  
    
    **param archivo_old:** nombre con direccion absoluta del archivo con el que será renombrado el archivo origen luego de parsear.  
    **type archivo_origen:** str  
    """

    logger.info ("\n--Se comenzo parseo arhivo RBS --")
    
    #**Debo cargar diccionario de TLK-NOMBRE GESTION.**
    sql = "SELECT cod_tlk,nom_gestion FROM t_tlk_nombregestion;"
    comentario="Traer nombre gestion"
    #**Cargo diccionarios para trabajar con nombres.**
    dic_gestion={}
    resultado= conector(sql,"select",comentario)
    for x in resultado:
        dic_gestion[x[0]]=[x[1]] 

    #**Debo cargar equivelente - (TIPO NODO)<-->**
    sql = "SELECT nro_tlk,modelo,letra_gestion from t_diccionario_nodos_tlk;"
    comentario="Traer tipos nodos"
    dic_nodo={}
    resultado= conector(sql,"select",comentario)
    for x in resultado:
        dic_nodo[x[0]]=[x[1],x[2]] 

    #**Contador de lines de archivo.**
    contador=0 
    with open(archivo_origen,'r') as archivo:
        with open(archivo_destino,"w", newline="") as archivo2:
            wr = csv.writer(archivo2, quoting=csv.QUOTE_ALL)
            archivo = archivo.read().splitlines()
            #**Contador solo para saltar primera línea.**
            contador_salto=1
            for linea in archivo:
                if contador_salto > 1:
                    #**Divido linea a linea por punto y coma.**
                    linea_parseada = linea.split (";")
                    #**Creación campos para la BD**
                    servicio = linea_parseada[0]
                    nro_equipo= linea_parseada[4]
                    #**Extraigo del numero equipo el nuermo de slot.**
                    slot = linea_parseada[4][5:7]
                    #**Extraigo del numero equipo el nuermo de puerto.**               
                    puerto = linea_parseada[4][7:9]   
                    #**Extraigo del numero equipo el nuermo de ontslot.**                          
                    ont =   linea_parseada[4][9:12]
                    estado_ont= linea_parseada[5]
                    fecha_inicio_estado = linea_parseada[6]
                    dias_desde_ultimo_estado = linea_parseada[7]
                    etiqueta = linea_parseada[9]
                    nodo = linea_parseada[11]
                    nodo_slot_puerto_ont = linea_parseada[11]+"-"+slot+"/"+puerto+"/"+ont
                    linea_nueva=[nodo_slot_puerto_ont,servicio,nro_equipo,estado_ont, fecha_inicio_estado,dias_desde_ultimo_estado,etiqueta,nodo, slot, puerto, ont ]
                    wr.writerow(linea_nueva)
                #**Solo elimina la primera linea.**
                contador_salto = contador_salto + 1 
                contador = contador+1

    if FileCheck(archivo_old):
        os.remove(archivo_old)
    os.rename(archivo_origen, archivo_old)
    logger.info( f'Se terminó el parseo del arhivo: {archivo_origen}')
    logger.info(f'Se renombro el arhivo {archivo_origen} en el arhivo {archivo_old} \n')


"""##Parseo de Inventario Zabbix"""


def sacar_grupo(grupos):
    """***Chequea pertenencia de nodo a grupo deseado***

    Recive una lista de Grupos Zabbix vinculadas al nodo, chequea si es alguno de los grupos
    esperados y devuelve el grupo como tipo.

    Es esperado que devuelva el modelo del nodo que corresponde al grupo vinculado al nodo en Zabbix.

    **param grupos:** Grupos vinculados al nodo en Zabbix.  
    **type grupos:** list

    **returns:** Modelo del nodo.  
    **rtype:** str
    """
    for tipo in modelos_nodos:
        if tipo in grupos:
            return tipo 


def regex_puerto(nombre,tipo):
    """***Extrae puerto en un formato especifico a partir de string***

    A partir de una string extrae el numero de puerto en formato **PLACA/PUERTO** para PON/Uplink y
    **PLACA/PUERTO/ONT** para las ONT.

    **param nombre:** String a buscar puerto.  
    **type nombre:** str

    **param tipo:** Definir si se quiere obtener puerto para PON/Uplink o ONT. Recibe "PON"/"ONT".  
    **type tipo:** str

    **returns:** Puerto en formato **PLACA/PUERTO** para PON/Uplink, **PLACA/PUERTO/ONT** para ONT.  
    **rtype:** str
    """

    Puerto = ""
    if tipo == "PON":
        match_puerto = re.search("([0-9])[/-]([0-9]{1,2})[/-]([0-9]{1,2})",nombre)
    elif tipo == "ONT":
        match_puerto = re.search("([0-9]{1,2})[/-]([0-9]{1,2})[/-]([0-9]{1,2})",nombre)
    if match_puerto:
        Puerto = match_puerto.group()
    else:
        Puerto = "DROP"
    return Puerto


def regex_puerto_nokia(nombre):
    match_puerto = re.search("([0-9])[/-]([0-9]{1,2})[/-]([0-9]{1,2})",nombre)
    if match_puerto:
        Puerto = match_puerto.group()[2:]
        return Puerto
    elif "nt-a:xfp:1" in nombre:
        Puerto = "a/1"
        return Puerto
    elif "nt-a:xfp:2" in nombre:
        Puerto = "a/2"
        return Puerto
    elif "nt-b:xfp:1" in nombre:
        Puerto = "b/1"
        return Puerto
    else:
        Puerto = "DROP"
        return Puerto


def regex_etiqueta(nombre):
    """**Extrae etiqueta de gestion en un formato especifico a partir de string**

    A partir de una string extrae la etiqueta de gestion como fue ingresada a Zabbix. Este valor viene
    en el name desde Zabbix solamente para ONT.

    Por lo general la etiqueta es el numero del servicio del cliente y su nombre.

    **param nombre:** String a buscar la etiqueta.  
    **type nombre:** str

    **returns:** Etiqueta en formato gestion.  
    **rtype:** str
    """    
    Etiqueta = ""
    match_etiqueta = re.search("(?<=([0-9]) : ).*",nombre)
    if match_etiqueta:
        Etiqueta = match_etiqueta.group()[:-5]
    return Etiqueta


def sacar_direccion(nombre):
    """***Extrae direccion en formato TX/RX a partir de string***

    A partir de una string extrae direccion del trafico del puerto. Este valor viene
    en la misma string donde se saca el puerto y etiqueta.

    Se traduce Bits Sents como TX y Bits Received como RX.

    **param nombre:** String a buscar la direccion.  
    **type nombre:** str

    **returns:** Direccion TX/RX.  
    **rtype:** str
    """
    Direccion =  ""
    match_tx = re.search("Bits sent",nombre)
    match_rx = re.search("Bits received",nombre)
    if match_tx:
        Direccion = "TX"
    elif match_rx:
        Direccion = "RX"
    return Direccion


def metodo(opcion):
    """***Define crudozabbix***

    A partir de una string define si ejectuar la funcion *curdozabbix()* traida desde
    *direcciones* o utliza la pasada desde el *orquestador_manual*.

    "auto" ejecuta *crudozabbix()*. Para cambiar esta direccion debe editarse la funcion
    importada desde *direcciones*.

    **param opcion:** String donde "auto" ejecuta *crudozabbix()* o expesifica la direccion
    donde buscar el archivo crudo.  
    **type opcion:** str

    **returns:** Direccion de archivo crudo.
    **rtype:** str
    """
    if opcion == "auto":
        return crudozabbix()
    else:
        crudoz = opcion
        return crudoz

#Parseo de ONT
def parseo_ont(opcion):
    """***Parsea crudos de zabbix y crea .pickle para reportes ONT.***

    Recorre cada linea del archivo crudozabbix. Luego de pasar por filtros
    hace append a una lista de tuplas formadas por Modelo de nodo, Nodo, Puerto, Direccion,
    Etiqueta, Hora en la que se realizo la medida, Fecha en la que se realizo la medida, 
    Promedio de la hora donde se realizo el pico, Pico, estas dos ultimas en Bps.

    Primero cada linea es traducida de JSON a LIST. Luego se chequea que la linea (ahora list)
    del archivo crudo contenga ONT en la key applications. 
    Si esto es True, se traucen valos de la lista a variables a cargar en la tupla.

    Antes de crear las tuplas y hacer el append, tambien se chequean que ciertas medidas en correspondencia
    a TX o RX no sobrepasen ciertos valores. Esto surge por registros de numeros imposibles en las interfaces
    al momento de monitorearlas. Ejemplo un puerto de 2.5 Gbps de capacidad registrando 4 Gbps de trafico.

    Una ves pasado este ultimo filtro, las lista final con todas las tuplas formateadas se escribe en el archivo .pickle 
    para ONT traido desde **direcciones**.

    Ademas se logean errores y el comienzo y finalizacion de la funcion.

    Variables a cargar en las tuplas:
    *Tipo, Nodo, Nombre* y *Direccion* son claves dentro de la lista de facil acceso.

    *Puerto* debe llamar a *regex_puerto()* usando la variable *Nombre* y la string "ONT" para generar dicha variable.

    *Etiqueta* debe llamar a *regex_etiqueta()* usando la key name para generar dicha variable.

    *Tiempo* es una conversion de unix time a un formato humano. Zabbix utiliza EPOCH Unix Time para marcar
    unidades de tiempo.
    
    *Promedio* y *pico* son Bits convertidos a Mbs para tener unidades de mejor lectura en los reportes.

    Para comprender mejor este formateo, conviene revisar un archivo crudo NDJSON generado por zabbix.

    **param opcion:** String pasado a la llamada de metodo(). Define el crudozabbix
    a utilizar (orquestador_manual o auto).  
    **type opcion:** str

    **returns:** Esta funcion no tiene retornos.
    """

    logger.info("Comienza el Parseo de ONTS")
    contador_carga = 0
    contador_error = 0
    lista_tuplas = []
    crudoz = metodo(opcion)
    with open(crudoz,"r") as crudo:
        crudo = crudo.read().splitlines()
        for linea in crudo:
            linea = json.loads(linea)
            if "ONT" in linea["applications"] and "Radio Base" in linea["name"]:
                Tipo = sacar_grupo(linea["groups"])
                Nodo = linea["host"]["host"]
                Nombre = linea["name"]
                Puerto = regex_puerto(Nombre,"ONT")
                Direccion = Nombre[-2:]
                Etiqueta = regex_etiqueta(Nombre)
                Tiempo = datetime.fromtimestamp(linea["clock"]).strftime('%Y-%m-%d %H:%M:%S').split()
                Promedio = float(linea["avg"])/1024/1024
                Pico = float(linea['max'])/1024/1024
                if (Direccion == "TX" and Pico < 2500 and Promedio < 2500) or (Direccion == "RX" and Pico < 1250 and Promedio < 1250):
                    tupla = (Tipo, Nodo,Puerto,Direccion, Etiqueta, Tiempo[1],Tiempo[0],Promedio,Pico)
                    lista_tuplas.append(tupla)
                    contador_carga = contador_carga + 1
                else:
                    contador_error = contador_error + 1
                    pass
            else:
                contador_error = contador_error + 1

    with open(archivo_pickle_ONT(),"wb") as archivo_pickle:
        pickle.dump(lista_tuplas,archivo_pickle)
    
    logger.info("Finalizo el Parseo de ONTS")
    logger.info("Datos de ONTs Parseados:{}. Lineas Descartadas {}".format(contador_carga,contador_error))


def parseo_pon(opcion):
    """***Parsea crudos de zabbix y crea .pickle para reportes PON/Uplink.***

    Recorre cada linea del archivo crudozabbix. Luego de pasar por filtros
    hace append a una lista de tuplas formadas por Id Zabbix y TLK (utilziadas para agilizar 
    consultas en la BD), Modelo de nodo, Nodo, Puerto, Direccion, Hora en la que se realizo la medida,
    Fecha en la que se realizo la medida, Promedio de la hora donde se realizo el pico, 
    Pico, estas dos ultimas en Bps.

    Primero cada linea es traducida de JSON a LIST. Luego se chequea que la linea (ahora list)
    del archivo crudo contenga modelos de nodos que sabemos parsear ademas de Network Interfaces en la key applications. 
    Si esto es True, se traucen valos de la lista a variables a cargar en la tupla.

    Antes de crear las tuplas y hacer el append, tambien se chequean que ciertas medidas en correspondencia
    a TX o RX no sobrepasen ciertos valores. Esto surge por registros de numeros imposibles en las interfaces
    al momento de monitorearlas. Ejemplo un puerto de 2.5 Gbps de capacidad registrando 4 Gbps de trafico.

    Una ves pasado este ultimo filtro, las lista final con todas las tuplas formateadas se escribe en el archivo .pickle 
    PON traido desde **direcciones**.

    Ademas se logean errores y el comienzo y finalizacion de la funcion.

    Variables a cargar en las tuplas:
    *Tipo, Nodo* y *Nombre* son claves dentro de la lista de facil acceso.

    *Puerto* debe llamar a *regex_puerto()* usando la variable *Nombre* y la string "ONT" para generar dicha variable.

    *Direccion* debe llamar a *sacar_direccion()* usando la variable *Nombre* para generar dicha variable.

    *Tiempo* es una conversion de unix time a un formato humano. Zabbix utiliza EPOCH Unix Time para marcar
    unidades de tiempo.
    
    *Promedio* y *pico* son Bits convertidos a Mbs para tener unidades de mejor lectura en los reportes.

    *id_zabbix* y *id_tlk* son concatenacion de variables (*Nodo/Puerto/Direccion*) y guiones en formato string. Se utlizan como
    inidices para consutlas en la BD.

    Para comprender mejor este formateo, conviene revisar un archivo crudo NDJSON generado por zabbix.

    **param opcion:** String pasado a la llamada de *metodo()*. Define el crudozabbix
    a utilizar (*orquestador_manual* o *auto*).  
    **type opcion:** str

    **returns:** Esta funcion no tiene retornos.
    """
    logger.info("Comienza el Parseo de Puertos PON")
    contador_carga = 0
    contador_error = 0
    lista_tuplas = []

    crudoz = metodo(opcion)

    with open(crudoz,"r") as crudo:
            crudo = crudo.read().splitlines()
            for linea in crudo:
                linea = json.loads(linea)
                if ("C300" in linea["groups"] and "Network interfaces" in linea["applications"]) or ("MA5800" in linea["groups"] and "Network interfaces" in linea["applications"]) or ("ISAM-FX" in linea["groups"] and "Network interfaces" in linea["applications"]):
                    Tipo = sacar_grupo(linea["groups"])
                    Nodo = linea["host"]["host"]
                    Nombre = linea["name"]
                    if "ISAM-FX" in linea["groups"]:
                        Puerto = regex_puerto_nokia(Nombre)
                        if Puerto == "DROP":
                            continue
                    else:
                        Puerto = regex_puerto(Nombre,"PON")[2:]
                        if Puerto == "OP":
                            contador_error = contador_error + 1
                            continue
                    Direccion = sacar_direccion(Nombre)
                    Tiempo = datetime.fromtimestamp(linea["clock"]).strftime('%Y-%m-%d %H:%M:%S').split()
                    Promedio = float(linea["avg"])/1024/1024
                    Pico = float(linea['max'])/1024/1024
                    id_zabbix = str(Nodo + "_" + Puerto + "_" + Direccion)
                    id_tlk = str(Nodo + "_" + Puerto)
                    if (Direccion == "TX" and Pico < 2500 and Promedio < 2500) or (Direccion == "RX" and Pico < 1250 and Promedio < 1250) or (Puerto == "21/1" and Pico < 10000 and Promedio < 10000) or (Puerto == "22/1" and Pico < 10000 and Promedio < 10000) or (Puerto == "9/0" and Pico < 10000 and Promedio < 10000) or (Puerto == "10/0" and Pico < 10000 and Promedio < 10000):
                        tupla = (id_zabbix, id_tlk, Tipo, Nodo,Puerto,Direccion,Tiempo[1],Tiempo[0],Promedio,Pico)
                        lista_tuplas.append(tupla)
                        contador_carga = contador_carga + 1
                    else:
                        contador_error = contador_error + 1
                        pass
                else:
                    contador_error = contador_error + 1

    with open(archivo_pickle_PON(),"wb") as archivo_pickle:
        pickle.dump(lista_tuplas,archivo_pickle)

    logger.info("Finalizo el Parseo de PON")
    logger.info("Datos puertos PON Parseados:{}. Lineas Descartadas {}".format(contador_carga,contador_error))


