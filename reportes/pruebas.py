
# from datetime import datetime

# now = datetime.now()

# for x in range(0,100):
#     while x >= 80:
#         print
# current_time = now.strftime("%H:%M:%S")
# print(type(current_time))
'''
import subprocess
proc = subprocess.Popen(["ping", "192.168.1.1"], stdout=subprocess.PIPE, universal_newlines=True, shell=True)
(out, err) = proc.communicate()
print (out)
print (test nuevo)
'''
# archivo parseado
"""
import pickle
with open ("Merged-Trends-2020-10-08.pickle","rb") as archivo:
    lista = pickle.load(archivo)
    contador = 0
    for linea in lista:
        if linea[0] == "MA5800":
            print(linea)
            contador = contador + 1
        if contador == 100:
            break
"""

# import json
# import re
# contador = 0
# with open ("Merged-Trends-2020-10-08.ndjson","r") as archivo:
#     archivo = archivo.read().splitlines()
#     for linea in archivo:
#         linea = json.loads(linea)
#         if "C300" in linea["groups"]:
#             #Nombre = linea["name"].split("/")
#             #print(Nombre)
#             #contador = contador + 1
#         #if contador == 50:
#         #    break
#         #    Placa = int(Nombre[1])
#         #    print(Placa)
#             Nombre = linea["name"]
#             print(Nombre)
#             match_puerto = re.search("([0-9])[/-]([0-9]{1,2})[/-]([0-9]{1,2})",Nombre)
#             if match_puerto:
#                 Puerto = match_puerto.group()
#                 print(Puerto[2:])
            
help(type)
