#IMPORTO EL CONECTOR Y LOGGER DE REFACTOR
import sys
sys.path.append("./reportes/Refactor")
from conector import conector

def get_rbs():
    sql = "SELECT `nodo`,`etiqueta_ont`,`slot`,`puerto`,`ont` FROM `t_servicios_RBS`"
    rbs = conector(sql,"select","Consultando ONTS")
    return rbs

def get_rbs_tlk():
    sql ="SELECT `id_tlk`, `nro_ont` FROM `t_reporte_puertos_telelink` WHERE `rbs_ont_tlk` > 0"
    rbs = conector(sql,"select","Consultando ONTS de TLK")
    return rbs