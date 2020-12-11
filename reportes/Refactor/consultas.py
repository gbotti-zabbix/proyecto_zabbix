#!/usr/bin/python

######pusheo zabbix#####
sql_truncate_cdiarios_PON = 'TRUNCATE crudos_diarios;'
sql_truncate_cdiarios_ONT = 'TRUNCATE crudos_diarios_ont;'
sql_push_diarios_ONT = "INSERT INTO `crudos_diarios_ont` (`tipo`,`nodo`, `puerto`, `direccion`, `etiqueta`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
sql_push_diarios_PON = "INSERT INTO `crudos_diarios` (`id_zabbix`,`id_tlk`,`tipo`,`nodo`, `puerto`, `direccion`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


#####flujo DB#####
###Consultas###
class consultas():
    def __init__(self,query,tipo,mensaje):
        self.query = query
        self.tipo = tipo
        self.mensaje = mensaje

##consultas diarias##
#PON
insert_picos_diarios_semanal_pon = consultas("insert into picos_diarios_semanal (id_zabbix, id_tlk, tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.id_zabbix, t1.id_tlk, t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.id_zabbix order by t2.pico desc) as rn from crudos_diarios t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_diarios_semanal")
insert_picos_diarios_mensual_pon = consultas("insert into picos_diarios_mensual (id_zabbix, id_tlk, tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.id_zabbix, t1.id_tlk, t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.id_zabbix order by t2.pico desc) as rn from crudos_diarios t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_diarios_mensual")
#ONT
insert_picos_diarios_semanal_ont = consultas("insert into picos_diarios_semanal_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from crudos_diarios_ont t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_diarios_semanal_ont")
insert_picos_diarios_mensual_ont = consultas("insert into picos_diarios_mensual_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from crudos_diarios_ont t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_diarios_mensual_ont")


##consultas semanales##
#PON
insert_promedio_semanal_pon = consultas("insert into promedio_semanal(id_zabbix,promedio_semana) select id_zabbix, avg(pico) as promedio_semana from picos_diarios_semanal group by id_zabbix;","Flujo","Insertando datos en promedio_semanal")
insert_picos_semanal_pon = consultas("insert into picos_semanal (id_zabbix, id_tlk ,tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.id_zabbix, t1.id_tlk, t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.id_zabbix order by t2.pico desc) as rn from picos_diarios_semanal t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_semanal")
insert_reporte_semanal_pon = consultas("insert into reporte_semanal(tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediosemana,wf,datos,emp,rbs) select pico.tipo, pico.nodo,pico.puerto,pico.direccion,pico.hora,pico.fecha,pico.promedio,pico.pico, promedio.promedio_semana, tlk.WF, tlk.Datos, tlk.Empresariales, tlk.RBS FROM picos_semanal pico LEFT JOIN promedio_semanal promedio ON pico.id_zabbix = promedio.id_zabbix LEFT JOIN t_resumen_servicios_tlk tlk ON pico.id_tlk = tlk.id_tlk GROUP BY pico.id_zabbix;","Flujo","Insertando datos en reporte_semanal")
insert_respaldo_semanal_pon = consultas("insert into respaldo_reporte_semanal(tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediosemana,wf,datos,emp,rbs) select tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediosemana,wf,datos,emp,rbs FROM reporte_semanal;","Flujo","Insertando datos en respaldo_reporte_semanal")
#ONT
insert_promedio_semanal_ont = consultas("insert into promedio_semanal_ont(tipo,nodo,puerto,direccion,promedio_semana) select tipo,nodo, puerto, direccion, avg(pico) as promedio_semana from picos_diarios_semanal_ont group by tipo, nodo, puerto, direccion;","Flujo","Insertando datos en promedio_semanal_ont")
insert_picos_semanal_ont = consultas("insert into picos_semanal_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from picos_diarios_semanal_ont t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_semanal_ont")
insert_reporte_semanal_ont = consultas("insert into reporte_semanal_ont(tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediosemana) select pico.tipo,pico.nodo,pico.puerto,pico.etiqueta,pico.direccion,pico.hora,pico.fecha,pico.promedio,pico.pico, promedio.promedio_semana FROM promedio_semanal_ont promedio, picos_semanal_ont pico WHERE pico.tipo = promedio.tipo and pico.nodo = promedio.nodo and pico.puerto = promedio.puerto and pico.direccion = promedio.direccion GROUP BY pico.tipo, pico.nodo, pico.puerto, pico.direccion;","Flujo","Insertando datos en reporte_semanal_ont")
insert_respaldo_semanal_ont = consultas("insert into respaldo_reporte_semanal_ont(tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediosemana) select tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediosemana FROM reporte_semanal_ont;","Flujo","Insertando datos en respaldo_reporte_semanal_ont")

##consultas mensuales##
#PON
insert_promedio_mensual_pon =  consultas("insert into promedio_mensual(id_zabbix,promedio_mes) select id_zabbix, avg(pico) as promedio_mes from picos_diarios_mensual group by id_zabbix;","Flujo","Insertando datos en promedio_mensual")
insert_picos_mensual_pon =  consultas("insert into picos_mensual (id_zabbix, id_tlk ,tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.id_zabbix, t1.id_tlk, t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.id_zabbix order by t2.pico desc) as rn from picos_diarios_mensual t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_mensual")
insert_reporte_mensual_pon =  consultas("insert into reporte_mensual(tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediomes,wf,datos,emp,rbs) select pico.tipo, pico.nodo,pico.puerto,pico.direccion,pico.hora,pico.fecha,pico.promedio,pico.pico, promedio.promedio_mes, tlk.WF, tlk.Datos, tlk.Empresariales, tlk.RBS FROM picos_mensual pico LEFT JOIN promedio_mensual promedio ON pico.id_zabbix = promedio.id_zabbix LEFT JOIN t_resumen_servicios_tlk tlk ON pico.id_tlk = tlk.id_tlk GROUP BY pico.id_zabbix;","Flujo","Insertando datos en reporte_mensual")
insert_respaldo_mensual_pon =  consultas("insert into respaldo_reporte_mensual(tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediomes,wf,datos,emp,rbs) select tipo,nodo,puerto,direccion,hora,fecha,promediohora,pico,promediomes,wf,datos,emp,rbs FROM reporte_mensual;","Flujo","Insertando datos en respaldo_reporte_mensual")
#ONT
insert_promedio_mensual_ont =  consultas("insert into promedio_mensual_ont(tipo,nodo,puerto,direccion,promedio_mes) select tipo,nodo, puerto, direccion, avg(pico) as promedio_mes from picos_diarios_mensual_ont group by tipo, nodo, puerto, direccion;","Flujo","Insertando datos en promedio_mensual_ont")
insert_picos_mensual_ont =  consultas("insert into picos_mensual_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from picos_diarios_mensual_ont t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_mensual_ont")
insert_reporte_mensual_ont =  consultas("insert into reporte_mensual_ont(tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediomes) select pico.tipo, pico.nodo,pico.puerto,pico.etiqueta,pico.direccion,pico.hora,pico.fecha,pico.promedio,pico.pico, promedio.promedio_mes FROM promedio_mensual_ont promedio, picos_mensual_ont pico WHERE pico.tipo = promedio.tipo and pico.nodo = promedio.nodo and pico.puerto = promedio.puerto and pico.direccion = promedio.direccion GROUP BY pico.tipo, pico.nodo, pico.puerto, pico.direccion;","Flujo","Insertando datos en reporte_mensual_ont")
insert_respaldo_mensual_ont =  consultas("insert into respaldo_reporte_mensual_ont(tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediomes) select tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,pico,promediomes FROM reporte_mensual_ont;","Flujo","Insertando datos en respaldo_reporte_mensual_ont")

###Truncates###
##Truncates semanales##
#PON
truncate_picos_diarios_semanal_pon = consultas('TRUNCATE picos_diarios_semanal;',"Truncate","Truncando datos en picos_diarios_semanal")
truncate_promedio_semanal_pon = consultas('TRUNCATE promedio_semanal;',"Truncate","Truncando datos en promedio_semanal")
truncate_picos_semanal_pon = consultas('TRUNCATE picos_semanal;',"Truncate","Truncando datos en picos_semanal")
truncate_reporte_semanal_pon = consultas('TRUNCATE reporte_semanal;',"Truncate","Truncando datos en reporte_semanal")
truncate_respaldo_semanal_pon = consultas('TRUNCATE respaldo_reporte_semanal;',"Truncate","Truncando datos en respaldo_reporte_semanal")
#ONT
truncate_picos_diarios_semanal_ont = consultas('TRUNCATE picos_diarios_semanal_ont;',"Truncate","Truncando datos en picos_diarios_semanal_ont")
truncate_promedio_semanal_ont = consultas('TRUNCATE promedio_semanal_ont;',"Truncate","Truncando datos en promedio_semanal_ont")
truncate_picos_semanal_ont = consultas('TRUNCATE picos_semanal_ont;',"Truncate","Truncando datos en picos_semanal_ont")
truncate_reporte_semanal_ont = consultas('TRUNCATE reporte_semanal_ont;',"Truncate","Truncando datos en reporte_semanal_ont")
truncate_respaldo_semanal_ont = consultas('TRUNCATE respaldo_reporte_semanal_ont;',"Truncate","Truncando datos en respaldo_reporte_semanal_ont")

##Truncates mensuales##
#PON
truncate_picos_diarios_mensual_pon = consultas('TRUNCATE picos_diarios_mensual;',"Truncate","Truncando datos en picos_diarios_mensual")
truncate_promedio_mensual_pon = consultas('TRUNCATE promedio_mensual;',"Truncate","Truncando datos en promedio_mensual")
truncate_picos_mensual_pon = consultas('TRUNCATE picos_mensual;',"Truncate","Truncando datos en picos_mensual")
truncate_reporte_mensual_pon = consultas('TRUNCATE reporte_mensual;',"Truncate","Truncando datos en reporte_mensual")
truncate_respaldo_mensual_pon = consultas('TRUNCATE respaldo_reporte_mensual;',"Truncate","Truncando datos en respaldo_reporte_mensual")
#ONT
truncate_picos_diarios_mensual_ont = consultas('TRUNCATE picos_diarios_mensual_ont;',"Truncate","Truncando datos en picos_diarios_mensual_ont")
truncate_promedio_mensual_ont = consultas('TRUNCATE promedio_mensual_ont;',"Truncate","Truncando datos en promedio_mensual_ont")
truncate_picos_mensual_ont = consultas('TRUNCATE picos_mensual_ont;',"Truncate","Truncando datos en picos_mensual_ont")
truncate_reporte_mensual_ont = consultas('TRUNCATE reporte_mensual_ont;',"Truncate","Truncando datos en reporte_mensual_ont")
truncate_respaldo_mensual_ont = consultas('TRUNCATE respaldo_reporte_mensual_ont;',"Truncate","Truncando datos en respaldo_reporte_mensual_ont")

##Flujos##
#Diario
flujo_diario = [insert_picos_diarios_semanal_pon,insert_picos_diarios_mensual_pon,insert_picos_diarios_semanal_ont,insert_picos_diarios_mensual_ont]
#Semanales
flujo_semanal_pon = [truncate_promedio_semanal_pon,truncate_picos_semanal_pon,truncate_reporte_semanal_pon,insert_promedio_semanal_pon,insert_picos_semanal_pon,insert_reporte_semanal_pon,insert_respaldo_semanal_pon,truncate_picos_diarios_semanal_pon]
flujo_semanal_ont = [truncate_promedio_semanal_ont,truncate_picos_semanal_ont,truncate_reporte_semanal_ont,insert_promedio_semanal_ont,insert_picos_semanal_ont,insert_reporte_semanal_ont,insert_respaldo_semanal_ont,truncate_picos_diarios_semanal_ont]
flujo_semanal = [flujo_semanal_pon,flujo_semanal_ont]
#Mensuales
flujo_mensual_pon = [truncate_promedio_mensual_pon,truncate_picos_mensual_pon,truncate_reporte_mensual_pon,insert_promedio_mensual_pon,insert_picos_mensual_pon,insert_reporte_mensual_pon,insert_respaldo_mensual_pon,truncate_picos_diarios_mensual_pon]
flujo_mensual_ont = [truncate_promedio_mensual_ont,truncate_picos_mensual_ont,truncate_reporte_mensual_ont,insert_promedio_mensual_ont,insert_picos_mensual_ont,insert_reporte_mensual_ont,insert_respaldo_mensual_ont,truncate_picos_diarios_mensual_ont]
flujo_mensual = [flujo_mensual_pon,flujo_mensual_ont]
#truncar respaldos
flujo_trunca_respaldos_semanales = [truncate_respaldo_semanal_pon,truncate_respaldo_semanal_ont]
flujo_trunca_respaldos_mensuales = [truncate_respaldo_mensual_pon,truncate_respaldo_mensual_ont]

#####Reporte Zabbix#####
sql_ont_semanal = "SELECT * FROM reporte_semanal_ont order by pico DESC"
sql_ont_mensual = "SELECT * FROM reporte_mensual_ont order by pico DESC"
sql_pon_semanal = "SELECT * FROM reporte_semanal order by pico DESC"
sql_pon_mensual = "SELECT * FROM reporte_mensual order by pico DESC"