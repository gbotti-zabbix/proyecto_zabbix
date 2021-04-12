### Intro

En la siguente documentaicion se explica que tareas cumple y como funciona el codigo desarrollado para Zabbix por parte de funcionarios de ACAF/DTD. 

El objetivo global de las aplicaciones desarrolladas es:
*  Generar reporortes de trafico de puertos PON y ONTs.
*  Cargar automaticamente ONTs con Radio Bases al Zabbix de ACAF/OyM.
*  Auditar distintas bases de datos.

Estos objetivos pueden ir creciendo en un futuro de requerirse implementar funcionaldiades que ACAF o Antel vean necesarias.

Se describe que herramientas se utilizan, como se cruza la informacion entre los sistemas pertinentes, y detalles del codigo explicito.

### El manual

En la barra lateral de navegacion se encuentran vinculos hacia el codigo explicito en python, acompañado de comentarios que permiten comprender mejor el funcionamiento de dicho codigo.

En esta pagina se describen detalles generalistas sobre el funcionamiento de la plataforma:

*   **Herramientas**: se aclara el software utilziado para crear las aplicaicones.
*   **Sistemas**: describe las plataformas utilizada para la recoleccion, procesamiento y almacenamiento de los datos pertinente a el objetivo fina ldel codigo. 
*   **Codigo**: Describe a grandes rasgos como funciona el codigo y como se deberian leer los scripts del menu lateral.
*   **Documentacion**: Como se creo esta documentacion y como mantenerla.
*   **Enlaces utiles**: Links a documentacion de utilidad.

### Herramientas
**Python**: Lenguaje de programacion utilizado para los scripts de las aplicaciones.
**VsStudio Code**: IDE utilizado para programar los script python entre demas cosas.
Modulos de VS Code utiles:
*   *Python*: Reconoce sintaxys python.
*   *ident-rainbow*: Colorea indentaciones para mejor lectura del codigo.
*   *GitLens*: Soporte git en el visor de repositorios.
*   *json*: Reconoce sintaxys json.
*   *Material Icon Theme*: Iconografia mas clara.
*   *MySQL Syntax*: Reconoce sintaxys sql.
*   *NDJSON Colorizer*: Reconoce sintaxys NDJson.
*   *VsCode NDJson*: Mejora de Colorizer.

Ninguno de estos modulos son necesarios, solo facilitan la tarea.

**Mysql WorkBench:** Aplicacion para manejo de BD. Util para testear consultas.
**Git:** Control de versiones.
**Git Desktop:** GUI para git.
**Navegador con PHP 7:** Para la correcta vizualiacion de Zabbix.
Extensiones utiles(Firefox):
*   *Rested*: Asistente para consultas php. Util para testear Zabbix API.

### Sistemas
El codigo depende de los siguentes sistemas para funcionar. Se recomienda tenner un conomiento general de como se generan y accede a los datos de estos.

*   **Zabbix 4.0+:** Toma las medidas con las que generar el reporte y las guarda en un archivo con formato NDJSON. Tambien se interviene sobre la API para crear ONTs con RBS a monitorear. El codigo esta testeado con versiones 4.0.2 y 5.0.2 de Zabbix. 
*   **Telelink:** Archivos crudos con le invnetario de puertos PON. En la actualidad, semanal.
*   **Gestion:** Reporte de etiquetas extraido de la red de gestion, realizado por Ocampo.
*   **MariaDB 10.8+:** Base de datos MySQL donde se guardan y cruzan datos utiles para reportes. Los scripts de reportes mueven los datos de TLK, Zabbix y gestion hacia esta.

### Codigo
##### Formato de comentarios en codigo (Help())
En la pagina actual, sobre la barra izquerda se encuentran los enlaces al codigo de los script. En estas paginas encontrara, sobre la derecha el codigo explicito y sobre la izquierda explicaciones detallas de este. Estas explicaciones son el Help() de las funciones, por lo que si se llama a estos, deberia traer el mismo contendio (con el HTML MarkDown). 

En estas paginas no se mostrara informacion de usuarios o contraseñas utilzados. Para esta informacion consultar los manuales de Zabbix ACAF.

En las explicaciones de la izquierda, puede que se encuentre con la siguente nomenclatura:
* **Negrita**: Ejemplos, modulos, nombres de archivos. Tambien marcan retornos y tipos de parametros en las funciones (returns, type) ademas de algunos subtiulos.
* *Cursivas*: Variables, funciones, objetos, metodos, consultas sql. De ser funciones/objetos/metodos se acompaña la palabra con ().
* ***Negrita/Cursiva***: Resumen de la funcion.

##### Python Requeriments
Modulos de python necesarios para trabajar y testear el codigo.
***Enlace a requeriments.txt***

##### Funcionamiento
El codigo se separa en 3 aplicaciones. Por aplicaciones nos referimos a un conjunto de scripts (por lo general en python) que realizan varias tareas. 
Estas tres aplicaciones son:

*   **Auditorias de TLK/Gestion/Zabbix**
    >Este codigo no requiere de orquestacion, es ejcutado por llamdas desde el cron en fechas pertinentes. Este cron es manejado por el root de la VM reportes.
    Los scripts consultas y direcciones brindan recursos a los dos scripts de auditoria.

    * ***auditorias_ONT.py*** compara las ONTs con RBS registradas en el listado de gestion contra las de TLK. Ambos listados se cargan previamente a la Base de Datos de reportes a partir de los scripts de reportes.
    * ***auditorias_PON.py*** compara los puertos PON monitoreados por Zabbix contra los registrados en TLK. Ambos listados se cargan previmanete a la Base de Datos de reportes a partir de los scripts de reportes.
    * ***consultas .py*** consultas utilizadas por los script de auditorias para consutlar y comparar los datos en la BD de reportes.
    * ***direcciones_auditorias.py*** contiene directorios y listados utiles al momento de escribir los datos audtiados.

*   **Carga de ONTs a Zabbix**
    >   Se busca cargar automaticamente RBS por ONT a monitorear en Zabbix. El cron de root en la VM de reportes llama al ***orquestador_carga_ont.py***, el cual gestiona la carga manual o automatica de estas RBS mediante la API de Zabbix a partir de un listado proveniente de Gestion y cargado a la BD de reportes mediante los script de reportes.

    >    A grandes rasgos la diferencia entre la carga manual y automatica de ONTs con RBS es que una es llamada por el cron y surge de un listado (automatica) y la otra solicita algunos datos de la ONT a cargar (manual). Este ultimo tambien esta pensado para cargar ONT sin RBS. La creacion de las ONT se hace mediante la API de Zabbix.
    
    >   El orquestador utiliza ***requester. py*** para enviar las operaciones a la API, y ***llamadas .py*** para crear y formatear estas operaciones(formateo JSON), ademas de hacer algunas consultas a la BD para obtener los listados de ONT con RBS a ingersar.
    
    >   ***sesiones_manual*** crea una llave para utilizar la API a partir de usuario y contraseña de la plataforma, mientras que ***sesiones .py*** lo hace de forma manual con un usuario y contraseña seteados a fuego en api.pyc (no visible en la docuemtnacion). Sin estas llaves, la API de Zabbix no acepta las peticiones.
    
    >   ***direcciones_carga_ont.py*** cueta con directorios y urls utiles para el procedimiento y ***logger. py*** registra las operaciones en un log.

    * ***direcciones_carga_ont.py*** directorios y direcciones utiles para los scripts.
    * ***llamadas. py*** formatea consultas hacia la Zabbix API y reportes DB.
    * ***logger. py*** logea el procedimiento.
    * ***orquestador_carga_ont.py*** coordina el funcionamioento de la aplicacion llamado a los scripts correspondientes para cada paso.
    * ***requester. py*** envia las consultas de ***llamadas .py*** hacia la API.
    * ***sesiones_manual.py*** genera una API Key a partir de usuario y contraseña de Zabbix.
    * ***sesiones. py*** genera una API Key a partir de un usuario y contraseña seteado en ***api .pyc***(scipt no docuemntado).

*   **Reportes de Puertos PON/ONT entre Zabbix/TLK/Gestion**
    >   El objetivo final de la aplicacion es generar reportes .xlsx con informacion de trafico de todos los puertos PON y ONT monitoreados por el Zabbix de ACAF/OyM ademas de sumarle informacion de TLK y/o gestion. Los reportes reflejan periodos semanales y mensuales separandolos por tecnologia (ONT o PON).

    >   La aplicacion parsea archivos crudos de trafico generados por Zabbix, archivos de inventario de TLK utilizados en Ritaf y reportes de gestion, y los inserta en una base de datos MYSQL para su futuro procesamiento. Con estos datos se hacen maniobras periodicas para generar filtros semanales y mensuales con los que finalmente se crean los reportes en archivos excel .xlsx.
    
    >   ***orquestador_reportes.py*** corre como un deamon, en un loop infinito donde chequea dias y horas para ejecturar distintas tareas utilizando los demas scripts. Como lo dice el nombre, orquesta todas las tareas de la aplicacion. El ***orquestador_reportes_manual.py*** ejecuta tareas en un orden parecido, pero en ves de entrar en un loop, pide fechas especificas para buscar crudos y realizar los reportes a medida. Por lo genera el orquestador manual se utiliza cuando fallo la carga automatica por alguna falla del codigo.
    
    > ***parseo .py*** se encarga de formatear el archivo crudo de Zabbix (NDJSON), el inventario crudo de TLK y gestion (ambos csv), y descartar valores inecesarios o medidas erroneas. Terminado esto, vuelca los datos a un archivo .pickle para los datos de Zabbix, y csv para los de TLK/Gestion. ***pusheo. py*** toma los archivo .pickle y csv parseados para insertarlos en la BD alojada en la VM de reportes.
    
    > ***conector. py*** es una "interfaz" para realizar consultas a la BD de reportes. No solo realiza las query, de ser necesario devuelve los resultados (si esta generara datos de respuesta). En ***consultas. py*** estan las query sql pertinentes para la realizacion de los reportes. Se utilizan querys de trunks, selects e inserts para procesar los datos en fechas y horas correspondientes. ***flujos_db.py*** toma las consultas de ***consultas .py*** y las ordena para que sean ejecutadas de formas especificas (por tecnologia, periodo, etc). De esta forma los datos procesados se van insertando en entablas intermedias hasta que se forman las tablas finales desde donde se extraeran los datos a guardar en el archivo .xlsx. 
    
    > ***reporte .py*** orquesta las consultas a las tablas finales generadas por el codigo comentado en el parrafo anterior (consultas y flujos). Con estos datos genera los  archivos final .xlsx escribiendolos en un formato especifico, generando algunos filtros extra, y separando la informacion en distintas hojas para una mejor lectura.
    
    > ***direcciones .py*** contiene directorios, nombres de archivos utiles y algunas listas utilizadas para filtros en el codigo. ***logger .py*** registra en archivos log las operaciones de la aplicacion.

    * ***conector. py*** transfiere consultas a la BD, de ser necesario devuelve resultados.
    * ***consultas. py*** querys sql necesarias para generar los datos finales para los reportes.
    * ***direcciones. py*** contiene directorios, nombres de archvos y listas utiles para los script.
    * ***flujo_db. py*** oredena las consultas por periodos y/o tecnologias.
    * ***logger. py*** registra las tareas realizadas por los script.
    * ***orquestador_reportes_manual.py*** realiza las mimas tareas que el orquestador, pero a partir de fechas pasadas por el usuario. Es normalmente utilizado cuando el codigo automatico falla.
    * ***orquestador_reportes.py*** orquesta y coordina todos los script pertinentes a los reportes. Llama las funciones en ordenes especificos para asegurarse la generacion de reportes mensuales y semanales por tecnologia.
    * ***parseo. py*** toma datos crudos de Zabbix, TLK y gestion, y los parsea en formatos utiles para los reportes y faciles de cargar en la BD de reportes.
    * ***pusheo. py*** toma los datos parseados por ***parseo .py*** y los inserta en la BD.
    * ***reporte. py*** genera los archivos .xlsx finales a partir de los datos procesados en la BD.

### Documentacion

El codigo se documenta utilizando lenguaje HTML Mark Down para los help() de las funciones, objetos y scripts.

Luego se utiza pycco para generar los archivos HTML a partir de los archivos.py con el formato que la documentacion actual presenta. Este formato es automatico propio de pycco. Para agilziar la tarea se utiliza Watchdogs para python al momento de ejecutar pycco, generando los archivo html cada ves que realizamos un cambio en el codigo.

Por ultimo este indice se hizo con un make html generico de Sphinx y se adaptaron los vinculos y retirarnon herramientras de busqueda no necesarias.

Todo se guarda en el repositorio de python junto con el codigo. Tambien se cuelga en github pages como pagina privada.

### Enlaces Utiles
* **Repo del proyecto**: https://github.com/zabbixacaf/proyecto_zabbix
* **Visual Studio Code**: https://code.visualstudio.com/
* **Mysql WorkBench**: https://www.mysql.com/products/workbench/
* **GitHub Desktop**: https://desktop.github.com/
* **Documentacion oficial de Zabbix**: https://www.zabbix.com/documentation/current/manual
* **Como documentar codigo con python**: https://realpython.com/documenting-python-code/
* **Generalidades sobre git**: https://guides.github.com/introduction/git-handbook/
* **Curso basico de python**: https://www.udemy.com/course/python-3-al-completo-desde-cero/