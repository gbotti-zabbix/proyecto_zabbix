import os
import csv
import logging

from datetime import datetime
from conector import conector

# Se eliminan los handlers anteriores
if logging.getLogger('').hasHandlers():
    logging.getLogger('').handlers.clear()

#>>>>funcion chequeo existencia archvio<<<<<<<<<<<#
def FileCheck(fn):
    """
    Funcion que perminte chquear la existencia de un arhvio, devuelve 1 si existe, loqueo error si no existe.
    """
    try:
        open(fn, "r")
        return 1
    except IOError:
        logging.error (f"Error 23: Archivo no Existe. {fn}")
        return 0
#fin FileCheck(fn)



#>>>>>>funcion parsear inventario telelink<<<<<<<<<<<<<<<#
def f_parsear_inventario (archivo_origen,archivo_destino,archivo_old):
    """ Funcion para parsear el inventario de Telelink, recibe 3 nombres arhivos
        archivo_origen: recibe el path y nombre del archivo a parsear
        archivo_destino: es el nombre del arhivo con que se graban los datos paresados
        arhivo_old: luego de parsear el arhivo lo dejo con otro nombre.
    """

    #-- Cargo diccionarios para trabajar con nombres ----
    # debo cargar diccionario de TLK-NOMBRE GESTION
    
    sql
    conector()

    # debo cargar equivelente - (TIPO NODO)<-->


 
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
                    tipo_equipo = f_diccionario_equ_tlk(linea_parseada[1])           # cambio el 70 por c300    
                    nro_nodo = linea_parseada[1][2:4]                           #estraigo del numero equipo el nuermo de nodo
                    nombre_gestion= f_nombre_gestion(cod_telelink,int(nro_nodo),tipo_equipo)
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
                #if contador == 5:
                #   break
    #------------------------------------------------------
    logging.info(f'función f_parsear_inventario ejecutada {archivo_destino} con {contador} lineas')
    if FileCheck(archivo_old):
        os.remove(archivo_old)


    os.rename(archivo_origen, archivo_old)
    logging.info( f'Se terminó el parseo del arhivo: {archivo_origen}')
    logging.info(f'Se renombro el arhivo {archivo_origen} en el arhivo {archivo_old}')

#---fin f_parsear_inventario---# 