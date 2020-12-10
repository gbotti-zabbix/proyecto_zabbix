import logger
from consultas import flujo_diario, flujo_mensual, flujo_semanal

from conector import conector

def flujos(periodo):
    if periodo == "dia":
        logger.info("Comienza el flujo diario de la BD")
        for consulta in flujo_diario:
            conector(consulta.query,consulta.tipo,consulta.mensaje)
        logger.info("Finalizo el flujo diario de la BD")

    elif periodo == "semana":
        logger.info("Comienza el flujo semanal de la BD")
        for lista in flujo_semanal:
            for consulta in lista:
                conector(consulta.query,consulta.tipo,consulta.mensaje)
        logger.info("Finalizo el flujo semanal de la BD")

    elif periodo == "mes":
        logger.info("Comienza el flujo mensual de la BD")
        for lista in flujo_mensual:
            for consulta in lista:
                conector(consulta.query,consulta.tipo,consulta.mensaje)
        logger.info("Finalizo el flujo mensual de la BD")

