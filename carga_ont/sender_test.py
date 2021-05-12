import os
import time



while True:
    os.system("zabbix_sender -z 10.0.0.101 -s Zabbix-Reportes -k scriptreportes  -o 0")
    time.sleep(45)