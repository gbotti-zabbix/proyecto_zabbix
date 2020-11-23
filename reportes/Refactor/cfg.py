#========variables globales=========

#---   LOGS  --------------
file_log= "/var/log/reportes_zabbix/proc_tlk_BD.log"


#======= Directorios de Trabajo===========

# -directorio origen y destino de archivos 
path_files="/var/lib/reportes-zabbix/reporte_tlk/"  #directorio trabajo



#======= Telelink inventarios y procesados=========
file_tlk="PLN245_procesado.TXT"               #nombre archivo origen
file_tlk_dst="PLN245_pareseado.csv"              #nombre archivo destino
file_tlk_old="PLN245_procesado.old.TXT"              #luego parseo renombro archivo original



#=========dato base datos========================
#-variables para conexión a la base de datos
host_DB="localhost"
user_DB="reportes"
password_DB="antel2020"
database_DB="reportes_zabbix"