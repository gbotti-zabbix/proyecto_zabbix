#!/usr/bin/python

import logger
import time
import pusheo
import os
import traceback

from direcciones import archivo_tlk, archivo_tlk_dst, archivo_tlk_viejo, archivo_rbs_DCS, archivo_rbs_DCS_dst, archivo_rbs_DCS_old

from datetime import datetime
from pusheo import f_cargar_inv_en_BD,f_cargar_inv_RBS_en_BD, pusheo_crudos_diarios_PON, pusheo_crudos_diarios_ONT, f_procesar_resumne_tlk_BD
from parseo import parseo_ont, parseo_pon, f_parsear_inventario, f_parseo_inventario_RBS
from flujo_db import flujos
from reporte import reportes_xlsx

""" ###Parseo, pusheo, flujos en la BD y generacion de reportes PON/ONT de forma manual

Parte de la informacion ingresada en los inputs de las funciones para encontar 
archivos crudos de fechas especificas, y desde estos gestionar su ingreso a la BD
y/o generacion de reportes.

Las funciones llamadas detectan crudos a parsear, los pushean a la BD y generan los flujos
de consultas necesarioas para crear datos utiles para los reportes. Por ultimo crean los
archivos finales de reportes consultando la BD.

Se utilizan funciones que controlan dias y fechas para decidir que procedimientos ejecutar.

El *orquestador_manual* solo tiene la funcion de coordinar los distintos eslabones de los reportes
solo cuando hubo fallo con el **orquestador_automatico** o se pretende cargar crudos viejos a la BD.
Las funcionalidades finas deben editarse en las funciones importadas y llamadas desde
las funciones orquestador.

Contiene las funciones:  
    **checkFileExistance** - Chequea que el archivo crudo a parsear exista.  
    **checklunes** - Chequea que sea lunes.  
    **checkdia** - Chequea que sea primero de mes.  
    **crudo_rename** - Renombra archivos .pickle a fechas correctas.  
    **reporte_rename** - Renombra archivos .xlsx a fechas correctas. / **NO IMPLEMENTADO-VACIO**  
    **orquestador_tlk** -  Orquesta la llamada a las funciones encargadas  
    de todo el proceso de parseo de curdos y pusheos a la BD para los crudos TLK.  
    **orquestador_zbx** - Orquesta la llamada a las funciones encargadas
    de todo el proceso de generacion de reportes de PON y ONT. Parseo de curdos, pusheos, etc.  
    **menu** - Llama a funciones especificas a partir del input del usuario.
"""

def checkFileExistance(filePath):
    """***Chequea la existencia de un archivo***

    Recibe un directorio como string. Si encuentra el archivo devuelve
    True, de lo contrario devuelve False.

    **param filePath:** Directorio en formato str a chequear.  
    **type filePath:** str

    **returns:** True o Flase dependiendo si encontro el archivo o no.  
    **rtpye:** bool
    """

    try:
        with open(filePath, 'r') as f:
            logger.info("Se encontro {}".format(filePath))
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False

def checklunes(tarea_semanal):
    """***Chequea si es Lunes a partir de int***

    Por la necesidad de apadatar el orquestador autoamtico al manual
    esta funcion hace de puente en el chequeo del dia Lunes. Tecnicamente se
    obliga a la aplicacion funion a pasar un 1 si recibe un 1.

    **param tarea_semanal:** Confirma que sea lunes.  
    **type tarea_semanal:** int

    **returns:** 1 o 0 dependiendo si se le pasa un 1.  
    **rtpye:** int
    """

    if tarea_semanal == 1:
        return 1
    else:
        return 0

def checkdia(tarea_mensual):
    """***Chequea si es primero de mes a partir de int***

    Por la necesidad de apadatar el orquestador autoamtico al manual
    esta funcion hace de puente en el chequeo del primer dia del mes. 
    Tecnicamente se obliga a la aplicacion funion a pasar un 1 si recibe un 1.

    **param tarea_semanal:** Confirma que sea lunes.  
    **type tarea_semanal:** int

    **returns:** 1 o 0 dependiendo si se le pasa un 1.
    **rtpye:** int
    """

    if tarea_mensual == 1:
        return 1
    else:
        return 0
    
def crudo_rename(fecha):
    """***Renombra crudos .pickle***

    A partir de una fecha renombra los crudos generados por el orquestador manual.

    Debido a que reutiliza codigo del orquestador automatico, al quererse cargar crudos
    de fechas pasadas, genera pickles con la fecha al momento de llamar el **orquestador_manual**.
    Por ejemplo, esto genera que un crudo del 13/02/2021 genere un archivo .pickle con la fecha
    26/02/21 (hoy) en el nombre. No solo no es correcto el nombre, sino que superpone los archivos
    si se cargan varias fechas el mismo dia.

    **param fecha:** Fecha con la que renombrar archivos .pickle.  
    **type fecha:** str.

    **returns:** Esta funcion no tiene retornos.
    """
    os.rename("/var/lib/reportes-zabbix/crudos/Merged-Trends-{}.pickle".format(datetime.today().date()),"/var/lib/reportes-zabbix/crudos/Merged-Trends-{}.pickle".format(fecha))
    os.rename("/var/lib/reportes-zabbix/crudos/Merged-Trends-{}_ONT.pickle".format(datetime.today().date()),"/var/lib/reportes-zabbix/crudos/Merged-Trends-{}.pickle_ONT".format(fecha))

def reporte_rename(fecha):
    """***NO SE HA IMPLEMENTADO ESTA FUNCION Y ESTA VACIA***"""
    pass

def orquestador_tlk():
    """***Gestiona/llama todas las funciones para pushear crudos TLK a la BD***

    Se chequea la existencia de archivos crudos de TLK con fecha de hoy
    al momento de llamar la funcion . De encontrar el archivo:

    Logea que encontro el archivo.

    Se llama al funcion *f_parsear_inventario* pasando los nombres de archivos a generar.

    Luego se carga el parseo diario a la BD con la funcion *f_cargar_inv_en_BD()*.

    Por ultimo ejecuta las consultas en la BD que generan la informacion util para los
    reportes y se logea la finalizacion del proceso. De haber una expecion estas tambien
    son capturadas y logeadas.

    **returns:** Esta funcion no tiene retornos.
    """

    try:
        #**Existe archivo TLK**
        if checkFileExistance(archivo_tlk):
            #**Llamo a parser inventario tlk**
            logger.info(f'Arvhivo inventario TLK encontrado: {archivo_tlk}')
            logger.info("\n>>>>>>>>>>COMIENZO PROCESAMIENTO INVENTARIO TELELINK<<<<<<<<<<<<")
            f_parsear_inventario (archivo_tlk,archivo_tlk_dst,archivo_tlk_viejo)

            #**Cargo inventario tlk parseado a la BD**
            f_cargar_inv_en_BD(archivo_tlk_dst)

            #**Proceso BD inventario tlk**
            f_procesar_resumne_tlk_BD()
            logger.info(">>>>>>>>>>FIN PROCESAMIENTO INVENTARIO TELELINK<<<<<<<<<<<<\n\n")
        #**if fin existe archivo TLK**

        #**existe archivo RBS DSC**
        elif checkFileExistance(archivo_rbs_DCS):
            #**llamo a parser inventario RBS**
            logger.info(f'Arvhivo inventario RBS encontrado: {archivo_rbs_DCS}')
            logger.info("\n>>>>>>>>>>COMIENZO PROCESAMIENTO INVENTARIO RBS<<<<<<<<<<<<")
            f_parseo_inventario_RBS (archivo_rbs_DCS,archivo_rbs_DCS_dst,archivo_rbs_DCS_old)

            #**Cargo inventario RBS parseado a la BD**
            f_cargar_inv_RBS_en_BD(archivo_rbs_DCS_dst)

            #**Proceso BD inventario tl**
            logger.info(">>>>>>>>>>FIN PROCESAMIENTO INVENTARIO RBS<<<<<<<<<<<<\n\n")
        #**if fin existe archivo TLK**
    except Exception as e:
        logger.error(traceback.format_exc())

def orquestador_zbx():
    """***Gestiona/llama todas las funciones para pushear crudos Zabbix a la BD***
    
    Se chequea la existencia de archivos crudos de Zabbix (Merged-Tends) con 
    la fecha pasada ante el input fecha. De encontrar el archivo:

    Se llaman a las funciones de *parseo()* tanto para ONT como PON con las direcciones
    de crudozabbix generadas en la variable crudozabbix. Una ves que finalizan se borra
    el archivo crudo (NDJSON), y se logea esto ultimo.

    Se pushean los crudos diarios de PON y ONT a la BD.

    Se llaman a los flujos de la BD que debene realizarse todos los dias.

    Se renombra los archivos .pickle generados por el parseo

    Si se paso un 1 en *tarea_semanal*, se ejecutan flujos de BD correspondientes
    a la semana y se crean los reportes .xlsx de ONT y PON.

    Si se paso un 1 en *tarea_mensual*, se ejecutan flujos de BD correspondientes
    al mes y se crean los reportes .xlsx de ONT y PON.
    
    Por ultimo se captura cualquier exepcion en el proceso y se logea.

    **param fecha:** Fecha del archivo crudo a pushear en fomrato YYYY-MM-DD.  
    **type fecha:** input(str)

    **param tarea_semanal:** Selecciona si se desea generar tareas y reportes semanales.  
    **type tarea_semanal:** input(int)

    **param tarea_mensual:** Selecciona si se desea generar tareas y reportes mensuales.  
    **type tarea_mensual:** input(int)

    **returns:** Esta funcion no tiene retornos.
    """

    fecha = input("Ingrese la fecha a puseshar\n Formato: YYYY-MM-DD\n")
    crudozabbix = "/var/lib/reportes-zabbix/Merged-Trends-{}.ndjson".format(fecha)
    tarea_semanal = int(input("Precione 1 para generar reporte semanal\n"))
    tarea_mensual = int(input("Precione 1 para generar reporte mensual\n"))
    try:
        if checkFileExistance(crudozabbix):
            parseo_ont(crudozabbix)
            parseo_pon(crudozabbix)
            os.remove(crudozabbix)
            logger.info("Se borro archivo crudozabbix")
            pusheo_crudos_diarios_PON()
            pusheo_crudos_diarios_ONT()
            flujos("dia")
            crudo_rename(fecha)
        if checklunes(tarea_semanal) == 1:
            flujos("semana")
            reportes_xlsx("PON","semana")
            reportes_xlsx("ONT","semana")
            reporte_rename(fecha)
        if checkdia(tarea_mensual) == 1:
            flujos("mes")
            reportes_xlsx("PON","mes")
            reportes_xlsx("ONT","mes")
            reporte_rename(fecha)
    except Exception as e:
        logger.error(traceback.format_exc())

def menu():
    """***Menu del orquestador manual***

    Llama a las funciones importantes de orquestadores dependiendo del input
    de menu.

    1 ejcuta carga de crudos de TLK. 2 ejecuta la carga de crudos de zabbix
    y puede generar reportes. 3 Hace ambas funciones.

    **param menu:** Opcion para definir que crudo pushear y/o generar reportes.  
    **tpye menu:** input(int)

    **returns:** Esta funcion no tiene retornos.
    """
    menu = int(input("1 para carga TLK \n 2 Para carga zbx \n 3 para ambos \n"))
    if menu == 1:
        orquestador_tlk()
    elif menu == 2:
        orquestador_zbx()
    elif menu == 3:
        orquestador_tlk()
        orquestador_zbx()


#Llamo a menu quien llamara a las otras funciones dependiendo del input del user.
menu()