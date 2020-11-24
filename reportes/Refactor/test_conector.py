from conector import conector
import logger
from datetime import datetime

# sql = "select * from t_diccionario_nodos_tlk"

# mensaje = logger.info("Test")

# resultado = conector(sql,"select",mensaje)

#print (datetime.today().weekday())
dia = datetime.now().strftime("%d")
print (type(dia))
if dia == 24:
    print ("Ecole")

