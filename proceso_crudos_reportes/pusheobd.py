import mysql.connector
import csv
import pickle

#coneccion a la BD
mydb = mysql.connector.connect(host="192.168.211.4",user="reportes",password="antel2020",database="diarios_crudos")
mycursor = mydb.cursor()

with open ('./proceso_crudos_reportes/test-pickle2', 'rb') as lista:
    lista_tuplas = pickle.load(lista)
    sql = "INSERT INTO `crudos` (`nodo`, `puerto`, `direccion`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    mycursor.executemany(sql, lista_tuplas)

    mydb.commit()

    print(mycursor.rowcount, "Ingresado.")