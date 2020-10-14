import mysql.connector
import sys

#CONECTOR BD 

def conector():
    mydb = mysql.connector.connect(host="localhost",user="reportes",password="antel2020",database="reportes_zabbix")
    return mydb

#SEMANAL

def insert_picos_diarios_semanal(mydb):#LISTO
    sql = "insert into picos_diarios_semanal (tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from crudos_diarios t2) t1 where t1.rn =1;"
    mydb.cursor().execute(sql)
    mydb.commit()
    print(mydb.cursor().rowcount)
    mydb.cursor().close()
    mydb.close()

def insert_promedio_semanal(mydb):#LISTO
    sql = "insert into promedio_semanal(tipo,nodo,puerto,direccion,promedio_semana) select tipo,nodo, puerto, direccion, avg(pico) as promedio_semana from picos_diarios_semanal group by tipo, nodo, puerto, direccion;"
    mydb.cursor().execute(sql)
    mydb.commit()
    print(mydb.cursor().rowcount)
    mydb.cursor().close()
    mydb.close()

def insert_picos_semanal(mydb):#LISTO
    sql = "insert into picos_semanal (tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from picos_diarios_semanal t2) t1 where t1.rn =1;"
    mydb.cursor().execute(sql)
    mydb.commit()
    print(mydb.cursor().rowcount)
    mydb.cursor().close()
    mydb.close()

def insert_reporte_semanal(mydb):#LISTO
    sql = "insert into reporte_semanal(tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediosemana) select pico.tipo, pico.nodo,pico.puerto,pico.direccion,pico.hora,pico.fecha,pico.promedio,pico.pico, promedio.promedio_semana FROM promedio_semanal promedio, picos_semanal pico WHERE pico.tipo = promedio.tipo and pico.nodo = promedio.nodo and pico.puerto = promedio.puerto and pico.direccion = promedio.direccion GROUP BY pico.tipo, pico.nodo, pico.puerto, pico.direccion;"
    mydb.cursor().execute(sql)
    mydb.commit()
    print(mydb.cursor().rowcount)
    mydb.cursor().close()
    mydb.close()

def insert_resaldo_semanal(mydb):#LISTO
    sql = "insert into respaldo_reporte_semanal(tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediosemana) select tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediosemana FROM reporte_semanal;"
    mydb.cursor().execute(sql)
    mydb.commit()
    print(mydb.cursor().rowcount)
    mydb.cursor().close()
    mydb.close()

#MENSUAL

def insert_picos_diarios_mensual():#PASS
    pass

def insert_picos_mensual():#PASS
    pass

def insert_promedio_mensual():#PASS
    pass

def insert_reporte_mensual():#PASS
    pass

def insert_resaldo_mensual():#PASS
    pass

#MENU

if sys.argv[1] == "insert_picos_diarios_semanal":
    insert_picos_diarios_semanal(conector())
elif sys.argv[1] == "insert_promedio_semanal":
    insert_promedio_semanal(conector())
elif sys.argv[1] == "insert_picos_semanal":
    insert_picos_semanal(conector())
elif sys.argv[1] == "insert_reporte_semanal":
    insert_reporte_semanal(conector())
elif sys.argv[1] == "insert_resaldo_semanal":
    insert_resaldo_semanal(conector())