#!/usr/bin/python

import requests
import json

from direcciones_carga_ont import url
""" ###Request para Zabbix API

Recibe una *url* de Zabbix API y un *payload*, con estos datos hace un request http utilizando
el header seteado en encabezado.

Para cambiar la direccion de la API editar la variable *URL* importada desde **direcciones_carga_ont**.

Contiene la funcion **requester**.
"""

encabezado = {"Content-Type": "application/json-rpc"}

def requester(payload):
    """***Request HTTP a la API de zabbix***

    Se pasa un *payload* con el request post en formato JavaScript. Con este se hace un post a la API
    de zabbix seteada en la *URL*. Para que esta conteste es obligatorio pasar el header seteado
    en la variable *encabezado*.

    Retorna un dict(JSON) con la respuesta  de la API.
    
    **param payload:** String en JSON (JavaScript).  
    **type payload:** str

    **returns:** JSON con respuesta JavaScript al request realizado.  
    **rtype:** dict(JSON)
    """

    r = requests.post(url,headers=encabezado,json=payload)
    return r