from conector import conector


sql = "SELECT nro_tlk FROM t_diccionario_nodos_tlk;"
comentario="Traer tipos nodos"

print (sql)
resultado= conector(sql,comentario,"select")
for x in resultado:
  print(x) 







