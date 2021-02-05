#/usr/bin/python
import logger
import sys

from llamadas import get_rbs, ont_check, host_get, get_inter_id, get_app_id, get_oid, create_ont, get_name, get_zabbix_key, create_graph, get_name_auto
from sesiones import autorizar, logout

#METODO MANUAL O AUTOMATICO (manual es ingreso a mano)

def orquestador_carga_ont(metodo):  
    if metodo == "manual":
        logger.info("Comienza la carga manual de ONTs")
        opcion = int(input("Carga: \n 1- ONT \n 2- ONT con RBS\n"))
        while opcion > 2 or opcion < 1:
            print("Opcion incorrecta \n")
            opcion = int(input("Carga: \n 1- ONT \n 2- ONT con RBS\n"))
        else:
            if opcion == 1:
                tipo = "ONT"
            elif opcion == 2:
                tipo = "Radio Base"
        opcion_e = input("Ingrese 1 para ingresar etitquetas, sino precione enter para continuar\n")
        if opcion_e == "1":
            etiqueta_m = input("Ingrese la etiqueta:\nEjemplo: GP0801-22024459-PINAZO-MORAN\n")
        else:
            pass
        nodo = input("Ingrese nombre de nodo en Gestion:\nEjemplo: AGUADA-13Z\n")
        puerto = input("Ingrese Slot/Puerto/ONT:\nEjemplo: 17/1/4\n")
        llave = autorizar()
        hostid = host_get(nodo,llave)
        inter_id = get_inter_id(hostid,llave)
        ip = inter_id["ip"]
        oid = get_oid("zte",puerto)
        try:
            nombre = get_name_auto(ip,oid["oid_etiqueta"],puerto,tipo)
        except IndexError as ee:
            print("No se pudo generar nombre para {}".format(nodo,"/",puerto))
            raise SystemExit(0)
        zkey = get_zabbix_key(puerto)
        appid = get_app_id(hostid,llave)
        chequeo = ont_check("key_",hostid,zkey["RX"],llave)
        if chequeo == 0:
            logger.info(str(nodo)+(" ")+str(zkey))
            logger.info(str(nombre))
            logger.info("******")
            itemid_1 = create_ont(nombre["RX"],zkey["RX"],hostid,inter_id["inter_id"],oid["oid_rx"],appid,llave)
            itemid_2 = create_ont(nombre["TX"],zkey["TX"],hostid,inter_id["inter_id"],oid["oid_tx"],appid,llave)
            nombreg = nombre["RX"][:-5]
            create_graph(nombreg,itemid_1,itemid_2,llave)
            print("Los item de ONT {} en el nodo {} deberian estar creados.".format(nombre,nodo))
        elif chequeo == 1:
            print("La ONT {} con puerto {} ya esta siendo monitoreada en el nodo {}".format(nombre,puerto,nodo))
    elif metodo == "auto":
        logger.info("Comienza la carga automatica de ONTs")
        lista = []
        repetidas = []
        faltante = 0
        encontrado = 0
        descarte = 0
        llave = autorizar()
        lista_rbs = get_rbs()
        contador_break = 0
        for rbs in lista_rbs:
            nodo = rbs[0]
            puerto = str(rbs[2]) + "/" + str(rbs[3]) + "/" + str(rbs[4])
            if rbs[0][-1] != "Z":
                logger.info("Se descarto la ONT {} {}".format(nodo,puerto))
                logger.info(rbs[0])
                #print("Se descarto la ONT {} {}".format(nodo,puerto))
                #print(rbs[0])
                descarte = descarte +1
                pass
            else:
                hostid = host_get(nodo,llave)
                inter_id = get_inter_id(hostid,llave)
                try:
                    ip = inter_id["ip"]
                except TypeError as e:
                    faltante = faltante + 1
                    pass
                oid = get_oid("zte",puerto)
                #GET NAME VIEJO CON OID
                '''
                try:
                    nombre = get_name(ip,oid["oid_etiqueta"],puerto,"Radio Base")
                except IndexError as ee:
                    print("No se pudo generar nombre para {}".format(rbs))
                    faltante = faltante + 1
                    pass
                '''
                etiqueta = rbs[1]
                nombre = get_name("Radio Base",puerto,etiqueta)
                zkey = get_zabbix_key(puerto)
                comparador = str(nodo)+str(zkey["RX"])+str(hostid)
                appid = get_app_id(hostid,llave)
                if comparador in lista:
                    repetidas.append(comparador)
                else:
                    chequeo = ont_check("key_",hostid,zkey["RX"],llave)
                    #aca crearia la lista de las ont no creadas y crearia las que corresponde.
                    if chequeo == 0:
                        if contador_break >= 3:
                            break
                        #print(nodo,zkey)
                        #print(nombre)
                        #print("******")
                        logger.info(str(nodo)+(" ")+str(zkey))
                        logger.info(str(nombre))
                        logger.info("******")
                        lista.append(comparador)
                        faltante = faltante + 1
                        #Tiene que crear un ITEM PARA TX y OTRO PARA CX
                        itemid_1 = create_ont(nombre["RX"],zkey["RX"],hostid,inter_id["inter_id"],oid["oid_rx"],appid,llave)
                        itemid_2 = create_ont(nombre["TX"],zkey["TX"],hostid,inter_id["inter_id"],oid["oid_tx"],appid,llave)
                        nombreg = nombre["RX"][:-5]
                        create_graph(nombreg,itemid_1,itemid_2,llave)
                        #logger.info("Se crearon los item de ONT {} en el nodo {}".format(nombre,nodo))
                        #contador_break = contador_break + 1
                    elif chequeo == 1:
                        encontrado = encontrado + 1
                        lista.append(comparador)

        logger.info("{} ONTs encontradas,{} repetidas, {} sin encontrar y {} descartadas".format(encontrado,len(repetidas),faltante,descarte))
        #print("{} ONTs encontradas,{} repetidas, {} sin encontrar y {} descartadas".format(encontrado,len(repetidas),faltante,descarte))
        logout(llave)
        #print(repetidas)
        

#Menu
if sys.argv[1] == "auto":
    orquestador_carga_ont("auto")
elif sys.argv[1] == "manual":
    orquestador_carga_ont("manual")