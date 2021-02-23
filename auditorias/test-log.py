import random
import time

with open("/var/log/reportes_zabbix/test.log","a") as archivo:
    for i in range(0,10000000):
        numero = random.randrange(200,1000)
        time.sleep(30)
        archivo.write(numero)
        archivo.write("\n")