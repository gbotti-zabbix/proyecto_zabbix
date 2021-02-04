from direcciones_auditorias import auditoria_pon, puertos_uplink, puertos_uplink_h, c300_19p, puertos_uplink_19
from consultas import get_puertos_pon_tlk, get_puertos_pon_zbx
from datetime import datetime

def auditar_pon():
    fecha = datetime.now()
    lista_zbx = get_puertos_pon_zbx()
    lista_tlk = get_puertos_pon_tlk()
    nlista_zbx = []
    nlista_tlk = []
    diferenciatk = []
    diferenciazbx = []
    for puerto in lista_zbx:
        if (puerto[1] in puertos_uplink) or ((puerto[0][-1:] == "H") and (puerto[1] in puertos_uplink_h)) or ((puerto[0] in c300_19p) and (puerto[1] in puertos_uplink_19)):
            pass
        else:
            nlista_zbx.append(puerto[0]+"_"+puerto[1])
    for puerto in lista_tlk:
        nlista_tlk.append(puerto[0])
    for puerto in nlista_zbx:
        if puerto in nlista_tlk:
            pass
        else:
            diferenciazbx.append(puerto)
    for puerto in nlista_tlk:
        if puerto in nlista_zbx:
            pass
        else:
            diferenciatk.append(puerto)
    with open(auditoria_pon,"a") as archivo:
        archivo.write("Comienza auditoria PON. Fecha {}".format(datetime.now()))
        archivo.write("\n")
        archivo.write("\n")
        archivo.write("####Chequeo Zabbix contra TLK.####")
        archivo.write("\n")
        for puerto in diferenciazbx:
            archivo.write("{} : Zabbix : ".format(fecha.year+"/"+fecha.month+"/"+fecha.day) + puerto)
            archivo.write("\n")
        archivo.write("\n")
        archivo.write("\n")
        archivo.write("####Chequeo TLK contra Zabbix.####")
        archivo.write("\n")
        for puerto in diferenciatk:
            archivo.write("TLK : " + puerto)
            archivo.write("\n")
        archivo.write("{} puertos PON en TLK no se encontraron el listado de Zabbix.".format(len(diferenciatk)))
        archivo.write("\n")
        archivo.write("{} puertos PON en Zabbix no se encontraron el listado de TLK.".format(len(diferenciazbx)))
        archivo.write("\n")
        archivo.write("Finalizo auditoria PON. Fecha {}".format(datetime.now()))
        archivo.write("\n")
        archivo.write("\n")

auditar_pon()