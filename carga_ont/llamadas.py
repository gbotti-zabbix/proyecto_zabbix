import requests
import json
import os 

from api import usuario_sv, contraseña_sv
from requester import requester

#IMPORTO EL CONECTOR DE REFACTOR
import sys
sys.path.append("./reportes/Refactor")
from conector import conector

#sql para ont
#SELECT `nombre_gestion`,`slot_nodo`,`puerto_nodo`,`nro_ont` FROM `t_reporte_puertos_telelink` WHERE `rbs_ont_tlk`>0;

#SACO LISTADO DE ONT A CHEKEAR
def get_rbs():
    sql = "SELECT `nombre_gestion`,`slot_nodo`,`puerto_nodo`,`nro_ont` FROM `t_reporte_puertos_telelink` WHERE `rbs_ont_tlk`>0;"
    rbs = conector(sql,"select","Consultando ONTS")
    return rbs

#CHEQUEO SI UNA ONT EXISTE POR KEY O NOMBRE.
#OPCION MARCA COMO BUSCAR (key_,name), PARAMETRO ES LO QUE BUSCAR (la key o nombre especifico)
def ont_check(opcion,parametro,auth):
    ont_check = {
    "jsonrpc": "2.0",
    "method": "item.get",
    "params": {
        "output": ["{}".format(opcion)],
        "search": {
            "{}".format(opcion): "{}".format(parametro)
        },
        "sortfield": "name"
    },
    "auth": "{}".format(auth),
    "id": 1
    }
    chequeo = requester(ont_check)
    if len(chequeo.json()["result"]) < 1:
        #print("No se encontro la ONT: {}".format(parametro))
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
        print("No se encontro el nodo: {}".format(nodo))
    else:
        print(hostid.json()["result"][0]["hostid"])
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
        print("No se encontro el hostid: {}".format(hostid))
    else:
        print(app_id.json()["result"])
        print(app_id.json()["result"][0]["applicationid"])
        return app_id.json()["result"][0]["applicationid"]

#SACAR OID SEGUN VENDOR DE NODO, SLOT, PUERTO, ONT Y DIRECCION
def get_oid(tipo,puerto,direccion):
    if tipo == "zte":
        base_RX = ".1.3.6.1.4.1.3902.1082.500.4.2.2.2.1.1.28527"
        base_TX = ".1.3.6.1.4.1.3902.1082.500.4.2.2.2.1.44.2852"
        puerto = puerto.split("/")
        slot = int(puerto[0])
        puertopon = int(puerto[1])
        ont = int(puerto[2])
        if ont > 32:
            print("El valor de ONT es incorrecto")
            pass
        else:
            try:
                if direccion == "RX":
                    oid = base_RX + dic_oid_zte(str(slot)+str(puertopon)) + "." + str(ont)
                    print(oid)
                    return oid
                elif direccion == "TX":
                    oid = base_TX + dic_oid_zte(str(slot)+str(puertopon)) + "." + str(ont)
                    print(oid)
                    return oid
            except KeyError as e:
                print("Uno de los valores del puerto es incorrecto")
    else:
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
def get_name(ip,oid,puerto,tipo):
    #LA IP LA SACO DESDE get inter_id
    etiqueta = os.popen("sshpass -p {} ssh {}@10.0.0.101 'snmpwalk -v 2c -c private {} {}'".format(contraseña_sv,usuario_sv,ip,oid)).read()
    etiqueta = etiqueta.split("\"")
    RX = "{} : {} : {} : RX".format(tipo,puerto,etiqueta[1])
    TX = "{} : {} : {} : TX".format(tipo,puerto,etiqueta[1])
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
            print("La ONT con key \"{}\" ya existe".format(llave))
            return 0
    except KeyError as e:
        if len(create_ont.json()["result"]) > 0:
            print(create_ont.json()["result"])
        else:
            print("Algo salio mal al crear la ONT: {}".format(nombre))


test = get_inter_id("11289","eafffac9d622b5939c3c3e65df2aff91")
print(test["ip"])
print(test["inter_id"])