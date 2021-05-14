import time
import os

while True:
    os.system("zabbix_sender -z 10.0.0.101 -s Zabbix-Reportes -k testaction -o 0")
    time.sleep(30)