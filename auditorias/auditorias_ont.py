
from consultas import get_rbs_tlk, get_rbs

from datetime import datetime

def auditar_ont():
    lista_g = get_rbs()
    lista_tlk = get_rbs_tlk()
    nlista_g = []
    nlista_tlk = []
    diferenciatlk = []
    diferenciag = []
    for rbs in lista_g:
        dato = rbs[0] + "_" + str(rbs[2]) + "/" + str(rbs[3]) + "/" + str(rbs[4])
        nlista_g.append(dato)
    for rbs in lista_tlk:
        dato = rbs[0] + "/" + str(rbs[1])
        nlista_tlk.append(dato)
    for rbs in nlista_tlk:
        if rbs in nlista_g:
            pass
        else:
            diferenciatlk.append(rbs)
    for rbs in nlista_g:
        if rbs in nlista_tlk:
            pass
        else:
            diferenciag.append(rbs)
    with open("/var/lib/reportes-zabbix/auditorias/auditoria_ont.txt","a") as archivo:
        archivo.write("Comienza auditoria ONTs. Fecha {}".format(datetime.now()))
        archivo.write("\n")
        archivo.write("\n")
        archivo.write("Chequeo TLK contra gestion.")
        for rbs in diferenciatlk:
            archivo.write(rbs)
            archivo.write("\n")
        archivo.write("{} ONTs en TLK no se encontraron el listado de gestion.".format(len(diferenciatlk)))
        archivo.write("\n")        
        archivo.write("######")
        archivo.write("\n")
        archivo.write("\n")
        archivo.write("Chequeo Gestion contra TLK.")
        for rbs in diferenciag:
            archivo.write(rbs)
            archivo.write("\n")
        archivo.write("{} ONTs en Gestion no se encontraron el listado de TLK.".format(len(diferenciag)))
        archivo.write("\n")
        archivo.write("######")
        archivo.write("\n")
        archivo.write("\n")
        archivo.write("Finalizo auditoria ONTs. Fecha {}".format(datetime.now()))
        archivo.write("\n")
        archivo.write("\n")


auditar_ont()