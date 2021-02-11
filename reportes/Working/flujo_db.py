import logger
from consultas import flujo_diario, flujo_mensual, flujo_semanal, flujo_delete_respaldos_semanales, flujo_delete_respaldos_mensuales

from conector import conector

def flujos(periodo):
    if periodo == "dia":
        logger.info("Comienza el flujo diario de la BD")
        for consulta in flujo_diario:
            conector(consulta.query,consulta.tipo,consulta.mensaje)
        logger.info("Finalizo el flujo diario de la BD")

    elif periodo == "semana":
        logger.info("Comienza el flujo semanal de la BD")
        #carga de datos
        for lista in flujo_semanal:
            for consulta in lista:
                conector(consulta.query,consulta.tipo,consulta.mensaje)
        #limpeiza de respaldos
        for consulta in flujo_delete_respaldos_semanales:
            conector(consulta.query,consulta.tipo,consulta.mensaje)
        logger.info("Finalizo el flujo semanal de la BD")

    elif periodo == "mes":
        logger.info("Comienza el flujo mensual de la BD")
        #carga de datos
        for lista in flujo_mensual:
            for consulta in lista:
                conector(consulta.query,consulta.tipo,consulta.mensaje)
        #limpieza de respaldos
        for consulta in flujo_delete_respaldos_mensuales:
            conector(consulta.query,consulta.tipo,consulta.mensaje)
        logger.info("Finalizo el flujo mensual de la BD")