import pickle

with open ('picos', 'rb') as picos:
    lista_picos = pickle.load(picos)


print(len(lista_picos), type(lista_picos))