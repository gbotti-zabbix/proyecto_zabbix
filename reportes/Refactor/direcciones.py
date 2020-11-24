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

#=========dato base datos========================#
#-variables para conexión a la base de datos
host_DB="192.168.211.4"
user_DB="reportes"
password_DB="antel2020"
database_DB="reportes_zabbix"


#========DESARROLLO===========#