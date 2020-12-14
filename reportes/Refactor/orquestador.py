#!/usr/bin/python

import logger
import time
import pusheo
import os

from direcciones import archivo_tlk, archivo_tlk_dst, archivo_tlk_viejo, archivo_rbs_DCS, archivo_rbs_DCS_dst, archivo_rbs_DCS_old, crudozabbix
from datetime import datetime
from pusheo import f_cargar_inv_en_BD, pusheo_crudos_diarios_PON, pusheo_crudos_diarios_ONT
from parseo import parseo_ont, parseo_pon
from flujo_db import flujos
from reporte import reportes_xlsx

def checkFileExistance(filePath):
    try:
        with open(filePath, 'r') as f:
            logger.info("Se encontro {}".format(filePath))
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False


def checklunes():
    if datetime.today().weekday() == 0:
        return 1
    else:
        return 0


def checkdia():
    if datetime.now().strftime("%d") == "1":
        return 1
    else:
        return 0
    

def orquestador ():
    while True:
        # existe archivo TLK #
        if checkFileExistance(archivo_tlk):
            #-----llamo a parser inventario tlk----#
            logger.info(f'Arvhivo inventario TLK encontrado: {archivo_tlk}')
            logger.info("\n>>>>>>>>>>COMIENZO PROCESAMIENTO INVENTARIO TELELINK<<<<<<<<<<<<")
            f_parsear_inventario (archivo_tlk,archivo_tlk_dst,archivo_tlk_viejo)

            #----Cargo inventario tlk parseado a la BD---#
            f_cargar_inv_en_BD(archivo_tlk_dst)

            #--- Proceso BD inventario tlk-----#
            f_procesar_resumne_tlk_BD()
            logger.info(">>>>>>>>>>FIN PROCESAMIENTO INVENTARIO TELELINK<<<<<<<<<<<<\n\n")
        #if fin existe archivo TLK #

        # existe archivo RBS DSC #
        elif checkFileExistance(archivo_rbs_DCS):
            #-----llamo a parser inventario RBS----#
            logger.info(f'Arvhivo inventario RBS encontrado: {archivo_rbs_DCS}')
            logger.info("\n>>>>>>>>>>COMIENZO PROCESAMIENTO INVENTARIO RBS<<<<<<<<<<<<")
            f_parseo_inventario_RBS (archivo_rbs_DCS,path_files+archivo_rbs_DCS_dst,archivo_rbs_DCS_old)

            #----Cargo inventario RBS parseado a la BD---#
            #f_cargar_inv_en_BD(path_files+file_rbs_DCSk_dst)

            #--- Proceso BD inventario tlk-----#
            logger.info(">>>>>>>>>>FIN PROCESAMIENTO INVENTARIO RBS<<<<<<<<<<<<\n\n")
        #if fin existe archivo TLK #        
        # existe archivo Zabbix #
        elif checkFileExistance(crudozabbix()):
            #Parseo archivo de Zabbix PON y ONT
            parseo_ont()
            parseo_pon()
            #Borro crudozabbix
            os.remove(crudozabbix())
            logger.info("Se borro archivo crudozabbix")
            #usheo pickles de ONT y PON
            pusheo_crudos_diarios_PON()
            pusheo_crudos_diarios_ONT()
            #Ejecuto funciones sql diarias")
            flujos("dia")
            if checklunes() == 1:
                #Ejecuto funcione sql semanal")
                flujos("semana")
                #Saco reporte semanal")
                reportes_xlsx("PON","semana")
                reportes_xlsx("ONT","semana")
            if checkdia() == 1:
                #Ejecuto funcione sql mensual")
                flujos("mes")
                #Saco reporte mensual")
                reportes_xlsx("PON","mes")
                reportes_xlsx("ONT","mes")
        else:
            time.sleep(30)

#-----main----#

'''Tengo que borrar los pickles muy viejos de respaldo '''