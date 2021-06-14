#!/usr/bin/python

from datetime import date

""" ###Direcciones de archivos o datos hardcodeados utilizados para todos los demas scripts.

El archivo cuenta con direcciones de directorios donde guardar achivos especificos, encabezados
utilizados en los reportes y algunos datos utilizados para filtros de puertos y/o nodos.
"""

##variables globales##

###PRODUCCIÓN###

####LOGS####
"""***Direcciones de logs y pid***

*file_log* es la direccion utilizada por logger para guardar los logeos.

pid es donde el deamon de *orquestador_reportes* genera el PID del proceso.
"""
file_log= "/var/log/reportes_zabbix/reportes.log"
pid = "/tmp/orquestador_reportes_zabbix.pid"


####Archivos inventarios y procesados####
"""***Directorios y formatos de nombres para archivos TLK***

Direcciones y convecniones de nombres utilizadas por parseo en las funcioens 
referentes a los invetnarios de TLK.
"""

#***directorio origen y destino de archivos***  

#directorio trabajo reporte tlk
path_files_tlk="/var/lib/reportes-zabbix/reporte_tlk/"  
#directorio trabajo reporte RBS
path_files_RBS="/var/lib/reportes-zabbix/reporte_RBS/"  

#nombre archivo origen  
file_tlk="PLN245_procesado.TXT"
#nombre archivo destino
file_tlk_dst="PLN245_parseado.csv"
#luego parseo renombro archivo original
file_tlk_old="PLN245_procesado.old.TXT"

#Concatenacion de nombres de archivos finales
archivo_tlk = path_files_tlk+file_tlk
archivo_tlk_dst = path_files_tlk+file_tlk_dst
archivo_tlk_viejo = path_files_tlk+file_tlk_old

file_rbs_DCS= "reportes_RBS.csv"
file_rbs_DCS_dst= "RBS_parseado.csv"
file_rbs_DCS_old= "reportes_RBS.old.csv"

archivo_rbs_DCS= path_files_RBS+file_rbs_DCS
archivo_rbs_DCS_dst= path_files_RBS+file_rbs_DCS_dst
archivo_rbs_DCS_old = path_files_RBS+file_rbs_DCS_old



##Inventarios Zabbix##

def crudozabbix():
    """***Genera la direccion para encontrar el archivo crudo de zabbix diario***

    **returns:** string con la direccion del Merged-Trends crudo proveniente de zabbix-server de la fecha
    en la que se ejecuto la funcion.  
    **rtype:** str
    """
    crudozabbix = "/var/lib/reportes-zabbix/Merged-Trends-" + str(date.today()) + ".ndjson"
    return crudozabbix


def archivo_pickle_ONT():
    """***Genera la direccion para guardar el archivo ONT.pickle luego de parsear crudos de zabbix***

    **returns:** string con la direccion del ONT.pickle parseado desde el Merged-Trends proveniente de zabbix-server
    de la fecha en la que se ejecuto la funcion.  
    **rtype:** str
    """
    archivo_pickle_ONT = "/var/lib/reportes-zabbix/crudos/Merged-Trends-" + str(date.today()) + "_ONT.pickle"
    return archivo_pickle_ONT


def archivo_pickle_PON():
    """***Genera la direccion para guardar el archivo .pickle luego de parsear crudos de zabbix***

    **returns:** string con la direccion del .pickle parseado desde el Merged-Trends proveniente de zabbix-server
    de la fecha en la que se ejecuto la funcion.  
    **rtype:** str
    """
    archivo_pickle_PON = "/var/lib/reportes-zabbix/crudos/Merged-Trends-" + str(date.today()) + ".pickle"
    return archivo_pickle_PON

#***Comandos para limpiar .pickle de ONT y PON con mas de 30 dias de antiguedad.***
limpiar_pickle_pon = "find /var/lib/reportes-zabbix/crudos/ -name \"Merged-Trends-*.pickle\" -type f -mtime +30 -exec rm -f {} \;"
limpiar_pickle_ont = "find /var/lib/reportes-zabbix/crudos/ -name \"Merged-Trends-*_ONT.pickle\" -type f -mtime +30 -exec rm -f {} \;"
limpiar_reporte_semanal = "find /var/lib/reportes-zabbix/reportes_semanales/ -name \"Reporte_Semanal*\" -type f -mtime +60 -exec rm -f {} \;"
limpiar_reporte_mensual = "find /var/lib/reportes-zabbix/reportes_mensuales/ -name \"Reporte_Mensual*\" -type f -mtime +180 -exec rm -f {} \;"

#***Zabbix sender.***
pusheo_diario_ok = "zabbix_sender -z 10.0.0.101 -s Zabbix-Reportes -k scriptreportes  -o 0"

##Reporte Zabbix##

def excel_PON_semanal():
    """***Genera la direccion para guardar el archivo reporte-semanal.xlsx***

    **returns:** string con la direccion para generar reporte-semanal.xlsx de la fecha en la que se ejecuto la funcion.  
    :rtype: str
    """
    excel_PON_semanal = "/var/lib/reportes-zabbix/reportes_semanales/Reporte_Semanal_" + str(date.today()) + ".xlsx"
    return excel_PON_semanal

def excel_PON_mensual():
    """***Genera la direccion para guardar el archivo reporte-mensual.xlsx***

    **returns:** string con la direccion para generar reporte-mensual.xlsx de la fecha en la que se ejecuto la funcion.  
    **rtype:** str
    """
    excel_PON_mensual = "/var/lib/reportes-zabbix/reportes_mensuales/Reporte_Mensual_" + str(date.today()) + ".xlsx"
    return excel_PON_mensual

def excel_ONT_semanal():
    """***Genera la direccion para guardar el archivo reporte-semanal_ONT.xlsx***

    **returns:** string con la direccion para generar reporte-semanal_ONT.xlsx de la fecha en la que se ejecuto la funcion.  
    **rtype:** str
    """
    excel_ONT_semanal = "/var/lib/reportes-zabbix/reportes_semanales/Reporte_Semanal_" + str(date.today()) + "_ONT.xlsx"
    return excel_ONT_semanal

def excel_ONT_mensual():
    """***Genera la direccion para guardar el archivo reporte-mensual_ONT.xlsx***

    **returns:** string con la direccion para generar reporte-mensual_ONT.xlsx de la fecha en la que se ejecuto la funcion.  
    **rtype:** str
    """
    excel_ONT_mensual = "/var/lib/reportes-zabbix/reportes_mensuales/Reporte_Mensual_" + str(date.today()) + "_ONT.xlsx"
    return excel_ONT_mensual

class DefiniciónEncabezados:
    """***Clase que define el nombre de hoja junto con el encabezado correspondiente.***

    Une encabezados con nombre de hojas para generar los reportes semanalas y mensuales.

    Solo cuenta con un *constructor*.
    """
    def __init__(self, nombreHoja, encabezados):
        """**param nombreHoja:** Nombre de la hoja.  
        **type nombreHoja:** str

        **param encabezados:** Lista de encabezados a insertar en conjunto con *nombreHoja*.  
        **type encabezados:** list(str)

        **returns:** esta clase no tiene retornos.
        """
        self.nombreHoja = nombreHoja
        self.encabezados = encabezados




"""***Lista de encabezados  a usar con DefiniciónEncabezados***

Los encabezados se separan por hojas de puertos PON, puertos de Uplink
o ONTs.

Esto se debe a que algunas hojas traen menos datos o directamente distintos (ONT).  
"""

encabezados_PON_PON = {"A1":"Modelo Nodo","B1":"Nodo","C1":"Slot/Puerto","D1":"Hora Pico","E1":"Fecha Pico","F1":"Pico","G1":"% Utilizacion","H1":"Prom. Hora Pico","I1":"Prom. Picos Diarios","J1":"Prom. Horas Pico","K1":"Total ONT","L1":"Servicios Datos","M1":"Servicios Empresariales","N1":"Empresariales de RBS"}
encabezados_PON_uplink = {"A1":"Modelo Nodo","B1":"Nodo","C1":"Slot/Puerto","D1":"Hora Pico","E1":"Fecha Pico","F1":"Pico","G1":"% Utilizacion","H1":"Prom. Hora Pico","I1":"Prom. Picos Diarios","J1":"Prom. Horas Pico"}
encabezados_ONT = {"A1":"Modelo Nodo","B1":"Nodo","C1":"Slot/Puerto/ONT","D1":"Etiqueta","E1":"Hora Pico","F1":"Fecha Pico","G1":"Pico","H1":"% Utilizacion","I1":"Prom. Hora Pico","J1":"Prom. Picos Diarios","K1":"Prom. Horas Pico"}


"""***Datos para la hoja de descripciones***

Usando los encabezados paso las descripciones de las columnas de las demas hojas.

Estos encabezados se escriben en la hoja descripciones. 
"""
descripcion_PON = {"A1":"Modelo Nodo: Modelo del nodo. C300, ISAM FX, MA5800, etc.","A2":"Nodo: Nombre del nodo utilizado en listados de conectividad.","A3":"Slot/Puerto: Numero de placa y puerto PON monitoreado.","A4":"Hora Pico: Margen de hora en la que se genero el pico maximo de la semana o mes. Ej.: 20:00 significa entre 20:00 y 21:00.","A5":"Fecha Pico: Fecha en la que se genero el pico maximo de la semana o mes.","A6":"Pico: Medida de trafico mas alta de la semana o mes, muestreada cada 5 minutos.","A7":"% Utilizacion: Porcentaje del ancho de banda del puerto que ocupo el pico.","A8":"Prom. Hora: Trafico promedio de la hora en la que se genero el pico.","A9":"Prom. Pico: Promedio de los picos diarios, de toda la semana o mes.","A10":"Prom. Horas Pico: Promedio de las horas con mas trafico, por dia, de la semana o mes.","A11":"Total ONT: Total de ONT que figuran en TLK al momento de generar el reporte.","A12":"Servicio Datos: Total de servicio de datos que figuran en TLK al momento de generar el reporte.","A13":"Servicios Empresariales: Total de servicios empresariales que figuran en TLK al momento de generar el reporte.","A14":"Empresariales de RBS: Total de servicios empresariales que atienden Radio Bases, registrados en TLK al momento de generar el reporte.","A16":"* Los datos pertenecientes a TLK solo figuran para puertos PON."}
descripcion_ONT = {"A1":"Modelo Nodo: Modelo del nodo. C300, ISAM FX, MA5800, etc.","A2":"Nodo: Nombre del nodo utilizado en listados de conectividad.","A3":"Slot/Puerto/ONT: Numero de placa, puerto PON y ONT monitoreada.","A4":"Etiqueta: Etiqueta sobre el puerto logico que figura en NetNumen.","A5":"Hora Pico: Margen de hora en la que se genero el pico maximo de la semana o mes. Ej.: 20:00 significa entre 20:00 y 21:00.","A6":"Fecha Pico: Fecha en la que se genero el pico maximo de la semana o mes.","A7":"Pico: Medida de trafico mas alta de la semana o mes, muestreada cada 5 minutos.","A8":"% Utilizacion: Porcentaje del ancho de banda del puerto que ocupo el pico.","A9":"Prom. Hora Pico: Trafico promedio de la hora en la que se genero el pico.","A10":"Prom. Picos Diarios: Promedio de los picos diarios, de toda la semana o mes.","A11":"Prom. Horas Pico: Promedio de las horas con mas trafico, por dia, de la semana o mes."}

"""***Defino los objetos para PON y ONT***

Paso los nombres de hojas junto con los encabezados que les corresponden.
"""
hojas_PON = [DefiniciónEncabezados("Subida PON", encabezados_PON_PON), DefiniciónEncabezados("Bajada PON", encabezados_PON_PON), DefiniciónEncabezados("Subida Uplink", encabezados_PON_uplink), DefiniciónEncabezados("Bajada Uplink", encabezados_PON_uplink),DefiniciónEncabezados("Descripciones",descripcion_PON)]
hojas_ONT = [DefiniciónEncabezados("Subida ONT", encabezados_ONT), DefiniciónEncabezados("Bajada ONT", encabezados_ONT),DefiniciónEncabezados("Descripciones",descripcion_ONT)]

"""***Datos para filtros en los parseos***
*c300_19p:* Lista de nodos C300 de 19 pulgadas.

*modelos_nodos:* Los distintos modelos de nodos GPON en produccion.

Los *puertos_uplik* definen los numeros de los puertos mencioandos por vendor o formato
(H por Huawei, 19 por C300 de 19 pulgadas).

Los *puertos_uplik_omitidos* filtran puertos que no queremos mostrar en los reportes (z por
C300 y z_19 por C300 de 19 pulgadas).
"""

###### NODOS DE 19' ######
c300_19p = ["G-AZNAREZ-01Z", "MARISCALA-01Z", "A-ARENA-01Z"]

######MODELOS DE NODOS EN PRODUCCION ######
modelos_nodos = ["MA5600T","MA5800","C300","ISAM-FX","C600"]

###### NUMERO DE LOS PUERTOS DE UPLINK ######
puertos_uplink = ["21/1","22/1"]

puertos_uplink_h = ["9/0","10/0"]

puertos_uplink_n = ["a/1","a/2","b/1"]

puertos_uplink_19 = ["19/1","20/1"]

puertos_uplink_omitidos_z = ["21/2","21/3","21/4","22/2","22/3","22/4",]

puertos_uplink_omitidos_z_19 = ["19/2","19/3","19/4","20/2","20/3","20/4"]

###Datos Base Datos###

####variables para conexión a la base de datos####
"""***Datos de DB usados por conector***

Datos que apuntan a la base de datos que queremos conector consulte.  
*host_DB:* Ip del BD Server.

*user_DB:* user name con privilegios sobre la BD.

*password_DB:* password del user name con privilegios sobre la BD.

*database_DB:* Nombre de la base de datos a consultar.
"""

host_DB="localhost"
user_DB="reportes"
password_DB="antel2020"
database_DB="reportes_zabbix"


##FIN PRODUCCIÓN##

##Direcciones de Testing##
def direccioens_testeo():
    """***Se repiten parametros que solo se utilizan para testear codigo.***

    Estos apuntan a una BD de respaldo y pueden tener algunas direcciones cambiadas con respecto
    a produccion.
    """

    ###DESARROLLO###

    #####LOGS####
    file_log= "reportes.log"
    pid = "/tmp/orquestador_reportes_zabbix.pid"

    ####Archivos inventarios y procesados####

    #directorio trabajo
    path_files= "./proyecto_zabbix/"  
    #nombre archivo origen
    file_tlk="PLN245_procesado.TXT"
    #nombre archivo destino   
    file_tlk_dst="PLN245_parseado.csv"     
    #luego parseo renombro archivo original     
    file_tlk_old="PLN245_procesado.old.TXT"            

    #Concatenacion de nombres de archivos finales
    archivo_tlk = path_files+file_tlk
    archivo_tlk_dst = path_files+file_tlk_dst
    archivo_tlk_viejo = path_files+file_tlk_old

    file_rbs_DCS= "reportes_RBS.csv"
    file_rbs_DCS_dst= "RBS_parseado.csv"
    file_rbs_DCS_old= "reportes_RBS.old.csv"

    archivo_rbs_DCS= path_files+file_rbs_DCS
    archivo_rbs_DCS_dst= path_files+file_rbs_DCS_dst
    archivo_rbs_DCS_old = path_files+file_rbs_DCS_old

    ####Inventarios Zabbix####
    def crudozabbix():
        crudozabbix = "Merged-Trends-2020-12-07.ndjson"
        return crudozabbix


    def archivo_pickle_ONT():
        archivo_pickle_ONT = "Pickle_ONT"
        return archivo_pickle_ONT


    def archivo_pickle_PON():
        archivo_pickle_PON = "Pickle_PON"
        return archivo_pickle_PON

    limpiar_pickle_pon = ""
    limpiar_pickle_ont = ""

    ####Reporte Zabbix####

    def excel_PON_semanal():
        excel_PON_semanal = "Reporte PON Semanal.xlsx"
        return excel_PON_semanal

    def excel_PON_mensual():
        excel_PON_mensual = "Reporte PON Mensual.xlsx"
        return excel_PON_mensual

    def excel_ONT_semanal():
        excel_ONT_semanal = "Reporte ONT Semanal.xlsx"
        return excel_ONT_semanal

    def excel_ONT_mensual():
        excel_ONT_mensual = "Reporte ONT Mensual.xlsx"
        return excel_ONT_mensual

    class DefiniciónEncabezados:
        def __init__(self, nombreHoja, encabezados):
            self.nombreHoja = nombreHoja
            self.encabezados = encabezados

    encabezados_PON_PON = {"A1":"Modelo Nodo","B1":"Nodo","C1":"Slot/Puerto","D1":"Hora Pico","E1":"Fecha Pico","F1":"Pico","G1":"% Utilizacion","H1":"Prom. Hora Pico","I1":"Prom. Picos Diarios","J1":"Total ONT","K1":"Servicios Datos","L1":"Servicios Empresariales","M1":"Empresariales de RBS"}
    encabezados_PON_uplink = {"A1":"Modelo Nodo","B1":"Nodo","C1":"Slot/Puerto","D1":"Hora Pico","E1":"Fecha Pico","F1":"Pico","G1":"% Utilizacion","H1":"Prom. Hora Pico","I1":"Prom. Picos Diarios"}
    encabezados_ONT = {"A1":"Modelo Nodo","B1":"Nodo","C1":"Slot/Puerto/ONT","D1":"Etiqueta","E1":"Hora Pico","F1":"Fecha Pico","G1":"Pico","H1":"% Utilizacion","I1":"Prom. Hora Pico","J1":"Prom. Picos Diarios"}

    hojas_PON = [DefiniciónEncabezados("Subida PON", encabezados_PON_PON), DefiniciónEncabezados("Bajada PON", encabezados_PON_PON), DefiniciónEncabezados("Subida Uplink", encabezados_PON_uplink), DefiniciónEncabezados("Bajada Uplink", encabezados_PON_uplink)]
    hojas_ONT = [DefiniciónEncabezados("Subida ONT", encabezados_ONT), DefiniciónEncabezados("Bajada ONT", encabezados_ONT)]

    c300_19p = ["G-AZNAREZ-01Z", "MARISCALA-01Z", "A-ARENA-01Z"]

    modelos_nodos = ["MA5600T","MA5800","C300","ISAM FX","C600"]

    ####dato base datos####
    #variables para conexión a la base de datos
    host_DB="192.168.211.4"
    user_DB="reportes"
    password_DB="antel2020"
    database_DB="reportes_zabbix_test"
