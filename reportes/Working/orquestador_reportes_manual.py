#!/usr/bin/python

import logger
import time
import pusheo
import os
import traceback
#
import pickle
#
from direcciones import archivo_tlk, archivo_tlk_dst, archivo_tlk_viejo, archivo_rbs_DCS, archivo_rbs_DCS_dst, archivo_rbs_DCS_old, limpiar_pickle_pon, limpiar_pickle_ont, pid
#date esta de mas
from datetime import date, datetime
from pusheo import f_cargar_inv_en_BD,f_cargar_inv_RBS_en_BD, pusheo_crudos_diarios_PON, pusheo_crudos_diarios_ONT, f_procesar_resumne_tlk_BD
from parseo import parseo_ont, parseo_pon, f_parsear_inventario, f_parseo_inventario_RBS
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


def checklunes(tarea_semanal):
    if tarea_semanal == 1:
        return 1
    else:
        return 0


def checkdia(tarea_mensual):
    if tarea_mensual == 1:
        return 1
    else:
        return 0
    
def crudo_rename(fecha):
    os.rename(r,"/var/lib/reportes-zabbix/crudos/Merged-Trends-{}.pickle".format(datetime.today().date()),r,"/var/lib/reportes-zabbix/crudos/Merged-Trends-{}.pickle".format(fecha))
    os.rename(r,"/var/lib/reportes-zabbix/crudos/Merged-Trends-{}_ONT.pickle".format(datetime.today().date()),r,"/var/lib/reportes-zabbix/crudos/Merged-Trends-{}.pickle_ONT".format(fecha))

def reporte_rename(fecha):
    pass

def orquestador_tlk():
    try:
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
            f_parseo_inventario_RBS (archivo_rbs_DCS,archivo_rbs_DCS_dst,archivo_rbs_DCS_old)

            #----Cargo inventario RBS parseado a la BD---#
            f_cargar_inv_RBS_en_BD(archivo_rbs_DCS_dst)

            #--- Proceso BD inventario tlk-----#
            logger.info(">>>>>>>>>>FIN PROCESAMIENTO INVENTARIO RBS<<<<<<<<<<<<\n\n")
        #if fin existe archivo TLK # 
    except Exception as e:
        logger.error(traceback.format_exc())

def orquestador_zbx():
    fecham = input("Ingrese la fecha a puseshar\n Formato: YYYY-MM-DD\n")
    crudozabbix = "/var/lib/reportes-zabbix/Merged-Trends-{}.ndjson".format(fecham)
    tarea_semanal = int(input("Precione 1 para generar reporte semanal\n"))
    tarea_mensual = int(input("Precione 1 para generar reporte mensual\n"))
    try:
        if checkFileExistance(crudozabbix):
            #Parseo archivo de Zabbix PON y ONT
            parseo_ont()
            parseo_pon()
            #Borro crudozabbix
            os.remove(crudozabbix)
            logger.info("Se borro archivo crudozabbix")
            #pusheo pickles de ONT y PON
            pusheo_crudos_diarios_PON()
            pusheo_crudos_diarios_ONT()
            crudo_rename(fecham)
            #borra crudos pickle viejos ONT y PON
            os.system(limpiar_pickle_pon)
            os.system(limpiar_pickle_ont)
            #Ejecuto funciones sql diarias")
            flujos("dia")
        if checklunes(tarea_semanal) == 1:
            #Ejecuto funcione sql semanal")
            flujos("semana")
            #Saco reporte semanal")
            reportes_xlsx("PON","semana")
            reportes_xlsx("ONT","semana")
            reporte_rename(fecham)
        if checkdia(tarea_mensual) == 1:
            #Ejecuto funcione sql mensual")
            flujos("mes")
            #Saco reporte mensual")
            reportes_xlsx("PON","mes")
            reportes_xlsx("ONT","mes")
            reporte_rename(fecham)
    except Exception as e:
        logger.error(traceback.format_exc())

def menu():
    menu = int(input("1 para carga TLK \n 2 Para carga zbx \n 3 para ambos \n"))
    if menu == 1:
        orquestador_tlk()
    elif menu == 2:
        orquestador_zbx()
    elif menu == 3:
        orquestador_tlk()
        orquestador_zbx()


#flujos("dia")
#menu()



with open("/var/lib/reportes-zabbix/crudos/Merged-Trends-" + str(date.today()) + ".pickle","r") as archivo:
    lista_tuplas = pickle.load(archivo)
    for lista in lista_tuplas:
        print(lista)