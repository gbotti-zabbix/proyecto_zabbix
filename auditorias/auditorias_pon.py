from direcciones import auditoria_pon
from consultas import get_puertos_pon_tlk, get_puertos_pon_zbx

def auditar_pon():
    lista_zbx = get_puertos_pon_zbx()
    lista_tlk = get_puertos_pon_tlk()
    nlista_zbx = []
    diferenciatk = []
    diferenciazbx = []
    for puerto in lista_zbx:
        nlista_zbx.append(puerto[0]+"_"+puerto[1])
    for puerto in nlista_zbx:
        if puerto in lista_tlk:
            pass
        else:
            diferenciazbx.append(puerto)
    for puerto in lista_tlk:
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
            archivo.write(puerto)
            archivo.write("\n")
        archivo.write("{} puertos PON en Zabbix no se encontraron el listado de TLK.".format(len(diferenciazbx)))
        archivo.write("\n")
        archivo.write("\n")
        archivo.write("####Chequeo TLK contra Zabbix.####")
        archivo.write("\n")
        for puerto in diferenciatk:
            archivo.write(puerto)
            archivo.write("\n")
        archivo.write("{} puertos PON en TLK no se encontraron el listado de Zabbix.".format(len(diferenciatk)))
        archivo.write("\n")
        archivo.write("\n")
        archivo.write("Finalizo auditoria PON. Fecha {}".format(datetime.now()))
        archivo.write("\n")
        archivo.write("\n")


auditar_pon()