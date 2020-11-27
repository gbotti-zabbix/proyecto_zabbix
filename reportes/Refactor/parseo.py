import os
import csv
import logger

from datetime import datetime
from conector import conector



#>>>>funcion chequeo existencia archvio<<<<<<<<<<<#
def FileCheck(fn):
    """
    Funcion que perminte chquear la existencia de un archivo, devuelve 1 si existe, loqueo error si no existe.
    """
    try:
        open(fn, "r")
        return 1
    except IOError:
        logger.error (f"Error 23: Archivo no Existe: {fn}")
        return 0
#fin FileCheck(fn)



#>>>>>>funcion parsear inventario telelink<<<<<<<<<<<<<<<#
def f_parsear_inventario (archivo_origen,archivo_destino,archivo_old):
    """ Funcion para parsear el inventario de Telelink, recibe 3 nombres arhivos
        archivo_origen: recibe el path y nombre del archivo a parsear
        archivo_destino: es el nombre del arhivo con que se graban los datos paresados
        arhivo_old: luego de parsear el arhivo lo dejo con otro nombre.
    """
    logger.info ("\n--Se comenzo parseo arhivo--")
    #-- Cargo diccionarios para trabajar con nombres ----
    # debo cargar diccionario de TLK-NOMBRE GESTION
    sql = "SELECT cod_tlk,nom_gestion FROM t_tlk_nombregestion;"
    comentario="Traer nombre gestion"
    dic_gestion={}
    resultado= conector(sql,"select",comentario)
    for x in resultado:
        dic_gestion[x[0]]=[x[1]] 


    

    # debo cargar equivelente - (TIPO NODO)<-->
    sql = "SELECT nro_tlk,modelo,letra_gestion from t_diccionario_nodos_tlk;"
    comentario="Traer tipos nodos"
    dic_nodo={}
    resultado= conector(sql,"select",comentario)
    for x in resultado:
        dic_nodo[x[0]]=[x[1],x[2]] 

 
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
                    tipo_equipo = dic_nodo[linea_parseada[1][0:2]][0]
                    nro_nodo = linea_parseada[1][2:4]                           #estraigo del numero equipo el nuermo de nodo
                    nombre_gestion= dic_gestion[cod_telelink][0]+"-"+nro_nodo
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
                #if contador == 30:
                #   break
    #------------------------------------------------------
    logger.info(f'función f_parsear_inventario ejecutada {archivo_destino} con {contador} lineas')
    if FileCheck(archivo_old):
        os.remove(archivo_old)


    os.rename(archivo_origen, archivo_old)
    logger.info( f'Se terminó el parseo del arhivo: {archivo_origen}')
    logger.info(f'Se renombro el arhivo {archivo_origen} en el arhivo {archivo_old} \n')

#---fin f_parsear_inventario---# 



def f_parseo_inventario_RBS(archivo_origen,archivo_destino,archivo_old):
    """Función que recibe el archivo de Radbio Bases y luego lo parsea,
       Recibe el nombre arhivo origen a paresar, el nombre archivo destino
        parseado y como renombrar el archivo original
    """

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
                    #----creación campos para la BD---------
                    servicio = linea_parseada[0]
                    nro_equipo= linea_parseada[4]
                    slot = linea_parseada[4][5:7]                               #estraigo del numero equipo el nuermo de slot 
                    puerto = linea_parseada[4][7:9]                             #estraigo del numero equipo el nuermo de puerto    
                    ont =   linea_parseada[4][9:12]                             #estraigo del numero equipo el nuermo de ontslot =
                    estado_ont= linea_parseada[5]
                    fecha_inicio_estado = linea_parseada[6]
                    dias_desde_ultimo_estado = linea_parseada[7]
                    etiqueta = linea_parseada[9]
                    nodo = linea_parseada[11]
                    nodo_slot_puerto_ont = linea_parseada[11]+"-"+slot+"/"+puerto+"/"+ont
                    linea_nueva=[nodo_slot_puerto_ont,servicio,nro_equipo,estado_ont, fecha_inicio_estado,dias_desde_ultimo_estado,etiqueta,nodo, slot, puerto, ont ]
                    #print (linea_nueva)
                    wr.writerow(linea_nueva)
                contador_salto = contador_salto + 1 #solo elimina la primera linea
    #----------------------------------------------------
                contador = contador+1
    #descomentar para procesar 30 lineas
                #if contador == 2:
                #   break
    if FileCheck(archivo_old):
        os.remove(archivo_old)
    os.rename(archivo_origen, archivo_old)
    logger.info( f'Se terminó el parseo del arhivo: {archivo_origen}')
    logger.info(f'Se renombro el arhivo {archivo_origen} en el arhivo {archivo_old} \n')


