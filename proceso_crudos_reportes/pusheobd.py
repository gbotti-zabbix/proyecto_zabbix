#!/usr/bin/python
import mysql.connector
import pickle
from datetime import datetime, date

print(datetime.now())
archivo_pickle = "/var/lib/reportes-zabbix/Merged-Trends-" + str(date.today()) + ".pickle"
contador_insert = 0
lista_final = []
contador_final = []
sql = "INSERT INTO `crudos_diarios` (`nodo`, `puerto`, `direccion`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s)"


with open (archivo_pickle, 'rb') as lista:
    #carga de lista
    lista_tuplas = pickle.load(lista)
    #

mydb = mysql.connector.connect(host="192.168.211.4",user="reportes",password="antel2020",database="reportes_zabbix")
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
print(datetime.datetime.now())