SELECT pd.tipo, pd.nodo, pd.puerto, pd.direccion, pd.fecha, pd.hora, pd.promedio as promediohora, promediopicos, pd.pico 
FROM picos_diarios pd
INNER JOIN
	(SELECT puerto, direccion, nodo, AVG(pico) as promediopicos, MAX(pico) as MaxPico
    FROM picos_diarios
    GROUP BY puerto, direccion,nodo) groupedpd
ON pd.puerto = groupedpd.puerto
and pd.direccion = groupedpd.direccion
and pd.nodo = groupedpd.nodo
and pd.pico = groupedpd.MaxPico
and promediopicos = groupedpd.promediopicos order by pico DESC limit 10;