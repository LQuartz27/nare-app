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
	air_gap_en_bbdd = air_gap - elev_mesa

	QUERY = f"""
    UPDATE DM_EVENT SET tvd_current = '{air_gap_en_bbdd}' WHERE well_id = '{well_id}' AND event_code IN ('ODR','REN');
    UPDATE DM_EVENT SET tvd_plugback = '{prof_en_bbdd}' WHERE well_id = '{well_id}' AND event_code IN ('ODR','REN');
	"""
	return QUERY


def get_ajustar_profundidades_eventos_subsuelo_qry(view_prof, elev_mesa , well_id):

	prof_en_bbdd = view_prof - elev_mesa

	QUERY = f"""
    UPDATE DM_EVENT SET tvd_current = '{prof_en_bbdd}' WHERE well_id = '{well_id}' AND event_code NOT IN ('ODR','REN','MOB');
    UPDATE DM_EVENT SET tvd_plugback = '{prof_en_bbdd}' WHERE well_id = '{well_id}' AND event_code NOT IN ('ODR','REN','MOB');
	"""
	return QUERY


def get_ajuste_MDs_current_query(delta, well_id):
    QUERY = f"""
	UPDATE DM_DAILY SET md_current = md_current + ({delta}) WHERE well_id = '{well_id}' AND md_current IS NOT NULL;
	"""
    return QUERY


def get_ajuste_MDs_from_to_query(delta, well_id):
    QUERY = f"""
	UPDATE DM_ACTIVITY SET md_from = md_from + ({delta}) WHERE well_id = '{well_id}' AND md_from IS NOT NULL;
	UPDATE DM_ACTIVITY SET md_to = md_to + ({delta}) WHERE well_id = '{well_id}' AND md_to IS NOT NULL;
	"""
    return QUERY


def get_ajuste_MDs_survey_query(delta, well_id):
    QUERY = f"""
	UPDATE CD_SURVEY_STATION SET md = md + ({delta}) WHERE well_id = '{well_id}' AND md IS NOT NULL;
	UPDATE CD_SURVEY_STATION SET tvd = tvd + ({delta}) WHERE well_id = '{well_id}' AND tvd IS NOT NULL;
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
	
	UPDATE CD_CEMENT_JOB SET md_float = md_float + ({delta}) WHERE well_id = '{well_id}' AND md_float IS NOT NULL;
	UPDATE CD_CEMENT_JOB SET tvd_float = tvd_float + ({delta}) WHERE well_id = '{well_id}' AND tvd_float IS NOT NULL;

	UPDATE CD_CEMENT_FLUID SET slurry_top_tvd = slurry_top_tvd + ({delta}) WHERE well_id = '{well_id}' AND slurry_top_tvd IS NOT NULL;
	UPDATE CD_CEMENT_FLUID SET slurry_base_tvd = slurry_base_tvd + ({delta}) WHERE well_id = '{well_id}' AND slurry_base_tvd IS NOT NULL;

	UPDATE CD_CEMENT_STAGE SET md_top = md_top + ({delta}) WHERE well_id = '{well_id}' AND md_top IS NOT NULL;
	UPDATE CD_CEMENT_STAGE SET tvd_top = tvd_top + ({delta}) WHERE well_id = '{well_id}' AND tvd_top IS NOT NULL;
	UPDATE CD_CEMENT_STAGE SET md_base = md_base + ({delta}) WHERE well_id = '{well_id}' AND md_base IS NOT NULL;
 
	UPDATE CD_ASSEMBLY SET
	md_assembly_base = md_assembly_base + ({delta})
	WHERE well_id = '{well_id}' AND
	md_assembly_base IS NOT NULL AND
	CD_ASSEMBLY.event_id IN (SELECT event_id FROM DM_EVENT WHERE well_id='{well_id}' AND DM_EVENT.event_code IN ('ODR','REN'));

	UPDATE CD_ASSEMBLY SET md_assembly_top = md_assembly_top + ({delta})
	WHERE well_id = '{well_id}' AND
	md_assembly_top IS NOT NULL  AND
	CD_ASSEMBLY.event_id IN (SELECT event_id FROM DM_EVENT WHERE well_id='{well_id}' AND DM_EVENT.event_code IN ('ODR','REN'));
	"""
    return QUERY


def get_perfo_time_summary_qry(wellname):

    ODR_REN_TIME_SUMMARY_QUERY = f"""
    SELECT
         CD_WELL.well_common_name AS POZO,
         CD_WELLBORE.wellbore_name AS WELLBORE,
         DM_EVENT.event_code AS EVENTO,
         DM_DAILY.report_no AS NUM_REPORTE,
         --DM_DAILY.date_report AS FECHA_REPORTE,
         DM_ACTIVITY.time_from AS TIME_FROM, 
         DM_ACTIVITY.time_to AS TIME_TO,
         DM_ACTIVITY.activity_duration AS DURACION, 
         DM_ACTIVITY.activity_memo AS DESCRIPCION,
         DM_ACTIVITY.md_from + {'{fn IFNULL(CD_DATUM.datum_elevation, 0)}'} AS MD_FROM,
         DM_ACTIVITY.md_to + {'{fn IFNULL(CD_DATUM.datum_elevation, 0)}'} AS MD_TO
    FROM
         DM_ACTIVITY, DM_DAILY, DM_EVENT, CD_SITE, CD_WELLBORE, CD_WELL LEFT OUTER 
         JOIN CD_DATUM ON (CD_WELL.well_id = CD_DATUM.well_id)
    WHERE
         (((CD_WELL.well_common_name LIKE '%{wellname}%'  ) AND 
         (DM_EVENT.event_code IN('ODR', 'REN')  ))) AND ((DM_DAILY.well_id = 
         DM_ACTIVITY.well_id AND DM_DAILY.event_id = DM_ACTIVITY.event_id AND 
         DM_DAILY.daily_id = DM_ACTIVITY.daily_id) AND (DM_EVENT.well_id = 
         DM_DAILY.well_id AND DM_EVENT.event_id = DM_DAILY.event_id) AND 
         (CD_WELL.well_id = DM_EVENT.well_id) AND (CD_SITE.site_id = 
         CD_WELL.site_id) AND (CD_WELLBORE.well_id = DM_DAILY.well_id AND 
         CD_WELLBORE.wellbore_id = DM_DAILY.wellbore_id) AND (CD_WELL.well_id = 
         CD_WELLBORE.well_id) AND (CD_WELLBORE.well_id = DM_ACTIVITY.well_id AND 
         CD_WELLBORE.wellbore_id = DM_ACTIVITY.wellbore_id)) AND (( ( 
         {'{fn UCASE(CD_DATUM.is_default )}'} = 'Y' ) OR ( CD_DATUM.datum_id IS NULL )))
    ORDER BY
         1 ASC, 3 ASC, 6 ASC
    """
    return ODR_REN_TIME_SUMMARY_QUERY


def get_asignar_P_qry(well_id):
    QRY=f"""
    UPDATE DM_ACTIVITY SET
	DM_ACTIVITY.activity_class='P'
	WHERE DM_ACTIVITY.activity_class IS NULL AND 
          DM_ACTIVITY.well_id='{well_id}'
    """
    return QRY


def get_taladros_qry(wellname):

    taladros_qry = f"""
    SELECT well_common_name AS POZO,
           event_code AS EVENTO,
           E.date_ops_start AS INICIO_EVENTO,
           E.primary_service_provider AS PRINC_PROVEEDOR,
           event_reason AS EVENT_REASON,
           rig_name AS RIG_NAME,
           rig_owner AS RIG_OWNER,
           rig_no AS RIG_No
    FROM DM_RIG_OPERATION_EVENT_LINK_T R
    INNER JOIN CD_WELL W ON R.well_id = W.well_id
    INNER JOIN DM_EVENT E ON R.event_id=E.event_id
    INNER JOIN CD_RIG RIG ON R.rig_id=RIG.rig_id
    WHERE W.well_id = (SELECT well_id FROM CD_WELL WHERE well_common_name='{wellname}')
    ORDER BY E.date_ops_start ASC

    """
    
    return taladros_qry


def get_events_time_summary_qry(wellname):

    ALL_EVENTS_TIME_SUMMARY_QUERY = f"""
    SELECT
         CD_WELL.well_common_name AS POZO,
         CD_WELLBORE.wellbore_name AS WELLBORE,
         DM_EVENT.event_code AS SIGLA,
         DM_EVENT.date_ops_start AS EVENT_START_DATE,
         DM_DAILY.report_no AS NUM_REPORTE,
         --DM_DAILY.date_report AS FECHA_REPORTE,
         DM_ACTIVITY.time_from AS TIME_FROM, 
         DM_ACTIVITY.time_to AS TIME_TO,
         DM_ACTIVITY.activity_duration AS DURACION, 
         DM_ACTIVITY.activity_memo AS DESCRIPCION
    FROM
         DM_ACTIVITY, DM_DAILY, DM_EVENT, CD_SITE, CD_WELLBORE, CD_WELL LEFT OUTER 
         JOIN CD_DATUM ON (CD_WELL.well_id = CD_DATUM.well_id)
    WHERE
         (CD_WELL.well_common_name LIKE '%{wellname}%' )  AND
           ((DM_DAILY.well_id = DM_ACTIVITY.well_id AND DM_DAILY.event_id = DM_ACTIVITY.event_id AND 
            DM_DAILY.daily_id = DM_ACTIVITY.daily_id) AND (DM_EVENT.well_id = DM_DAILY.well_id AND DM_EVENT.event_id = DM_DAILY.event_id) AND 
         (CD_WELL.well_id = DM_EVENT.well_id) AND (CD_SITE.site_id = CD_WELL.site_id) AND (CD_WELLBORE.well_id = DM_DAILY.well_id AND 
         CD_WELLBORE.wellbore_id = DM_DAILY.wellbore_id) AND (CD_WELL.well_id = CD_WELLBORE.well_id) AND (CD_WELLBORE.well_id = DM_ACTIVITY.well_id AND 
         CD_WELLBORE.wellbore_id = DM_ACTIVITY.wellbore_id)) AND (( ( 
         {'{fn UCASE(CD_DATUM.is_default )}'} = 'Y' ) OR ( CD_DATUM.datum_id IS NULL )))
         
    ORDER BY 7 ASC
         
    """
    return ALL_EVENTS_TIME_SUMMARY_QUERY


def get_wellbore_eq_status_qry(wellname):
    WE_STATUS_QUERY = f"""
    SELECT
     CD_WELLBORE.wellbore_name AS WELLBORE,
     DM_EVENT.event_code AS EVENTO,
     DM_EVENT.date_ops_start AS INICIO_EVENTO, 
     DM_REPORT_JOURNAL.report_no AS REPORT_NUM,
     DM_REPORT_JOURNAL.date_report AS REPORT_DATE, 
     CD_ASSEMBLY.assembly_name AS ENSAMBLAJE,
     CD_ASSEMBLY_STATUS.status AS STATUS, 
     CD_ASSEMBLY_STATUS.date_status AS STATUS_DATE
     
    FROM
         CD_ASSEMBLY_STATUS, CD_ASSEMBLY, CD_WELLBORE, CD_WELL, CD_SITE, 
         DM_REPORT_JOURNAL, DM_EVENT
    WHERE
         (((CD_WELL.well_common_name = '{wellname}'))) AND ((CD_ASSEMBLY.well_id = 
         CD_ASSEMBLY_STATUS.well_id AND CD_ASSEMBLY.wellbore_id = 
         CD_ASSEMBLY_STATUS.wellbore_id AND CD_ASSEMBLY.assembly_id = 
         CD_ASSEMBLY_STATUS.assembly_id) AND (CD_WELLBORE.well_id = 
         CD_ASSEMBLY.well_id AND CD_WELLBORE.wellbore_id = CD_ASSEMBLY.wellbore_id) 
         AND (CD_WELL.well_id = CD_WELLBORE.well_id) AND (CD_SITE.site_id = 
         CD_WELL.site_id) AND (DM_REPORT_JOURNAL.report_journal_id = 
         CD_ASSEMBLY.report_journal_id) AND (CD_WELL.well_id = 
         DM_REPORT_JOURNAL.well_id) AND (DM_EVENT.well_id = 
         DM_REPORT_JOURNAL.well_id AND DM_EVENT.event_id = 
         DM_REPORT_JOURNAL.event_id) AND (CD_WELL.well_id = DM_EVENT.well_id) AND 
         (CD_WELLBORE.well_id = DM_REPORT_JOURNAL.well_id AND 
         CD_WELLBORE.wellbore_id = DM_REPORT_JOURNAL.wellbore_id))
    ORDER BY
         3 ASC, 4 ASC
    """
    
    return WE_STATUS_QUERY


def get_prediccion_ocm_base_qry(wellname):
    QRY=f"""
    SELECT
        CD_WELL.well_common_name AS Nombre,
        DM_EVENT.event_code AS Codigo,
        DM_ACTIVITY.md_from + {'{fn IFNULL(CD_DATUM.datum_elevation, 0)}'} AS MDFrom,
        DM_ACTIVITY.md_to + {'{fn IFNULL(CD_DATUM.datum_elevation, 0)}'} AS MDto, 
        DM_ACTIVITY.time_from AS Desde, 
        DM_ACTIVITY.time_to  AS Hasta, 
        DM_ACTIVITY.activity_memo AS Operación
    FROM
        DM_ACTIVITY, DM_EVENT, CD_SITE, CD_WELL LEFT OUTER JOIN CD_DATUM ON 
        (CD_WELL.well_id = CD_DATUM.well_id) 
    WHERE
        (DM_EVENT.event_code IN('ODR', 'OCM')) AND
        (CD_WELL.well_common_name = '{wellname}') AND
        ((DM_EVENT.well_id = DM_ACTIVITY.well_id AND 
          DM_EVENT.event_id = DM_ACTIVITY.event_id) AND
         (CD_WELL.well_id = DM_EVENT.well_id) AND
         (CD_SITE.site_id = CD_WELL.site_id)
        ) AND
        (( ( {'{fn UCASE( CD_DATUM.is_default )}'} = 'Y' ) OR
           ( CD_DATUM.datum_id IS NULL )
        ))
    """

    return QRY

def get_events_ids_qry():
    QRY = """
    SELECT event_id FROM dm_event
    """
    return QRY


def get_insert_event_qry(well_id, neweventid, startdate, finaldate):
    null = 'NULL'
    
    INSERT_QRY = f"""
    INSERT INTO 
    DM_EVENT_T
    ([well_id]
    ,[event_id]
    ,[amount_last_cost_est]
    ,[phase]
    ,[cost_authorized]
    ,[currency_code]
    ,[exchange_rate]
    ,[date_authorized]
    ,[date_ops_end]
    ,[date_last_cost_est]
    ,[date_off_prod]
    ,[date_on_prod]
    ,[date_ops_start]
    ,[event_reason]
    ,[estimated_days]
    ,[equip_type]
    ,[event_code]
    ,[event_no]
    ,[event_objective_1]
    ,[event_type]
    ,[event_objective_2]
    ,[event_team]
    ,[is_final_report]
    ,[is_readonly]
    ,[status_end]
    ,[remarks]
    ,[reporting_standard]
    ,[reporting_time]
    ,[create_date]
    ,[wellhead_connection]
    ,[tvd_current]
    ,[create_user_id]
    ,[create_app_id]
    ,[tvd_plugback]
    ,[update_date]
    ,[update_user_id]
    ,[update_app_id]
    ,[budget_type]
    ,[planned_wci]
    ,[actual_wci]
    ,[well_geometry]
    ,[wta1]
    ,[wta2]
    ,[wellbore_interface]
    ,[rig_move_distance]
    ,[initial_load_volume_oil]
    ,[initial_load_volume_water]
    ,[initial_load_volume_other]
    ,[job_type_id]
    ,[cost_type]
    ,[service_type]
    ,[primary_service_provider]
    ,[lost_gas_vol]
    ,[lost_oil_vol]
    ,[is_project_readonly]
    ,[contingency_percent]
    ,[operated_type]
    ,[operated_type_code]
    ,[pa_su_completion_days]
    ,[event_operator]
    ,[event_objective_3])

    VALUES

    ('{well_id}',
    '{neweventid}',
    {null}, 
    'ACTUAL',
    {null},
    {null},
    {null},
    {null},
    '{finaldate}',
    {null},
    {null},
    {null},
    '{startdate}',
    'COMPLETAMIENTO',
    '2',
    'EQ. MEN DE SERVICIO',
    'OCM',
    '1',
    'COMPLETAMIENTO ORIGINAL PRODUCTOR',
    'COMPLETAMIENTO ORIGINAL',
    'A BOMBEO MECANICO (BM) - CONVENCIONAL',
    'INACTIVO',
    {null},
    'N',
    'ACTIVO',
    {null},
    '1',
    {null},
    {null},
    {null},
    '200',
    {null},
    {null},
    {null},
    {null},
    {null},
    {null},
    'PROYECTADO/PROY',
    'RIGLESS',
    'PROD',
    'HORIZONTAL',
    'BM',
    {null},
    {null},
    {null},
    {null},
    {null},
    {null},
    {null},
    {null},
    {null},
    'MANSAROVAR ENERGY COLOMBIA LTD.',
    {null},
    {null},
    {null},
    {null},
    {null},
    {null},
    {null},
    {null},
    'PRODUCTOR UNA ZONA')
    """

    return INSERT_QRY


def get_poblar_casing_qry(well_id, od, id, drift, weight, bottom_connection,connection_name, codigo_grado, grado):
    QRY = f"""
    UPDATE CD_ASSEMBLY_COMP SET

    id_body = '{id}',
    id_drift = '{drift}',
    approximate_weight = '{weight}',
    bot_conn_type = '{bottom_connection}',
    connection_name = '{connection_name}',
    grade_id = '{codigo_grado}',
    grade= '{grado}'

    WHERE od_body = '{od}' AND
    sect_type_code = 'CAS' AND
    comp_name IN ('Casing','Pup Joint') AND
    well_id = '{well_id}'
    """

    return QRY


def get_poblar_liner_qry(well_id, od, id, drift, weight, bottom_connection,connection_name, codigo_grado, grado):
    QRY = f"""
    UPDATE CD_ASSEMBLY_COMP SET

    id_body = '{id}',
    id_drift = '{drift}',
    approximate_weight = '{weight}',
    bot_conn_type = '{bottom_connection}',
    connection_name = '{connection_name}',
    grade_id = '{codigo_grado}',
    grade= '{grado}'

    WHERE od_body = '{od}' AND
    sect_type_code = 'CAS' AND
    comp_name IN ('Liner','Slotted Liner','Pup Joint') AND
    well_id = '{well_id}'
    """

    return QRY


def get_set_min_id_qry(well_id, od, id):
    QRY=f"""
    UPDATE CD_ASSEMBLY SET
    id_min = '{id}',
    od_max = assembly_size
    WHERE assembly_size = '{od}' AND well_id = '{well_id}'
    """

    return QRY


def get_set_elev_mesa_casings_qry(well_id, elev_terreno):
    # Para que se visualice la diferencia entre elevacion de mesa y del terreno
    # se debe asignar al campo la altura del terreno, pero negativa
    QRY = f"""
    UPDATE CD_ASSEMBLY SET

    tvd_assembly_top = '{-elev_terreno}' -- ALTURA DEL TERRENO NEGATIVO
    ,md_assembly_top = '{-elev_terreno}' -- ALTURA DEL TERRENO NEGATIVO
    
    WHERE well_id = '{well_id}' AND
    string_type = 'Casing' AND
    assembly_name NOT LIKE '%LINER%'
    """

    return QRY


def get_set_0015_qry(well_id):
    QRY = f"""
    Update DM_CASING set

    run_number = '1',
    activity_phase = '0015'

    WHERE event_id IN (SELECT event_id FROM DM_EVENT WHERE well_id = '{well_id}' AND
                       event_code  NOT IN ('MOB','MOV','ODR','OCM','ABA','ABN') ) AND
    well_id = '{well_id}'
    """
    return QRY


def get_post_inj_status_qry(well_id):
    QRY = f"""
    Update DM_EVENT set event_team = 'INACTIVO'
    WHERE well_id = '{well_id}' AND event_code = 'WSV' AND event_reason ='POST-INJECTION'
    """

    return QRY


def get_pre_inj_status_qry(well_id):
    QRY = f"""
    Update DM_EVENT set status_end = 'INACTIVO'
    WHERE well_id = '{well_id}' AND event_code = 'WSV' AND event_reason ='PRE-INJECTION'
    """

    return QRY


def get_flushing_status_qry(well_id):
    QRY = f"""
    Update DM_EVENT set event_objective_1 ='FLUSHING', event_objective_2 = 'FLUSING CORRECTIVO' , event_objective_3 = 'PRUEBA DE INTEGRIDAD DE TUBERÍA-TUBERÍA ROTA'
    WHERE well_id = '{well_id}' AND event_code = 'WSV' AND event_reason ='FLUSHING AND D'
    """

    return QRY


def get_delete_csg_hole_sect(well_id):
    QRY = f"""
    DELETE FROM CD_HOLE_SECT WHERE well_id = '{well_id}' AND comp_type_code = 'CAS'
    """
    return QRY
