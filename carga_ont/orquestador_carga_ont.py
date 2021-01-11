from llamadas import get_rbs, ont_check, host_get, get_inter_id, get_app_id, get_oid, create_ont
from sesiones import autorizar, logout

#METODO MANUAL O AUTOMATICO (manual es ingreso a mano)

def orquestador_carga_ont(metodo):  
    if metodo == "manual":
        #TENGO QUE LLAMAR A LAS FUNCIOENS CON INPUTS
        pass
    elif metodo == "auto":
        contador = 0
        llave = autorizar()
        print(llave)
        lista_rbs = get_rbs()
        for rbs in lista_rbs:
            print(rbs)
            contador = contador + 1
        print(contador)
        logout(llave)

orquestador_carga_ont("auto")

#create_ont("AAA_TEST_ONT","TEST_LLAVE","11288","1363","TEST OID","71245","fc6c4c0d30ed633e8dd173e4f69e628b")
#create_ont("AAB_TEST_ONT","TEST_LLAVE_2","11288","1363","TEST OID","71245","fc6c4c0d30ed633e8dd173e4f69e628b")