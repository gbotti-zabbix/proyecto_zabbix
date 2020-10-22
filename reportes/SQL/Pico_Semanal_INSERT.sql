insert into picos_semanales (tipo, nodo, puerto, direccion, hora, fecha, promedio, pico) select t1.tipo, t1.nodo, t1.puerto, t1.direccion, t1.hora,
t1.fecha, t1.promedio, t1.pico
                from ( select t2.*, row_number() over (partition by t2.tipo, t2.nodo, t2.puerto, t2.direccion order by t2.pico desc) as rn from picos_diarios
    t2
)t1 where t1.rn =1;

