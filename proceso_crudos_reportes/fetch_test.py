import mysql.connector
import datetime
contador = 0

mydb = mysql.connector.connect(host="192.168.211.4",user="reportes",password="antel2020",database="reportes_zabbix")
mycursor = mydb.cursor()

mycursor.execute("SELECT nodo,puerto,direccion,hora,fecha,promedio, pico FROM picos_diarios GROUP BY nodo, puerto,direccion,fecha ORDER BY pico DESC LIMIT 10;")

myresult = mycursor.fetchall()

#print (type(myresult[0][0]),type(myresult[0][1]),type(myresult[0][2]),type(myresult[0][3]),type(myresult[0][4]),type(myresult[0][5]),type(myresult[0][6]))
print (myresult)