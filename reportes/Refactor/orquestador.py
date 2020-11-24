from direcciones import path_files, file_tlk, crudozabbix
import logger
from pusheo import f_cargar_inv_en_BD


def checkFileExistance(filePath):
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False

def checkdate():
    if datetime.today().weekday() == 0:
        return "Lunes"
    elif datetime.now().strftime("%d") == 1:
        return "Primero"
    else:
        return 0
    


def orquestador ():
    while True:
        # existe archivo TLK #
        if checkFileExistance(path_files+file_tlk):
            #-----llamo a parser inventario tlk----#
            logger.info(f'Arvhivo inventario TLK encontrado: {filePath}')
            f_parsear_inventario (path_files+file_tlk,path_files+file_tlk_dst,path_files+file_tlk_old)

            #----Cargo inventario tlk parseado a la BD---#
            f_cargar_inv_en_BD(path_files+file_tlk_dst)

            #--- Proceso BD inventario tlk-----#
            

        # existe archivo Zabbix #
        elif checkFileExistance(crudozabbix):
            print("Se parseo archivo de TLK")
            print("Se pushea archivo TLK")
            print("Se ejecutan funciones sql diarias")
            if checkdate() == "Lunes":
                print("Se ejecutan funcione sql semanal")
                print("Se saca el reporte")
            elif checkdate() == "Primero":
                print("Se ejecutan funcione sql mensuales")
                print("Se saca el reporte mensual")

        time.sleep(30)
