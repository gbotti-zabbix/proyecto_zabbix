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

def crear_hojas(workbook,titulos):
    contador = 0
    for titulo in titulos:
        if contador == 0:
            workbook["Sheet"].title = titulo.nombreHoja
            contador = contador + 1 
        else:
            workbook.create_sheet(titulo.nombreHoja) 


def crear_encabezados(workbook,hojas):
    for hoja in hojas:
        for key in hoja.encabezados:
            workbook[hoja.nombreHoja][key] = hoja.encabezados[key]


def apend_data_PON(workbook,hojas,periodo):
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
    workbook = Workbook()
    if tipo == "ONT":
            logger.info("Comenzo a crearse el reporte {} de ONT".format(periodo))
            crear_hojas(workbook,hojas_ONT)
            crear_encabezados(workbook,hojas_ONT)
            apend_data_ONT(workbook,hojas_ONT,periodo)
            if periodo == "mes":
                workbook.save(filename=excel_ONT_mensual())
                #os.system("chmod 775 {}".format(excel_ONT_mensual))
            elif periodo == "semana":
                workbook.save(filename=excel_ONT_semanal())
                #os.system("chmod 775 {}".format(excel_ONT_semanal))
            logger.info("Se culmino la creacion del reporte {} de ONT".format(periodo))

    elif tipo == "PON":
            logger.info("Comenzo a crearse el reporte {} de PON".format(periodo))
            crear_hojas(workbook,hojas_PON)
            crear_encabezados(workbook,hojas_PON)
            apend_data_PON(workbook,hojas_PON,periodo)
            if periodo == "mes":
                workbook.save(filename=excel_PON_mensual())
                #os.system("chmod 775 {}".format(excel_PON_semanal))
            elif periodo == "semana":
                workbook.save(filename=excel_PON_semanal())
                #os.system("chmod 775 {}".format(excel_PON_semanal))
            logger.info("Se culmino la creacion del reporte {} de PON".format(periodo))

#reportes_xlsx("PON","semana")
#reportes_xlsx("ONT","semana")
#reportes_xlsx("PON","mes")
#reportes_xlsx("ONT","mes")