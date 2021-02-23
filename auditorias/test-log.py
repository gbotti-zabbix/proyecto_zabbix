import random
import time


for i in range(0,10000000):
    with open("/var/log/reportes_zabbix/test.log","a") as archivo:
        numero = random.randrange(200,1000)
        print(numero)
        archivo.write(str(numero))
        archivo.write("\n")
        archivo.close()
        time.sleep(30)