#!/usr/bin/python

from openpyxl import Workbook
from openpyxl.styles import NamedStyle, Font, Border, Alignment, Side
import mysql.connector
from datetime import datetime, date, timedelta
import sys
import logger
import os

from direcciones import excel_PON_semanal, excel_PON_mensual, excel_ONT_semanal, excel_ONT_mensual, hojas_PON, hojas_ONT, c300_19p, puertos_uplink, puertos_uplink_h, puertos_uplink_19, puertos_uplink_omitidos_z, puertos_uplink_omitidos_z_19
from consultas import sql_ont_semanal, sql_ont_mensual, sql_pon_semanal, sql_pon_mensual
from conector import conector
""" Hace un select en la BD y crea los reportes .xlsx

Se hace un pull desde la BD para generar los reportes semanales y mensuales de PON y ONTs.

Las funciones de crear generan y vinculan hojas y encabezados. Los apend_data cargan estos objetos
con los datos a escribir por hoja ademas de realizar algunos filtros.

Por ultimo reportes_xlsx hace las correspondientes llamadas a las funciones y escribe los datos
en los archivos finales de reportes.

Si se desea modificar encabezados o nombre de hojas, deben editarse las variables y funciones
importadas desde direcciones. De la misma manera, si la informacion a extraer de la BD cambiara
se deben editar las variables y funciones importadas desde consultas.

Contiene las funciones:
    * crear_hojas - Crea las hojas para determinado workbook
    * crear_encabezados - Crea encabezados correspondientes a cada hoja para determinado workbook
    * apend_data_PON - Filtra e inserta la informacion correspondiente por hoja para determinado workbook
    vinculado con el reporte PON.
    * apend_data_ONT - Filtra e inserta la informacion correspondiente por hoja para determinado workbook
    vinculado con el reporte ONT.
    * reportes_xlsx - Crea el workbook y llama a las funciones correspondientes del reporte a genera.
    Escribe el archivo con la info insertada con funciones append y crear.
"""
def crear_hojas(workbook,titulos):
    """ Crea las hojas por workbook
    
    Se pasa una lista de objetos. El bucle recorre la lista bucando las claves referentes a los titulos de las
    hojas. Con estas claves se crean las hojas dentro de la clase workbook.

    Como workbook crea por defecto la primer hoja con nombre sheet, se usa un contador binario par editar esta
    primer pagina.

    :param workbook: Objeto creado a partir de workbook()
    :type workbook: class

    :titulos: Lista de objetos con encabezados y nombres de hojas.
    :type titulos: list

    :returns: Esta funcion no tiene retornos.
    """
    contador = 0
    for titulo in titulos:
        if contador == 0:
            workbook["Sheet"].title = titulo.nombreHoja
            contador = contador + 1 
        else:
            workbook.create_sheet(titulo.nombreHoja) 


def crear_encabezados(workbook,hojas):
    """ Crea los encabezados cada hoja en el workbook
    
    Se pasa una lista de objetos. El bucle recorre la lista usando el nombre de hoja como key
    para vincular y crear los encabezados. Tecnicamente, cada objeto trae nombre de hoja y encabezados,
    la primera accede a una direccion en el objeto con la key nombre, luego le carga los encabezaddos
    que vienen junto con ese nombre en la lista.

    :param workbook: Objeto creado a partir de workbook()
    :type workbook: class

    :param hojas: Lista de objetos con encabezados y nombres de hojas.
    :type hojas: list

    :returns: Esta funcion no tiene retornos.
    """
    for hoja in hojas:
        for key in hoja.encabezados:
            workbook[hoja.nombreHoja][key] = hoja.encabezados[key]


def apend_data_PON(workbook,hojas,periodo):
    """ Consulta la BD y escribe los datos PON en el objeto workbook

    A partir del parametro periodo, decide que consulta hacer. "semana" hace un select
    sobre reporte_semanal y "mes" sobre reporte_mensual.

    El select trae todos los datos en listas de tuplas, se itera sobre esta separando
    direcciones en viarables. 

    Comapran tupla a tupla, la direccion del trafico y si el puerto esta entre los grupos desados
    de puertos y si estan fuera de los no deseados. Esto filtra puertos de respaldo en el uplink,
    y permite separar Subida y Bajada de Pon y Uplink. Ademas, los puertos de uplink no cuentan
    con informacion de TLK.

    Una ves realizados los filtros correspondientes, se hace "append" de la informacion de las tuplas en
    el workbook, apuntando a la hoja correcta.

    Tener en cuenta, para que la informacion escrita corresponda con los encabezados, deben pasarse
    en el mismo orden que que fueron creados en el workbook. Ejemplo, si los encabezados se definen por
    [hora,pico], los datos traidos de la BD deben ser escritos en esa hoja corresponiendo al orden
    hora/pico. El orden de la variable lista_append define esto.

    Variables desde listas:

    tipo, nodo, puerto, direccion, fecha, y hora son strings.

    prom_hora_pico, prom_picos_diarios, pico, promedio_hora son float.

    wf, emp, rbs son int.

    :param workbook: Objeto creado a partir de workbook()
    :type workbook: class

    :param hojas: Lista de objetos con encabezados y nombres de hojas.
    :type hojas: list

    :param periodo: Define que consulta se utilizara para la funcion.
    "semana" consulta datos de reporte semanal. "mes" consulta datos
    del reporte mensual.
    :type periodo: str

    :returns: Esta funcion no tiene retornos.
    """
    if periodo == "semana":
        resultado = conector(sql_pon_semanal,"select","Select del reporte semanal de PON")
    elif periodo == "mes":
        resultado = conector(sql_pon_mensual,"select","Select del reporte mensual de PON")
    for dato in resultado:
        tipo = dato[1]
        nodo = dato[2]
        puerto = dato[3]
        direccion = dato[4]
        hora = dato[5]
        fecha = dato[6]
        prom_hora_pico = dato[7]
        prom_picos_diarios = dato[8]
        pico = dato[9]
        promedio_hora = dato[10]
        wf = dato[11]
        datos = dato[12]
        emp = dato[13]
        rbs = dato[14]
        if (direccion == "RX" and puerto in puertos_uplink) or (direccion == "RX" and tipo == "MA5800" and puerto in puertos_uplink_h) or (direccion == "RX" and nodo in c300_19p and puerto in puertos_uplink_19):
            lista_append = [tipo,nodo,puerto,hora,fecha,pico,(pico*100)/10000,prom_hora_pico,prom_picos_diarios,promedio_hora]
            workbook["Bajada Uplink"].append(lista_append)
        elif (direccion == "TX" and puerto in puertos_uplink) or (direccion == "TX" and tipo == "MA5800" and puerto in puertos_uplink_h) or (direccion == "TX" and nodo in c300_19p and puerto in puertos_uplink_19):
            lista_append = [tipo,nodo,puerto,hora,fecha,pico,(pico*100)/10000,prom_hora_pico,prom_picos_diarios,promedio_hora]
            workbook["Subida Uplink"].append(lista_append)
        elif ((direccion == "TX") and (nodo in c300_19p) and (puerto not in puertos_uplink_omitidos_z_19)) or ((direccion == "TX") and (nodo not in c300_19p) and (puerto not in puertos_uplink_omitidos_z)):
            lista_append = [tipo,nodo,puerto,hora,fecha,pico,(pico*100)/2500,prom_hora_pico,prom_picos_diarios,promedio_hora,wf,datos,emp,rbs]
            workbook["Bajada PON"].append(lista_append)
        elif ((direccion == "RX") and (nodo in c300_19p) and (puerto not in puertos_uplink_omitidos_z_19)) or ((direccion == "RX") and (nodo not in c300_19p) and (puerto not in puertos_uplink_omitidos_z)):
            lista_append = [tipo,nodo,puerto,hora,fecha,pico,(pico*100)/1250,prom_hora_pico,prom_picos_diarios,promedio_hora,wf,datos,emp,rbs]
            workbook["Subida PON"].append(lista_append)


def apend_data_ONT(workbook,hojas,periodo):
        """ Consulta la BD y escribe los datos ONT en el objeto workbook

    A partir del parametro periodo, decide que consulta hacer. "semana" hace un select
    sobre reporte_semanal y "mes" sobre reporte_mensual.

    El select trae todos los datos en listas de tuplas, se itera sobre esta separando
    direcciones en viarables. 

    Comapran tupla a tupla, la direccion del trafico. Esto permite separar Subida y Bajada
    de las ONT.

    Una ves realizados los filtros correspondientes, se hace "append" de la informacion de las tuplas en
    el workbook, apuntando a la hoja correcta.

    Tener en cuenta, para que la informacion escrita corresponda con los encabezados, deben pasarse
    en el mismo orden que que fueron creados en el workbook. Ejemplo, si los encabezados se definen por
    [hora,pico], los datos traidos de la BD deben ser escritos en esa hoja corresponiendo al orden
    hora/pico. El orden de la variable lista_append define esto.

    Variables desde listas:

    tipo, nodo, puerto, etiqueta, direccion, fecha, y hora son strings.

    prom_hora_pico, prom_picos_diarios, pico, promedio_hora son float.

    :param workbook: Objeto creado a partir de workbook()
    :type workbook: class

    :param hojas: Lista de objetos con encabezados y nombres de hojas.
    :type hojas: list

    :param periodo: Define que consulta se utilizara para la funcion.
    "semana" consulta datos de reporte semanal. "mes" consulta datos
    del reporte mensual.
    :type periodo: str

    :returns: Esta funcion no tiene retornos.
    """
    if periodo == "semana":
        resultado = conector(sql_ont_semanal,"select","Select del reporte semanal de ONT")
    elif periodo == "mes":
        resultado = conector(sql_ont_mensual,"select","Select del reporte mensual de ONT")
    for dato in resultado:
        tipo = dato[1]
        nodo = dato[2]
        puerto = dato[3]
        etiqueta = dato[4]
        direccion = dato[5]
        hora = dato[6]
        fecha = dato[7]
        prom_hora_pico = dato[8]
        prom_picos_diarios = dato[9]
        pico = dato[10]
        promedio_hora = dato[11]
        if direccion == "RX":
            lista_append = [tipo,nodo,puerto,etiqueta,hora,fecha,pico,(pico*100)/10000,prom_hora_pico,prom_picos_diarios,promedio_hora]
            workbook["Subida ONT"].append(lista_append)
        elif direccion == "TX":
            lista_append = [tipo,nodo,puerto,etiqueta,hora,fecha,pico,(pico*100)/10000,prom_hora_pico,prom_picos_diarios,promedio_hora]
            workbook["Bajada ONT"].append(lista_append)


def reportes_xlsx(tipo,periodo):
    """ Llamas de funciones y escritura de archivos reportes

    Comienza creando una instancia de workbook(), este objeto es usado por
    el constructor de .xlsx openpyxl.

    El parametro tipo define si se ejecutaran funciones para crear el reporte
    de ONTs o PON (incluyendo uplink eh informacion de TLK). El flujo de esta fucnion
    es igual para ambos reportes.

    Luego de logear el inicio de la tarea, se llaman a las funciones crear
    las cuales definen los nombres y encabezados de paginas. Las funciones append
    consultan datos especificos a la BD y los insertan el workbook.

    Periodo definira si se debe hacer una consutla sobre reporte_mensual o 
    reporte_semanal en la BD. Ademas marca el archivo de reporte que se debe crear
    dependiendo si es un reporte de datos semanales o mensuales y la tecnologia que
    este reflejara (PON/Uplink o ONT).

    Una ves dentro del if de periodo, se escribe el archivo y luego se ponen permisos
    775 para poder ser importados desde el servidor de ritaf, el cual mueve los .xlsx hacia
    directorios en la red corporativa.
    
    Se logea la finalizacion del proceso.
    
    :param tipo: Define tareas a ejecutar. "ONT" genera reportes
    de ONT. "PON" genera reportes de puertos PON/Uplink.
    :type tipo: str

    :param periodo: Periodo de consultas a realizar. "mes" genera
    reportes mensuales. "semana" genera reportes semanales.
    :type periodo: str

    :returns: Esta funcion no tiene retornos.
    """
    workbook = Workbook()
    if tipo == "ONT":
            logger.info("Comenzo a crearse el reporte {} de ONT".format(periodo))
            crear_hojas(workbook,hojas_ONT)
            crear_encabezados(workbook,hojas_ONT)
            apend_data_ONT(workbook,hojas_ONT,periodo)
            if periodo == "mes":
                workbook.save(filename=excel_ONT_mensual())
                os.chmod(excel_ONT_mensual(),0o755)
            elif periodo == "semana":
                workbook.save(filename=excel_ONT_semanal())
                os.chmod(excel_ONT_semanal(),0o755)
            logger.info("Se culmino la creacion del reporte {} de ONT".format(periodo))

    elif tipo == "PON":
            logger.info("Comenzo a crearse el reporte {} de PON".format(periodo))
            crear_hojas(workbook,hojas_PON)
            crear_encabezados(workbook,hojas_PON)
            apend_data_PON(workbook,hojas_PON,periodo)
            if periodo == "mes":
                workbook.save(filename=excel_PON_mensual())
                os.chmod(excel_PON_mensual(),0o755)
            elif periodo == "semana":
                workbook.save(filename=excel_PON_semanal())
                os.chmod(excel_PON_semanal(),0o755)
            logger.info("Se culmino la creacion del reporte {} de PON".format(periodo))


