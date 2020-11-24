from direcciones import path_files, file_tlk, crudozabbix
import logger
from datetime import datetime
import time

#from pusheo import f_cargar_inv_en_BD


def checkFileExistance(filePath):
    try:
        with open(filePath, 'r') as f:
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
        if checkFileExistance(path_files+file_tlk):
            #-----llamo a parser inventario tlk----#
            logger.info(f'Arvhivo inventario TLK encontrado: {path_files+file_tlk}')
            logger.info("\n>>>>>>>>>>COMIENZO PROCESAMIENTO INVENTARIO TELELINK<<<<<<<<<<<<")
            f_parsear_inventario (path_files+file_tlk,path_files+file_tlk_dst,path_files+file_tlk_old)

            #----Cargo inventario tlk parseado a la BD---#
            f_cargar_inv_en_BD(path_files+file_tlk_dst)

            #--- Proceso BD inventario tlk-----#
            f_procesar_resumne_tlk_BD()
            logger.info(">>>>>>>>>>FIN PROCESAMIENTO INVENTARIO TELELINK<<<<<<<<<<<<\n\n")
        #if fin existe archivo TLK #

        # existe archivo Zabbix #
        elif checkFileExistance(crudozabbix):
            print("Se parseo archivo de TLK")
            print("Se pushea archivo TLK")
            print("Se ejecutan funciones sql diarias")
            if checklunes() == 1:
                print("Se ejecutan funcione sql semanal")
                print("Se saca el reporte")
            if checkdia() == 1:
                print("Se ejecutan funcione sql mensuales")
                print("Se saca el reporte mensual")

        time.sleep(5)

orquestador()