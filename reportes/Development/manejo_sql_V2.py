import mysql.connector
import sys

#CONECTOR BD 

def conector_insert(sql):
    mydb = mysql.connector.connect(host="localhost",user="reportes",password="antel2020",database="reportes_zabbix")
    cursor = mydb.cursor()
    cursor.execute(sql)
    mydb.commit()
    print(cursor.rowcount)
    mydb.cursor().close()
    mydb.close()

###OLT###
#SEMANAL

def insert_picos_diarios_semanal():
    sql = "insert into picos_diarios_semanal_v2 (gestion_nodo_slot_puerto_direccion, gestion_nodo_slot_puerto, tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.gestion_nodo_slot_puerto_direccion, t1.gestion_nodo_slot_puerto, t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.gestion_nodo_slot_puerto_direccion order by t2.pico desc) as rn from crudos_diarios_v2 t2) t1 where t1.rn =1;"
    return sql

def insert_promedio_semanal():
    sql = "insert into promedio_semanal_v2(gestion_nodo_slot_puerto_direccion, promedio_semana) select gestion_nodo_slot_puerto_direccion, avg(pico) as promedio_semana from picos_diarios_semanal_v2 group by gestion_nodo_slot_puerto_direccion;"
    return sql

def insert_picos_semanal():
    sql = "insert into picos_semanal_v2 (gestion_nodo_slot_puerto_direccion, gestion_nodo_slot_puerto, tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.gestion_nodo_slot_puerto_direccion, t1.gestion_nodo_slot_puerto, t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.gestion_nodo_slot_puerto_direccion order by t2.pico desc) as rn from picos_diarios_semanal_v2 t2) t1 where t1.rn =1;"
    return sql

def insert_reporte_semanal():
    sql = "insert into reporte_semanal_v2(tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediosemana,rbs,emp) select pico.tipo, pico.nodo,pico.puerto,pico.direccion,pico.hora,pico.fecha,pico.promedio,pico.pico, promedio.promedio_semana, tlkr.rbs_x_puerto, tlke.empresariales_x_puerto FROM promedio_semanal_v2 promedio, picos_semanal_v2 pico, t_rbs_x_puerto tlkr, t_empresariales_x_puerto tlke WHERE pico.gestion_nodo_slot_puerto_direccion = promedio.gestion_nodo_slot_puerto_direccion AND pico.gestion_nodo_slot_puerto = tlkr.indice_gestion_slot_puerto AND pico.gestion_nodo_slot_puerto = tlke.indice_gestion_slot_puerto GROUP BY pico.gestion_nodo_slot_puerto_direccion;"
    return sql

def insert_resaldo_semanal():
    sql = "insert into respaldo_reporte_semanal(tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediosemana) select tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediosemana FROM reporte_semanal;"
    return sql

#MENSUAL

def insert_picos_diarios_mensual():
    sql = "insert into picos_diarios_mensual (tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from crudos_diarios t2) t1 where t1.rn =1;"
    return sql

def insert_promedio_mensual():
    sql = "insert into promedio_mensual(tipo,nodo,puerto,direccion,promedio_mes) select tipo,nodo, puerto, direccion, avg(pico) as promedio_mes from picos_diarios_mensual group by tipo, nodo, puerto, direccion;"
    return sql

def insert_picos_mensual():
    sql = "insert into picos_mensual (tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from picos_diarios_mensual t2) t1 where t1.rn =1;"
    return sql

def insert_reporte_mensual():
    sql = "insert into reporte_mensual(tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediomes) select pico.tipo, pico.nodo,pico.puerto,pico.direccion,pico.hora,pico.fecha,pico.promedio,pico.pico, promedio.promedio_mes FROM promedio_mensual promedio, picos_mensual pico WHERE pico.tipo = promedio.tipo and pico.nodo = promedio.nodo and pico.puerto = promedio.puerto and pico.direccion = promedio.direccion GROUP BY pico.tipo, pico.nodo, pico.puerto, pico.direccion;"
    return sql

def insert_resaldo_mensual():
    sql = "insert into respaldo_reporte_mensual(tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediomes) select tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediomes FROM reporte_mensual;"
    return sql


###ONT###
#SEMANAL

def insert_picos_diarios_semanal_ont():
    sql = "insert into picos_diarios_semanal_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from crudos_diarios_ont t2) t1 where t1.rn =1;"
    return sql

def insert_promedio_semanal_ont():
    sql = "insert into promedio_semanal_ont(tipo,nodo,puerto,direccion,promedio_semana) select tipo,nodo, puerto, direccion, avg(pico) as promedio_semana from picos_diarios_semanal_ont group by tipo, nodo, puerto, direccion;"
    return sql

def insert_picos_semanal_ont():
    sql = "insert into picos_semanal_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from picos_diarios_semanal_ont t2) t1 where t1.rn =1;"
    return sql

def insert_reporte_semanal_ont():
    sql = "insert into reporte_semanal_ont(tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediosemana) select pico.tipo,pico.nodo,pico.puerto,pico.etiqueta,pico.direccion,pico.hora,pico.fecha,pico.promedio,pico.pico, promedio.promedio_semana FROM promedio_semanal_ont promedio, picos_semanal_ont pico WHERE pico.tipo = promedio.tipo and pico.nodo = promedio.nodo and pico.puerto = promedio.puerto and pico.direccion = promedio.direccion GROUP BY pico.tipo, pico.nodo, pico.puerto, pico.direccion;"
    return sql

def insert_resaldo_semanal_ont():
    sql = "insert into respaldo_reporte_semanal_ont(tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediosemana) select tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediosemana FROM reporte_semanal_ont;"
    return sql

#MENSUAL

def insert_picos_diarios_mensual_ont():
    sql = "insert into picos_diarios_mensual_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from crudos_diarios_ont t2) t1 where t1.rn =1;"
    return sql

def insert_promedio_mensual_ont():
    sql = "insert into promedio_mensual_ont(tipo,nodo,puerto,direccion,promedio_mes) select tipo,nodo, puerto, direccion, avg(pico) as promedio_mes from picos_diarios_mensual_ont group by tipo, nodo, puerto, direccion;"
    return sql

def insert_picos_mensual_ont():
    sql = "insert into picos_mensual_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from picos_diarios_mensual_ont t2) t1 where t1.rn =1;"
    return sql

def insert_reporte_mensual_ont():
    sql = "insert into reporte_mensual_ont(tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediomes) select pico.tipo, pico.nodo,pico.puerto,pico.etiqueta,pico.direccion,pico.hora,pico.fecha,pico.promedio,pico.pico, promedio.promedio_mes FROM promedio_mensual_ont promedio, picos_mensual_ont pico WHERE pico.tipo = promedio.tipo and pico.nodo = promedio.nodo and pico.puerto = promedio.puerto and pico.direccion = promedio.direccion GROUP BY pico.tipo, pico.nodo, pico.puerto, pico.direccion;"
    return sql

def insert_resaldo_mensual_ont():
    sql = "insert into respaldo_reporte_mensual_ont(tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediomes) select tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediomes FROM reporte_mensual_ont;"
    return sql


#MENU
###OLT###
#SEMANAL
if sys.argv[1] == "insert_picos_diarios_semanal":
    conector_insert(insert_picos_diarios_semanal())
elif sys.argv[1] == "insert_promedio_semanal":
    conector_insert(insert_promedio_semanal())
elif sys.argv[1] == "insert_picos_semanal":
    conector_insert(insert_picos_semanal())
elif sys.argv[1] == "insert_reporte_semanal":
    conector_insert(insert_reporte_semanal())
elif sys.argv[1] == "insert_resaldo_semanal":
    conector_insert(insert_resaldo_semanal())
#MENSUAL
elif sys.argv[1] == "insert_picos_diarios_mensual":
    conector_insert(insert_picos_diarios_mensual())
elif sys.argv[1] == "insert_promedio_mensual":
    conector_insert(insert_promedio_mensual())
elif sys.argv[1] == "insert_picos_mensual":
    conector_insert(insert_picos_mensual())
elif sys.argv[1] == "insert_reporte_mensual":
    conector_insert(insert_reporte_mensual())
elif sys.argv[1] == "insert_resaldo_mensual":
    conector_insert(insert_resaldo_mensual())
###ONT###
#SEMANAL
if sys.argv[1] == "insert_picos_diarios_semanal_ont":
    conector_insert(insert_picos_diarios_semanal_ont())
elif sys.argv[1] == "insert_promedio_semanal_ont":
    conector_insert(insert_promedio_semanal_ont())
elif sys.argv[1] == "insert_picos_semanal_ont":
    conector_insert(insert_picos_semanal_ont())
elif sys.argv[1] == "insert_reporte_semanal_ont":
    conector_insert(insert_reporte_semanal_ont())
elif sys.argv[1] == "insert_resaldo_semanal_ont":
    conector_insert(insert_resaldo_semanal_ont())
#MENSUAL
elif sys.argv[1] == "insert_picos_diarios_mensual_ont":
    conector_insert(insert_picos_diarios_mensual_ont())
elif sys.argv[1] == "insert_promedio_mensual_ont":
    conector_insert(insert_promedio_mensual_ont())
elif sys.argv[1] == "insert_picos_mensual_ont":
    conector_insert(insert_picos_mensual_ont())
elif sys.argv[1] == "insert_reporte_mensual_ont":
    conector_insert(insert_reporte_mensual_ont())
elif sys.argv[1] == "insert_resaldo_mensual_ont":
    conector_insert(insert_resaldo_mensual_ont())