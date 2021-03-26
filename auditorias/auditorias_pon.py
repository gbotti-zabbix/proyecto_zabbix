from direcciones_auditorias import auditoria_pon, puertos_uplink, puertos_uplink_h, c300_19p, puertos_uplink_19
from consultas import get_puertos_pon_tlk, get_puertos_pon_zbx
from datetime import datetime

""" ###Compara puertos PON monitoreados en ZBX contra TLK.

Compara los puertos PON monitorados por Zabbix contra puertos PON en el
inventario de Telelink.

Escribe la diferencia total de puertos desde cada inventario, ademas de 
la informacion de los puertos que no se encontraron.

Esta informacion se escribe para ambos listados con el formato:  
**FECHA(YYYY/MM/DD) : Zabbix/TLK : NOMBRE DE NODO-NUMERO DE NODO_PLACA/PUERTO PON.**  
**Ej**: 2021/2/18 : Zabbix : P-MOLINO-26Z_7/7.

Este script es manejado por el CRON. Este lo llama todos los 5 de mes a las 18:35.  
**35 18 5 * * /usr/local/bin/python3.8 /etc/proyecto_zabbix/auditorias/auditorias_pon.py**

Contiene la funcion **auditar_pon**.
"""

def auditar_pon():
    """**Ejecuta las funciones que auditan puertos PON entre Zabbix-TLK**

    Comienza obteniendo las listas de puertos PON monitoreados por Zabbix y registrados en TLK.
    Estas se cargan en las variables *lista_zbx/tlk*. Ademas se crean *listas vacias* donde se guardaran
    diferencias. Tambien se carga la *fecha y hora* de ejecucion de la funcion.

    Se recorren ambas listas y se hace append de sus valores a las variables con nombre *nlista*.
    Se debe hacer este procedimiento porque los datos a comparar se guardan en diferentes formatos
    para TLK y Zabbix. Ademas sobre zabbix se filtran los puertos de Uplink, dado que estos no cuentan
    con informacion en TLK.

    Se itera sobre las *nuevas listas* chequeando si cada valor existe en la lista a contrastar. Por ejemplo
    se itera sobre *nlista_zbx*, para cada valor iterado es comprueba si existe en la lista *nlista_tlk*. Si no existe,
    se hace un append de ese valor a la lista *diferenciazbx*. Para la lista *nlista_tlk* se hace lo mismo pero comparando
    contra *nlista_zbx*.

    Se logean mensajes de comienzo de las tareas, se escriben los totales de diferencias entre los listados.
    Se recorren las listas de diferencias escribiendo en el archivo los valores uno a uno para ambas listas. 
    Por ultimo se logea la finalizacion de los procedimientos. 

    **returns**: Esta funcion no tiene retornos.
    """
    
    fecha = datetime.now()
    lista_zbx = get_puertos_pon_zbx()
    lista_tlk = get_puertos_pon_tlk()
    nlista_zbx = []
    nlista_tlk = []
    diferenciatk = []
    diferenciazbx = []
    for puerto in lista_zbx:
        if (puerto[1] in puertos_uplink) or ((puerto[0][-1:] == "M") and (puerto[1] in puertos_uplink_h)) or ((puerto[0] in c300_19p) and (puerto[1] in puertos_uplink_19)):
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
        archivo.write("####Chequeo Zabbix contra TLK.####")
        archivo.write("\n")
        for puerto in diferenciazbx:
            archivo.write("{} : Zabbix : ".format(str(fecha.year)+"/"+str(fecha.month)+"/"+str(fecha.day)) + puerto)
            archivo.write("\n")
        archivo.write("\n")
        archivo.write("####Chequeo TLK contra Zabbix.####")
        archivo.write("\n")
        for puerto in diferenciatk:
            archivo.write("{} : TLK : ".format(str(fecha.year)+"/"+str(fecha.month)+"/"+str(fecha.day)) + puerto)
            archivo.write("\n")
        archivo.write("{} puertos PON en TLK no se encontraron el listado de Zabbix.".format(len(diferenciatk)))
        archivo.write("\n")
        archivo.write("{} puertos PON en Zabbix no se encontraron el listado de TLK.".format(len(diferenciazbx)))
        archivo.write("\n")
        archivo.write("Finalizo auditoria PON. Fecha {}".format(datetime.now()))
        archivo.write("\n")

#***Llamada a la funcion***
auditar_pon()