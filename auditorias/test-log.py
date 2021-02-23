import random
import time

with open("/var/log/reportes_zabbix/test.log","a") as archivo:
    for i in range(0,10000000):
        numero = random.randrange(200,1000)
        print(numero)
        archivo.write(str(numero))
        archivo.write("\n")
        time.sleep(30)