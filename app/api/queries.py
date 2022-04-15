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