from test2 import variable, otro, archivo
import time

class consultas():
    def __init__(self,query):
        self.query = query
    
    def sacar_tipo(self):
        if self.query == "Hola":
            tipo = "Tipo Hola"
            return tipo
    def sacar_mensaje(self):
        if self.query == "Hola":
            mensaje = "Mensaje Hoja"
            return mensaje


#test = consultas("Hola")

#print (test.query,test.sacar_tipo(),test.sacar_mensaje())

while True:
    print(variable())
    print(otro)
    print(archivo)
    time.sleep(5)