#!/usr/bin/python

from conector import conector
import logger
import direcciones


def f_cargar_inv_en_BD (archivo_csv):
    """
    Función carga el archivo de inventario parseado en csv a la BD
    Recibe la direcciónd el archivo parseado
    Borra la tabla 
    Carga el archivo.
    """
    # Borro talbla
    sql = 'TRUNCATE t_reporte_puertos_telelink;'
    comentario_sql= "Borrar tabla t_reporte_puertos_telelink "
    conector(sql,"otro",comentario_sql)
    
    #cargo Archivo
    sql_cargar_PLN = "LOAD DATA INFILE \'"+archivo_csv+"\' INTO TABLE t_reporte_puertos_telelink FIELDS TERMINATED BY \',\' ENCLOSED BY \'\"\' LINES TERMINATED BY \'\\r\\n\' ;"
    comentario_sql = "Cargar reporte telelink CSV paresado"
    conector(sql_cargar_PLN,"otro",comentario_sql)


def f_procesar_resumne_tlk_BD():
    #-------- Borro todas las tablas-----#
    sql_borrar_t_id_nodo_slot_puerto = 'TRUNCATE t_id_nodo_slot_puerto;'
    comentario_id="Borrado t_id_nodo_slot_puerto"

    sql_borrar_t_wf_x_puerto = 'TRUNCATE t_wf_x_puerto;'
    comentario_wf="Borrado t_wf_puerto"

    sql_borrar_t_datos_x_puerto = 'TRUNCATE t_datos_x_puerto;'
    comentario_datos="Borrado t_datos_puerto"

    sql_borrar_t_empresariales_x_puerto = 'TRUNCATE t_empresariales_x_puerto;'
    comentario_empresariales="Borrado t_empresariales_puerto"

    sql_borrar_t_rbs_x_puerto = 'TRUNCATE t_rbs_x_puerto;'
    comentario_rbs="Borrado t_rbs_puerto"

    sql_borrar_t_resumen_servicios_tlk = 'TRUNCATE t_resumen_servicios_tlk ;'
    comentario_resumen="Borrado t_resumen"

    conector(sql_borrar_t_id_nodo_slot_puerto,"otro",comentario_id)
    conector(sql_borrar_t_wf_x_puerto,"otro",comentario_wf)
    conector(sql_borrar_t_datos_x_puerto,"otro",comentario_datos)
    conector(sql_borrar_t_empresariales_x_puerto,"otro",comentario_empresariales)
    conector(sql_borrar_t_rbs_x_puerto,"otro",comentario_rbs)
    conector(sql_borrar_t_resumen_servicios_tlk,"otro", comentario_resumen)

    #--------Cargo t_id_nodo_slot_puerto-----#

    sql = "insert into  t_id_nodo_slot_puerto ( id_tlk, nombre_gestion, slot_nodo, puerto_nodo ) SELECT id_tlk, nombre_gestion, slot_nodo, puerto_nodo from  t_reporte_puertos_telelink GROUP by id_tlk;"
    desc_sql="Carga tabla t_id_nodo_slot_puerto"
    conector(sql,"otro",desc_sql)

    #--------Cargo tabla cantidad ONT por puerto  ------------------#
    sql = "insert into t_wf_x_puerto (id_tlk,wf_x_puerto) SELECT t.id_tlk, count(t.estado_ont_tlk) as wf FROM `t_reporte_puertos_telelink` t WHERE t.estado_ont_tlk = 20  GROUP by t.id_tlk;"
    desc_sql ="Carga cantidad wf por puerto"
    conector (sql,"otro",desc_sql)

    #-------Cargo tabla cantidad servicios de datos por puerto -----------------#

    sql = "insert into t_datos_x_puerto (id_tlk,datos_x_puerto) SELECT t.id_tlk, count(t.estado_ont_tlk) as wf FROM t_reporte_puertos_telelink t WHERE t.estado_ont_tlk = 20 and t.datos_ont_tlk=1 GROUP by t.id_tlk;"
    desc_sql ="Carga cantidad servicios de datos por puerto"
    conector (sql,"otro",desc_sql)

    #-------Cargo tabla cantidad servicios de empresariales por puerto -----------------#

    sql = "insert into t_empresariales_x_puerto (id_tlk,empresariales_x_puerto) SELECT t.id_tlk, count(t.estado_ont_tlk) as wf FROM t_reporte_puertos_telelink t WHERE t.estado_ont_tlk = 20 and t.empresarial_ont_tlk=1 GROUP by t.id_tlk;"
    desc_sql ="Carga cantidad servicios empresariales por puerto"
    conector (sql,"otro",desc_sql)

    #-------Cargo tabla cantidad servicios de rbs por puerto -----------------#

    sql = "insert into t_rbs_x_puerto (id_tlk,rbs_x_puerto) SELECT t.id_tlk, count(t.estado_ont_tlk) as wf FROM t_reporte_puertos_telelink t WHERE t.estado_ont_tlk = 20 and t.rbs_ont_tlk=1 GROUP by t.id_tlk;"
    desc_sql ="Carga cantidad radiobases por puerto"
    conector (sql,"otro",desc_sql)

    # -------Cargo la tabla resuemen de servicios por puerto ----------------- #

    sql = "INSERT INTO t_resumen_servicios_tlk (id_tlk,WF,Datos,Empresariales, RBS) SELECT t_id_nodo_slot_puerto.id_tlk,IFNULL (t_wf_x_puerto.wf_x_puerto,0) AS WF , IFNULL (t_datos_x_puerto.datos_x_puerto ,0 ) AS DATOS,IFNULL (t_empresariales_x_puerto.empresariales_x_puerto ,0 ) AS EMPRESARIALES,IFNULL (t_rbs_x_puerto.rbs_x_puerto ,0 ) AS RBS FROM t_id_nodo_slot_puerto LEFT JOIN t_wf_x_puerto on t_wf_x_puerto.id_tlk = t_id_nodo_slot_puerto.id_tlk LEFT JOIN t_datos_x_puerto on t_datos_x_puerto.id_tlk = t_id_nodo_slot_puerto.id_tlk LEFT JOIN t_empresariales_x_puerto on t_empresariales_x_puerto.id_tlk = t_id_nodo_slot_puerto.id_tlk LEFT JOIN t_rbs_x_puerto on t_rbs_x_puerto.id_tlk = t_id_nodo_slot_puerto.id_tlk;" 
    desc_sql ="llenado tabla resuemen servicios por it_tlk"
    conector (sql,"otro",desc_sql)

    logger.info('Se termino de cargar BD ')

    ######### Fin Carga Tablas  y servicios por puerto ##############


#Pusheo zabbix

def pusheo_crudos_diarios_PON(fecha):

    #variables que uso mas adelante y consulta sql
    print(datetime.now())
    archivo_pickle = "/var/lib/reportes-zabbix/crudos/Merged-Trends-" + fecha + ".pickle"
    contador_insert = 0
    lista_final = []
    contador_final = []
    sql = "INSERT INTO `crudos_diarios` (`id_zabbix`,`id_tlk`,`tipo`,`nodo`, `puerto`, `direccion`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #

    with open (archivo_pickle, 'rb') as lista:
        #carga de lista
        lista_tuplas = pickle.load(lista)
        #

    mydb = mysql.connector.connect(host="localhost",user="reportes",password="antel2020",database="reportes_zabbix")
    mycursor = mydb.cursor()

    for dato in lista_tuplas:
        lista_final.append(dato)
        contador_insert = contador_insert + 1
        if contador_insert == 100000:
            mycursor.executemany(sql, lista_final)
            mydb.commit()
            contador_final.append(mycursor.rowcount)
            contador_insert = 0
            lista_final.clear()

    mycursor.executemany(sql, lista_final)
    mydb.commit()
    contador_final.append(mycursor.rowcount)
    print("Total Ingresado",sum(contador_final))
    print(datetime.now())


def pusheo_crudos_diarios_ONT(fecha):

    print(datetime.now())

    archivo_pickle = "/var/lib/reportes-zabbix/crudos/Merged-Trends-" + fecha + "_ONT.pickle"
    sql = "INSERT INTO `crudos_diarios_ont` (`tipo`,`nodo`, `puerto`, `direccion`, `etiqueta`, `hora`, `fecha`, `promedio`, `pico`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    
    #carga el pickle
    with open (archivo_pickle, 'rb') as lista:
        lista_tuplas = pickle.load(lista)
    #
    
    #coneccion con la BD
    mydb = mysql.connector.connect(host="localhost",user="reportes",password="antel2020",database="reportes_zabbix")
    mycursor = mydb.cursor()
    #

    #pusheo a BD
    mycursor.executemany(sql, lista_tuplas)
    mydb.commit()
    contador_ingresos = mycursor.rowcount
    print("Total Ingresado",contador_ingresos)
    print(datetime.now())