import mysql.connector
import logging
import direcciones

# Se le pasa query, tipo de query, mensaje para log, y lista si es tipo many
def conector(sql,tipo,mensaje,*args):
    mydb = mysql.connector.connect(host=direcciones.host_db,user=direcciones.user_DB,password=direcciones.password_DB,database=direcciones.database_DB)
    logging.info( f' Ejecutando: {tipo_sql}')
    cursor = mydb.cursor()
    if tipo == "many":
        cursor.executemany(sql, args[0])
    elif tipo == "select":
        resultado = cursor.fetchall()
        mydb.cursor().close()
        mydb.close()
        return resultado
    else:
        cursor.execute(sql)
    mydb.commit()
    logging.info (f' Succuessfully loaded: {cursor.rowcount} affected rows ')
    print(cursor.rowcount)
    cursor.close()
    mydb.close()