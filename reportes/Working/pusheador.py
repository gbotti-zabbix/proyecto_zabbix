#!/usr/bin/python
import sys
import mysql.connector
import pickle
from datetime import datetime, date

def pusheo_crudos_diarios():
    fecha_pickle = input("Que fecha de PON desea pushear?\n Formato: YYYY-MM-DD: ")

    #variables que uso mas adelante y consulta sql
    print(datetime.now())
    archivo_pickle = "/var/lib/reportes-zabbix/crudos/Merged-Trends-" + fecha_pickle + ".pickle"
    contador_insert = 0
    lista_final = []
    contador_final = []
    sql = "INSERT INTO `crudos_diarios` (`tipo`,`nodo`, `puerto`, `direccion`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
    #

    with open (archivo_pickle, 'rb') as lista:
        #carga de lista
        lista_tuplas = pickle.load(lista)
        #

    mydb = mysql.connector.connect(host="localhost",user="reportes",password="antel2020",database="reportes_zabbix")
    mycursor = mydb.cursor()

    for dato in lista_tuplas:
        lista_final.append(dato)
        contador_insert = contador_insert + 1
        if contador_insert == 100000:
            mycursor.executemany(sql, lista_final)
            mydb.commit()
            contador_final.append(mycursor.rowcount)
            contador_insert = 0
            lista_final.clear()

    mycursor.executemany(sql, lista_final)
    mydb.commit()
    contador_final.append(mycursor.rowcount)
    print("Total Ingresado",sum(contador_final))
    print(datetime.now())


def pusheo_crudos_diarios_ONT():

    fecha_pickle = input("Que fecha de ONT desea pushear?\n Formato: YYYY-MM-DD: ")

    print(datetime.now())

    archivo_pickle = "/var/lib/reportes-zabbix/crudos/Merged-Trends-" + fecha_pickle + "_ONT.pickle"
    sql = "INSERT INTO `crudos_diarios_ont` (`tipo`,`nodo`, `puerto`, `direccion`, `etiqueta`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    
    #carga el pickle
    with open (archivo_pickle, 'rb') as lista:
        lista_tuplas = pickle.load(lista)
    #
    
    #coneccion con la BD
    mydb = mysql.connector.connect(host="localhost",user="reportes",password="antel2020",database="reportes_zabbix")
    mycursor = mydb.cursor()
    #

    #pusheo a BD
    mycursor.executemany(sql, lista_tuplas)
    mydb.commit()
    contador_ingresos = mycursor.rowcount
    print("Total Ingresado",contador_ingresos)
    print(datetime.now())

#Menu
if sys.argv[1] == "PON":
    pusheo_crudos_diarios()
elif sys.argv[1] == "ONT":
    pusheo_crudos_diarios_ONT()