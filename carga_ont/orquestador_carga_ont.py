from llamadas import ont_check, host_get, get_inter_id, get_app_id, get_oid
from sesiones import autorizar, logout
from api import usuario, contraseña

#METODO MANUAL O AUTOMATICO (manual es ingreso a mano)

def orquestador_carga_ont(metodo):  
    if metodo == "manual":
        #TENGO QUE LLAMAR A LAS FUNCIOENS CON INPUTS
        pass
    elif metodo == "auto":
        pass

orquestador_carga_ont("auto")