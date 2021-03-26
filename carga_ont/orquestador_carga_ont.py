#!/usr/bin/python
import logger
import sys

from llamadas import get_rbs, ont_check, host_get, get_inter_id, get_app_id, get_oid, create_ont, get_name, get_zabbix_key, create_graph, get_name_auto
from sesiones import autorizar, logout
""" ###Creacion Manual/Automatica de ONT en Zabbix

A partir del metodo con el que se llama a *orquestador_carga_ont()* se chequea
la existencia de ONTs en Zabbix, y se crean items  y graficas para monitorearlas.

Gran parte del proceso se hace con funciones importadas de llamadas, estas pueden
utilizar la Zabbix API para devolver valroes utiles.

Parte del proceso conlleva utiilizar datos guardados en **api.pyc**. Decidimos utilizar un
archivo compilado para que no sea leibles por IDEs informacion de usuarios pertinentes
a nuestro despliegue de zabbix.

Contiene la funcion **orquestador_carga_ont**.
"""

def orquestador_carga_ont(metodo):
    """***Creacion Manual/Automatica de ONT en Zabbix***
    En resumen, para **crear una ONT** se necesita un Item RX, otro TX y una grafica que agrupe los dos.  
    Para crear uno de estos items necesitamos obtener los siguentes valores:  

    * **nombre:** Surge a partir de un formato que agrupa un tag (**"Radio Base"/"ONT"**), **puerto** y **etiqueta de gestion**.  
    * **zkey:** Key del item en zabbix, existe para RX y TX, se genera concatenando una string base a el puerto.  
    * **hostid:** Se obtiene a partir del nombre del nodo en Zabbix.  
    * **inter_id:** Numero que identifica la interfaz SNMP dentro del nodo en Zabbix.  
    * **oid:** Direccion SNMP a la que Zabbix consultara la nodo el trafico de la ONT. Se genera a partir de cruces
    de puerto con datos fijos proporcionados por el vendor.  
    * **appid:** Numero que identifica la APP ONT dentro del nodo. Esto es un tag que facilita el filtro de items
    dentro del propio zabbix.  
    * **llave:** API Key para hacer las consultas a la api de zabbix. Se genera desde un usario con privilegios en la
    api.
    
    Para **crear las graficas** de estos items requerimos:  

    * **nombreg:** Es la misma variable que nombre, pero sin referirse a una direccion de trafico especifica(la grafica
    muestra ambas direcciones).  
    * **itemid_1 y 2:** ID de los item creados en Zabbix. Debemos tener un ID que corresponde al item creado para cada
    direccion.  
    * **llave:** API Key para hacer las consultas a la api de zabbix. Se genera desde un usario con privilegios en la
    api.

    Estos valores o la comparacion de la existencia de las ONT aveces requieren datos intermedios a recolectar desde
    zabbix, debajo se explica en detalle el proceso seguido por esta funcion.

    Dependiendo del metodo con el que se llame a la funcion, se ejectuan los siguentes
    procedimientos:

    * **Auto**:
        * Se logea comienzo de la tarea, ademas se crean variables y listas utilizadas
        para la comparacion de ONT a crear en Zabbix.  
    
        * Se carga la llamada de *autorizar()* en *llave*, esta contiene la Zabbix API Key utilizada
        mas adelante en las llamdas a la API. *lista_rbs* contendra todas las rbs de gestion al
        momento de ejecutar el script, para esto utiliza *get_rbs()*. La variable *contador_break*
        se deja definida pero no esta en uso.
    
        * Comienza a iterarse sobre *lista_rbs* y se asigan las variables nodo y puerto (**SLOT/PUERTO/ONT**).
        Si la str al final de nodo no es Z, se descarta la ONT, se logea el descarte y crece el **contador
        descartes**. 
        
        * De pasar el filtro, *hostid* obtiene dicho ID llamando a *host_get()* con el nombre del nodo y la API Key.  
        Host ID identifica el nodo en zabbix. *inter_id* obtiene el Interface ID llamando a *get_inter_id()* con el
        host id obtenido anteriormente y la API Key. Interface ID identifica la interfaz SNMP dentro del nodo.  
        *Interface_id* tambien trae la IP del nodo en gestion (la utilizada en la interfaz SNMP en zabbix). Esta
        ultima se carga en la variable *IP*. Se levanta una exepcion si *inter_id* no trae la key ip, esto significa
        que o faltan datos en zabbix, o algo fallo en la consulta a la API.
        
        * *oid* llama a *get_oid()* pasando vendor y puerto para obtener un dic con las OID necesarias para monitorear la ONT.  
        
        * *Etiqueta* simplemente es un valor ya presente en la consulta del registro de gestion con *get_rbs()*.  
        
        * *Nombre* contendra un dic con los nombres de ambos item de la ONT (RX y TX), se llama *get_name()* con
        un tag identificador **"Radio Base"**, **puerto** y **etiqueta**. zkey llama a get_zabbix_key() con puerto para obtener un dic
        con las Key RX y TX que utilizara cada item de la ONT.  
        
        * *comparador* es una variable de str concatenadas, utiliaza en un if posterior para chequear que no hay ONT repetidas en
        el listado de gestion. *appid* llama a *get_app_id()* con el host id obtenido y la API key, esto trae el Application ID
        correspondiente a la APP ONT configurada en el nodo con la mencionada Host ID. El App ID es una forma facil de
        identificar que tipo de item es la ONT dentro de zabbix (diferenciar puertos pon de ont).  
        
        * Luego de comparar si hay rbs repetidas se chequea si la ont ya existe en zabbix, para esto chequeo llama a la funcion
        *ont_check()*, donde *key_* elige de que forma se chequea (en este caso por Item Key), hostid es el nodo donde comprobar
        la existencia de la Item Key (cada item key es unica por nodo), **zkey["RX"]** es la key a busca en el nodo y llave la 
        API Key.  
        
        * Si *chequeo()* devuelve 0 se logea informacion de la ONT a cargar, se suma 1 a faltante (para contar cuantas
        ont se ingresaron), y se crean los Item de RX y TX con las variables *item_1/2*. Estas variables llaman a *create_ont()*
        con *nombre,zkey,oid* y la *direccion* del item como llave (Ej:**["RX"]**); *hostid* sera el nodo donde crear los item, 
        **inter_id["inter_id"]** señala que los item pertenecen a la interfaz SNMP del nodo, por ultimo *appid* es la APP ONT del nodo
        donde se estan creando los Items y *llave* la API Key.  
        
        * *nombreg* es nombre pero sin la farte donde se señala direccion del item. Las graficas en zabbix al contener RX y TX, no
        tienen una direccion especifica como nombre. La llamada a *create_graph()* creara las graficas para *item_1/2* con *nombreg*
        como nombre utilizando la AIP Key. 

        * Si *chequeo* da 1, signifca que la ONT ya existe en Zabbix y no sera creada. Esta ONT se suma a la lista *comparador* para
        poder logear un total de ONTs que no se crearon.  
        Por ultimo se logean ONT encontradas, repetidas, sin encontrar y descartadas, ademas de llamar a *logout()* con la *llave* 
        para dar de baja la API Key. De lo contrario se acumularian estas llaves cada ves que se ejecuta la maniobra.  

    * **Manual**: 
    
        * El flujo del procedimiento es igual al de auto, pero se agregan inputs y los chequeos son mas directos. Solo
        se señalan diferencias importantes.  

        * *opcion* es un input para definir parte del tag del nombre del item a crear, 1 Escribe **"ONT :"**, 2 escribe **"Radio Base :"**.
        Esto se define en la variable tipo, concatenada mas adelante al momento de crear el nombre del item. Para nodo tambien
        se ejecuta un input pidiendo el nombre del nodo como se registra en gestion. Mismo caso para puerto donde se espera un
        formato **SLOT/PUERTO/ONT**.
        
        * *opcion_e* permite ingresar la etiqueta de gestion a mano, precionado 1. De precionar enter el sistema busca automaticamente
        la etiqueta ejecutando un SNMP Walk desde Zabbix-Server. Si ya contamos con la etiqueta y podemos evitar este procedimiento,
        mejor. A partir de esto nombre se crea con la etiqueta ingresada a mano o con la extraida con el Walk. Se levanta una exepcion
        en caso de que no se pueda hacer el Walk al puerto ingresado o conteste un error, en este caso se da de baja la API key y se 
        debe reinicar el procedimiento.

        * Se chequea la existencia de la ONT de la misma forma que el procedimiento automatico, y se realizan las mismas acciones de
        creacion de Items y graficas con sus correspondientes logeos. Por ultimo hay una exepcion general de ocurrir un error en cualquier
        parte del proceso.

    **param metodo:** Define si se ejecuta el proceso **manual** o **auto** para la creacion
    de ONTs en Zabbix.  
    **type metodo:** str

    **returns:** Esta funcion no tiene retornos.
    """

    if metodo == "manual":
        try:
            logger.info("Comienza la carga manual de ONTs")
            opcion = int(input("Carga: \n 1- ONT \n 2- ONT con RBS\n"))
            while opcion > 2 or opcion < 1:
                print("Opcion incorrecta \n")
                opcion = int(input("Carga: \n 1- ONT \n 2- ONT con RBS\n"))
            else:
                if opcion == 1:
                    tipo = "ONT"
                elif opcion == 2:
                    tipo = "Radio Base"
            nodo = input("Ingrese nombre de nodo en Gestion:\nEjemplo: AGUADA-13Z\n")
            puerto = input("Ingrese Slot/Puerto/ONT:\nEjemplo: 17/1/4\n")
            llave = autorizar()
            hostid = host_get(nodo,llave)
            inter_id = get_inter_id(hostid,llave)
            ip = inter_id["ip"]
            oid = get_oid("zte",puerto)
            opcion_e = input("Ingrese 1 para ingresar etitquetas, sino precione enter para continuar\n")
            if opcion_e == "1":
                etiqueta = input("Ingrese la etiqueta:\nEjemplo: GP0801-22024459-PINAZO-MORAN\n")
                nombre = get_name(tipo,puerto,etiqueta)
            else:
                try:
                    nombre = get_name_auto(ip,oid["oid_etiqueta"],puerto,tipo)
                except IndexError as ee:
                    print("ERROR: No se pudo generar nombre para {}".format(nodo,"/",puerto))
                    logout(llave)
                    raise SystemExit(0)
            zkey = get_zabbix_key(puerto)
            appid = get_app_id(hostid,llave)
            chequeo = ont_check("key_",hostid,zkey["RX"],llave)
            if chequeo == 0:
                logger.info(str(nodo)+(" ")+str(zkey))
                logger.info(str(nombre))
                logger.info("******")
                itemid_1 = create_ont(nombre["RX"],zkey["RX"],hostid,inter_id["inter_id"],oid["oid_rx"],appid,llave)
                itemid_2 = create_ont(nombre["TX"],zkey["TX"],hostid,inter_id["inter_id"],oid["oid_tx"],appid,llave)
                nombreg = nombre["RX"][:-5]
                create_graph(nombreg,itemid_1,itemid_2,llave)
                print("Los item de ONT {} en el nodo {} deberian estar creados.".format(nombre,nodo))
                logout(llave)
            elif chequeo == 1:
                print("ERROR: La ONT {} con puerto {} ya esta siendo monitoreada en el nodo {}".format(nombre,puerto,nodo))
                logout(llave)
        except TypeError as e:
            print("El nodo {} o puerto {} no existen en Zabbix".format(nodo,puerto))
            logout(llave)
    elif metodo == "auto":
        logger.info("Comienza la carga automatica de ONTs")
        lista = []
        repetidas = []
        faltante = 0
        encontrado = 0
        descarte = 0
        llave = autorizar()
        lista_rbs = get_rbs()
        contador_break = 0
        for rbs in lista_rbs:
            nodo = rbs[0]
            puerto = str(rbs[2]) + "/" + str(rbs[3]) + "/" + str(rbs[4])
            if rbs[0][-1] != "Z":
                logger.info("Se descarto la ONT {} {}".format(nodo,puerto))
                logger.info(rbs[0])
                descarte = descarte +1
                pass
            else:
                hostid = host_get(nodo,llave)
                inter_id = get_inter_id(hostid,llave)
                try:
                    ip = inter_id["ip"]
                except TypeError as e:
                    faltante = faltante + 1
                    pass
                oid = get_oid("zte",puerto)
                etiqueta = rbs[1]
                nombre = get_name("Radio Base",puerto,etiqueta)
                zkey = get_zabbix_key(puerto)
                comparador = str(nodo)+str(zkey["RX"])+str(hostid)
                appid = get_app_id(hostid,llave)
                if comparador in lista:
                    repetidas.append(comparador)
                else:
                    chequeo = ont_check("key_",hostid,zkey["RX"],llave)
                    if chequeo == 0:
                        if contador_break >= 3:
                            break
                        logger.info(str(nodo)+(" ")+str(zkey))
                        logger.info(str(nombre))
                        logger.info("******")
                        lista.append(comparador)
                        faltante = faltante + 1
                        itemid_1 = create_ont(nombre["RX"],zkey["RX"],hostid,inter_id["inter_id"],oid["oid_rx"],appid,llave)
                        itemid_2 = create_ont(nombre["TX"],zkey["TX"],hostid,inter_id["inter_id"],oid["oid_tx"],appid,llave)
                        nombreg = nombre["RX"][:-5]
                        create_graph(nombreg,itemid_1,itemid_2,llave)
                    elif chequeo == 1:
                        encontrado = encontrado + 1
                        lista.append(comparador)

        logger.info("{} ONTs encontradas,{} repetidas, {} sin encontrar y {} descartadas".format(encontrado,len(repetidas),faltante,descarte))
        logout(llave)
        

# ###Menu
""" Menu para llamar a *orquestador_carga_ont()* con variables de sistema al ejectutar
**orquestador_carga_ont.py**.

* **auto** ejecuta la carga automatica de ONTs a Zabbix.  
* **manual** despliega inputs para crear una ONT a mano.
"""
if sys.argv[1] == "auto":
    orquestador_carga_ont("auto")
elif sys.argv[1] == "manual":
    orquestador_carga_ont("manual")