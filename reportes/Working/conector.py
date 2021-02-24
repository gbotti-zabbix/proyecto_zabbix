#!/usr/bin/python

import mysql.connector
import logger
import direcciones
""" Hacia una BD, pasa consultas y devuelve resultados

El script permite pasar una consulta a una BD y recibir un resultado. Ademas logea
la consulta a la BD.

Las variables importadas desde direcciones traen informacion de credenciales pertinentes
de la BD a donde se quieren hacer las consultas.

Si se quiere apuntar a otra BD cambiar host_DB, user_DB, password_DB y database_DB en direcciones (o importar variables sesde otro modulo).

Contiene la funcion conector.
"""

# Se le pasa query, tipo de query, mensaje para log, y lista si es tipo many
def conector(sql,tipo,mensaje,*args):
    """ Envia una consulta a una BD, retorna el resultado, logea la accion y valores afectados.

    :param sql: consulta SQL en formato string. Ej: "SELECT * from tabla"
    :type sql: str
    
    :param tipo: Puede pasar "many" y utilizar *args para instertar en la BD una lista grande de datos.
    "select" hace una query de select y retorna el resultado en formato en una lista de tuplas.
    De pasarlo vacio ejecuta una unica ves la consutla pasada por sql.
    :type tipo: str
    
    :param mensaje: Mensaje a logear. Ira acompañado de INFO HORA Y FECHA. Por lo general describe
    de forma simple la query y que tabla afecta. Ej: TRUNCANDO tabla, SELECT sobre tabla.
    :type mensaje: str
    
    :param *args: Lista de datos a insertar al llamar la funcion con tipo "many". 
    Por lo general es una lista de tuplas, pero depende de la funcion que llama a conector.
    :tpye *args: list

    :returns: Al llamarla con tipo "select" retorna una lista de tuplas y cuantos valores se vieron afectados,
    esto ultimo solo se logea. Las demas llamadas de tipo solo logean. 
    :rtype: list, str
    """
    mydb = mysql.connector.connect(host=direcciones.host_DB,user=direcciones.user_DB,password=direcciones.password_DB,database=direcciones.database_DB)
    logger.info( f' Ejecutando: {tipo}. Mensaje: {mensaje}')
    cursor = mydb.cursor()
    if tipo == "many":
        cursor.executemany(sql, args[0])
    elif tipo == "select":
        cursor.execute(sql)
        resultado = cursor.fetchall()
        mydb.cursor().close()
        mydb.close()
        return resultado
    else:
        cursor.execute(sql)
    mydb.commit()
    logger.info (f' Succuessfully loaded: {cursor.rowcount} affected rows ')
    cursor.close()
    mydb.close()