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
	DELETE FROM CD_ASSEMBLY_COMP_STATUS
	WITH (ROWLOCK, READPAST) --WITH (NOLOCK) (READPAST)
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


def get_ajuste_MDs_query1(delta, well_id):
    QUERY = f"""
	UPDATE DM_ACTIVITY
	SET
	md_from = md_from+({delta}),
	md_to = md_to+({delta})
	WHERE well_id='{well_id}';

	UPDATE DM_DAILY

	SET md_current = md_current+({delta}),
		progress = progress+({delta}) 

	WHERE well_id = '{well_id}'
	"""
    return QUERY


def get_elevaciones_query(well_id):
	QUERY = f"""
	SELECT datum_elevation, water_depth
	FROM CD_DATUM AS D INNER JOIN CD_WELL AS W
		ON W.well_id = D.well_id
	WHERE W.well_id = '{well_id}' AND is_default='Y';
	"""
	return QUERY


def get_ajustar_profundidades_eventos_perfo_qry(view_prof, elev_mesa , elev_terreno, well_id):

	prof_en_bbdd = view_prof - elev_mesa
	air_gap = elev_mesa - elev_terreno 

	QUERY = f"""
	---PROPIEDADES DEL EVENTO

    UPDATE DM_EVENT SET tvd_current = '{air_gap}' WHERE well_id = '{well_id}' AND event_col NOT IN ('ODR','REN','MOB');
    UPDATE DM_EVENT SET tvd_plugback = '{prof_en_bbdd}' WHERE well_id = '{well_id}' AND event_col NOT IN ('ODR','REN','MOB');
	"""
	return QUERY


def get_ajustar_profundidades_eventos_subsuelo_qry(view_prof, elev_mesa , well_id):

	prof_en_bbdd = view_prof - elev_mesa

	QUERY = f"""
	---PROPIEDADES DEL EVENTO

    UPDATE DM_EVENT SET tvd_current = '{prof_en_bbdd}' WHERE well_id = '{well_id}' AND event_col NOT IN ('ODR','REN','MOB');
    UPDATE DM_EVENT SET tvd_plugback = '{prof_en_bbdd}' WHERE well_id = '{well_id}' AND event_col NOT IN ('ODR','REN','MOB');
	"""
	return QUERY


def get_ajuste_MDs_query(delta, well_id):
    QUERY = f"""
	UPDATE CD_WELLBORE SET authorized_md = authorized_md + ({delta}) WHERE well_id = '{well_id}' AND authorized_md IS NOT NULL;
	UPDATE CD_WELLBORE SET authorized_tvd = authorized_tvd + ({delta}) WHERE well_id = '{well_id}' AND authorized_tvd IS NOT NULL;

	UPDATE DM_STIM_TREATMENT SET interval_base = interval_base + ({delta}) WHERE well_id = '{well_id}' AND interval_base IS NOT NULL;
	UPDATE DM_STIM_TREATMENT SET interval_top = interval_top + ({delta}) WHERE well_id = '{well_id}' AND interval_top IS NOT NULL;

	UPDATE DM_PIPE_RUN SET set_length_estimate = set_length_estimate + ({delta}) WHERE well_id = '{well_id}' AND set_length_estimate IS NOT NULL;
	UPDATE DM_LOG_INTERVAL SET md_top = md_top + ({delta}) WHERE well_id = '{well_id}' AND md_top IS NOT NULL;
	UPDATE DM_LOG_INTERVAL SET md_base = md_base + ({delta}) WHERE well_id = '{well_id}' AND md_base IS NOT NULL;

	UPDATE DM_DAILY SET md_current = md_current + ({delta}) WHERE well_id = '{well_id}' AND md_current IS NOT NULL;
	UPDATE DM_ACTIVITY SET md_from = md_from + ({delta}) WHERE well_id = '{well_id}' AND md_from IS NOT NULL;
	UPDATE DM_ACTIVITY SET md_to = md_to + ({delta}) WHERE well_id = '{well_id}' AND md_to IS NOT NULL;

	UPDATE CD_HOLE_SECT_GROUP SET md_hole_sect_base = md_hole_sect_base + ({delta}) WHERE well_id = '{well_id}' AND md_hole_sect_base IS NOT NULL;
	UPDATE CD_HOLE_SECT_GROUP SET md_hole_sect_top = md_hole_sect_top + ({delta}) WHERE well_id = '{well_id}' AND md_hole_sect_top IS NOT NULL;
	UPDATE CD_HOLE_SECT_GROUP SET tvd_hole_sect_base = tvd_hole_sect_base + ({delta}) WHERE well_id = '{well_id}' AND tvd_hole_sect_base IS NOT NULL;
	UPDATE CD_HOLE_SECT_GROUP SET tvd_hole_sect_top = tvd_hole_sect_top + ({delta}) WHERE well_id = '{well_id}' AND tvd_hole_sect_top IS NOT NULL;
	UPDATE CD_FLUID SET md_mud_sample = md_mud_sample + ({delta}) WHERE well_id = '{well_id}' AND md_mud_sample IS NOT NULL;
	UPDATE CD_FLUID SET tvd_mud_sample = tvd_mud_sample + ({delta}) WHERE well_id = '{well_id}' AND tvd_mud_sample IS NOT NULL;

	UPDATE DM_BHA_RUN SET md_in = md_in + ({delta}) WHERE well_id = '{well_id}' AND md_in IS NOT NULL;
	UPDATE DM_BHA_RUN SET md_out = md_out + ({delta}) WHERE well_id = '{well_id}' AND md_out IS NOT NULL;

	UPDATE CD_SURVEY_STATION SET md = md + ({delta}) WHERE well_id = '{well_id}' AND md IS NOT NULL;
	UPDATE CD_SURVEY_STATION SET tvd = tvd + ({delta}) WHERE well_id = '{well_id}' AND tvd IS NOT NULL;
	---CEMENT
	UPDATE CD_CEMENT_JOB SET md_float = md_float + ({delta}) WHERE well_id = '{well_id}' AND md_float IS NOT NULL;
	UPDATE CD_CEMENT_JOB SET tvd_float = tvd_float + ({delta}) WHERE well_id = '{well_id}' AND tvd_float IS NOT NULL;

	UPDATE CD_CEMENT_FLUID SET slurry_top_tvd = slurry_top_tvd + ({delta}) WHERE well_id = '{well_id}' AND slurry_top_tvd IS NOT NULL;
	UPDATE CD_CEMENT_FLUID SET slurry_base_tvd = slurry_base_tvd + ({delta}) WHERE well_id = '{well_id}' AND slurry_base_tvd IS NOT NULL;

	UPDATE CD_CEMENT_STAGE SET md_top = md_top + ({delta}) WHERE well_id = '{well_id}' AND md_top IS NOT NULL;
	UPDATE CD_CEMENT_STAGE SET tvd_top = tvd_top + ({delta}) WHERE well_id = '{well_id}' AND tvd_top IS NOT NULL;
	UPDATE CD_CEMENT_STAGE SET md_base = md_base + ({delta}) WHERE well_id = '{well_id}' AND md_base IS NOT NULL;
	"""
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