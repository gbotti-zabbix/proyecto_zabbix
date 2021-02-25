#!/usr/bin/python

from conector import conector
import logger
import direcciones
import pickle
from consultas import sql_push_diarios_ONT, sql_push_diarios_PON, sql_truncate_cdiarios_PON, sql_truncate_cdiarios_ONT
""" Pusheo de archivos parseados a la BD

Toma los archivos generados por parseo y los inserta en la BD para su posterior 
prosesamiento y generacion de reportes.

Importar pickle es esencial para poder abrir los archivos parseados.

Si se agregaran campos o se necesitara cambiar el funcionamiento de las consultas
para el pusheos de crudos de zabbix, se debe editar la variables y funciones importadas
desde consultas. Si deseamos editar las consultas utilizadas en los pusheos de TLK y 
gestion, debemos modificar la funcion f_procesar_resumne_tlk_BD.

Para cambiar nombres de archivos parseados deberian editarse las variables y funciones importadas
desde direcciones.

Contiene las funciones:
    * f_cargar_inv_en_BD - Carga inventario TLK a la BD a partir del csv generado en el parseo de crudos.
    * f_cargar_inv_RBS_en_BD - Carga inventario de RBS en ONT traido de gestion a la BD a partir del csv generado en el parseo de crudos.
    * f_procesar_resumne_tlk_BD - Consultas utlizadas para las dos funciones anteriores.
    * pusheo_crudos_diarios_PON - Carga puertos PON/Uplink a crudos_diarios en la BD a partir de archivo parseado .pickle.
    * pusheo_crudos_diarios_ONT - Carga puertos ONT a crudos_diarios_ONT a partir de archivo parseado .pickle.
"""

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
    conector(sql,"Truncar",comentario_sql)
    
    #cargo Archivo
    sql_cargar_PLN = "LOAD DATA INFILE \'"+archivo_csv+"\' INTO TABLE t_reporte_puertos_telelink FIELDS TERMINATED BY \',\' ENCLOSED BY \'\"\' LINES TERMINATED BY \'\\r\\n\' ;"
    comentario_sql = "Cargar reporte telelink CSV paresado"
    conector(sql_cargar_PLN,"Load",comentario_sql)

def f_cargar_inv_RBS_en_BD (archivo_csv_RBS):
    """
    Función carga el archivo de  inventario de Radio BASES parseado en csv a la BD
    Recibe la direcciónd el archivo parseado
    Borra la tabla 
    Carga el archivo.
    """
    # Borro talbla
    sql = 'TRUNCATE t_servicios_RBS;'
    comentario_sql= "Borrar tabla t_servicios_RBS "
    conector(sql,"Truncar",comentario_sql)
    
    #cargo Archivo
    sql_cargar_RBS= "LOAD DATA LOCAL INFILE \'"+archivo_csv_RBS+"\' INTO TABLE t_servicios_RBS FIELDS TERMINATED BY \',\' ENCLOSED BY \'\"\' LINES TERMINATED BY \'\\r\\n\' ;"
    comentario_sql = "Cargar reporte RBS paresado"
    conector(sql_cargar_RBS,"Load",comentario_sql)

def f_procesar_resumne_tlk_BD():
    """ Consultas para pusheo de TLK

    Al llamar la funcion se ejecutan las consultas en orden, de forma parecida a 
    lo definido en flujo_db, pero estas consultas solo afectan tablas relacionadas
    con los inventarios de TLK y gestion (RBS en ONT).

    Cada consulta va a compañada de un mensaje necesario a pasar a conector. Ademas
    se logea el inicio y finalizacion de la tarea.

    :returns: Esta funcion no tiene retornos.
    """
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

    conector(sql_borrar_t_id_nodo_slot_puerto,"Truncar",comentario_id)
    conector(sql_borrar_t_wf_x_puerto,"Truncar",comentario_wf)
    conector(sql_borrar_t_datos_x_puerto,"Truncar",comentario_datos)
    conector(sql_borrar_t_empresariales_x_puerto,"Truncar",comentario_empresariales)
    conector(sql_borrar_t_rbs_x_puerto,"Truncar",comentario_rbs)
    conector(sql_borrar_t_resumen_servicios_tlk,"Truncar", comentario_resumen)

    #--------Cargo t_id_nodo_slot_puerto-----#

    sql = "insert into  t_id_nodo_slot_puerto ( id_tlk, nombre_gestion, slot_nodo, puerto_nodo ) SELECT id_tlk, nombre_gestion, slot_nodo, puerto_nodo from  t_reporte_puertos_telelink GROUP by id_tlk;"
    desc_sql="Carga tabla t_id_nodo_slot_puerto"
    conector(sql,"insert",desc_sql)

    #--------Cargo tabla cantidad ONT por puerto  ------------------#
    sql = "insert into t_wf_x_puerto (id_tlk,wf_x_puerto) SELECT t.id_tlk, count(t.estado_ont_tlk) as wf FROM `t_reporte_puertos_telelink` t WHERE t.estado_ont_tlk = 20  GROUP by t.id_tlk;"
    desc_sql ="Carga cantidad wf por puerto"
    conector (sql,"insert",desc_sql)

    #-------Cargo tabla cantidad servicios de datos por puerto -----------------#

    sql = "insert into t_datos_x_puerto (id_tlk,datos_x_puerto) SELECT t.id_tlk, count(t.estado_ont_tlk) as wf FROM t_reporte_puertos_telelink t WHERE t.estado_ont_tlk = 20 and t.datos_ont_tlk=1 GROUP by t.id_tlk;"
    desc_sql ="Carga cantidad servicios de datos por puerto"
    conector (sql,"insert",desc_sql)

    #-------Cargo tabla cantidad servicios de empresariales por puerto -----------------#

    sql = "insert into t_empresariales_x_puerto (id_tlk,empresariales_x_puerto) SELECT t.id_tlk, count(t.estado_ont_tlk) as wf FROM t_reporte_puertos_telelink t WHERE t.estado_ont_tlk = 20 and t.empresarial_ont_tlk=1 GROUP by t.id_tlk;"
    desc_sql ="Carga cantidad servicios empresariales por puerto"
    conector (sql,"insert",desc_sql)

    #-------Cargo tabla cantidad servicios de rbs por puerto -----------------#

    sql = "insert into t_rbs_x_puerto (id_tlk,rbs_x_puerto) SELECT t.id_tlk, count(t.estado_ont_tlk) as wf FROM t_reporte_puertos_telelink t WHERE t.estado_ont_tlk = 20 and t.rbs_ont_tlk=1 GROUP by t.id_tlk;"
    desc_sql ="Carga cantidad radiobases por puerto"
    conector (sql,"insert",desc_sql)

    # -------Cargo la tabla resuemen de servicios por puerto ----------------- #

    sql = "INSERT INTO t_resumen_servicios_tlk (id_tlk,WF,Datos,Empresariales, RBS) SELECT t_id_nodo_slot_puerto.id_tlk,IFNULL (t_wf_x_puerto.wf_x_puerto,0) AS WF , IFNULL (t_datos_x_puerto.datos_x_puerto ,0 ) AS DATOS,IFNULL (t_empresariales_x_puerto.empresariales_x_puerto ,0 ) AS EMPRESARIALES,IFNULL (t_rbs_x_puerto.rbs_x_puerto ,0 ) AS RBS FROM t_id_nodo_slot_puerto LEFT JOIN t_wf_x_puerto on t_wf_x_puerto.id_tlk = t_id_nodo_slot_puerto.id_tlk LEFT JOIN t_datos_x_puerto on t_datos_x_puerto.id_tlk = t_id_nodo_slot_puerto.id_tlk LEFT JOIN t_empresariales_x_puerto on t_empresariales_x_puerto.id_tlk = t_id_nodo_slot_puerto.id_tlk LEFT JOIN t_rbs_x_puerto on t_rbs_x_puerto.id_tlk = t_id_nodo_slot_puerto.id_tlk;" 
    desc_sql ="llenado tabla resuemen servicios por it_tlk"
    conector (sql,"insert",desc_sql)

    logger.info('Se termino de cargar BD ')

    ######### Fin Carga Tablas  y servicios por puerto ##############


#Pusheo zabbix

def pusheo_crudos_diarios_PON():
    """ Insert de archivo pickle a la BD (PON/Uplink).

    Comienza logeando el inicio de la tarea, llamando a conector y pasando sql que truncan tablas
    donde se insertaran los datos del dia.

    Abre el archivo pickle marcado en direcciones, este archivo se "despiklea" en una lista de tuplas.

    Para no sobrecargar la BD con inserts, se iteran 100 mil valores en la lista, se cargan a una nueva lista,
    y esta utlima es la insertada en la BD en la tabla crudos_diarios. Para esto se llama conector
    con el comando "many". La lista se limpia una ves insertado y se vuelven a cargar 100 mil valores mas.
    
    Al final se hace un ultimo insert para los valores que no llegan a iterar otro ciclo de 100 mil valores.

    Tambien se logea la finalizacion de la tarea.

    :returns: Esta funcion no tiene retornos.
    """
    logger.info("Comienza pusheo de crudos diarios PON")
    conector(sql_truncate_cdiarios_PON,"Truncate","Truncando crudos diarios PON")
    #variables que uso mas adelante y consulta sql
    contador_insert = 0
    lista_final = []
    contador_final = []
    #

    with open (direcciones.archivo_pickle_PON(), 'rb') as lista:
        #carga de lista
        lista_tuplas = pickle.load(lista)
        #

    for dato in lista_tuplas:
        lista_final.append(dato)
        contador_insert = contador_insert + 1
        if contador_insert == 100000:
            conector(sql_push_diarios_PON, "many", "Insert de crudos diarios PON.", lista_final)
            contador_final.append(contador_insert)
            contador_insert = 0
            lista_final.clear()

    conector(sql_push_diarios_PON, "many", "Insert de crudos diarios PON.", lista_final)
    contador_final.append(contador_insert)

    logger.info("Finalizo pusheo de crudos diarios PON. Se ingresaron {} columnas".format(sum(contador_final)))


def pusheo_crudos_diarios_ONT():
    """ Insert de archivo pickle a la BD (PON).

    Comienza logeando el inicio de la tarea, llamando a conector y pasando sql que truncan tablas
    donde se insertaran los datos del dia.

    Abre el archivo pickle marcado en direcciones, este archivo se "despiklea" en una lista de tuplas.

    Se llama a conector pasando la lista junto con el comando "many" para insertar los datos en
    crudos_diarios_ONT. 

    Por ultimo se logea la finalizacion de la tarea.

    :returns: Esta funcion no tiene retornos.
    """
    logger.info("Comienza pusheo de crudos diarios ONT")
    conector(sql_truncate_cdiarios_ONT,"Truncate","Truncando crudos diarios ONT")
    #carga el pickle
    with open (direcciones.archivo_pickle_ONT(), 'rb') as lista:
        lista_tuplas = pickle.load(lista)

    #pusheo a BD
    conector(sql_push_diarios_ONT, "many", "Insert de crudos diarios ONT", lista_tuplas)
    logger.info("Finalizo pusheo de crudos diarios ONT")


