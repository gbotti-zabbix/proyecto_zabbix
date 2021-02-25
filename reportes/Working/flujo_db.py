import logger
from consultas import flujo_diario, flujo_mensual, flujo_semanal, flujo_delete_respaldos_semanales, flujo_delete_respaldos_mensuales

from conector import conector

""" Recorre flujos y llama a conector

Este script se encarga de pasar los flujos definidos en consultas a conector, para truncar,
cargar o seleccionar los datos pertinentes a los reportes.

De esta forma podemos dividir de forma comoda todas las acciones en la BD que se requieren para los reportes
semanales, mensuales y por tecnologias de ONT, PON.

Desde este modulo tambien se pasan los flujos encargados de borrar respaldos viejos.

Para cambiar el orden en que se hacen las consultas, debe modificarse las variables importadas desde consultas.

Contiene la funcion flujos.
"""

def flujos(periodo):
    """ Recorre lista de flujos, las pasa a conector y logea el inicio/final de las tareas

    :param periodo: Periodo del flujo que se desea recorrer. "dia" hace seleccion de picos/promedios picos diarios.
    "semana" ejecuta todos los flujos correspondiente al reporte semanal.
    "mes" ejecuta todos los flujos correspondiente al reporte mensual.
    :type: str

    :returns: esta funcion no tiene retornos.
    """

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