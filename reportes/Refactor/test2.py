from datetime import datetime, date

def variable():
    with open("numero.txt","r") as numero:
        numero = numero.read()
        return numero

fecha = str(date.today())

archivo = "Este seria el archivo con fecha" + fecha + "de mierda"

otro = 70


print (archivo)