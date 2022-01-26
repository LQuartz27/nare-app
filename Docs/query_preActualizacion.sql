--- Saca el Well ID

SELECT
well_id
FROM CD_WELL
WHERE well_common_name = 'URN 13' -- NOMBRE DEL POZO
---- Actualiza propiedades del Well a partir del Well ID y Tipo de Geometria
Update CD_WELL set

api_no = 'A-0'
,well_purpose = 'OIL PRODUCER'
,pumper_route = 'DESARROLLO'
,redrill_no = 'TIPO J' --Tipo de Geometria

WHERE well_id = 'Mj4YfwadTW' -- Well ID

---- Actualiza propiedades de los Eventos a partir del Tipo de Geometria, well ID y (TD - Altura de la mesa)



-- MOB



Update DM_EVENT set

event_code= 'MOB'
,event_type = 'MOVILIZACIÓN'
,event_objective_1 = 'TRANSPORTE DE EQUIPO A LOCACIÓN'
,event_objective_2 = 'ENTRE LOCACIONES E INICIAL PARA ODR Y OCM'
,event_objective_3 = 'TRANSPORTE DE EQUIPO A LOCACIÓN'
,event_reason = NULL
,actual_wci = 'DRLG'
,well_geometry = NULL
,service_type = 'PROACTIVE'
,budget_type = 'PROYECTADO/PROY'
,planned_wci = 'RIG'
,equip_type = 'EQ. DE PERFORACIÓN'
,event_team = NULL
,status_end = 'ACTIVO'
,primary_service_provider = 'MANSAROVAR ENERGY COLOMBIA LTD.'
,tvd_plugback = NULL
,tvd_current = NULL
,wta1 = NULL
,wellhead_connection = NULL
,wta2 = NULL
,wellbore_interface = NULL

WHERE event_code = 'MOV' AND well_id = 'Mj4YfwadTW' -- Well ID




---ODR
Update DM_EVENT set

event_type = 'PERFORACIÓN'
,event_objective_1 = 'DESARROLLO'
,event_objective_2 = 'DESARROLLO'
,event_objective_3 = 'DESARROLLO'
,event_reason = NULL
,actual_wci = 'DRLG'
,well_geometry = 'TIPO J' --Tipo de Geometria
,service_type = 'PROACTIVE'
,budget_type = 'PROYECTADO/PROY'
,planned_wci = 'RIG'
,equip_type = 'EQ. DE PERFORACIÓN'
,event_team = 'ACTIVO'
,status_end = 'ACTIVO'
,primary_service_provider = 'MANSAROVAR ENERGY COLOMBIA LTD.'
,tvd_plugback = '-463.3' --altura de la mesa NEGATIVA-
,tvd_current = '1672.1' --TD menos la altura de la mesa-
,wta1 = 'BM'
,wellhead_connection = NULL
,wta2 = NULL
,wellbore_interface = NULL

WHERE event_code = 'ODR' AND well_id = 'Mj4YfwadTW' -- Well ID


----WSV

Update DM_EVENT set

event_code= 'WSV'
,event_type = 'SERVICIO A POZO'
,event_objective_1 = 'MANTENIMIENTO DE EQUIPO DE BOMBEO MECÁNICO (BM)'
,event_objective_2 = 'CAMBIO DE BOMBA O COMPONENTES FONDO'
,event_objective_3 = 'MANT EQ BOMB MEC - CONVENCIONAL-BHA'
,event_reason = NULL
,actual_wci = 'PROD'
,well_geometry = 'TIPO J' --Tipo de Geometria
,service_type = 'PROACTIVE'
,budget_type = 'PROYECTO/GASTO'
,planned_wci = 'RIGLESS'
,equip_type = 'EQ. MEN DE SERVICIO'
,event_team = 'ACTIVO'
,status_end = 'ACTIVO'
,primary_service_provider = 'MANSAROVAR ENERGY COLOMBIA LTD.'
,tvd_plugback = '1672.1' --TD menos la altura de la mesa-
,tvd_current = '1672.1' --TD menos la altura de la mesa-
,wta1 = 'BM'
,wellhead_connection = NULL
,wta2 = NULL
,wellbore_interface = NULL

WHERE event_code != 'MOB' AND event_code != 'ODR' AND event_code != 'OCM' AND event_code != 'REN' AND well_id = 'Mj4YfwadTW' -- Well ID

---- Actualiza parametros de los Casing a partir del Well ID

Update DM_CASING set

run_number = '1',
activity_phase = '0015'

WHERE well_id = 'Mj4YfwadTW' -- Well ID

--- Actualiza parametros de los reportes WE Tubing 2 7/8" a partir del Well ID, Ultima sección del hueco y altura del terreno "NEGATIVO"

UPDATE CD_ASSEMBLY set

string_class = '0015'
,hole_size = '6.125' --DIAMETRO ULTIMA SECCION DEL HUECO
,od_max = '2.875'
,md_assembly_top = '-411.9' -- ALTURA DEL TERRENO NEGATIVO
,assembly_name = 'PROD STRING'
,assembly_size = '2.875'
,id_min = '2.347'

WHERE assembly_name != 'SAND' AND string_type = 'Tubing'
AND assembly_name IN ('TUBING ASSEMBLY','TUBING ASSEMBLY #1','TUBING ASSEMBLY #2','TUBING ASSEMBLY #3',
'TUBING ASSEMBLY #4','PROD STRING','PRODUCTION TUBING STRING','PRODUCTION TUBING STRING ','TUBING PROD. STRING ','TUBING PROD. STRING')
AND well_id = 'Mj4YfwadTW' ---- Well ID

--- Actualiza parametros de los reportes WE Varilla de 7/8" a partir del Well ID, Ultima sección del hueco y altura del terreno "NEGATIVO"

UPDATE CD_ASSEMBLY set

string_class = '0015'
,hole_size = '6.125' --ULTIMA SECCION DEL HUECO
,od_max = '2.256'
,md_assembly_top = '-411.9' -- ALTURA DEL TERRENO NEGATIVO
,assembly_name = 'ROD STRING'
,assembly_size = '0.875'
,id_min = '0'

WHERE assembly_name != 'SAND' AND string_type = 'Tubing' AND assembly_name IN ('ROD STRING')
AND well_id = 'Mj4YfwadTW' ---- Well ID


---Actualiza parametros de los componentes Tubing 3.5

UPDATE CD_ASSEMBLY_COMP SET



id_body = '2.992',
id_drift = '2.867',
approximate_weight = '9.3'



WHERE od_body = '3.5' AND sect_type_code = 'TBG' AND well_id = 'lwdMIpfV5S'



---Actualiza parametros de los componentes Tubing 2 7/8"



UPDATE CD_ASSEMBLY_COMP SET

id_body = '2.441',
id_drift = '2.347',
approximate_weight = '6.5'


WHERE od_body = '2.875' AND sect_type_code IN ('TBG','CAS') AND well_id = 'lwdMIpfV5S'