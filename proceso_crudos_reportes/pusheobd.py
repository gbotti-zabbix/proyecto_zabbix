# import mysql.connector
# import csv
# import pickle

# #coneccion a la BD
# mydb = mysql.connector.connect(host="192.168.211.4",user="reportes",password="antel2020",database="diarios_crudos")
# mycursor = mydb.cursor()

# with open ('./proceso_crudos_reportes/test-pickle2', 'rb') as lista:
#     lista_tuplas = pickle.load(lista)
#     sql = "INSERT INTO `crudos` (`nodo`, `puerto`, `direccion`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
#     mycursor.executemany(sql, lista_tuplas)

#     mydb.commit()

#     print(mycursor.rowcount, "Ingresado.")

#!/usr/bin/python
from datetime import date
import mysql.connector
import csv
import pickle

archivo_pickle = "./proceso_crudos_reportes/test-pickle"

#coneccion a la BD
#mydb = mysql.connector.connect(host="localhost",user="reportes",password="antel2020",database="reportes_zabbix",connect_timeout=1000)
#mycursor = mydb.cursor()

with open (archivo_pickle, 'rb') as lista:
    #carga de lista
    lista_tuplas = pickle.load(lista)
    #
#coneccion con BD
mydb = mysql.connector.connect(host="192.168.211.4",user="reportes",password="antel2020",database="reportes_zabbix")
mycursor = mydb.cursor()
#

#pusheo
sql = "INSERT INTO `crudos_diarios` (`nodo`, `puerto`, `direccion`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
mycursor.executemany(sql, lista_tuplas)
mydb.commit()
#

print(mycursor.rowcount, "Ingresado.")
