from conector import conector


sql = "SELECT nro_tlk FROM t_diccionario_nodos_tlk;"
comentario="Traer tipos nodos"

resultado= conector(sql,"select",comentario)
for x in resultado:
  print(x) 







