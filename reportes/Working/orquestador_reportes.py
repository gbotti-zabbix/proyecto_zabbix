#!/usr/bin/python

import logger
import time
import pusheo
import os
import traceback

from daemonize import Daemonize
from direcciones import archivo_tlk, archivo_tlk_dst, archivo_tlk_viejo, archivo_rbs_DCS, archivo_rbs_DCS_dst, archivo_rbs_DCS_old, crudozabbix, limpiar_pickle_pon, limpiar_pickle_ont, pid
from datetime import datetime
from pusheo import f_cargar_inv_en_BD,f_cargar_inv_RBS_en_BD, pusheo_crudos_diarios_PON, pusheo_crudos_diarios_ONT, f_procesar_resumne_tlk_BD
from parseo import parseo_ont, parseo_pon, f_parsear_inventario, f_parseo_inventario_RBS
from flujo_db import flujos
from reporte import reportes_xlsx
"""***Parseo, pusheo, flujos en la BD y generacion de reportes PON/ONT.***

Este script se encarga de llamar a todas las funciones que son pertinentes a la creacion
de los reportes a partir de info de Zabbix, Telelink y Gestion.

Las funciones llamadas detectan crudos a parsear, los pushean a la BD y generan los flujos
de consultas necesarioas para crear datos utiles para los reportes. Por ultimo crean los
archivos finales de reportes consultando la BD.

Se utilizan funciones que controlan dias, fechas y horas para decidir que procedimientos ejecutar.

El orquestador solo tiene la funcion de coordinar los distintos eslabones de los reportes.
Las funcionalidades finas deben editarse en las funciones importadas y llamadas desde
*orquestador_reportes()*.

Una ves ejecutado el script, se genera un daemon de linux con su correspondiente PID y Socket,
por lo que no captura la terminal desde la que se ejecuta. Para detener el script se debe matar
el proceso con su correspondiente PID.

Contiene las funciones:  
    **checkFileExistance** - Chequea que el archivo crudo a parsear exista.  
    **checkhora** - Chequea si al momento de ejecutarlo es la hora pasada como str.
    **checklunes** - Chequea que sea lunes.  
    **checkdia** - Chequea que sea primero de mes.  
    **orquestador_reportes** -  Orquesta la llamada a las funciones encargadas
    de todo el proceso de generacion de reportes. Parseo de curdos, pusheos, etc.  
    **deamon** - Genera un daemon desde el codigo python de orquestador.  
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

def checkhora(hora):
    """***Comprueba si es x hora***

    Comprueba si al momento de llamar la funcion la hora actual
    es igual a la pasada en hora. Devuelve 1 de ser iguales las horas,
    de lo contrario retorna 0.  
    
    **param hora:** Hora en formato str a chequear.  
    **type hora:** str

    **returns:** 1 o 0 dependiendo si es es la hora filtrada o no.  
    **rtpye:** int
    """
    hora_now = datetime.now().time().strftime("%H")
    if hora_now == hora:
        return 0
    else:
        return 1


def checklunes():
    """***Chequea si es Lunes***

    Comprueba si al momento de llamar la funcion es Lunes.
    De serlo devuelve 1, de lo contrario 0

    **returns:** 1 o 0 dependiendo si es lunes o no.  
    **rtpye:** int
    """

    if datetime.today().weekday() == 0:
        return 1
    else:
        return 0


def checkdia():
    """***Chequea si es primero de mes***

    Comprueba si al momento de llamar la funcion es primero de mes.
    De serlo devuelve 1, de lo contrario 0.

    **returns:** 1 o 0 dependiendo si es lunes o no.  
    **rtpye:** int
    """
    if datetime.now().strftime("%d") == "01":
        return 1
    else:
        return 0
    

def orquestador_reportes():
    """***Gestiona/llama todas las funciones relevante a los reportes***

    Comienza con un ciclo while de 30 min de sleep entre ciclo. En cada ciclo se chequea
    la existencia de archivos crudos de TLK, gestion o Zabbix. De encontrar alguno, comienza
    las tareas de ingreso de crudos diarios, flujos de datos en al BD y/o generacion de reportes.

    * **Se verifica que no sean las 00 o 03 hs**
        De no ser las 00 o 03 hs se continua. Esto se utiliza para asegurarnos que se copien los crudos
        provenientes de ritaf y/o Zabbix antes de intentar parcearlos.

    * **Si encuentra archivo TLK (*archivo_tlk*):**  
        Logea que encontro el archivo.

        Se llama al funcion *f_parsear_inventario()* pasando los nombres de archivos a generar.

        Luego se carga el parseo diario a la BD con la funcion *f_cargar_inv_en_BD()*.

        Por ultimo ejecuta las consultas en la BD que generan la informacion util para los
        reportes y se logea la finalizacion del proceso

    * **Si encuentra el archivo de Gestion(*archivo_rbs_DCS*):**  
        Logea que encontro el archivo.

        Se llama al funcion *f_parseo_inventario_RBS()()* pasando los nombres de archivos a generar.

        Luego se carga el parseo diario a la BD con la funcion *f_cargar_inv_RBS_en_BD()*.

        Se logea la finalizacion del proceso.

    * **Si encuentra el archivo de Zabbix(*crudozabbix()*):**  
        Se llaman a las funciones de parseo tanto para ONT como PON. Una ves que finalizan se borra
        el archivo crudo (NDJSON), y se logea esto ultimo.

        Se pushean los crudos diarios de PON y ONT a la BD.

        Se limpian archivos pickle con mas de 30 dias.

        Se llaman a los flujos de la BD que debene realizarse todos los dias.

        Si checklunes retorna 1, se ejecutan flujos de BD correspondientes a la semana y
        se crean los reportes .xlsx de ONT y PON.

        Si checkdia retorna 1, se ejecutan flujos de BD correspondientes a la semana y
        se crean los reportes .xlsx de ONT y PON.
    
    Por ultimo se captura cualquier exepcion en el proceso y se logea.
    
    **returns:** Esta funcion no tiene retornos.
    """

    try:
        while True:
            if checkhora("03") == 0:
                if checkFileExistance(archivo_tlk):
                    logger.info(f'Arvhivo inventario TLK encontrado: {archivo_tlk}')
                    logger.info("\n>>>>>>>>>>COMIENZO PROCESAMIENTO INVENTARIO TELELINK<<<<<<<<<<<<")
                    f_parsear_inventario (archivo_tlk,archivo_tlk_dst,archivo_tlk_viejo)

                    f_cargar_inv_en_BD(archivo_tlk_dst)

                    f_procesar_resumne_tlk_BD()
                    logger.info(">>>>>>>>>>FIN PROCESAMIENTO INVENTARIO TELELINK<<<<<<<<<<<<\n\n")

                elif checkFileExistance(archivo_rbs_DCS):
                    logger.info(f'Arvhivo inventario RBS encontrado: {archivo_rbs_DCS}')
                    logger.info("\n>>>>>>>>>>COMIENZO PROCESAMIENTO INVENTARIO RBS<<<<<<<<<<<<")
                    f_parseo_inventario_RBS (archivo_rbs_DCS,archivo_rbs_DCS_dst,archivo_rbs_DCS_old)

                    f_cargar_inv_RBS_en_BD(archivo_rbs_DCS_dst)

                    logger.info(">>>>>>>>>>FIN PROCESAMIENTO INVENTARIO RBS<<<<<<<<<<<<\n\n")

            elif checkhora("00") == 0:
                if checkFileExistance(crudozabbix()):
                    parseo_ont("auto")
                    parseo_pon("auto")
                    os.remove(crudozabbix())
                    logger.info("Se borro archivo crudozabbix")
                    pusheo_crudos_diarios_PON()
                    pusheo_crudos_diarios_ONT()
                    os.system(limpiar_pickle_pon)
                    os.system(limpiar_pickle_ont)
                    flujos("dia")
                    if checklunes() == 1:
                        flujos("semana")
                        reportes_xlsx("PON","semana")
                        reportes_xlsx("ONT","semana")
                    if checkdia() == 1:
                        flujos("mes")
                        reportes_xlsx("PON","mes")
                        reportes_xlsx("ONT","mes")
            else:
                time.sleep(1200)
    except Exception as e:
        logger.error(traceback.format_exc())
        orquestador_reportes()

#**Se crea y ejecuta demonio para la funcion *orquestador_reportes*.**
daemon = Daemonize(app="orquestador_reportes", pid=pid, action=orquestador_reportes)
daemon.start()
