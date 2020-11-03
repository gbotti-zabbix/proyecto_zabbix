import mysql.connector
import sys

#CONECTOR BD 

def conector_insert(sql):
    #mydb = mysql.connector.connect(host="localhost",user="reportes",password="antel2020",database="reportes_zabbix")
    mydb = mysql.connector.connect (host="192.168.211.4",user="reportes",password="antel2020",database="reportes_zabbix")
    cursor = mydb.cursor()
    cursor.execute(sql)
    mydb.commit()
    print(cursor.rowcount)
    mydb.cursor().close()
    mydb.close()




conector_insert ("select * from t_rbs_x_puerto ")



