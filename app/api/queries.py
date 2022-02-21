WELL_COMMON_NAMES_QUERY = """
SELECT DISTINCT CD_WELL.well_common_name 
FROM CD_WELL
"""


def get_well_id_query(well_common_name):

	WELL_ID_QUERY = """
	SELECT well_id
	FROM CD_WELL
	WHERE well_common_name = '{}' -- NOMBRE DEL POZO
	""".format(well_common_name)

	return WELL_ID_QUERY


def get_borrado_component_status_query(well_id):

	BORRADO_COMPONENT_STATUS_QUERY = """
			--Borra por pozo, Lineas del Status de los componentes WE
	DELETE FROM CD_ASSEMBLY_COMP_STATUS
	WHERE well_id = '{}'
	""".format(well_id)

	return BORRADO_COMPONENT_STATUS_QUERY


def get_compo_status_rows_query(well_id):
	
	QUERY = """
	SELECT COUNT(*) AS NUM_REGISTROS
	FROM CD_ASSEMBLY_COMP_STATUS
	WHERE well_id = '{}'
	""".format(well_id)

	return QUERY


def get_ajuste_MDs_query(delta, well_id):
    QUERY = """
	UPDATE DM_ACTIVITY
	SET
	md_from = md_from+({}),
	md_to = md_to+({})
	WHERE well_id='{}'
	""".format(delta, delta, well_id)

    return QUERY

GET_TO_UPDATE_DATA_query = """
Select 
DM_EVENT.well_id,
DM_EVENT.event_id,
(Select CD_WELL.well_common_name from CD_WELL where CD_WELL.well_id=DM_EVENT.well_id) as Pozo,

DM_EVENT.event_code,
CASE
	WHEN DM_EVENT.event_code='ODR' THEN 'ODR'
    WHEN DM_EVENT.event_code='OCM' THEN 'OCM'
    WHEN DM_EVENT.event_code='MOB' THEN 'MOB'
    WHEN DM_EVENT.event_code='RDG' THEN 'RDG'
    WHEN DM_EVENT.event_code='WSV' THEN 'WSV'
    WHEN DM_EVENT.event_code='MOV' THEN 'MOB'
	WHEN DM_EVENT.event_code='ABN' THEN 'ABA'
	WHEN DM_EVENT.event_code='FLU' THEN 'WSV'
	WHEN DM_EVENT.event_code='MNT' THEN 'WSV'
	WHEN DM_EVENT.event_code='RP' THEN 'WSV'
	WHEN DM_EVENT.event_code='STB' THEN 'WSV'
	WHEN DM_EVENT.event_code='STM' THEN 'WSV'
	WHEN DM_EVENT.event_code='WOV' THEN 'WRK'
    ELSE
    DM_EVENT.event_code
END As P_event_code,


DM_EVENT.event_objective_1,
CASE
	WHEN DM_EVENT.event_code='MOV' THEN 'TRANSPORTE DE EQUIPO A LOCACIÓN' 
	WHEN DM_EVENT.event_code='ODR' THEN 'DESARROLLO'
	WHEN DM_EVENT.event_code='ABN' THEN 'ABANDONO'
	WHEN DM_EVENT.event_code='OCM' THEN 'COMPLETAMIENTO ORIGINAL PRODUCTOR'
    ELSE
    DM_EVENT.event_objective_1
END as P_objective_1,


DM_EVENT.event_objective_2,
CASE
	WHEN DM_EVENT.event_code='MOV' THEN 'ENTRE LOCACIONES E INICIAL PARA ODR Y OCM' 
	WHEN DM_EVENT.event_code='ODR' THEN 'DESARROLLO'
	WHEN DM_EVENT.event_code='ABN' THEN 'ABANDONO POZO PRODUCTOR'
	WHEN DM_EVENT.event_code='OCM' THEN ''
    ELSE
    DM_EVENT.event_objective_2
END as P_objective_2,

DM_EVENT.event_objective_3,
CASE
	WHEN DM_EVENT.event_code='MOV' THEN 'TRANSPORTE DE EQUIPO A LOCACIÓN' 
	WHEN DM_EVENT.event_code='ODR' THEN 'DESARROLLO'
	WHEN DM_EVENT.event_code='ABN' THEN ''
	WHEN DM_EVENT.event_code='OCM' THEN ''
    ELSE
    DM_EVENT.event_objective_3
END as P_objective_3,


DM_EVENT.event_team,
CASE
	WHEN DM_EVENT.event_code='MOV' THEN '' 
	WHEN DM_EVENT.event_code<>'MOV' AND DM_EVENT.event_team IS NULL THEN 'ACTIVO' 
    ELSE
    DM_EVENT.event_team
END as P_event_team,


DM_EVENT.tvd_current,
CASE
	WHEN DM_EVENT.event_code='MOV' THEN '' 
	WHEN DM_EVENT.event_code<>'MOV' and DM_EVENT.tvd_current is null THEN
	(Select MAX(DM_DAILY.md_current) from DM_DAILY where  DM_DAILY.well_id=DM_EVENT.well_id and DM_DAILY.event_id=DM_EVENT.event_id)
    ELSE
    DM_EVENT.tvd_current
END  as P_tvd_current,


DM_EVENT.equip_type,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN DM_EVENT.event_code IN ('MOV','ODR','OCM') THEN 'EQ. DE PERFORACIÓN' 
	WHEN DM_EVENT.event_code IN ('WOV','ABA') THEN 'EQ. MAY DE SERVICIO' 
	ELSE
	'EQ. MEN DE SERVICIO'
END as P_equip_type,


DM_EVENT.primary_service_provider,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
    WHEN DM_EVENT.event_code IS NOT NULL AND DM_EVENT.primary_service_provider IS NULL THEN 'MANSAROVAR ENERGY COLOMBIA LTD.'
	ELSE
	DM_EVENT.primary_service_provider
END as P_primary_service_provider,


DM_EVENT.actual_wci,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN DM_EVENT.event_code IN ('MOV','ODR','OCM') THEN 'DRLG' 
	WHEN DM_EVENT.event_code NOT IN ('MOV','ODR','OCM') THEN 'PROD' 
END as P_actual_wci,


DM_EVENT.well_geometry,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN DM_EVENT.event_code IS NOT NULL AND DM_EVENT.well_geometry IS NULL  THEN 
	(Select CD_WELL.redrill_no from CD_WELL where CD_WELL.well_id=DM_EVENT.well_id)
    ELSE
    DM_EVENT.well_geometry
END as P_well_geometry,


DM_EVENT.event_type,
CASE
    WHEN DM_EVENT.event_code='ODR' THEN 'PERFORACIÓN'
    WHEN DM_EVENT.event_code='MOB' THEN 'MOVILIZACIÓN'
    WHEN DM_EVENT.event_code='RDG' THEN 'REDISEÑO'
    WHEN DM_EVENT.event_code='WSV' THEN 'SERVICIO A POZO'
	WHEN DM_EVENT.event_code='MOV' THEN 'MOVILIZACIÓN'
	WHEN DM_EVENT.event_code='ABN' THEN 'ABANDONO'
	WHEN DM_EVENT.event_code='FLU' THEN 'SERVICIO A POZO'
	WHEN DM_EVENT.event_code='MNT' THEN 'SERVICIO A POZO'
	WHEN DM_EVENT.event_code='RP' THEN 'SERVICIO A POZO'
	WHEN DM_EVENT.event_code='STB' THEN 'SERVICIO A POZO'
	WHEN DM_EVENT.event_code='STM' THEN 'SERVICIO A POZO'
	WHEN DM_EVENT.event_code='WOV' THEN 'WORKOVER'
	WHEN DM_EVENT.event_code='OCM' THEN 'COMPLETAMIENTO ORIGINAL'
    ELSE
    DM_EVENT.event_type
END As P_event_type,


DM_EVENT.estimated_days,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN DM_EVENT.event_code IS NOT NULL AND DM_EVENT.estimated_days IS NULL THEN
	Round((Select SUM(DM_ACTIVITY.activity_duration)/24 from DM_ACTIVITY where DM_ACTIVITY.well_id=DM_EVENT.well_id and  DM_ACTIVITY.event_id=DM_EVENT.event_id),2)
    ELSE
    DM_EVENT.estimated_days
END as P_estimated_days,


DM_EVENT.tvd_plugback,
CASE
	WHEN DM_EVENT.event_code='MOV' THEN '' 
	WHEN DM_EVENT.event_code<>'MOV' and DM_EVENT.tvd_plugback is null THEN
	(Select MAX(DM_DAILY.md_current) from DM_DAILY where  DM_DAILY.well_id=DM_EVENT.well_id and DM_DAILY.event_id=DM_EVENT.event_id)
    ELSE
    DM_EVENT.tvd_plugback
END  as P_tvd_plugback,



DM_EVENt.event_reason,
CASE
	WHEN DM_EVENT.event_code='MOV' THEN 'TRANSP EQUIPO' 
	WHEN DM_EVENT.event_code='ODR' THEN 'DESARROLLO'
	WHEN DM_EVENT.event_code='ABN' THEN 'ABANDONO'
	WHEN DM_EVENT.event_code='OCM' THEN 'COMPLETAMIENTO ORIG'
	ELSE
	DM_EVENT.wellbore_interface
END as P_event_reason,

DM_EVENt.wta1,
CASE
	WHEN DM_EVENT.event_code IS NOT NULL AND DM_EVENT.wellhead_connection IS NULL THEN '' 
    ELSE
    DM_EVENT.wellhead_connection
END as P_wta1,

DM_EVENt.rig_move_distance,
CASE
	WHEN DM_EVENT.event_code IS NOT NULL THEN '' 
END as P_rig_move_distance,

DM_EVENt.wta2,
CASE
	WHEN DM_EVENT.event_code IS NOT NULL THEN '' 
END as P_wta2,


DM_EVENT.planned_wci,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN DM_EVENT.event_code IN ('MOV','ODR','OCM') THEN 'RIG' 
	WHEN DM_EVENT.event_code NOT IN ('MOV','ODR','OCM') THEN 'RIGLESS' 
END as P_planned_wci,


DM_EVENT.budget_type,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN DM_EVENT.event_code IN ('MOV','ODR','OCM') THEN 'PROYECTADO/PROY' 
	WHEN DM_EVENT.event_code NOT IN ('MOV','ODR','OCM','ABA','ABN') THEN 'PROYECTO/GASTO' 
	WHEN DM_EVENT.event_code IN ('ABA','ABN') THEN 'ABANDONO' 
END as P_budget_type,

DM_EVENT.service_type,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN DM_EVENT.event_code IS NOT NULL THEN 'PROACTIVE' 
END as P_service_type,


DM_EVENT.date_ops_start,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN DM_EVENT.event_code IS NOT NULL and DM_EVENT.date_ops_start is null THEN
	(Select cast(FORMAT(MIN(DM_ACTIVITY.time_from), 'yyyy-MM-dd HH:mm:ss') AS VARCHAR) from DM_ACTIVITY where DM_ACTIVITY.well_id=DM_EVENT.well_id and  DM_ACTIVITY.event_id=DM_EVENT.event_id)
    ELSE
    cast(FORMAT(DM_EVENT.date_ops_start, 'yyyy-MM-dd HH:mm:ss') AS VARCHAR)
END as P_date_ops_start,


DM_EVENT.date_ops_end,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN DM_EVENT.event_code IS NOT NULL and DM_EVENT.date_ops_end is null THEN
	(Select cast(FORMAT(MAX(DM_ACTIVITY.time_to), 'yyyy-MM-dd HH:mm:ss') AS VARCHAR) from DM_ACTIVITY where DM_ACTIVITY.well_id=DM_EVENT.well_id and  DM_ACTIVITY.event_id=DM_EVENT.event_id)
    ELSE
    cast(FORMAT(DM_EVENT.date_ops_end, 'yyyy-MM-dd HH:mm:ss') AS VARCHAR)
END as P_date_ops_end,

DM_EVENT.status_end,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN DM_EVENT.event_code IN ('ABA','ABN') THEN 'ABANDONADO' 
	WHEN DM_EVENT.event_code NOT IN ('ABA','ABN') THEN 'ACTIVO' 
END as P_status_end,


(Select Top 1 DM_RIG_OPERATION.date_rig_pickup from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id) as date_rig_pickup,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN (Select COUNT(DM_RIG_OPERATION.rig_operation_id) from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id)<>0 
	THEN
	(Select cast(FORMAT(MIN(DM_ACTIVITY.time_from), 'yyyy-MM-dd HH:mm:ss') AS VARCHAR) from DM_ACTIVITY where DM_ACTIVITY.well_id=DM_EVENT.well_id and  DM_ACTIVITY.event_id=DM_EVENT.event_id)
	ELSE
	''
END as P_date_rig_pickup,



(Select Top 1 DM_RIG_OPERATION.date_time_on_location from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id) as date_rig_pickup,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN (Select COUNT(DM_RIG_OPERATION.rig_operation_id) from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id)<>0 
	THEN
	(Select cast(FORMAT(MIN(DM_ACTIVITY.time_from), 'yyyy-MM-dd HH:mm:ss') AS VARCHAR) from DM_ACTIVITY where DM_ACTIVITY.well_id=DM_EVENT.well_id and  DM_ACTIVITY.event_id=DM_EVENT.event_id)
	ELSE
	''
END as P_date_time_on_location,

(Select Top 1 DM_RIG_OPERATION.date_rig_up from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id) as date_rig_pickup,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN (Select COUNT(DM_RIG_OPERATION.rig_operation_id) from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id)<>0 
	THEN
	(Select cast(FORMAT(MIN(DM_ACTIVITY.time_from), 'yyyy-MM-dd HH:mm:ss') AS VARCHAR) from DM_ACTIVITY where DM_ACTIVITY.well_id=DM_EVENT.well_id and  DM_ACTIVITY.event_id=DM_EVENT.event_id)
	ELSE
	''
END as P_date_rig_up,

(Select Top 1 DM_RIG_OPERATION.date_time_charge_start from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id) as date_rig_pickup,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN (Select COUNT(DM_RIG_OPERATION.rig_operation_id) from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id)<>0 
	THEN
	(Select cast(FORMAT(MIN(DM_ACTIVITY.time_from), 'yyyy-MM-dd HH:mm:ss') AS VARCHAR) from DM_ACTIVITY where DM_ACTIVITY.well_id=DM_EVENT.well_id and  DM_ACTIVITY.event_id=DM_EVENT.event_id)
	ELSE
	''
END as P_date_time_charge_start,

(Select Top 1 DM_RIG_OPERATION.date_time_ops_start from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id) as date_rig_pickup,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN (Select COUNT(DM_RIG_OPERATION.rig_operation_id) from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id)<>0 
	THEN
	(Select cast(FORMAT(MIN(DM_ACTIVITY.time_from), 'yyyy-MM-dd HH:mm:ss') AS VARCHAR) from DM_ACTIVITY where DM_ACTIVITY.well_id=DM_EVENT.well_id and  DM_ACTIVITY.event_id=DM_EVENT.event_id)
	ELSE
	''
END as P_date_time_ops_start,

(Select Top 1 DM_RIG_OPERATION.date_time_ops_finished from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id) as date_rig_pickup,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN (Select COUNT(DM_RIG_OPERATION.rig_operation_id) from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id)<>0 
	THEN
	(Select cast(FORMAT(MAX(DM_ACTIVITY.time_to), 'yyyy-MM-dd HH:mm:ss') AS VARCHAR) from DM_ACTIVITY where DM_ACTIVITY.well_id=DM_EVENT.well_id and  DM_ACTIVITY.event_id=DM_EVENT.event_id)
	ELSE
	''
END as P_date_time_ops_finished,

(Select Top 1 DM_RIG_OPERATION.date_rig_released from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id) as date_rig_pickup,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN (Select COUNT(DM_RIG_OPERATION.rig_operation_id) from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id)<>0 
	THEN
	(Select cast(FORMAT(MAX(DM_ACTIVITY.time_to), 'yyyy-MM-dd HH:mm:ss') AS VARCHAR) from DM_ACTIVITY where DM_ACTIVITY.well_id=DM_EVENT.well_id and  DM_ACTIVITY.event_id=DM_EVENT.event_id)
	ELSE
	''
END as P_date_rig_released,

(Select Top 1 DM_RIG_OPERATION.date_rig_down from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id) as date_rig_pickup,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN (Select COUNT(DM_RIG_OPERATION.rig_operation_id) from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id)<>0 
	THEN
	(Select cast(FORMAT(MAX(DM_ACTIVITY.time_to), 'yyyy-MM-dd HH:mm:ss') AS VARCHAR) from DM_ACTIVITY where DM_ACTIVITY.well_id=DM_EVENT.well_id and  DM_ACTIVITY.event_id=DM_EVENT.event_id)
	ELSE
	''
END as P_date_rig_down,

(Select Top 1 DM_RIG_OPERATION.date_time_off_location from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id) as date_rig_pickup,
CASE
	WHEN DM_EVENT.event_code IS NULL THEN '' 
	WHEN (Select COUNT(DM_RIG_OPERATION.rig_operation_id) from  DM_RIG_OPERATION_EVENT_LINK, DM_RIG_OPERATION where DM_RIG_OPERATION_EVENT_LINK.rig_operation_id=DM_RIG_OPERATION.rig_operation_id and DM_RIG_OPERATION_EVENT_LINK.well_id=DM_EVENT.well_id and DM_RIG_OPERATION_EVENT_LINK.event_id=DM_EVENT.event_id)<>0 
	THEN
	(Select cast(FORMAT(MAX(DM_ACTIVITY.time_to), 'yyyy-MM-dd HH:mm:ss') AS VARCHAR) from DM_ACTIVITY where DM_ACTIVITY.well_id=DM_EVENT.well_id and  DM_ACTIVITY.event_id=DM_EVENT.event_id)
	ELSE
	''
END as P_date_time_off_location,


'EEJ' as status_0,
'INICIO ACTIVIDAD' as status_0_Razon,
(Select cast(FORMAT(MIN(DM_ACTIVITY.time_from), 'yyyy-MM-dd HH:mm:ss') AS VARCHAR) from DM_ACTIVITY where DM_ACTIVITY.well_id=DM_EVENT.well_id and  DM_ACTIVITY.event_id=DM_EVENT.event_id) as status_0_inicio,
(Select cast(FORMAT(MAX(DM_ACTIVITY.time_to), 'yyyy-MM-dd HH:mm:ss') AS VARCHAR) from DM_ACTIVITY where DM_ACTIVITY.well_id=DM_EVENT.well_id and  DM_ACTIVITY.event_id=DM_EVENT.event_id) as status_0_fin,


'FNE' as status_1,
'FIN ACTIVIDAD' as status_1,
(Select cast(FORMAT(MAX(DM_ACTIVITY.time_to), 'yyyy-MM-dd HH:mm:ss') AS VARCHAR) from DM_ACTIVITY where DM_ACTIVITY.well_id=DM_EVENT.well_id and  DM_ACTIVITY.event_id=DM_EVENT.event_id) as status_1_inicio,
(Select cast(FORMAT(MAX(DM_ACTIVITY.time_to), 'yyyy-MM-dd HH:mm:ss') AS VARCHAR) from DM_ACTIVITY where DM_ACTIVITY.well_id=DM_EVENT.well_id and  DM_ACTIVITY.event_id=DM_EVENT.event_id) as status_1_fin


from 
DM_EVENT,
CD_DATUM
WHERE
DM_EVENT.well_id=CD_DATUM.well_id and
CD_DATUM.is_default='Y' and
DM_EVENT.well_id='{}' 
order by
1 asc
"""