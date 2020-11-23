import mysql.connector
import logging

#----importación variables de configuración
import cfg


# Se le pasa query, tipo de query, mensaje para log, y lista si es tipo many
def conector(sql,tipo,mensaje,*args):
    mydb = mysql.connector.connect(host=cfg.host_DB,user=cfg.user_DB,password=cfg.password_DB,database=cfg.database_DB)
    logging.info( f'Ejecutando: {tipo_sql}')
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
    logging.info (f'Succuessfully loaded: {cursor.rowcount} affected rows')
    print(cursor.rowcount)
    cursor.close()
    mydb.close()