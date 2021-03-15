#IMPORTO EL CONECTOR Y LOGGER DE REFACTOR
import sys
sys.path.append("./reportes/Working")
from conector import conector

""" ### Contiene todas las consultas que son necesarias para comaprar inventarios a auditar

Las funciones llaman a conector() junto con un mensaje especifico y la consulta SELECT.

Todas las variables de este archivo deberian funcionar con el modulo conector. Este modulo es el 
mismo utilizado para los reportes PON y ONT. Por esto es enecesario el append inicial del directorio 
reportes/Working al sys path.

Si se quiere apuntar a otra BD cambiar host_DB, user_DB, password_DB y database_DB en direcciones 
(o importar variables sesde otro modulo).

Contiene las funciones:

    * **get_rbs**: Trae todas las radiobases en ONT registradas en gestion.
    * **get_rbs_tlk**: Trae todas las radiobases en ONT registradas en Telelink.
    * **get_puertos_pon_tlk**: Trae todos los puertos PON registrados en Telelink.
    * **get_puertos_pon_zbx**: Trae todos los puertos PON y Uplink monitoreados por zabbix.
"""

def get_rbs():
    """**SELECT de ONTs con RBS en gestion**

    Selecciona nombre de nodo, etiqueta de gesition, slot/puerto/ont del inventario de gestion.
    Devuelve el resultado en una lista de tuplas.

    * **returns**: Lista de tuplas con resultados del select.
    * **rtype**: list
    """
    sql = "SELECT `nodo`,`etiqueta_ont`,`slot`,`puerto`,`ont` FROM `t_servicios_RBS`"
    rbs = conector(sql,"select","Consultando ONTS")
    return rbs

def get_rbs_tlk():
    """**SELECT de ONTs con RBS en TLK.**

    Selecciona nombre de nodo/slot/puerto y numero de ONT del inventario de TLK.
    Devuelve el resultado en una lista de tuplas.

    * **returns**: Lista de tuplas con resultados del select.
    * **rtype**: list
    """
    sql ="SELECT `id_tlk`, `nro_ont` FROM `t_reporte_puertos_telelink` WHERE `rbs_ont_tlk` > 0"
    rbs = conector(sql,"select","Consultando ONTS de TLK")
    return rbs

def get_puertos_pon_tlk():
    """**SELECT de puertos PON en TLK.**

    Selecciona nombre de nodo/slot/puerto PON del inventario de TLK.
    Devuelve el resultado en una lista de tuplas.

    * **returns**: Lista de tuplas con resultados del select.
    * **rtype**: list
    """
    sql ="SELECT `id_tlk` FROM `t_resumen_servicios_tlk`"
    rbs = conector(sql,"select","Consultando Puertos PON TLK")
    return rbs

def get_puertos_pon_zbx():
    """**SELECT de puertos PON monitoreados por Zabbix.**

    Selecciona nombre de nodo y /slot/puerto PON monitoreados por Zabbix. Solo se 
    hace el selecto sobre la direccion RX debido a que todo puerto tiene ambas direcciones
    y al compararlo contra TLK esto no tiene importancia.
    
    Devuelve el resultado en una lista de tuplas.

    * **returns**: Lista de tuplas con resultados del select.
    * **rtype**: list
    """
    sql ="SELECT `nodo`, `puerto`FROM `reporte_semanal` WHERE `direccion` = 'RX'"
    rbs = conector(sql,"select","Consultando Puertos PON Zabbix")
    return rbs