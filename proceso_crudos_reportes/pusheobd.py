import mysql.connector

mydb = mysql.connector.connect(host="192.168.211.4",user="reportes",password="antel2020",database="diarios_crudos")
mycursor = mydb.cursor()

sql = "INSERT INTO `crudos` (`nodo`, `puerto`, `direccion`, `hora`, `fecha`, `promedio`, `pico`) VALUES ('{}','{}','{}','{}','{}',{},{})".format("Nodo2",'Puerto4','RX','23:30:00','2020-08-21',16.5,21.2)
#sql = "INSERT INTO `Prueba` (`test1`, `test2`) VALUES ('check1','check2')"
mycursor.execute(sql)

mydb.commit()

print(mycursor.rowcount, "Ingresado.")

print("1 record inserted, ID:", mycursor.lastrowid) 