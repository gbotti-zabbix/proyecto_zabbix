
from consultas import get_rbs_tlk, get_rbs
from datetime import datetime
from direcciones_auditorias import auditoria_ont

""" ###Compara listado RBS en ONT TLK contra gestion.

Compara el listado de RBS en ONT extraido de gestion contra RBS en ONT 
del inventario de Telelink.

Escribe la diferencia total de puertos desde cada inventario, ademas de 
la informacion de los puertos que no se encontraron.

Esta informacion se escribe para ambos listados con el formato:
NOMBRE DE NODO-NUMERO DE NODO-PLACA/PUERTO/ONT. Ej: ATAHUALPA-03Z_16/2/1.

Este script es manejado por el CRON. Este lo llama todos los 5 de mes a las 18:30.
30 18 5 * * /usr/local/bin/python3.8 /etc/proyecto_zabbix/auditorias/auditorias_ont.py

Contiene la funcion **auditar_ont**.
"""

def auditar_ont():
    """**Ejecuta las funciones que auditan ONT entre TLK-Gestion**

    Comienza obteniendo las listas de radio bases en ONT desde gestion y TLK. Estas
    se cargan en las variables lista_g/tlk. Ademas se crean listas vacias donde se guardaran
    diferencias. 

    Se recorren ambas listas y se hace append de sus valores a las variables con nombre nlista.
    Se debe hacer este procedimiento porque los datos a comparar se guardan en diferentes formatos
    para TLK y gestion.

    Se itera sobre las nuevas listas chequeando si cada valor existe en la lista a contrastar. Por ejemplo
    se itera sobre nlista_tlk, para cada valor iterado es comprueba si existe en la lista nlista_g. Si no existe,
    se hace un append de ese valor a la lista diferenciatlk. Para la lista nlista_g se hace lo mismo pero comparando
    contra nlista_tlk.

    Se logean mensajes de comienzo de las tareas, se escriben los totales de diferencias entre los listados.
    Se recorren las listas de diferencias escribiendo en el archivo los valores uno a uno para ambas listas. Por ultimo
    se logea la finalizacion de los procedimientos. 

    **returns**: Esta funcion no tiene retornos.
    """
    #
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
    with open(auditoria_ont,"a") as archivo:
        archivo.write("Comienza auditoria ONTs. Fecha {}".format(datetime.now()))
        archivo.write("\n")
        archivo.write("\n")
        archivo.write("####Chequeo TLK contra gestion.####")
        archivo.write("\n")
        for rbs in diferenciatlk:
            archivo.write(rbs)
            archivo.write("\n")
        archivo.write("{} ONTs en TLK no se encontraron el listado de gestion.".format(len(diferenciatlk)))
        archivo.write("\n")
        archivo.write("\n")
        archivo.write("####Chequeo Gestion contra TLK.####")
        archivo.write("\n")
        for rbs in diferenciag:
            archivo.write(rbs)
            archivo.write("\n")
        archivo.write("{} ONTs en Gestion no se encontraron el listado de TLK.".format(len(diferenciag)))
        archivo.write("\n")
        archivo.write("\n")
        archivo.write("Finalizo auditoria ONTs. Fecha {}".format(datetime.now()))
        archivo.write("\n")
        archivo.write("\n")


auditar_ont()

# auditar perfiles configurados
