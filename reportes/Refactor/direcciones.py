#!/usr/bin/python

from datetime import date

#========variables globales=========#


#========PRODUCCIÓN=========#

"""
#---   LOGS  --------------
file_log= "/var/log/reportes_zabbix/reportes.log"

#=======  Archivos inventarios y procesados=========#

# -directorio origen y destino de archivos
path_files="/var/lib/reportes-zabbix/reporte_tlk/"  #directorio trabajo

file_tlk="PLN245_procesado.TXT"               #nombre archivo origen
file_tlk_dst="PLN245_parseado.csv"              #nombre archivo destino
file_tlk_old="PLN245_procesado.old.TXT"              #luego parseo renombro archivo original



#=======  Inventarios Zabbix=========#
crudozabbix = "/var/lib/reportes-zabbix/Merged-Trends-" + str(date.today()) + ".ndjson"


#=========dato base datos========================#
#-variables para conexión a la base de datos
host_DB="localhost"
user_DB="reportes"
password_DB="antel2020"
database_DB="reportes_zabbix"

"""
#========FIN PRODUCCIÓN=========#

#========DESARROLLO===========#

#---   LOGS  --------------
file_log= "reportes.log"

#=======  Archivos inventarios y procesados=========#

# -directorio origen y destino de archivos
path_files= "./proyecto_zabbix/"  #directorio trabajo

file_tlk="PLN245_procesado.TXT"               #nombre archivo origen
file_tlk_dst="PLN245_parseado.csv"              #nombre archivo destino
file_tlk_old="PLN245_procesado.old.TXT"              #luego parseo renombro archivo original

#=======  Inventarios Zabbix=========#
crudozabbix = "test.txt"
archivo_pickle_ONT = "Pickle_ONT"
archivo_pickle_PON = "Pickle_PON"

#=======  Reporte Zabbix=========#
excel_PON_semanal = "Reporte PON Semanal.xlsx"
excel_PON_mensual = "Reporte PON Mensual.xlsx"
excel_ONT_semanal = "Reporte ONT Semanal.xlsx"
excel_ONT_mensual = "Reporte ONT Mensual.xlsx"

class DefiniciónEncabezados:
    def __init__(self, nombreHoja, encabezados):
        self.nombreHoja = nombreHoja
        self.encabezados = encabezados

encabezados_PON_PON = {"A1":"Modelo Nodo","B1":"Nodo","C1":"Slot/Puerto","D1":"Hora Pico","E1":"Fecha Pico","F1":"Pico","G1":"% Utilizacion","H1":"Prom. Hora Pico","I1":"Prom. Picos Diarios","J1":"Total ONT","K1":"Servicios Datos","L1":"Servicios Empresariales","M1":"Empresariales de RBS"}
encabezados_PON_uplink = {"A1":"Modelo Nodo","B1":"Nodo","C1":"Slot/Puerto","D1":"Hora Pico","E1":"Fecha Pico","F1":"Pico","G1":"% Utilizacion","H1":"Prom. Hora Pico","I1":"Prom. Picos Diarios"}
encabezados_ONT = {"A1":"Modelo Nodo","B1":"Nodo","C1":"Slot/Puerto/ONT","D1":"Etiqueta","E1":"Hora Pico","F1":"Fecha Pico","G1":"Pico","H1":"% Utilizacion","I1":"Prom. Hora Pico","J1":"Prom. Picos Diarios"}

hojas_PON = [DefiniciónEncabezados("Subida PON", encabezados_PON_PON), DefiniciónEncabezados("Bajada PON", encabezados_PON_PON), DefiniciónEncabezados("Subida Uplink", encabezados_PON_uplink), DefiniciónEncabezados("Bajada Uplink", encabezados_PON_uplink)]
hojas_ONT = [DefiniciónEncabezados("Subida ONT", encabezados_ONT), DefiniciónEncabezados("Bajada ONT", encabezados_ONT)]

#=========dato base datos========================#
#-variables para conexión a la base de datos
host_DB="192.168.211.4"
user_DB="reportes"
password_DB="antel2020"
database_DB="reportes_zabbix_test"


#========DESARROLLO===========#