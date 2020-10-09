import mysql.connector

def conector():
    mydb = mysql.connector.connect(host="192.168.211.4",user="reportes",password="antel2020",database="reportes_zabbix")
    return mydb

def insert_picos_diarios_semanal(mydb):
    sql = "INSERT INTO `test_picos` (`tipo`,`nodo`, `puerto`, `direccion`, `hora`,`pico`) VALUES ('C600','N-PALMIRA-01Z','18/7','TX','13:00:00',58)"
    mydb.cursor().execute(sql)
    mydb.commit()
    print(mydb.cursor().rowcount)
    mydb.cursor().close()
    mydb.close()

def menu():
    print("""* 1 para pico_diario_semanal
    * 2 para conector""")
    selector = int(input("Que quiere hacer:"))
    if selector == 1:
        insert_picos_diarios_semanal(conector())
    elif selector == 2:
        conector()

menu ()











def insert_picos_diarios_mensual():
    pass

def insert_picos_semanal():
    pass

def insert_picos_mensual():
    pass

def insert_promedio_semanal():
    pass

def insert_promedio_mensual():
    pass

def insert_reporte_semanal():
    pass

def insert_reporte_mensual():
    pass

def insert_resaldo_semanal():
    pass

def insert_resaldo_mensual():
    pass