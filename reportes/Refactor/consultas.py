#!/usr/bin/python

#pusheo zabbix
sql_truncate_cdiarios_PON = 'TRUNCATE crudos_diarios;'
sql_truncate_cdiarios_ONT = 'TRUNCATE crudos_diarios_ont;'
sql_push_diarios_ONT = "INSERT INTO `crudos_diarios_ont` (`tipo`,`nodo`, `puerto`, `direccion`, `etiqueta`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
sql_push_diarios_PON = "INSERT INTO `crudos_diarios` (`id_zabbix`,`id_tlk`,`tipo`,`nodo`, `puerto`, `direccion`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


#Reporte Zabbix
sql_ont_semanal = "SELECT * FROM reporte_semanal_ont order by pico DESC"
sql_ont_mensual = "SELECT * FROM reporte_mensual_ont order by pico DESC"
sql_pon_semanal = "SELECT * FROM reporte_semanal order by pico DESC"
sql_pon_mensual = "SELECT * FROM reporte_mensual order by pico DESC"