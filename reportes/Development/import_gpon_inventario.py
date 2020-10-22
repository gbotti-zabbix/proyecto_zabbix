
#import_gpon_inventario.py :
# importar inventarios desde ritaf, se va a realizar todos los lunes

import scp

#datos de Ritaf, con este usuario se entra a la carpeta inventarios.
host = 10.97.68.45
user = inventarios
password = !nvR!t4f

filename = PLN245_procesado.TXT
path_origen = /opt/apps/ftp/inventarios/gpon
path_destino = /var/lib/reportes-zabbix/gpon

origen = path_origen & "/" & filename

#copia del archivo
client = scp.Client(host=host, user=user, password=password)
client.transfer(origen, path_destino)

