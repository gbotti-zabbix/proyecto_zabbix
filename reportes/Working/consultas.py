#!/usr/bin/python
""" Contiene todas las consultas que son necesarias para cargar los crudos y generar los reportes

La gran mayoria son strings con la consulta especifica. Para los flujos creamos objetos llamados consultas.
El constructor de estos objetos usa la query, que tipo de query es y el mensaje a pasar a conector.

Todas las variables de este archivo deberian funcionar con el modulo conector.

Si se quiere apuntar a otra BD cambiar host_DB, user_DB, password_DB y database_DB en direcciones (o importar variables sesde otro modulo).

Contiene la clase consultas.
"""
######pusheo zabbix#####
"""Consultas pertinentes al ingreso diario de crudos desde zabbix hacia la BD

Los sql_truncate borran los datos del dia anterior mientras los sql_push insertan
los datos parseados del dia de PON y ONT.
"""
sql_truncate_cdiarios_PON = 'TRUNCATE crudos_diarios;'
sql_truncate_cdiarios_ONT = 'TRUNCATE crudos_diarios_ont;'
sql_push_diarios_ONT = "INSERT INTO `crudos_diarios_ont` (`tipo`,`nodo`, `puerto`, `direccion`, `etiqueta`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
sql_push_diarios_PON = "INSERT INTO `crudos_diarios` (`id_zabbix`,`id_tlk`,`tipo`,`nodo`, `puerto`, `direccion`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


#####flujo DB#####
###Consultas###
class consultas():
    """ Clase que define una cosulta en el formato esperado por el modulo conector.

    Solo cuenta con un constructor.
    """
    def __init__(self,query,tipo,mensaje):
        """
        :param query: Query sql a ejecutar, por lo general es una viarable con la query como string.
        :type query: str

        :param tipo: Parametros de conector a pasar, "many", "select" o vacio. Many conlleva pasar una lista como *arg.
        :type tipo: str

        :param mensaje: Mensaje a logear por conector.
        :type mensaje: str

        :returns: esta clase no tiene retornos.
        """
        self.query = query
        self.tipo = tipo
        self.mensaje = mensaje

##consultas diarias##
"""Consultas para sacar maximos del dia.

Los insert_picos_diarios insertan en tablas, por cada puerto, el pico maximo del dia junto con otros datos.
Esto se hace para tablas utilizadas para reportes mensuales y semanales, por PON y ONT.
"""
#PON
insert_picos_diarios_semanal_pon = consultas("insert into picos_diarios_semanal (id_zabbix, id_tlk, tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.id_zabbix, t1.id_tlk, t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.id_zabbix order by t2.pico desc) as rn from crudos_diarios t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_diarios_semanal")
insert_picos_diarios_mensual_pon = consultas("insert into picos_diarios_mensual (id_zabbix, id_tlk, tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.id_zabbix, t1.id_tlk, t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.id_zabbix order by t2.pico desc) as rn from crudos_diarios t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_diarios_mensual")
insert_picos_diarios_hora_semanal_pon = consultas("insert into picos_diarios_promedio_semanal (id_zabbix, fecha, promedio) select t1.id_zabbix, t1.fecha, t1.promedio from ( select t2.*, row_number() over (partition by t2.id_zabbix order by t2.promedio desc) as rn from crudos_diarios t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_diarios_promedio_semanal")
insert_picos_diarios_hora_mensual_pon = consultas("insert into picos_diarios_promedio_mensual (id_zabbix, fecha, promedio) select t1.id_zabbix, t1.fecha, t1.promedio from ( select t2.*, row_number() over (partition by t2.id_zabbix order by t2.promedio desc) as rn from crudos_diarios t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_diarios_promedio_mensual")

#ONT
insert_picos_diarios_semanal_ont = consultas("insert into picos_diarios_semanal_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from crudos_diarios_ont t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_diarios_semanal_ont")
insert_picos_diarios_mensual_ont = consultas("insert into picos_diarios_mensual_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from crudos_diarios_ont t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_diarios_mensual_ont")
insert_picos_diarios_hora_semanal_ont = consultas("insert into picos_diarios_promedio_semanal_ont (tipo, nodo, puerto, direccion, fecha, promedio) select t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.fecha, t1.promedio from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.promedio desc) as rn from crudos_diarios_ont t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_diarios_promedio_semanal_ont")
insert_picos_diarios_hora_mensual_ont = consultas("insert into picos_diarios_promedio_mensual_ont (tipo, nodo, puerto, direccion, fecha, promedio) select t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.fecha, t1.promedio from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.promedio desc) as rn from crudos_diarios_ont t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_diarios_promedio_mensual_ont")

##consultas semanales##
"""Consultas para sacar maximos de la semana.

Los insert_picos_semanal insertan en tablas, por cada puerto, el pico maximo del la semana junto con otros datos.
Los insert_promedio insertan en tablas, por cada puerto, el promedio de los picos maximos de toda la semana tomando el valor maximo por dia.
Los insert_promedio_hora hacen algo parecido a insert_promedio, pero en ves de usar los picos, usan los valores de horas promediadas mas altos por dia
de toda la semana.
Los insert_reporte insertan todos los datos que seran mostrados en el reporte semanal.
Los insert_respaldo copian 1 a 1 la tabla de reportes para generar un respaldo.
Esto se hace para tablas utilizadas para reportes semanales, por PON y ONT.
"""
#PON
insert_promedio_semanal_pon = consultas("insert into promedio_semanal(id_zabbix,promedio_semana) select id_zabbix, avg(pico) as promedio_semana from picos_diarios_semanal group by id_zabbix;","Flujo","Insertando datos en promedio_semanal")
insert_picos_semanal_pon = consultas("insert into picos_semanal (id_zabbix, id_tlk ,tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.id_zabbix, t1.id_tlk, t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.id_zabbix order by t2.pico desc) as rn from picos_diarios_semanal t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_semanal")
insert_promedio_hora_semanal_pon = consultas("insert into promedio_picos_promedio_semanal (id_zabbix,promedio_picos_promedio_semana) select id_zabbix, avg(promedio) as promedio_picos_promedio_semana from picos_diarios_promedio_semanal group by id_zabbix;","Flujo","Insertando datos en promedio_picos_promedio_semanal")
insert_reporte_semanal_pon = consultas("insert into reporte_semanal(tipo,nodo,puerto,direccion,hora,fecha,promediohora,promediosemana,pico,promedio_picos_promedios,wf,datos,emp,rbs) select pico.tipo, pico.nodo,pico.puerto,pico.direccion,pico.hora,pico.fecha,pico.promedio, promedio.promedio_semana, pico.pico, p_promedio.promedio_picos_promedio_semana, tlk.WF, tlk.Datos, tlk.Empresariales, tlk.RBS FROM picos_semanal pico LEFT JOIN promedio_semanal promedio ON pico.id_zabbix = promedio.id_zabbix LEFT JOIN promedio_picos_promedio_semanal p_promedio on pico.id_zabbix = p_promedio.id_zabbix LEFT JOIN t_resumen_servicios_tlk tlk ON pico.id_tlk = tlk.id_tlk GROUP BY pico.id_zabbix;","Flujo","Insertando datos en reporte_semanal")
insert_respaldo_semanal_pon = consultas("insert into respaldo_reporte_semanal(tipo,nodo,puerto,direccion,hora,fecha,promediohora,promediosemana,pico,promedio_picos_promedios,wf,datos,emp,rbs) select tipo,nodo,puerto,direccion,hora,fecha,promediohora,promediosemana,pico,promedio_picos_promedios,wf,datos,emp,rbs FROM reporte_semanal;","Flujo","Insertando datos en respaldo_reporte_semanal")
#ONT
insert_promedio_semanal_ont = consultas("insert into promedio_semanal_ont(tipo,nodo,puerto,direccion,promedio_semana) select tipo,nodo, puerto, direccion, avg(pico) as promedio_semana from picos_diarios_semanal_ont group by tipo, nodo, puerto, direccion;","Flujo","Insertando datos en promedio_semanal_ont")
insert_picos_semanal_ont = consultas("insert into picos_semanal_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from picos_diarios_semanal_ont t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_semanal_ont")
insert_promedio_hora_semanal_ont = consultas("insert into promedio_picos_promedio_semanal_ont(tipo,nodo,puerto,direccion,promedio_picos_promedio_semana) select tipo,nodo, puerto, direccion, avg(promedio) as promedio_picos_promedio_semana from picos_diarios_promedio_semanal_ont group by tipo, nodo, puerto, direccion;","Flujo","Insertando datos en promedio_picos_promedio_mensual")
insert_reporte_semanal_ont = consultas("insert into reporte_semanal_ont(tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,promediosemana,pico,promedio_picos_promedios) select pico.tipo,pico.nodo,pico.puerto,pico.etiqueta,pico.direccion,pico.hora,pico.fecha,pico.promedio, promedio.promedio_semana, pico.pico, p_promedio.promedio_picos_promedio_semana FROM promedio_semanal_ont promedio, picos_semanal_ont pico, promedio_picos_promedio_semanal_ont p_promedio WHERE pico.tipo = promedio.tipo and pico.nodo = promedio.nodo and pico.puerto = promedio.puerto and pico.direccion = promedio.direccion and pico.tipo = p_promedio.tipo and pico.nodo = p_promedio.nodo and pico.puerto = p_promedio.puerto and pico.direccion = p_promedio.direccion GROUP BY pico.tipo, pico.nodo, pico.puerto, pico.direccion;","Flujo","Insertando datos en reporte_semanal_ont")
insert_respaldo_semanal_ont = consultas("insert into respaldo_reporte_semanal_ont(tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,promediosemana,pico,promedio_picos_promedios) select tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,promediosemana,pico, promedio_picos_promedios FROM reporte_semanal_ont;","Flujo","Insertando datos en respaldo_reporte_semanal_ont")

##consultas mensuales##
"""Consultas para sacar maximos del mes.

Los insert_picos_mensual insertan en tablas, por cada puerto, el pico maximo del mes junto con otros datos.
Los insert_promedio insertan en tablas, por cada puerto, el promedio de los picos maximos de todo el mes tomando el valor maximo por dia.
Los insert_promedio_hora hacen algo parecido a insert_promedio, pero en ves de usar los picos, usan los valores de horas promediadas mas altos por dia
de todo el mes.
Los insert_reporte insertan todos los datos que seran mostrados en el reporte mensual
Los insert_respaldo copian 1 a 1 la tabla de reportes para generar un respaldo.
Esto se hace para tablas utilizadas para reportes mensuales, por PON y ONT.
"""
#PON
insert_promedio_mensual_pon =  consultas("insert into promedio_mensual(id_zabbix,promedio_mes) select id_zabbix, avg(pico) as promedio_mes from picos_diarios_mensual group by id_zabbix;","Flujo","Insertando datos en promedio_mensual")
insert_picos_mensual_pon =  consultas("insert into picos_mensual (id_zabbix, id_tlk ,tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.id_zabbix, t1.id_tlk, t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.id_zabbix order by t2.pico desc) as rn from picos_diarios_mensual t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_mensual")
insert_promedio_hora_mensual_pon = consultas("insert into promedio_picos_promedio_mensual (id_zabbix,promedio_picos_promedio_mes) select id_zabbix, avg(promedio) as promedio_picos_promedio_mes from picos_diarios_promedio_mensual group by id_zabbix;","Flujo","Insertando datos en promedio_picos_promedio_mensual")
insert_reporte_mensual_pon =  consultas("insert into reporte_mensual(tipo,nodo,puerto,direccion,hora,fecha,promediohora,promediomes,pico,promedio_picos_promedios,wf,datos,emp,rbs) select pico.tipo, pico.nodo,pico.puerto,pico.direccion,pico.hora,pico.fecha,pico.promedio, promedio.promedio_mes, pico.pico, p_promedio.promedio_picos_promedio_mes, tlk.WF, tlk.Datos, tlk.Empresariales, tlk.RBS FROM picos_mensual pico LEFT JOIN promedio_mensual promedio ON pico.id_zabbix = promedio.id_zabbix LEFT JOIN promedio_picos_promedio_mensual p_promedio on pico.id_zabbix = p_promedio.id_zabbix LEFT JOIN t_resumen_servicios_tlk tlk ON pico.id_tlk = tlk.id_tlk GROUP BY pico.id_zabbix;","Flujo","Insertando datos en reporte_mensual")
insert_respaldo_mensual_pon =  consultas("insert into respaldo_reporte_mensual(tipo,nodo,puerto,direccion,hora,fecha,promediohora,promediomes,pico,promedio_picos_promedios,wf,datos,emp,rbs) select tipo,nodo,puerto,direccion,hora,fecha,promediohora,promediomes,pico,promedio_picos_promedios,wf,datos,emp,rbs FROM reporte_mensual;","Flujo","Insertando datos en respaldo_reporte_mensual")
#ONT
insert_promedio_mensual_ont =  consultas("insert into promedio_mensual_ont(tipo,nodo,puerto,direccion,promedio_mes) select tipo,nodo, puerto, direccion, avg(pico) as promedio_mes from picos_diarios_mensual_ont group by tipo, nodo, puerto, direccion;","Flujo","Insertando datos en promedio_mensual_ont")
insert_picos_mensual_ont =  consultas("insert into picos_mensual_ont (tipo, nodo, puerto, etiqueta, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.etiqueta, t1.direccion, t1.hora, t1.fecha, t1.promedio, t1.pico from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from picos_diarios_mensual_ont t2) t1 where t1.rn =1;","Flujo","Insertando datos en picos_mensual_ont")
insert_promedio_hora_mensual_ont = consultas("insert into promedio_picos_promedio_mensual_ont(tipo,nodo,puerto,direccion,promedio_picos_promedio_mes) select tipo,nodo, puerto, direccion, avg(promedio) as promedio_picos_promedio_mes from picos_diarios_promedio_mensual_ont group by tipo, nodo, puerto, direccion;","Flujo","Insertando datos en promedio_picos_promedio_mensual_ont")
insert_reporte_mensual_ont =  consultas("insert into reporte_mensual_ont(tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,promediomes,pico,promedio_picos_promedios) select pico.tipo,pico.nodo,pico.puerto,pico.etiqueta,pico.direccion,pico.hora,pico.fecha,pico.promedio, promedio.promedio_mes, pico.pico, p_promedio.promedio_picos_promedio_mes FROM promedio_mensual_ont promedio, picos_mensual_ont pico, promedio_picos_promedio_mensual_ont p_promedio WHERE pico.tipo = promedio.tipo and pico.nodo = promedio.nodo and pico.puerto = promedio.puerto and pico.direccion = promedio.direccion and pico.tipo = p_promedio.tipo and pico.nodo = p_promedio.nodo and pico.puerto = p_promedio.puerto and pico.direccion = p_promedio.direccion GROUP BY pico.tipo, pico.nodo, pico.puerto, pico.direccion;","Flujo","Insertando datos en reporte_mensual_ont")
insert_respaldo_mensual_ont =  consultas("insert into respaldo_reporte_mensual_ont(tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,promediomes,pico,promedio_picos_promedios) select tipo,nodo,puerto,etiqueta,direccion,hora,fecha,promediohora,promediomes,pico, promedio_picos_promedios FROM reporte_mensual_ont;","Flujo","Insertando datos en respaldo_reporte_mensual_ont")

###Truncates###
##Truncates semanales##
""" Truncates de necesarios para generar el reporte semanal

Para cada tabla de la seccion de consultas mensuales, existe un truncate.
"""
#PON
truncate_picos_diarios_semanal_pon = consultas('TRUNCATE picos_diarios_semanal;',"Truncate","Truncando datos en picos_diarios_semanal")
truncate_picos_diarios_promedio_semanal_pon = consultas('TRUNCATE picos_diarios_promedio_semanal;',"Truncate","Truncando datos en picos_diarios_promedio_semanal")
truncate_promedio_semanal_pon = consultas('TRUNCATE promedio_semanal;',"Truncate","Truncando datos en promedio_semanal")
truncate_picos_semanal_pon = consultas('TRUNCATE picos_semanal;',"Truncate","Truncando datos en picos_semanal")
truncate_promedio_picos_promedio_semanal_pon = consultas('TRUNCATE promedio_picos_promedio_semanal;',"Truncate","Truncando datos en promedio_picos_promedio_semanal")
truncate_reporte_semanal_pon = consultas('TRUNCATE reporte_semanal;',"Truncate","Truncando datos en reporte_semanal")
#ONT
truncate_picos_diarios_semanal_ont = consultas('TRUNCATE picos_diarios_semanal_ont;',"Truncate","Truncando datos en picos_diarios_semanal_ont")
truncate_picos_diarios_promedio_semanal_ont = consultas('TRUNCATE picos_diarios_promedio_semanal_ont;',"Truncate","Truncando datos en picos_diarios_promedio_semanal_ont")
truncate_promedio_semanal_ont = consultas('TRUNCATE promedio_semanal_ont;',"Truncate","Truncando datos en promedio_semanal_ont")
truncate_picos_semanal_ont = consultas('TRUNCATE picos_semanal_ont;',"Truncate","Truncando datos en picos_semanal_ont")
truncate_promedio_picos_promedio_semanal_ont = consultas('TRUNCATE promedio_picos_promedio_semanal_ont;',"Truncate","Truncando datos en promedio_picos_promedio_semanal_ont")
truncate_reporte_semanal_ont = consultas('TRUNCATE reporte_semanal_ont;',"Truncate","Truncando datos en reporte_semanal_ont")

##Truncates mensuales##
""" Truncates de necesarios para generar el reporte mensual

Para cada tabla de la seccion de consultas mensuales, existe un truncate.
"""
#PON
truncate_picos_diarios_mensual_pon = consultas('TRUNCATE picos_diarios_mensual;',"Truncate","Truncando datos en picos_diarios_mensual")
truncate_picos_diarios_promedio_mensual_pon = consultas('TRUNCATE picos_diarios_promedio_mensual;',"Truncate","Truncando datos en picos_diarios_promedio_mensual")
truncate_promedio_mensual_pon = consultas('TRUNCATE promedio_mensual;',"Truncate","Truncando datos en promedio_mensual")
truncate_picos_mensual_pon = consultas('TRUNCATE picos_mensual;',"Truncate","Truncando datos en picos_mensual")
truncate_promedio_picos_promedio_mensual_pon = consultas('TRUNCATE promedio_picos_promedio_mensual;',"Truncate","Truncando datos en promedio_picos_promedio_mensual")
truncate_reporte_mensual_pon = consultas('TRUNCATE reporte_mensual;',"Truncate","Truncando datos en reporte_mensual")
#ONT
truncate_picos_diarios_mensual_ont = consultas('TRUNCATE picos_diarios_mensual_ont;',"Truncate","Truncando datos en picos_diarios_mensual_ont")
truncate_picos_diarios_promedio_mensual_ont = consultas('TRUNCATE picos_diarios_promedio_mensual_ont;',"Truncate","Truncando datos en picos_diarios_promedio_mensual_ont")
truncate_promedio_mensual_ont = consultas('TRUNCATE promedio_mensual_ont;',"Truncate","Truncando datos en promedio_mensual_ont")
truncate_picos_mensual_ont = consultas('TRUNCATE picos_mensual_ont;',"Truncate","Truncando datos en picos_mensual_ont")
truncate_promedio_picos_promedio_mensual_ont = consultas('TRUNCATE promedio_picos_promedio_mensual_ont;',"Truncate","Truncando datos en promedio_picos_promedio_mensual_ont")
truncate_reporte_mensual_ont = consultas('TRUNCATE reporte_mensual_ont;',"Truncate","Truncando datos en reporte_mensual_ont")

###Deletes-Respaldos###
""" Deletes utilizados para borra datos respaldados viejos.

Para todas las tablas donde guardamos los respaldos de las tablas finales de reportes, 
se pasa un delete que borra los datos con mas de 60 o 180 dias dependiendo si son reportes 
mensuales o semanales.

Esto se hace tanto para reportes de ONT como PON.
"""
#Deletes semanales
delete_respaldo_reporte_semanal_pon = consultas('delete from respaldo_reporte_semanal where fecha < now() - interval 60 DAY;',"Delete","Delete sobre respaldo_reporte_semanal con mas de 60 dias")
delete_respaldo_reporte_semanal_ont = consultas('delete from respaldo_reporte_semanal_ont where fecha < now() - interval 60 DAY;',"Delete","Delete sobre respaldo_reporte_semanal_ont con mas de 60 dias")
#Deletes Mensuales
delete_respaldo_reporte_mensual_pon = consultas('delete from respaldo_reporte_mensual where fecha < now() - interval 180 DAY;',"Delete","Delete sobre respaldo_reporte_mensual con mas de 180 dias")
delete_respaldo_reporte_mensual_ont = consultas('delete from respaldo_reporte_mensual_ont where fecha < now() - interval 180 DAY;',"Delete","Delete sobre respaldo_reporte_mensual_ont con mas de 180 dias")

##Flujos##
""" Declaracion de los bojetos consultas para coordinar la operacion de las consutlas en la BD.

Se agrupan los objetos en un orden definido por su correspondencia a reportes semanales o mensuales de ONT y PON.
El orden esta marcado sobre que tablas debene borrarse o popularse primero, y cual de esta accion se antepone a la otra.
Al momento de usarse estas listas de objetos, deben recorresrse desde el primer valor (0) al ultimo (-1).

Como ejemplo, al llamarse a flujo_semanal, deberia poder generarse todos los datos necesarios para el reporte semanal,
menos los pusheos de crudos, realizados al principio de este archivo.
"""
#Diario
flujo_diario = [insert_picos_diarios_semanal_pon,insert_picos_diarios_hora_semanal_pon,insert_picos_diarios_mensual_pon,insert_picos_diarios_hora_mensual_pon,insert_picos_diarios_semanal_ont,insert_picos_diarios_hora_semanal_ont,insert_picos_diarios_mensual_ont,insert_picos_diarios_hora_mensual_ont]
#Semanales
flujo_semanal_pon = [truncate_promedio_semanal_pon,truncate_picos_semanal_pon,truncate_promedio_picos_promedio_semanal_pon,truncate_reporte_semanal_pon,insert_promedio_semanal_pon,insert_picos_semanal_pon,insert_promedio_hora_semanal_pon,insert_reporte_semanal_pon,insert_respaldo_semanal_pon,truncate_picos_diarios_semanal_pon,truncate_picos_diarios_promedio_semanal_pon]
flujo_semanal_ont = [truncate_promedio_semanal_ont,truncate_picos_semanal_ont,truncate_promedio_picos_promedio_semanal_ont,truncate_reporte_semanal_ont,insert_promedio_semanal_ont,insert_picos_semanal_ont,insert_promedio_hora_semanal_ont,insert_reporte_semanal_ont,insert_respaldo_semanal_ont,truncate_picos_diarios_semanal_ont,truncate_picos_diarios_promedio_semanal_ont]
flujo_semanal = [flujo_semanal_pon,flujo_semanal_ont]
#Mensuales
flujo_mensual_pon = [truncate_promedio_mensual_pon,truncate_picos_mensual_pon,truncate_promedio_picos_promedio_mensual_pon,truncate_reporte_mensual_pon,insert_promedio_mensual_pon,insert_picos_mensual_pon,insert_promedio_hora_mensual_pon,insert_reporte_mensual_pon,insert_respaldo_mensual_pon,truncate_picos_diarios_mensual_pon,truncate_picos_diarios_promedio_mensual_pon]
flujo_mensual_ont = [truncate_promedio_mensual_ont,truncate_picos_mensual_ont,truncate_promedio_picos_promedio_mensual_ont,truncate_reporte_mensual_ont,insert_promedio_mensual_ont,insert_picos_mensual_ont,insert_promedio_hora_mensual_ont,insert_reporte_mensual_ont,insert_respaldo_mensual_ont,truncate_picos_diarios_mensual_ont,truncate_picos_diarios_promedio_mensual_ont]
flujo_mensual = [flujo_mensual_pon,flujo_mensual_ont]
#delete respaldos
flujo_delete_respaldos_semanales = [delete_respaldo_reporte_semanal_pon,delete_respaldo_reporte_semanal_ont]
flujo_delete_respaldos_mensuales = [delete_respaldo_reporte_mensual_pon,delete_respaldo_reporte_mensual_ont]

#####Reporte Zabbix#####
""" Select pertinentes a la creacion del xlsx de los reportes

Consultas que realiza el modulo reporte para traer los datos a foramtear en los archivos .xlsx.

Estas son pertinentes a reportes mensuales y semanalas de ONTs y PON.
"""
sql_ont_semanal = "SELECT * FROM reporte_semanal_ont order by pico DESC"
sql_ont_mensual = "SELECT * FROM reporte_mensual_ont order by pico DESC"
sql_pon_semanal = "SELECT * FROM reporte_semanal order by pico DESC"
sql_pon_mensual = "SELECT * FROM reporte_mensual order by pico DESC"

#####Auditoria#####
""" Selects utilizados para auditar fechas de datos cargados.

Se extraen fechas de los crudos diarios de PON y ONT para auditar cargas mas recientes.
"""
auditoria_ont = "SELECT `fecha` FROM `crudos_diarios_ont` WHERE `fecha` = '{}' limit 1;"
auditoria_pon = "SELECT `fecha` FROM `crudos_diarios` WHERE `fecha` = '{}' limit 1;"

