#!/usr/bin/python
""" Direcciones de archivos o datos hardcodeados utilizados para consultas a la API de Zabbix.

El archivo cuenta con direcciones de directorios donde guardar achivos especificos o url de sitios 
donde realizar request HTTP por los script de carga de ONTs.
"""

#Archivo de logeo para logger
file_log = "/var/log/carga_ont/ont.log"

#URL de la Zabbix API en produccion, con IP interna del DC
url = "http://10.0.0.101/zabbix/api_jsonrpc.php"