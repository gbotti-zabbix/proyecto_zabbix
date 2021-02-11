#!/usr/bin/python

import mysql.connector
import logger
import direcciones


# Se le pasa query, tipo de query, mensaje para log, y lista si es tipo many
def conector(sql,tipo,mensaje,*args):
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