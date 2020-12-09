#!/usr/bin/python

######pusheo zabbix#####
sql_truncate_cdiarios_PON = 'TRUNCATE crudos_diarios;'
sql_truncate_cdiarios_ONT = 'TRUNCATE crudos_diarios_ont;'
sql_push_diarios_ONT = "INSERT INTO `crudos_diarios_ont` (`tipo`,`nodo`, `puerto`, `direccion`, `etiqueta`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
sql_push_diarios_PON = "INSERT INTO `crudos_diarios` (`id_zabbix`,`id_tlk`,`tipo`,`nodo`, `puerto`, `direccion`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


#####flujo DB#####

#truncates

##consultas diarias##
#PON
sql_insert_picos_diarios_semanal_pon = "insert into picos_diarios_semanal (id_zabbix, id_tlk, tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.id_zabbix, t1.id_tlk, t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.id_zabbix order by t2.pico desc) as rn from crudos_diarios t2) t1 where t1.rn =1;"
sql_insert_picos_diarios_mensual_pon = "insert into picos_diarios_mensual (id_zabbix, id_tlk, tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.id_zabbix, t1.id_tlk, t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.id_zabbix order by t2.pico desc) as rn from crudos_diarios t2) t1 where t1.rn =1;"
#ONT
sql_insert_picos_diarios_semanal_ont = "insert into picos_diarios_semanal_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from crudos_diarios_ont t2) t1 where t1.rn =1;"
sql_insert_picos_diarios_mensual_ont = "insert into picos_diarios_mensual_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from crudos_diarios_ont t2) t1 where t1.rn =1;"

##consultas semanales##
#PON
sql_insert_promedio_semanal_pon = "insert into promedio_semanal(id_zabbix,promedio_semana) select id_zabbix, avg(pico) as promedio_semana from picos_diarios_semanal group by id_zabbix;"
sql_insert_picos_semanal_pon = "insert into picos_semanal (id_zabbix, id_tlk ,tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.id_zabbix, t1.id_tlk, t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.id_zabbix order by t2.pico desc) as rn from picos_diarios_semanal t2) t1 where t1.rn =1;"
sql_insert_reporte_semanal_pon = "insert into reporte_semanal(tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediosemana,wf,datos,emp,rbs) select pico.tipo, pico.nodo,pico.puerto,pico.direccion,pico.hora,pico.fecha,pico.promedio,pico.pico, promedio.promedio_semana, tlk.WF, tlk.Datos, tlk.Empresariales, tlk.RBS FROM picos_semanal pico LEFT JOIN promedio_semanal promedio ON pico.id_zabbix = promedio.id_zabbix LEFT JOIN t_resumen_servicios_tlk tlk ON pico.id_tlk = tlk.id_tlk GROUP BY pico.id_zabbix;"
sql_insert_respaldo_semanal_pon = "insert into respaldo_reporte_semanal(tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediosemana,wf,datos,emp,rbs) select tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediosemana,wf,datos,emp,rbs FROM reporte_semanal;"
#ONT
sql_insert_promedio_semanal_ont = "insert into promedio_semanal_ont(tipo,nodo,puerto,direccion,promedio_semana) select tipo,nodo, puerto, direccion, avg(pico) as promedio_semana from picos_diarios_semanal_ont group by tipo, nodo, puerto, direccion;"
sql_insert_picos_semanal_ont = "insert into picos_semanal_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from picos_diarios_semanal_ont t2) t1 where t1.rn =1;"
sql_insert_reporte_semanal_ont = "insert into reporte_semanal_ont(tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediosemana) select pico.tipo,pico.nodo,pico.puerto,pico.etiqueta,pico.direccion,pico.hora,pico.fecha,pico.promedio,pico.pico, promedio.promedio_semana FROM promedio_semanal_ont promedio, picos_semanal_ont pico WHERE pico.tipo = promedio.tipo and pico.nodo = promedio.nodo and pico.puerto = promedio.puerto and pico.direccion = promedio.direccion GROUP BY pico.tipo, pico.nodo, pico.puerto, pico.direccion;"
sql_insert_respaldo_semanal_ont = "insert into respaldo_reporte_semanal_ont(tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediosemana) select tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediosemana FROM reporte_semanal_ont;"

##consultas mensuales##
#PON
sql_insert_promedio_mensual_pon = "insert into promedio_mensual(id_zabbix,promedio_mes) select id_zabbix, avg(pico) as promedio_mes from picos_diarios_mensual group by id_zabbix;"
sql_insert_picos_mensual_pon = "insert into picos_mensual (id_zabbix, id_tlk ,tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.id_zabbix, t1.id_tlk, t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.id_zabbix order by t2.pico desc) as rn from picos_diarios_mensual t2) t1 where t1.rn =1;"
sql_insert_reporte_mensual_pon = "insert into reporte_mensual(tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediomes,wf,datos,emp,rbs) select pico.tipo, pico.nodo,pico.puerto,pico.direccion,pico.hora,pico.fecha,pico.promedio,pico.pico, promedio.promedio_mes, tlk.WF, tlk.Datos, tlk.Empresariales, tlk.RBS FROM picos_mensual pico LEFT JOIN promedio_mensual promedio ON pico.id_zabbix = promedio.id_zabbix LEFT JOIN t_resumen_servicios_tlk tlk ON pico.id_tlk = tlk.id_tlk GROUP BY pico.id_zabbix;"
sql_insert_respaldo_mensual_pon = "insert into respaldo_reporte_mensual(tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediomes,wf,datos,emp,rbs) select tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediomes,wf,datos,emp,rbs FROM reporte_mensual;"
#ONT
sql_insert_promedio_mensual_ont = "insert into promedio_mensual_ont(tipo,nodo,puerto,direccion,promedio_mes) select tipo,nodo, puerto, direccion, avg(pico) as promedio_mes from picos_diarios_mensual_ont group by tipo, nodo, puerto, direccion;"
sql_insert_picos_mensual_ont = "insert into picos_mensual_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from picos_diarios_mensual_ont t2) t1 where t1.rn =1;"
sql_insert_reporte_mensual_ont = "insert into reporte_mensual_ont(tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediomes) select pico.tipo, pico.nodo,pico.puerto,pico.etiqueta,pico.direccion,pico.hora,pico.fecha,pico.promedio,pico.pico, promedio.promedio_mes FROM promedio_mensual_ont promedio, picos_mensual_ont pico WHERE pico.tipo = promedio.tipo and pico.nodo = promedio.nodo and pico.puerto = promedio.puerto and pico.direccion = promedio.direccion GROUP BY pico.tipo, pico.nodo, pico.puerto, pico.direccion;"
sql_insert_respaldo_mensual_ont = "insert into respaldo_reporte_mensual_ont(tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediomes) select tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediomes FROM reporte_mensual_ont;"


#####Reporte Zabbix#####
sql_ont_semanal = "SELECT * FROM reporte_semanal_ont order by pico DESC"
sql_ont_mensual = "SELECT * FROM reporte_mensual_ont order by pico DESC"
sql_pon_semanal = "SELECT * FROM reporte_semanal order by pico DESC"
sql_pon_mensual = "SELECT * FROM reporte_mensual order by pico DESC"