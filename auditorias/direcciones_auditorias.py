"""Direcciones de archivos o datos hardcodeados utilizados para los scripts de auditorias.

El archivo cuenta con direcciones de directorios donde guardar achivos especificos y
algunos datos utilizados para filtros de puertos y/o nodos.
"""

#**Archivos de Auditoria**  
""" Directorios donde se guardan archivos de auditorias por tecnologia.
"""
auditoria_ont = "/var/lib/reportes-zabbix/auditorias/auditoria_ont.txt"

auditoria_pon = "/var/lib/reportes-zabbix/auditorias/auditoria_pon.txt"

#**Filtros de puertos uplink y nodos de 19 pulgadas**  
""" Datos para filtros en las comparaciones de puertos

**c300_19p**: Lista de nodos C300 de 19 pulgadas.

Las variables *puertos_uplik* definen los numeros de los puertos mencioandos por vendor o formato
(H por Huawei, 19 por C300 de 19 pulgadas).
"""

c300_19p = ["G-AZNAREZ-01Z", "MARISCALA-01Z", "A-ARENA-01Z"]

puertos_uplink = ["21/1","22/1","21/2","21/3","21/4","22/2","22/3","22/4"]

puertos_uplink_h = ["9/0","10/0"]

puertos_uplink_19 = ["19/1","20/1","19/2","19/3","19/4","20/2","20/3","20/4"]