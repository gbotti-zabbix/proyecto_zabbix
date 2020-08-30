import pickle

unos = []
dos = []
tres = []
cuatros = []
cincos = []
seis = []
sietes = []
ochos = []
nueves = []
suma= []
with open ('picos', 'rb') as picos:
    lista_picos = pickle.load(picos)
    for x in lista_picos:
        x = str(x)
        if x[0] == "1":
            unos.append(x[0])
        elif x[0] == "2":
            dos.append(x[0])
        elif x[0] == "3":
            tres.append(x[0])
        elif x[0] == "4":
            cuatros.append(x[0])
        elif x[0] == "5":
            cincos.append(x[0])
        elif x[0] == "6":
            seis.append(x[0])
        elif x[0] == "7":
            sietes.append(x[0])
        elif x[0] == "8":
            ochos.append(x[0])
        elif x[0] == "9":
            nueves.append(x[0])


print("Porcentaje de unos:",(len(unos)*100)/len(lista_picos))
print("Porcentaje de dos:",(len(dos)*100)/len(lista_picos))
print("Porcentaje de tres:",(len(tres)*100)/len(lista_picos))
print("Porcentaje de cuatros:",(len(cuatros)*100)/len(lista_picos))
print("Porcentaje de cincos:",(len(cincos)*100)/len(lista_picos))
print("Porcentaje de seis:",(len(seis)*100)/len(lista_picos))
print("Porcentaje de sietes:",(len(sietes)*100)/len(lista_picos))
print("Porcentaje de ochos:",(len(ochos)*100)/len(lista_picos))
print("Porcentaje de nueves:",(len(nueves)*100)/len(lista_picos))

suma.append((len(unos)*100)/len(lista_picos))
suma.append((len(dos)*100)/len(lista_picos))
suma.append((len(tres)*100)/len(lista_picos))
suma.append((len(cuatros)*100)/len(lista_picos))
suma.append((len(cincos)*100)/len(lista_picos))
suma.append((len(seis)*100)/len(lista_picos))
suma.append((len(sietes)*100)/len(lista_picos))
suma.append((len(ochos)*100)/len(lista_picos))
suma.append((len(nueves)*100)/len(lista_picos))

print("Porcentaje total:",sum(suma))