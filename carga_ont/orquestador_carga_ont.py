from llamadas import get_rbs, ont_check, host_get, get_inter_id, get_app_id, get_oid, create_ont
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
            key = "PONTX[zxAnPonOnuIfRxOctets.ONT{}".format(puerto)
            chequeo = ont_check("key_",key,llave)
            if modelo != "C300":
                descarte = descarte +1
            else:
                if chequeo == 0:
                    faltante = faltante + 1
                elif chequeo == 1:
                    encontrado = encontrado + 1
        print("{} ONTs encontradas, {} sin encontrar y {} descartadas".format(encontrado,faltante,descarte))
        logout(llave)

orquestador_carga_ont("auto")

#create_ont("AAA_TEST_ONT","TEST_LLAVE","11288","1363","TEST OID","71245","fc6c4c0d30ed633e8dd173e4f69e628b")
#create_ont("AAB_TEST_ONT","TEST_LLAVE_2","11288","1363","TEST OID","71245","fc6c4c0d30ed633e8dd173e4f69e628b")