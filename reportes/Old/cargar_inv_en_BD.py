import mysql.connector
import logging
import sys
from datetime import datetime

#importar variable
import cfg_reportes


#CONECTOR BD 

def ejecutar_sql(sql,tipo_sql):
    try:
        #---CONEXION PARA TEST!!!!!!!!!!!!##########
        mydb = mysql.connector.connect(host=cfg_reportes.host_DB,user=cfg_reportes.user_DB,password=cfg_reportes.password_DB,database=cfg_reportes.database_DB)
        logging.info( f' Connected to DB: {tipo_sql}')
        # Create cursor and execute Load SQL
        cursor = mydb.cursor()
        cursor.execute(sql)
        logging.info (f' Succuessfully loaded: {cursor.rowcount} affected rows ')
        mydb.commit()
        mydb.cursor().close()
        mydb.close()

    except Exception as e:
        logging.error (f'Error 22: {str(e)}')
        sys.exit(1)
   




def f_cargar_inv_en_BD (archivo_destino):

    nombre_archivo_destino = archivo_destino

    #=========================================#
    #     Cargar Datos desde archivo          #
    #=========================================#
    # primero borro talbla y luego cargo archivo
    sql_borrar_t_reporte_puertos_telelink = 'TRUNCATE t_reporte_puertos_telelink;'
    comentario_sql= "borrar_t_reporte_puertos_telelink"
    ejecutar_sql(sql_borrar_t_reporte_puertos_telelink,comentario_sql)
    
    sql_cargar_PLN = "LOAD DATA INFILE \'"+nombre_archivo_destino+"\' INTO TABLE t_reporte_puertos_telelink FIELDS TERMINATED BY \',\' ENCLOSED BY \'\"\' LINES TERMINATED BY \'\\r\\n\' ;"
    comentario_sql = "Cargar reporte telelink CSV paresado"
    ejecutar_sql(sql_cargar_PLN,comentario_sql)


    ############## Fin Cargo Datos archivo #######


    #===============================================#
    #   Carga Tablas  y servicios por puerto        #
    #===============================================#

    #-------- Borro todas las tablas-----#
    sql_borrar_t_id_nodo_slot_puerto = 'TRUNCATE t_id_nodo_slot_puerto;'
    comentario_id="Borrado_t_id_nodo_slot_puerto"

    sql_borrar_t_wf_x_puerto = 'TRUNCATE t_wf_x_puerto;'
    comentario_wf="Borrado_t_wf_puerto"

    sql_borrar_t_datos_x_puerto = 'TRUNCATE t_datos_x_puerto;'
    comentario_datos="Borrado_t_datos_puerto"

    sql_borrar_t_empresariales_x_puerto = 'TRUNCATE t_empresariales_x_puerto;'
    comentario_empresariales="Borrado_t_empresariales_puerto"

    sql_borrar_t_rbs_x_puerto = 'TRUNCATE t_rbs_x_puerto;'
    comentario_rbs="Borrado_t_rbs_puerto"

    sql_borrar_t_resumen_servicios_tlk = 'TRUNCATE t_resumen_servicios_tlk ;'
    comentario_resumen="Borrado_t_resumen"

    ejecutar_sql(sql_borrar_t_id_nodo_slot_puerto,comentario_id)
    ejecutar_sql(sql_borrar_t_wf_x_puerto,comentario_wf)
    ejecutar_sql(sql_borrar_t_datos_x_puerto,comentario_datos)
    ejecutar_sql(sql_borrar_t_empresariales_x_puerto,comentario_empresariales)
    ejecutar_sql(sql_borrar_t_rbs_x_puerto,comentario_rbs)
    ejecutar_sql(sql_borrar_t_resumen_servicios_tlk, comentario_resumen)

    #--------Cargo t_id_nodo_slot_puerto-----#

    sql = "insert into  t_id_nodo_slot_puerto ( id_tlk, nombre_gestion, slot_nodo, puerto_nodo ) SELECT id_tlk, nombre_gestion, slot_nodo, puerto_nodo from  t_reporte_puertos_telelink GROUP by id_tlk;"
    desc_sql="Carga tabal t_id_nodo_slot_puerto"
    ejecutar_sql (sql,desc_sql)

    #--------Cargo tabla cantidad ONT por puerto  ------------------#
    sql = "insert into t_wf_x_puerto (id_tlk,wf_x_puerto) SELECT t.id_tlk, count(t.estado_ont_tlk) as wf FROM `t_reporte_puertos_telelink` t WHERE t.estado_ont_tlk = 20  GROUP by t.id_tlk;"
    desc_sql ="Carga cantidad wf por puerto"
    ejecutar_sql (sql,desc_sql)

    #-------Cargo tabla cantidad servicios de datos por puerto -----------------#

    sql = "insert into t_datos_x_puerto (id_tlk,datos_x_puerto) SELECT t.id_tlk, count(t.estado_ont_tlk) as wf FROM t_reporte_puertos_telelink t WHERE t.estado_ont_tlk = 20 and t.datos_ont_tlk=1 GROUP by t.id_tlk;"
    desc_sql ="Carga cantidad servicios de datos por puerto"
    ejecutar_sql (sql,desc_sql)

    #-------Cargo tabla cantidad servicios de empresariales por puerto -----------------#

    sql = "insert into t_empresariales_x_puerto (id_tlk,empresariales_x_puerto) SELECT t.id_tlk, count(t.estado_ont_tlk) as wf FROM t_reporte_puertos_telelink t WHERE t.estado_ont_tlk = 20 and t.empresarial_ont_tlk=1 GROUP by t.id_tlk;"
    desc_sql ="Carga cantidad servicios empresariales por puerto"
    ejecutar_sql (sql,desc_sql)

    #-------Cargo tabla cantidad servicios de rbs por puerto -----------------#

    sql = "insert into t_rbs_x_puerto (id_tlk,rbs_x_puerto) SELECT t.id_tlk, count(t.estado_ont_tlk) as wf FROM t_reporte_puertos_telelink t WHERE t.estado_ont_tlk = 20 and t.rbs_ont_tlk=1 GROUP by t.id_tlk;"
    desc_sql ="Carga cantidad radiobases por puerto"
    ejecutar_sql (sql,desc_sql)

    # -------Cargo la tabla resuemen de servicios por puerto ----------------- #

    sql = "INSERT INTO t_resumen_servicios_tlk (id_tlk,WF,Datos,Empresariales, RBS) SELECT t_id_nodo_slot_puerto.id_tlk,IFNULL (t_wf_x_puerto.wf_x_puerto,0) AS WF , IFNULL (t_datos_x_puerto.datos_x_puerto ,0 ) AS DATOS,IFNULL (t_empresariales_x_puerto.empresariales_x_puerto ,0 ) AS EMPRESARIALES,IFNULL (t_rbs_x_puerto.rbs_x_puerto ,0 ) AS RBS FROM t_id_nodo_slot_puerto LEFT JOIN t_wf_x_puerto on t_wf_x_puerto.id_tlk = t_id_nodo_slot_puerto.id_tlk LEFT JOIN t_datos_x_puerto on t_datos_x_puerto.id_tlk = t_id_nodo_slot_puerto.id_tlk LEFT JOIN t_empresariales_x_puerto on t_empresariales_x_puerto.id_tlk = t_id_nodo_slot_puerto.id_tlk LEFT JOIN t_rbs_x_puerto on t_rbs_x_puerto.id_tlk = t_id_nodo_slot_puerto.id_tlk;" 
    desc_sql ="llenado tabla resuemen servicios por it_tlk"
    ejecutar_sql (sql,desc_sql)

    logging.info('Se termino de cargar BD ')

    ######### Fin Carga Tablas  y servicios por puerto ##############