#!/usr/bin/python
import sys
import mysql.connector
import pickle
from datetime import datetime, date

def conector_insert(sql):
    mydb = mysql.connector.connect(host="localhost",user="reportes",password="antel2020",database="reportes_zabbix")
    cursor = mydb.cursor()
    cursor.execute(sql)
    mydb.commit()
    print(cursor.rowcount)
    mydb.cursor().close()
    mydb.close()


def insert_picos_diarios_semanal():
    sql = "insert into picos_diarios_semanal (tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from crudos_diarios t2) t1 where t1.rn =1;"
    return sql


def insert_picos_diarios_mensual():
    sql = "insert into picos_diarios_mensual (tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from crudos_diarios t2) t1 where t1.rn =1;"
    return sql


def insert_picos_diarios_semanal_ont():
    sql = "insert into picos_diarios_semanal_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from crudos_diarios_ont t2) t1 where t1.rn =1;"
    return sql


def insert_picos_diarios_mensual_ont():
    sql = "insert into picos_diarios_mensual_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from crudos_diarios_ont t2) t1 where t1.rn =1;"
    return sql


def pusheo_crudos_diarios(fecha_pickle):

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


def pusheo_crudos_diarios_ONT(fecha_pickle):

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

tipo_pusheo = int(input("Desea Pushear:\n1- PON\n2-ONT\n3-Cancelar\nIngrese opcion numerica: "))

fecha_pickle = input("Que fecha desea pushear?\n Formato: YYYY-MM-DD: ")

inserter = int(input("Quiere insertarlo en picos diarios?\nIngrese una opcion numerica\n1- No\n2- Semanales\n3- Mensual"))


if tipo_pusheo == 1:
    pusheo_crudos_diarios(fecha_pickle)
    if inserter == 1:
        pass
    elif inserter == 2:
        conector_insert(insert_picos_diarios_semanal())
    elif inserter == 3:
        conector_insert(insert_picos_diarios_mensual())

elif tipo_pusheo == 2:
    pusheo_crudos_diarios_ONT(fecha_pickle)
    if inserter == 1:
        pass
    elif inserter == 2:
        conector_insert(insert_picos_diarios_semanal_ont())
    elif inserter == 3:
        conector_insert(insert_picos_diarios_mensual_ont())
elif tipo_pusheo == 3:
    pass