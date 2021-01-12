from llamadas import get_rbs, ont_check, host_get, get_inter_id, get_app_id, get_oid, create_ont, get_name
from sesiones import autorizar, logout

#METODO MANUAL O AUTOMATICO (manual es ingreso a mano)

def orquestador_carga_ont(metodo):  
    if metodo == "manual":
        #TENGO QUE LLAMAR A LAS FUNCIOENS CON INPUTS
        pass
    elif metodo == "auto":
        faltante = 0
        encontrado = 0
        descarte = 0
        llave = autorizar()
        lista_rbs = get_rbs()
        for rbs in lista_rbs:
            modelo = rbs[0]
            nodo = rbs[1]
            puerto = str(rbs[2]) + "/" + str(rbs[3]) + "/" + str(rbs[4])
            if modelo != "C300":
                print("Se descarto la ONT {} {}".format(nodo,puerto))
                descarte = descarte +1
            else:
                hostid = host_get(nodo,llave)
                inter_id = get_inter_id(hostid,llave)
                try:
                    ip = inter_id["ip"]
                except TypeError as e:
                    pass
                oid = get_oid("zte",puerto)
                try:
                    nombre = get_name(ip,oid["oid_etiqueta"],puerto,"Radio Base")
                except IndexError as ee:
                    print("No se pudo generar nombre para {}".format(rbs))
                    pass
                chequeo = ont_check("name",nombre["RX"],llave)
                #aca crearia la lista de las ont no creadas y crearia las que corresponde.
                if chequeo == 0:
                    print(nodo)
                    faltante = faltante + 1
                elif chequeo == 1:
                    encontrado = encontrado + 1
        print("{} ONTs encontradas, {} sin encontrar y {} descartadas".format(encontrado,faltante,descarte))
        logout(llave)
#DATOS DE LAS ONT QUE YA RECABE
'''
*LLave de logeo a la api
*Modelo de nodo al que pertenece la ONT
*Nodo especifico al que pertenece la ONT
*Puerto de la ONT
*Host ID
*Interface ID
*IP
*OIDs (Tengo que llamarlas en especifico por RX,TX Etiqueta)
*Nombres (Tengo que llamarlos en especifico por RX TX)
*Chequea su existencia
'''

#DATOS DE LAS ONT QUE NO RECABE
'''
APP ID



orquestador_carga_ont("auto")

#create_ont("AAA_TEST_ONT","TEST_LLAVE","11288","1363","TEST OID","71245","fc6c4c0d30ed633e8dd173e4f69e628b")
#create_ont("AAB_TEST_ONT","TEST_LLAVE_2","11288","1363","TEST OID","71245","fc6c4c0d30ed633e8dd173e4f69e628b")