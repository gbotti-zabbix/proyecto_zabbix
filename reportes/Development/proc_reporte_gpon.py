#archivo que lee el archivo PLN245_procesado.TXT, parsea y  lo guarda en la tabla t_reporte_puertos_telelink
import pickle
import csv
from datetime import datetime
from diccionario_tlk_gestion import f_nombre_gestion


def analizar_equ_tlk(equipo):
    nro_modelo = equipo[0:2]
    #print (nro_modelo)
    #diccionario modelos
    modelo = {"70":"C300","71":"MA5600T","72":"C320","73":"MA5800","74":"ISAM FX"}
    if nro_modelo not in modelo:
        #print (equipo)
        return ("NULL")
    return (modelo[nro_modelo])

def FileCheck(fn):
    try:
      open(fn, "r")
      return 1
    except IOError:
      print ("Error: Archivo no Existe.")
      return 0



def f_parsear_inventario ():

    
    #--- Direcciones para producción---------#
    #nombre_archivo_origen = "/var/lib/reportes-zabbix/reporte_tlk/PLN245_procesado.TXT"
    #nombre_archivo_destino = "/var/lib/reportes-zabbix/reporte_tlk/PLN245_parseado.csv"
    #------------------------------------#


    #-----Direcciones para pruebas----#
    nombre_archivo_origen = "C:/Users/e066446/Documents/GitHub/proyecto_zabbix/PLN245_procesado.TXT"
    nombre_archivo_destino = "C:/Users/e066446/Documents/GitHub/proyecto_zabbix/PLN245_parseado.TXT"
    #------------------------------------#
    
    #--------chequeo existencia del archivo--------#
    
    try:
        result = FileCheck(nombre_archivo_origen)
        print( f'[{datetime.now()}] Chequeo archivo origen encontrado [True=1,False=0]: {result}')
    except Exception as e:
        print(f'[{datetime.now()}]Error: {str(e)}')
        sys.exit(1)
 

    #----------fin chequeo origen------------------#

    contador=0
    with open(nombre_archivo_origen,'r') as archivo:
        #archivo parseado
        with open(nombre_archivo_destino,"w", newline="") as archivo2:
            wr = csv.writer(archivo2, quoting=csv.QUOTE_ALL)
            archivo = archivo.read().splitlines()
            contador_salto=1 #contador solo para saltar primera línea
            for linea in archivo:
                if contador_salto > 1:
                    linea_parseada = linea.split (";")                          #divido linea a linea por punto y coma
                    #print (linea_parseada)
                    cod_telelink = linea_parseada[0][:10]                       # codigo TLK
                    nro_equipo = linea_parseada[1]                              # nro de equipo TLK completo    
                    tipo_equipo = analizar_equ_tlk(linea_parseada[1])           # cambio el 70 por c300    
                    nro_nodo = linea_parseada[1][2:4]                           #estraigo del numero equipo el nuermo de nodo
                    nombre_gestion= f_nombre_gestion(cod_telelink,int(nro_nodo),tipo_equipo)
                    slot = linea_parseada[1][5:7]                               #estraigo del numero equipo el nuermo de slot 
                    puerto = linea_parseada[1][7:9]                             #estraigo del numero equipo el nuermo de puerto    
                    ont =   linea_parseada[1][9:12]                             #estraigo del numero equipo el nuermo de ont
                    estado = linea_parseada[2]
                    desc_estado = linea_parseada[3].strip()
                    fibra_primaria = linea_parseada[4].strip()
                    linea_parseada[5]=linea_parseada[5].strip()
                    if  linea_parseada[5]=='':
                        par_fibra= "Null"
                    else:
                        par_fibra=int(linea_parseada[5])
                    # Se cheque empresarial, si el campo es I, si tiene VozF, Datos o RBS.
                    # Chequeo si hay empresarial    
                    if linea_parseada[6]=="I":
                        indicador_empresarial = 1
                    else:
                        indicador_empresarial = 0
                    # Chequeo si hay VozF
                    if linea_parseada[7]=="S":
                        indicador_voz = 1
                    else:
                        indicador_voz = 0
                    # Chequeo si hay Datos
                    if linea_parseada[8]=="S":
                        indicador_datos = 1
                    else:
                        indicador_datos =  0
                    # Chequeo si hay RBS
                    if  "MRBS" in linea_parseada[9:18]:
                        indicador_RBS = 1
                    else:
                        indicador_RBS = 0
                    
                    indice_unico = nombre_gestion +  "_" + str(int(slot)) + "/" + str(int (puerto))
                    linea_nueva= [indice_unico,cod_telelink,nro_equipo,tipo_equipo,nombre_gestion,nro_nodo,slot,puerto, ont, estado, desc_estado,fibra_primaria,par_fibra, indicador_empresarial, indicador_voz, indicador_datos, indicador_RBS] 
                    #print (linea_nueva)
                    wr.writerow(linea_nueva)
                contador_salto = contador_salto + 1 #solo elimina la primera linea
    #----------------------------------------------------
                contador = contador+1
    #descomentar para procesar 30 lineas
                #if contador == 5:
                #   break
    #------------------------------------------------------
    print( f'[{datetime.now()}] Se escribio el archvo : {nombre_archivo_destino} con {contador} lineas')   

