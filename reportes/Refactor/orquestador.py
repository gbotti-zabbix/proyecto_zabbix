from direcciones import path_files, file_tlk, crudozabbix
import time
from datetime import datetime

def checkFileExistance(filePath):
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False

def checkdate():
    if datetime.today().weekday() == 1:
        return "Lunes"
    elif datetime.now().strftime("%d") == 1:
        return "Primero"
    else:
        return 0
    


def orquestador ():
    while True:
        # existe archivo TLK #
        if checkFileExistance(path_files+file_tlk):
            print("Se parseo archivo de TLK")
            print("Se pushea archivo TLK")
            print("Se ejecutan funciones sql")
            # logging.info("==============================================================================================")
            # logging.info(f"|                             SE INICIALIZO PROCESO                                          |")
            # logging.info("==============================================================================================\n\n")
            # logging.info( f' Se Encontró un nuevo archivo : {archivo1}')
            # #paresear archivo archivo proc_reporte_gpon.py
            # f_parsear_inventario(archivo1,archivo2,archivo1_old)
            # #Cargar BD carga_y_proceso_datos_tlk.py
            # f_cargar_inv_en_BD(archivo2)
            # logging.info("==============================================================================================")
            # logging.info(f"|                             SE FINALZÓ PROCESO                                              |")
            # logging.info("==============================================================================================\n\n")

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

        time.sleep(5)

orquestador()
