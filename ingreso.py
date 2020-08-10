with open ("datos_central.csv","r") as archivo:
    lista = []
    #Cargo el archivo en una lista
    archivo = archivo.read().splitlines()
    #Creo una lista de listas con los valores Nodo y Central TLK
    for x in archivo:
        lista.append(x.split(";"))
    #Uso las listas dentro de lista para llamar a la api por cada nodo
    for y in lista:
        print("El nodo {} pertenece a la central TLK {}".format(y[0],y[1]))

