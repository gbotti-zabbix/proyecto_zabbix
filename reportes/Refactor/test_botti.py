from conector import conector


sql = "SELECT nro_tlk,letra_gestion,modelo FROM t_diccionario_nodos_tlk;"
comentario="Trer tipos nodos"
respuesta = (conector(sql,comentario,"select"))

print(respuesta)