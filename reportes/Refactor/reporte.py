#!/usr/bin/python

from openpyxl import Workbook
from openpyxl.styles import NamedStyle, Font, Border, Alignment, Side
import mysql.connector
from datetime import datetime, date, timedelta
import sys

from direcciones import encabezados_PON, encabezados_ONT
from consultas import sql_ont_semanal, sql_ont_mensual, sql_pon_semanal, sql_pon_mensual
from conector import conector


def crear_hojas_ONT(workbook):

    # Creo Hojas
    subida_ont = workbook["Sheet"]
    subida_ont.title = "Subida ONT"
    bajada_ont = workbook.create_sheet("Bajada ONT")


def crear_hojas_PON(workbook):

    # Creo Hojas
    subida_pon = workbook["Sheet"]
    subida_pon.title = "Subida PON"
    bajada_pon = workbook.create_sheet("Bajada PON")
    subida_uplink = workbook.create_sheet("Subida Uplink")
    bajada_uplink = workbook.create_sheet("Bajada Uplink")


def crear_encabezados_ONT(subida_ont,bajada_ont):
    #ENCABEZADOS
    # Subida Ont
    subida_ont["A1"] = encabezados[0]
    subida_ont["B1"] = encabezados[1]
    subida_ont["C1"] = encabezados[2]
    subida_ont["D1"] = encabezados[3]
    subida_ont["E1"] = encabezados[4]
    subida_ont["F1"] = encabezados[5]
    subida_ont["G1"] = encabezados[6]
    subida_ont["H1"] = encabezados[7]
    subida_ont["I1"] = encabezados[8]
    subida_ont["J1"] = encabezados[9]

    # Bajada Ont
    bajada_ont["A1"] = encabezados[0]
    bajada_ont["B1"] = encabezados[1]
    bajada_ont["C1"] = encabezados[2]
    bajada_ont["D1"] = encabezados[3]
    bajada_ont["E1"] = encabezados[4]
    bajada_ont["F1"] = encabezados[5]
    bajada_ont["G1"] = encabezados[6]
    bajada_ont["H1"] = encabezados[7]
    bajada_ont["I1"] = encabezados[8]
    bajada_ont["J1"] = encabezados[9]

    return workbook


def crear_encabezados_PON(subida_pon,bajada_pon,subida_uplink,bajada_uplink):
    #ENCABEZADOS
    # Subida Pon
    subida_pon["A1"] = encabezados[0]
    subida_pon["B1"] = encabezados[1]
    subida_pon["C1"] = encabezados[2]
    subida_pon["D1"] = encabezados[3]
    subida_pon["E1"] = encabezados[4]
    subida_pon["F1"] = encabezados[5]
    subida_pon["G1"] = encabezados[6]
    subida_pon["H1"] = encabezados[7]
    subida_pon["I1"] = encabezados[8]
    subida_pon["J1"] = encabezados[9]
    subida_pon["K1"] = encabezados[10]
    subida_pon["L1"] = encabezados[11]
    subida_pon["M1"] = encabezados[12]
    # Bajada Pon
    bajada_pon["A1"] = encabezados[0]
    bajada_pon["B1"] = encabezados[1]
    bajada_pon["C1"] = encabezados[2]
    bajada_pon["D1"] = encabezados[3]
    bajada_pon["E1"] = encabezados[4]
    bajada_pon["F1"] = encabezados[5]
    bajada_pon["G1"] = encabezados[6]
    bajada_pon["H1"] = encabezados[7]
    bajada_pon["I1"] = encabezados[8]
    bajada_pon["J1"] = encabezados[9]
    bajada_pon["K1"] = encabezados[10]
    bajada_pon["L1"] = encabezados[11]
    bajada_pon["M1"] = encabezados[12]

    # Subida Uplink
    subida_uplink["A1"] = encabezados[0]
    subida_uplink["B1"] = encabezados[1]
    subida_uplink["C1"] = encabezados[2]
    subida_uplink["D1"] = encabezados[3]
    subida_uplink["E1"] = encabezados[4]
    subida_uplink["F1"] = encabezados[5]
    subida_uplink["G1"] = encabezados[6]
    subida_uplink["H1"] = encabezados[7]
    subida_uplink["I1"] = encabezados[8]

    # Bajada Uplink
    bajada_uplink["A1"] = encabezados[0]
    bajada_uplink["B1"] = encabezados[1]
    bajada_uplink["C1"] = encabezados[2]
    bajada_uplink["D1"] = encabezados[3]
    bajada_uplink["E1"] = encabezados[4]
    bajada_uplink["F1"] = encabezados[5]
    bajada_uplink["G1"] = encabezados[6]
    bajada_uplink["H1"] = encabezados[7]
    bajada_uplink["I1"] = encabezados[8]
    
    return workbook


def apend_data_ONT(subida_ont,bajada_ont,periodo):
    if periodo == "semana":
        sql = 
        resultado = conector(sql_ont_semanal,"select","Select del reporte semanal de ONT")
    elif periodo == "mes":
        sql = 
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
        if direccion == "RX":
            lista_append = [tipo,nodo,puerto,etiqueta,hora,fecha,pico,(pico*100)/10000,prom_hora_pico,prom_picos_diarios]
            subida_ont.append(lista_append)
        elif direccion == "TX":
            lista_append = [tipo,nodo,puerto,etiqueta,hora,fecha,pico,(pico*100)/10000,prom_hora_pico,prom_picos_diarios]
            bajada_ont.append(lista_append)
    return workbook


