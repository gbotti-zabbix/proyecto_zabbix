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


test = consultas("Hola")

print (test.query,test.sacar_tipo(),test.sacar_mensaje())


etiqueta = "1/22/4"

print(etiqueta[2:])