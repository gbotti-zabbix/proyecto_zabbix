#/usr/bin/python

import logger
import requests
import json
import os 

from api import usuario_sv, contraseña_sv
from requester import requester

#IMPORTO EL CONECTOR Y LOGGER DE REFACTOR
import sys
sys.path.append("./reportes/Refactor")
from conector import conector

#LISTA PRECARIA PARA GRAFICAS
lista_precaria = ["Radio Base : 13/3/11 : P74723-E84291-ANTEL-RADIOBASE-CELULAR ",
"1094866",
"1094867",
"Radio Base : 17/2/26 : P75363-E84343-E84346-ANTEL-RADIOBASE-CELULAR",
"1094868",
"1094869",
"Radio Base : 6/2/27 : P90558 - ANTEL RADIOBASE CELULAR",
"1094870",
"1094871",
"Radio Base : 7/5/9 : E83043 RadioBase P51834",
"1094872",
"1094873",
"Radio Base : 9/4/10 : P96084-E85504-ANTEL-RADIOBASE-CELULAR",
"1094874",
"1094875",
"Radio Base : 19/8/10 : P93782-ANTEL-RADIOBASE-CELULAR",
"1094876",
"1094877",
"Radio Base : 7/3/18 : P88902-E85342-E85343-ANTEL-RADIOBASE-CELULAR",
"1094878",
"1094879",
"Radio Base : 7/1/30 : P90557 RadioBase E85400",
"1094880",
"1094881",
"Radio Base : 5/8/30 : P92023-E85425-ANTEL RADIOBASE CELULAR",
"1094882",
"1094883",
"Radio Base : 6/3/32 : P69723-E83992-ANTEL-RADIOBASE-CELULAR",
"1094884",
"1094885",
"Radio Base : 13/3/9 : E85479 RadioBase P94797",
"1094886",
"1094887",
"Radio Base : 19/8/5 : P95687-ANTEL-RADIOBASE-CELULAR",
"1094888",
"1094889",
"Radio Base : 19/3/24 : P95527-E85488-ANTEL-RADIOBASE-CELULAR",
"1094890",
"1094891",
"Radio Base : 19/8/30 : P94575-22031558-ANTEL-RADIOBASE-CELULAR",
"1094892",
"1094893",
"Radio Base : 19/8/11 : P92252-E84820A-ANTEL-RADIOBASE-CELULAR",
"1094894",
"1094895",
"Radio Base : 16/1/19 : P73878-E84255-ANTEL-RADIOBASE-CELULAR",
"1094896",
"1094897",
"Radio Base : 16/3/20 : P89596 - ANTEL RADIOBASE CELULAR",
"1094898",
"1094899",
"Radio Base : 16/3/23 : P93729 - ANTEL RADIOBASE CELULAR",
"1094900",
"1094901",
"Radio Base : 3/4/25 : P73285-E84236-E84237-E84238-E84248-ANTEL RADIOBASE CELULAR",
"1094902",
"1094903",
"Radio Base : 3/4/26 : P73286-E84239-E84240-E84247-E84245-ANTEL RADIOBASE CELULAR",
"1094904",
"1094905",
"Radio Base : 3/4/29 : P74192 - ANTEL RADIOBASE CELULAR",
"1094906",
"1094907",
"Radio Base : 2/2/6 : P94264-22162085-ANTEL-RADIOBASE-CELULAR",
"1094908",
"1094909",
"Radio Base : 17/1/18 : P89835-ANTEL-RADIOBASE-CELULAR",
"1094910",
"1094911",
"Radio Base : 13/2/6 : P83506 RadioBase E85055",
"1094912",
"1094913",
"Radio Base : 18/3/17 : P93137 - ANTEL RADIOBASE CELULAR",
"1094914",
"1094915",
"Radio Base : 2/2/9 : P90998-E85401-ANTEL RADIOBASE CELULAR",
"1094916",
"1094917",
"Radio Base : 7/1/17 : P94102-23137312-ANTEL-RADIOBASE-CELULAR",
"1094918",
"1094919",
"Radio Base : 7/7/17 : P94109-23137336-ANTEL-RADIOBASE-CELULAR",
"1094920",
"1094921",
"Radio Base : 8/2/5 : P94110-23137429-ANTEL-RADIOBASE-CELULAR",
"1094922",
"1094923",
"Radio Base : 8/7/1 : P94111-23180316-ANTEL-RADIOBASE-CELULAR",
"1094924",
"1094925",
"Radio Base : 9/1/1 : P94120-23145278-ANTEL-RADIOBASE-CELULAR",
"1094926",
"1094927",
"Radio Base : 12/6/1 : P69916-E82502A-ANTEL RADIOBASE CELULAR",
"1094928",
"1094929",
"Radio Base : 14/6/10 : P48010-27163983-ANTEL-RADIOBASE-CELULAR",
"1094930",
"1094931",
"Radio Base : 2/6/9 : P72742 RADIOBASE E84228",
"1094932",
"1094933",
"Radio Base : 2/8/1 : P77351-E84483-E84484-ANTEL-RADIOBASE-CELULAR",
"1094934",
"1094935",
"Radio Base : 19/8/1 : P95855-E85499-ANTEL-RADIOBASE-CELULAR",
"1094936",
"1094937",
"Radio Base : 8/4/4 : E85350 RadioBase P89265",
"1094938",
"1094939",
"Radio Base : 17/3/1 : P47786-44799873-ANTEL-RADIOBASE-CELULAR",
"1094940",
"1094941",
"Radio Base : 17/3/2 : P56292 - ANTEL RADIOBASE CELULAR",
"1094942",
"1094943",
"Radio Base : 5/5/10 : P47788 - ANTEL RADIOBASE CELULAR",
"1094944",
"1094945"]


#SACO LISTADO DE ONT A CHEKEAR
def get_rbs():
    sql = "SELECT `nodo`,`etiqueta_ont`,`slot`,`puerto`,`ont` FROM `t_servicios_RBS`"
    rbs = conector(sql,"select","Consultando ONTS")
    return rbs

#CHEQUEO SI UNA ONT EXISTE POR KEY O NOMBRE.
#OPCION MARCA COMO BUSCAR (key_,name), HOST ID PARA ESPECIFICAR NODO DONDE SE BUSCA, PARAMETRO ES LO QUE BUSCAR (la key o nombre especifico)
def ont_check(opcion,hostid,parametro,auth):
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
        print("No se encontro la ONT: {}".format(parametro))
        return 0
    else:
        #print(chequeo.json()["result"])
        return 1

#SACAR UN HOST ID ESPECIFICO A PARTIR DEL NOMBRE 
def host_get(nodo,auth):
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
        print("Host get no encontro el nodo: {}".format(nodo))
    else:
        return hostid.json()["result"][0]["hostid"]

#SACAR UN INTERFACE ID A PARTIR DE HOST ID. TAMBIEN DEVUELVE IP DE LA INTERFACE.
def get_inter_id(hostid,auth):
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
        print("No se encontro el hostid: {}".format(hostid))
    else:
        inter_id = interfaceid.json()["result"][0]["interfaceid"]
        ip = interfaceid.json()["result"][0]["ip"]
        return {"inter_id":inter_id,"ip":ip}

#SACAR UN APP ID DE ONT A PARTIR DE HOST ID
def get_app_id(hostid,auth):
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
        print("No se encontro el hostid: {}".format(hostid))
    else:
        return app_id.json()["result"][0]["applicationid"]

#SACAR OID SEGUN VENDOR DE NODO, SLOT, PUERTO Y ONT
def get_oid(tipo,puerto):
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
            print("El valor de ONT es incorrecto")
            pass
        else:
            try:
                oid_rx = base_RX + dic_oid_zte(str(slot)+str(puertopon)) + "." + str(ont)
                oid_tx = base_TX + dic_oid_zte(str(slot)+str(puertopon)) + "." + str(ont)
                oid_etiqueta = base_etiqueta + dic_oid_zte(str(slot)+str(puertopon)) + "." + str(ont)
                return {"oid_rx":oid_rx,"oid_tx":oid_tx,"oid_etiqueta":oid_etiqueta}
            except KeyError as e:
                logger.info("Uno de los valores del puerto es incorrecto")
                print("Uno de los valores del puerto es incorrecto")
    else:
        logger.info("No se han integrado funcionalidades para las ont de {}".format(tipo))
        print("No se han integrado funcionalidades para las ont de {}".format(tipo))

#DEVUELVE OID A PARTIR DE CONCATENAR SLOT, PUERTO.
def dic_oid_zte(clave):
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

#Saco etiqueta para el name y lo devuelvo formateado. TIPO ES Radio Base, ONT. Retorna un DICC con los nombres.
#CODIGO ORIGINAL, USA OID Y HACE SNMP WALK
'''
def get_name(ip,oid,puerto,tipo):
    

    #LA IP LA SACO DESDE get inter_id
    etiqueta = os.popen("sshpass -p {} ssh {}@10.0.0.101 'snmpwalk -v 2c -c private {} {}'".format(contraseña_sv,usuario_sv,ip,oid)).read()
    etiqueta = etiqueta.split("\"")
    RX = "{} : {} : {} : RX".format(tipo,puerto,etiqueta[1])
    TX = "{} : {} : {} : TX".format(tipo,puerto,etiqueta[1])
    return {"RX":RX,"TX":TX}
'''
def get_name(tipo,puerto,etiqueta):
    RX = "{} : {} : {} : RX".format(tipo,puerto,etiqueta)
    TX = "{} : {} : {} : TX".format(tipo,puerto,etiqueta)
    return {"RX":RX,"TX":TX}

def get_zabbix_key(puerto):
    TX = "PONTX[zxAnPonOnuIfTxOctets.ONT{}]".format(puerto)
    RX = "PONRX[zxAnPonOnuIfRxOctets.ONT{}]".format(puerto)
    return {"RX":RX,"TX":TX}

#CREO ONT A PARTIR DE DATOS OBTENIDOS POR LAS DEMAS FUCNIONES. LA CONVINACION DE LLAVE/HOSTID DEBE SER UNICA
def create_ont(nombre,llave,hostid,interfaceid,oid,appid,auth):
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
            print("La ONT con nombre \"{}\" genero el error {}".format(nombre,create_ont.json()["error"]["data"]))
            return 0
    except KeyError as e:
        if len(create_ont.json()["result"]) > 0:
            logger.info(str(create_ont.json()["result"]))
            print(create_ont.json()["result"])
            logger.info("******")
        else:
            logger.info("Algo salio mal al crear la ONT: {}".format(nombre))
            print("Algo salio mal al crear la ONT: {}".format(nombre))

def create_graph():
    print("Ipa chipa chipa?")
    listita = []
    for iid in lista_precaria:
        listita.append(iid)
        if len(listita) == 3:
            print(listita)
            listita =[]


    '''
    {
    "jsonrpc": "2.0",
    "method": "graph.create",
    "params": {
        "name": "MySQL bandwidth",
        "width": 900,
        "height": 200,
        "gitems": [
            {
                "itemid": "22828",
                "color": "00AA00"
            },
            {
                "itemid": "22829",
                "color": "3333FF"
            }
        ]
    },
    "auth": "038e1d7b1735c6a5436ee9eae095879e",
    "id": 1
    }
    '''

def graph_check():
    pass


create_graph()