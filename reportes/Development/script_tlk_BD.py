import os
import time
import logging
from datetime import datetime


from parsear_inventario import f_parsear_inventario  #importarción de la funcion para paresar
from cargar_inv_en_BD import f_cargar_inv_en_BD       #importación de la función para guardar en BD  




def checkFileExistance(filePath):
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False


def procesar_tlk (nombre_archivo):
    while True:
        # si existe el archivo lo proceso #
        if checkFileExistance(nombre_archivo):
            logging.info("==============================================================================================")
            logging.info(f"|                             SE INICIALIZO PROCESO                                          |")
            logging.info("==============================================================================================\n\n")
            logging.info( f' Se Encontró un nuevo archivo : {nombre_archivo}')
            #paresear archivo archivo proc_reporte_gpon.py
            f_parsear_inventario(nombre_archivo)
            #Cargar BD carga_y_proceso_datos_tlk.py
            f_cargar_inv_en_BD("/var/lib/reportes-zabbix/reporte_tlk/PLN245_procesado.TXT")
            logging.info("==============================================================================================")
            logging.info(f"|                             SE FINALZÓ PROCESO                                                 |")
            logging.info("==============================================================================================\n\n")
        time.sleep(30)




#==============LOGS=======================#
# Definición del logger root
# -----------------------------------------------------------------------------
logging.basicConfig(
    format = '%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s',
    level  = logging.INFO,
    filemode = "a"
    )

# Nuevos handlers
# -----------------------------------------------------------------------------
# Si el root logger ya tiene handlers, se eliminan antes de añadir los nuevos.
# Esto es importante para que los logs no empiezen a duplicarse.
if logging.getLogger('').hasHandlers():
    logging.getLogger('').handlers.clear()

# Se añaden dos nuevos handlers al root logger, uno para los niveles de debug o
# superiores y otro para que se muestre por pantalla los niveles de info o
# superiores.
file_debug_handler = logging.FileHandler('logs_debug.log')
file_debug_handler.setLevel(logging.DEBUG)
file_debug_format = logging.Formatter('%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s')
file_debug_handler.setFormatter(file_debug_format)
logging.getLogger('').addHandler(file_debug_handler)

consola_handler = logging.StreamHandler()
consola_handler.setLevel(logging.INFO)
consola_handler_format = logging.Formatter('%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s')
consola_handler.setFormatter(consola_handler_format)
logging.getLogger('').addHandler(consola_handler)

# ======================= MAIN SCRIPT ============================================
logging.debug('Inicio main script')
logging.info('Inicio main script')

#=============CODIGO PROGRAMA======================
#-------------------PRODUCCIÓN--------------#
#archivo = "/var/lib/reportes-zabbix/reporte_tlk/PLN245_procesado.TXT"
#--------------------Test--------------------#
archivo = "C:/Users/e066446/Documents/GitHub/proyecto_zabbix/PLN245_procesado.TXT"

procesar_tlk(archivo)

#===============FIN ======================

logging.debug('Fin main script')
logging.info('Fin main script')

logging.shutdown()