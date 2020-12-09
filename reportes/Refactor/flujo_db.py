import logger
import consultas

from conector import conector


def flujo_diario():
    logger.info("Comienza el flujo diario de la BD")
    #PON
    conector(consultas.sql_insert_picos_diarios_semanal_pon,"Flujo","Insertando datos en picos_diarios_semanal")
    conector(consultas.sql_insert_picos_diarios_mensual_pon,"Flujo","Insertando datos en picos_diarios_mensual")
    #ONT
    conector(consultas.sql_insert_picos_diarios_semanal_ont,"Flujo","Insertando datos en picos_diarios_semanal_ont")
    conector(consultas.sql_insert_picos_diarios_mensual_ont,"Flujo","Insertando datos en picos_diarios_mensual_ont")

    logger.info("Finalizo el flujo diario de la BD")


def flujo_semanal():
    logger.info("Comienza el flujo semanal de la BD")
    ##PON
    #Truncate_1
    conector(consultas.sql_truncate_promedio_semanal_pon,"Truncate","Truncando datos en promedio_semanal")
    conector(consultas.sql_truncate_picos_semanal_pon,"Truncate","Truncando datos en picos_semanal")
    conector(consultas.sql_truncate_reporte_semanal_pon,"Truncate","Truncando datos en reporte_semana")
    conector(consultas.sql_truncate_respaldo_semanal_pon,"Truncate","Truncando datos en respaldo_semanal")
    #Flujo
    conector(consultas.sql_insert_promedio_semanal_pon,"Flujo","Insertando datos en promedio_semanal")
    conector(consultas.sql_insert_picos_semanal_pon,"Flujo","Insertando datos en picos_semanal")
    conector(consultas.sql_insert_reporte_semanal_pon,"Flujo","Insertando datos en reporte_semanal")
    conector(consultas.sql_insert_respaldo_semanal_pon,"Flujo","Insertando datos en respaldo_semanal")
    #Truncate_2
    conector(consultas.sql_truncate_picos_diarios_semanal_pon,"Truncate","Truncando datos en diarios_semanal")

    ##ONT
    #Truncate_1
    conector(consultas.sql_truncate_promedio_semanal_ont,"Truncate","Truncando datos en promedio_semanal_ont")
    conector(consultas.sql_truncate_picos_semanal_ont,"Truncate","Truncando datos en picos_semanal_ont")
    conector(consultas.sql_truncate_reporte_semanal_ont,"Truncate","Truncando datos en reporte_semanal_ont")
    conector(consultas.sql_truncate_respaldo_semanal_ont,"Truncate","Truncando datos en respaldo_semanal_ont")
    #Flujo
    conector(consultas.sql_insert_promedio_semanal_ont,"Flujo","Insertando datos en promedio_semanal_ont")
    conector(consultas.sql_insert_picos_semanal_ont,"Flujo","Insertando datos en picos_semanal_ont")
    conector(consultas.sql_insert_reporte_semanal_ont,"Flujo","Insertando datos en reporte_semanal_ont")
    conector(consultas.sql_insert_respaldo_semanal_ont,"Flujo","Insertando datos en respaldo_semanal_ont")
    #Truncate_2
    conector(consultas.sql_truncate_picos_diarios_semanal_ont,"Truncate","Truncando datos en diarios_semanal_ont")
    logger.info("Finalizo el flujo semanal de la BD")


def flujo_mensual():
    logger.info("Comienza el flujo mensual de la BD")
    ##PON
    #Truncate_1
    
    conector(consultas.sql_truncate_promedio_mensual_pon,"Truncate","")
    conector(consultas.sql_truncate_picos_mensual_pon,"Truncate","")
    conector(consultas.sql_truncate_reporte_mensual_pon,"Truncate","")
    conector(consultas.sql_truncate_respaldo_mensual_pon,"Truncate","")
    #Flujo
    conector(consultas.sql_insert_promedio_mensual_pon,"Flujo","")
    conector(consultas.sql_insert_picos_mensual_pon,"Flujo","")
    conector(consultas.sql_insert_reporte_mensual_pon,"Flujo","")
    conector(consultas.sql_insert_respaldo_mensual_pon,"Flujo","")
    #Truncate_2
    conector(consultas.sql_truncate_picos_diarios_mensual_pon,"Truncate","Truncando datos en picos_diarios_mensual")

    ##ONT
    #Truncate_1
    conector(consultas.sql_truncate_promedio_mensual_ont,"Truncate","")
    conector(consultas.sql_truncate_picos_mensual_ont,"Truncate","")
    conector(consultas.sql_truncate_reporte_mensual_ont,"Truncate","")
    conector(consultas.sql_truncate_respaldo_mensual_ont,"Truncate","")
    #Flujo
    conector(consultas.sql_insert_promedio_mensual_ont,"Flujo","")
    conector(consultas.sql_insert_picos_mensual_ont,"Flujo","")
    conector(consultas.sql_insert_reporte_mensual_ont,"Flujo","")
    conector(consultas.sql_insert_respaldo_mensual_ont,"Flujo","")
    #Truncate_2
    conector(consultas.sql_truncate_picos_diarios_mensual_ont,"Truncate","Truncando datos en picos_diarios_mensual_ont")
    logger.info("Finalizo el flujo mensual de la BD")

