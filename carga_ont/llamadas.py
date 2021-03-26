#!/usr/bin/python

import logger
import requests
import json
import os 

from api import usuario_sv, contraseña_sv
from requester import requester

#IMPORTO EL CONECTOR Y LOGGER DE REFACTOR
import sys
sys.path.append("./reportes/Working")
from conector import conector

""" ###Llamadas a la Zabbix API y otras funciones utiles la creacion de ONT en Zabbix.

Funciones que llaman a la Zabbix API para obetener valores pertinentes a la creacion de 
ONTS en el Zabbix y realizar comparaciones de ONT creadas. 
Algunas funciones en este archivo no llaman a la API.

Muchas son dependientes una de otras, para ver mejor como estan conectadas, 
conviene estudiar **orquestador_carga_ont**.

Contiene las funciones:  
    **get_rbs** - Saca un listado de ONTs a comprobar si ya existen en Zabbix.  
    **ont_check** - Cheque el listado de *get_rbs()* contra Zabbix mediante la Zabbix API.  
    **host_get** - Mediante la Zabbix API, obtiene Host ID desde nombre de nodo.  
    **get_inter_id** - Mediante la Zabbix API, obtiene Interface ID de SNMP desde Host ID.  
    **get_app_id** - Mediante la Zabbix API, obtiene Application ID de App ONT desde Host ID.  
    **get_oid** - Con puerto y vendor, genera OIDs a utilizar en la creacion de los Item de ONT.  
    **dic_oid_zte** - Devuelve valores pertinentes de la OID a partir de claves de diccionarios.  
    **get_name_auto** - Genera nombre del Item a crear en Zabbix, utilziando SNMP Walk en Zabbix-Server.  
    **get_name** - Genera nombre del Item a crear en Zabbix.  
    **get_zabbix_key** - Genera la Key de los Item a crear en Zabbix. Estas deben ser unicas por nodo.  
    **create_ont** - Mediante la Zabbix API, crea uno de los Item de la ONT (RX o TX).  
    Se puede hacer a mano, pero esta pensada para utilizar la info obtenida por los get listados anteriormente.  
    **create_graph** - Mediante la Zabbix API, crea la grafica de hasta dos Item. Pensada para usarse con los Item ID
    generados por *create_ont()*, pero tambien pueden pasarse los parametros a mano.
"""


def get_rbs():
    """***SELECT de ONTs con RBS en gestion.***

    Selecciona nombre de nodo, etiqueta de gesition, slot/puerto/ont del inventario de gestion.
    Devuelve el resultado en una lista de tuplas.

    **returns:** Lista de tuplas con resultados del select.  
    **rtype:** list
    """
    sql = "SELECT `nodo`,`etiqueta_ont`,`slot`,`puerto`,`ont` FROM `t_servicios_RBS`"
    rbs = conector(sql,"select","Consultando ONTS")
    return rbs

def ont_check(opcion,hostid,parametro,auth):
    """***Chequea la existencia de una ONT en Zabbix***

    Cunsulta mediante la API de Zabbix utilizando *item.get* la existencia de una ONT.

    Se puede utilizar la opcion *key_* y bucar la ONT por las key de items unicos en zabbix, o
    se puede utilizar el nombre del item.

    Ejemplo de *key*: **PONRX[zxAnPonOnuIfRxOctets.ONT2/1/15]**

    Ejemplo de *nombre*: **Radio Base : 2/1/15 : P47129-27160341-ANTEL-RADIOBASE-CELULAR : RX**

    Si encuentra la ONT devuelve 1, sino 0.

    **param opcion:** Parametro a buscar, *key_* busca por llave de item.  
    *name* busca por nombre del item.  
    **type opcion:** str

    **param hostid:** Host id identificador del nodo.  
    **type hostid:** str

    **param parametro:** Dato a buscar. Dependiente de opcion.  
    **type parametro:** str

    **param auth:** Key de Zabbix API.  
    **type auth:** str

    **returns:** 1 si se encontro la ONT en zabbix, 0 si no se encontro.
    **rtype:** int
    """

    ont_check = {
    "jsonrpc": "2.0",
    "method": "item.get",
    "hostids": "{}".format(hostid),
    "params": {
        "output": ["{}".format(opcion)],
        "search": {
            "{}".format(opcion): "{}".format(parametro)
        }
    },
    "auth": "{}".format(auth),
    "id": 1
    }
    chequeo = requester(ont_check)
    if len(chequeo.json()["result"]) < 1:
        logger.info("******")
        logger.info("No se encontro la ONT: {}".format(parametro))
        return 0
    else:
        return 1

def host_get(nodo,auth):
    """***Obtiene Host ID a partir de nombre de nodo***

    LLamando a la Zabbix API con *host.get*, a partir del nombre del nodo,
    obtiene el Host ID de dicho nodo.

    Ejemplo nombre de *nodo*: **CORDON-04Z**

    **param nodo:** Nombre de nodo a obtener Host ID.  
    **type nodo:** str

    **param auth:** Key de Zabbix API.  
    **type auth:** str

    **returns:** Si se encuentra nombre de nodo devuelve el Host ID en formato str.  
    Si no encuentra el nodo solo logea.  
    **rtype:** str
    """

    host_get = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "filter": {
                "host": [
                    "{}".format(nodo)
                ]
            },
            "output": "hostid"    
        },
        "auth": auth,
        "id": 1
    }
    hostid = requester(host_get)
    if len(hostid.json()["result"]) < 1:
        logger.info("Host get no encontro el nodo: {}".format(nodo))
    else:
        return hostid.json()["result"][0]["hostid"]

def get_inter_id(hostid,auth):
    """***Obtiene interface ID type 2 a partir de Host ID***

    Llamando a a la Zabbix API con *hostinterface.get*, usando el Host ID,
    devuelve un interface ID e IP de la interface SNMP registrada en zabbix para ese nodo. 
    Si no tiene interafaces SNMP o el nodo no existe en zabbix se logea un error.

    **param hostid:** Host id identificador del nodo.  
    **type hostid:** str

    **param auth:** Key de Zabbix API.  
    **type auth:** str

    **returns:** Si se encuentra una interface type 2 con el host id
    pasado, devuelve el Interface ID e IP en formato dic. Si no encuentra el nodo
    solo logea.  
    **rtype:** dic
    """ 

    interfaceid = {
        "jsonrpc": "2.0",
        "method": "hostinterface.get",
        "params": {
        "output": ["interfaceid","hostid","ip","type"],
            "hostids": "{}".format(hostid),
            "filter": {
                "type": "2"
            }     
        },
        "auth": "{}".format(auth),
        "id": 1
    }
    interfaceid = requester(interfaceid)
    if len(interfaceid.json()["result"]) < 1:
        logger.info("No se encontro el hostid: {}".format(hostid))
    else:
        inter_id = interfaceid.json()["result"][0]["interfaceid"]
        ip = interfaceid.json()["result"][0]["ip"]
        return {"inter_id":inter_id,"ip":ip}

def get_app_id(hostid,auth):
    """***Obtiene Application ID de ONT a partir de Host ID***

    Llamando a a la Zabbix API con *application.get*, usando el Host ID,
    devuelve un Application ID de la app ONT registrada en zabbix para ese nodo.
    Si no tiene app ONT o el nodo no existe en zabbix se logea un error.

    **param hostid:** Host id identificador del nodo.  
    **type hostid:** str

    **param auth:** Key de Zabbix API.  
    **type auth:** str

    **returns:** Si se encuentra una Application ONT con el host id
    pasado, devuelve el Application ID en formato str. Si no encuentra el nodo
    solo logea.  
    **rtype:** str
    """

    app_id = {
        "jsonrpc": "2.0",
        "method": "application.get",
        "params": {
            "output": ["applicationid","hostid","name"],
            "hostids": "{}".format(hostid),
        "filter": {
            "name": ["ONT"]
        }
        },
        "auth": "{}".format(auth),
        "id": 1
    }
    app_id = requester(app_id)
    if len(app_id.json()["result"]) < 1:
        logger.info("No se encontro el hostid: {}".format(hostid))
    else:
        return app_id.json()["result"][0]["applicationid"]

def get_oid(tipo,puerto):
    """***Genera OID a partir de Vendor y Puerto.***

    Recibe informacion de puerto en formato **SLOT/PUERTO/ONT** y nombre del **vendor**
    del nodo (por ahora solo zte). Luego de parsear los datos y realizar un pequeño
    filtro, une las variables *base_* con una busqueda en la funcion *dic_oid_zte()*, la cual
    hace corresponder oids con puertos.

    Retorna un dicccionario con todas las oids necesarias para que Zabbix monitoree de forma
    efectiva una ONT.

    **param tipo:** Vendor del nodo a generar OID (por ahora solo "zte").  
    **type tipo:** str

    **param puerto:** Numero de puerto en formato **SLOT/PUERTO/PON**.  
    **type puerto:** str

    **returns:** Si se logra generar la OID devuelve diccionario con oid_rx RX, oid_tx y oid_etiqueta.
    De ocurrir un error solo logea.  
    **rtype:** dic
    """

    if tipo == "zte":
        base_RX = ".1.3.6.1.4.1.3902.1082.500.4.2.2.2.1.1.2852"
        base_TX = ".1.3.6.1.4.1.3902.1082.500.4.2.2.2.1.44.2852"
        base_etiqueta = ".1.3.6.1.4.1.3902.1082.500.10.2.3.3.1.2.2852"
        puerto = puerto.split("/")
        slot = int(puerto[0])
        puertopon = int(puerto[1])
        ont = int(puerto[2])
        if ont > 32:
            logger.info("El valor de ONT es incorrecto")
            pass
        else:
            try:
                oid_rx = base_RX + dic_oid_zte(str(slot)+str(puertopon)) + "." + str(ont)
                oid_tx = base_TX + dic_oid_zte(str(slot)+str(puertopon)) + "." + str(ont)
                oid_etiqueta = base_etiqueta + dic_oid_zte(str(slot)+str(puertopon)) + "." + str(ont)
                return {"oid_rx":oid_rx,"oid_tx":oid_tx,"oid_etiqueta":oid_etiqueta}
            except KeyError as e:
                logger.info("Uno de los valores del puerto es incorrecto")
    else:
        logger.info("No se han integrado funcionalidades para las ont de {}".format(tipo))

def dic_oid_zte(clave):
    """***Devuelve parte de las OID de ONT ZTE a partir de SLOT/PUERTO***

    Recive clave de diccionario conteniendo **SLOT/PUERTO** (sin el **/**), si esta
    clave se encuentra en dic, se devuelve el valor correspondiente a dicha clave.
    Este valor es parte de la OID que *get_oid()* intenta generar. 

    **param clave:** Puerto PON en formato **SLOT/PUERTO**.  
    **type clave:** str

    **returns:** Si **SLOT/PUERTO** coincide en el dic, devuelve gragmento de OID
    necesario para *get_oid()*.  
    **rtype:** str
    """

    dic = {"21":"78721",
    "22":"78722",
    "23":"78723",
    "24":"78724",
    "25":"78725",
    "26":"78726",
    "27":"78727",
    "28":"78728",
    "31":"78977",
    "32":"78978",
    "33":"78979",
    "34":"78980",
    "35":"78981",
    "36":"78982",
    "37":"78983",
    "38":"78984",
    "41":"79233",
    "42":"79234",
    "43":"79235",
    "44":"79236",
    "45":"79237",
    "46":"79238",
    "47":"79239",
    "48":"79240",
    "51":"79489",
    "52":"79490",
    "53":"79491",
    "54":"79492",
    "55":"79493",
    "56":"79494",
    "57":"79495",
    "58":"79496",
    "61":"79745",
    "62":"79746",
    "63":"79747",
    "64":"79748",
    "65":"79749",
    "66":"79750",
    "67":"79751",
    "68":"79752",
    "71":"80001",
    "72":"80002",
    "73":"80003",
    "74":"80004",
    "75":"80005",
    "76":"80006",
    "77":"80007",
    "78":"80008",
    "81":"80257",
    "82":"80258",
    "83":"80259",
    "84":"80260",
    "85":"80261",
    "86":"80262",
    "87":"80263",
    "88":"80264",
    "91":"80513",
    "92":"80514",
    "93":"80515",
    "94":"80516",
    "95":"80517",
    "96":"80518",
    "97":"80519",
    "98":"80520",
    "121":"81281",
    "122":"81282",
    "123":"81283",
    "124":"81284",
    "125":"81285",
    "126":"81286",
    "127":"81287",
    "128":"81288",
    "131":"81537",
    "132":"81538",
    "133":"81539",
    "134":"81540",
    "135":"81541",
    "136":"81542",
    "137":"81543",
    "138":"81544",
    "141":"81793",
    "142":"81794",
    "143":"81795",
    "144":"81796",
    "145":"81797",
    "146":"81798",
    "147":"81799",
    "148":"81800",
    "151":"82049",
    "152":"82050",
    "153":"82051",
    "154":"82052",
    "155":"82053",
    "156":"82054",
    "157":"82055",
    "158":"82056",
    "161":"82305",
    "162":"82306",
    "163":"82307",
    "164":"82308",
    "165":"82309",
    "166":"82310",
    "167":"82311",
    "168":"82312",
    "171":"82561",
    "172":"82562",
    "173":"82563",
    "174":"82564",
    "175":"82565",
    "176":"82566",
    "177":"82567",
    "178":"82568",
    "181":"82817",
    "182":"82818",
    "183":"82819",
    "184":"82820",
    "185":"82821",
    "186":"82822",
    "187":"82823",
    "188":"82824",
    "191":"83073",
    "192":"83074",
    "193":"83075",
    "194":"83076",
    "195":"83077",
    "196":"83078",
    "197":"83079",
    "198":"83080"}
    return dic[clave]

def get_name_auto(ip,oid,puerto,tipo):
    """***Genera nombre de ONT para Zabbix de forma automatica.***

    Hace un SNMP Walk a el puerto del nodo identificado por ip y oid
    pasados a la funcion. Se hace  una coneccion ssh hacia el Zabbix_Server
    y desde este se hace el SNMP Walk hacia el nodo en gestion.

    El Walk se realiza con la *oid_etiqueta* generada por *dic_oid_zte*. Junto con la
    etiqueta que responda el nodo, y los parametros puerto y tipo pasados en la llamada
    de la funcion, se crean los nombres para los item RX y TX de la ONT a crear en zabbix.
    La funcion devuelve un dic con estos valores.

    Tipo puede ser "ONT o "Radio Base". El puerto tine formato **SLOT/PUERTO/PON**.

    Las variables *contraseña* y *usario* utilizadas para la conexion ssh se mantienen en **api.pyc**
    para que no sean leibles directamente desde el IDE.

    **param ip:** IP de nodo a consultar por SNMP.  
    **type ip:** str

    **param oid:** Oid etiqueta correspondiente al puerto a consultar por SNMP.  
    **type oid:** str

    **param puerto:** Puerto PON en formato **SLOT/PUERTO/ONT**.  
    **type puerto:** str

    **param tipo:** Escrbie en la etiqueta si es "Radio Base" o "ONT".  
    **type tipo:** str

    **returns:** Si la consulta SNMP es correcta, devuelve dic de nombres RX y TX para
    nombrar ONTS en zabbix.  
    **rtype:** dic
    """
    etiqueta = os.popen("sshpass -p {} ssh {}@10.0.0.101 'snmpwalk -v 2c -c private {} {}'".format(contraseña_sv,usuario_sv,ip,oid)).read()
    etiqueta = etiqueta.split("\"")
    RX = "{} : {} : {} : RX".format(tipo,puerto,etiqueta[1])
    TX = "{} : {} : {} : TX".format(tipo,puerto,etiqueta[1])
    return {"RX":RX,"TX":TX}

def get_name(tipo,puerto,etiqueta):
    """***Genera nombre de ONT para Zabbix***

    A partir de los string tipo (**"Radio Base, "ONT"**), puerto en foramto
    **SLOT/PUERTO/ONT** y **etiqueta**, genera y retorna el dic con los nombres 
    utilziados para la creacion de los Item RX y TX de ONT en Zabbix. 

    **param tipo:** Escrbie en la etiqueta si es "Radio Base" o "ONT".  
    **type tipo:** str

    **param puerto:** Puerto PON en formato **SLOT/PUERTO/ONT**.  
    **type puerto:** str

    **param etiqueta** Etiqueta del puerto en gestion. **Ej: P47129-27160341-ANTEL-RADIOBASE-CELULAR**  
    **type etiqueta** str

    **returns:** Devuelve dic de nombres RX y TX para nombrar ONTS en zabbix.  
    **rtype:** dic
    """
    RX = "{} : {} : {} : RX".format(tipo,puerto,etiqueta)
    TX = "{} : {} : {} : TX".format(tipo,puerto,etiqueta)
    return {"RX":RX,"TX":TX}

def get_zabbix_key(puerto):
    """***Genera las key para crear Items en Zabbix***

    Une en un str la variable puerto (**SLOT/PUERTO/ONT**), pasada en la llamada de la funcion,
    con las str hardcodeadas en las variables RX y TX.

    Devuelve un dic de key RX y TX.

    **param puerto:** Puerto PON en formato **SLOT/PUERTO/ONT**.  
    **type puerto:** str

    **returns:** Devuelve dic de keys RX y TX para crear ONTS en zabbix.  
    **rtype:** dic
    """
    TX = "PONTX[zxAnPonOnuIfTxOctets.ONT{}]".format(puerto)
    RX = "PONRX[zxAnPonOnuIfRxOctets.ONT{}]".format(puerto)
    return {"RX":RX,"TX":TX}

def create_ont(nombre,llave,hostid,interfaceid,oid,appid,auth):
    """***Crea un Item (RX o TX) de una ONT en Zabbix***
    
    A partir de los parametros pasados en la llamda de la funcion, se crea un Item correspondiente a una ONT
    en un nodo especifico, utililizando la Zabbix API con item.create.

    Estos parametros deberian generarse con las funciones *get_* que se encuentran mas arriba en el script
    (*host_get(), get_inter_id(), get_app_id(), get_app_id(), get_oid(), get_name(), get_zabbix_key()*).
    De todas formas esta funcion se puede llamar pasando los parametros completamente a mano.

    Retorna Item ID si la creacion fue exitosa.

    La item Key (*llave*) asignada al Item, debe ser unica en el nodo.

    **param nombre:** Nombre del Item a crear en Zabbix. Formato igual al generado por *get_name()*.  
    **type nombre:** str

    **param llave:** Key del Item a crear en Zabbix. Formato igual al generado por *get_zabbix_key()*.  
    **type llave:** str

    **param hostid:** Host ID del nodo donde se creara el Item de ONT. Se puede obtenero con *host_get()*.  
    **type hostid:** str

    **param interfaceid:** Interface ID type 2 (SNMP) del nodo donde se creara el item de ONT. Se puede
    obtener con *get_inter_id()*.  
    **type interfaceid:** str

    **param oid:** Oid del Item a crear en Zabbix. Se puede obtener con *get_oid()*.  
    **type oid:** str

    **param appid:** Application ID de la app ONT, del nodo donde se creara el Item en Zabbix.
    Se puede obtener con *get_app_id()*.  
    **type appid:** str

    **param auth:** Zabbix API Key.  
    **type auth:** str

    **returns:** Si la ONT se crea correctamente, devuelve un str con el Item ID del item recien creado.  
    Si la API retorna un error, la funcion retorna un 0 y logea el error informado por JSON desde la API.  
    Si hay un error durante la creacion del Item por alguna interrupcion, se logea que hubo un error pero
    no se producen retornos.  
    **rtype:** str/int.
    """
    create_ont = {
        "jsonrpc": "2.0",
        "method": "item.create",
        "params": {
            "name": nombre,
            "key_": llave,
            "hostid": hostid,
            "interfaceid": interfaceid,
        "type": 4,
            "value_type": "3",
            "snmp_community": "{$SNMP_COMMUNITY}",
        "snmp_oid": oid,
        "units": "bps",
            "delay": "5m",
            "applications": [
                appid
            ],
        "preprocessing": [
                {
                    "type": "10",
            "params":""
                },
            {
            "type": "1",
            "params": 8
            }
        ]
        },
        "auth": auth,
        "id": 1
    }
    create_ont = requester(create_ont)
    try:
        if create_ont.json()["error"]["code"] == -32602:
            logger.info("La ONT con nombre \"{}\" genero el error {}".format(nombre,create_ont.json()["error"]["data"]))
            return 0
    except KeyError as e:
        if len(create_ont.json()["result"]) > 0:
            logger.info(str(create_ont.json()["result"]))
            logger.info("******")
            return create_ont.json()["result"]["itemids"][0]
        else:
            logger.info("Algo salio mal al crear la ONT: {}".format(nombre))

def create_graph(nombre,itemid_1,itemid_2,llave):
    """***Crea graficas para ciertos Item ID***

    Genera las graficas de los item creados por *create_ont()*, de todas formas se pueden
    pasar los parametros de forma manual si se desea crear una grafica nueva.
    Utiliza la Zabbix API con *graph.create*.

    Solo puede crear graficas de hasta 2 item.

    Logea creacion de graficas y errores. Retorna int para error especifico.

    **param nombre:** Nombre de la grafica a crear en Zabbix.
    Formato igual al generado por *get_name()* sin direccion (**RX/TX**).  
    **type nombre:** str

    **param itemid_1:** Item ID de una de las direcciones a graficar (RX o TX).  
    **type itemid_1:** str

    **param itemid_2:** Item ID de una de las direcciones a graficar (RX o TX).  
    **type itemid_2:** str

    **param llave:** Zabbix API Key.  
    **type llave:** str

    **returns:** Si la grafica de la ONT se crea correctamente, logea la creacion de la grafica con el Graph ID sin retornos.  
    Si la API retorna un error, la funcion retorna un 0 y logea el error informado por JSON desde la API.  
    Si hay un error durante la creacion de la grafica por alguna interrupcion, se logea que hubo un error pero
    no se producen retornos.  
    **rtype:** int.
    """

    create_graph = {
        "jsonrpc": "2.0",
        "method": "graph.create",
        "params": {
            "name": "{}".format(nombre),
            "width": 900,
            "height": 200,
            "gitems": [
                {
                    "itemid": "{}".format(itemid_1),
                    "color": "199C0D"
                },
                {
                    "itemid": "{}".format(itemid_2),
                    "color": "F63100"
                }
            ]
        },
        "auth": "{}".format(llave),
        "id": 1
    }
    create_graph = requester(create_graph)
    try:
        if create_graph.json()["error"]["code"] == -32602:
            logger.info("La ONT con nombre \"{}\" genero el error {} al crear su grafica".format(nombre,create_graph.json()["error"]["data"]))
            return 0
    except KeyError as e:
        if len(create_graph.json()["result"]) > 0:
            logger.info(str(create_graph.json()["result"]))
            logger.info("******")
        else:
            logger.info("Algo salio mal al crear la grafica de la ONT: {}".format(nombre))