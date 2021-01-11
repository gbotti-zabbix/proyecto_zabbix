from llamadas import ont_check, host_get, get_inter_id, get_app_id, get_oid
from sesiones import autorizar, logout
from api import usuario, contraseña

#METODO MANUAL O AUTOMATICO (manual es ingreso a mano)

def orquestador_carga_ont(metodo):  
    if metodo == "manual":
        #TENGO QUE LLAMAR A LAS FUNCIOENS CON INPUTS
        pass
    elif metodo == "auto":
        print(usuario)
        print(contraseña)
        pass
    create_ont = {
        "jsonrpc": "2.0",
        "method": "item.create",
        "params": {
            "name": "A_TEST_ONT",
            "key_": "TEST_KEY",
            "hostid": "11288",
            "interfaceid": "1363",
        "type": 4,
            "value_type": "3",
            "snmp_community": "{$SNMP_COMMUNITY}",
        "snmp_oid": "TEST OID",
        "units": "bps",
            "delay": "5m",
            "applications": [
                "71245"
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
        "auth": "23f8f52facd8cfc607d92862d38d669a",
        "id": 1
    }
    print(create_ont)


orquestador_carga_ont("auto")