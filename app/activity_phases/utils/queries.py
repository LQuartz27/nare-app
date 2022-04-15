

def get_time_summary_qry(wellname):
    QRY = """
    SELECT
    A.activity_id,
    E.well_id,
    E.event_code,
    A.time_from,
    A.time_to,
    A.activity_phase 
    FROM DM_ACTIVITY A INNER JOIN
        DM_EVENT E ON E.event_id = A.event_id
    WHERE  E.well_id IN (SELECT well_id FROM CD_WELL WHERE CD_WELL.well_common_name='{wellname}') AND
           E.event_code IN ('ODR','REN')
    ORDER BY 2 ASC, 3 ASC
    """
    return QRY


def get_secciones_hueco_qry(well_id):
    QRY=f"""
    SELECT
    CD_HOLE_SECT.effective_diameter,
    CD_HOLE_SECT.sect_type_code,
    CD_HOLE_SECT_GROUP.activity_drl_phase,
    CD_WELL.well_common_name,
    CD_HOLE_SECT_GROUP.date_sect_start,
    CD_HOLE_SECT_GROUP.date_sect_end,
    CD_HOLE_SECT_GROUP.hole_name,
    CD_HOLE_SECT_GROUP.md_hole_sect_base + {'{fn IFNULL(CD_DATUM.datum_elevation, 0)}'},
    CD_HOLE_SECT_GROUP.md_hole_sect_top + {'{fn IFNULL(CD_DATUM.datum_elevation, 0)}'},
    CD_HOLE_SECT_GROUP.phase,
    CD_HOLE_SECT_GROUP.tvd_hole_sect_base + {'{fn IFNULL(CD_DATUM.datum_elevation, 0)}'},
    CD_HOLE_SECT_GROUP.tvd_hole_sect_top + {'{fn IFNULL(CD_DATUM.datum_elevation, 0)}'},
    CD_WELLBORE.wellbore_no,
    DM_EVENT.event_code
    FROM
    CD_HOLE_SECT, CD_HOLE_SECT_GROUP, CD_WELLBORE, CD_SITE, DM_EVENT, CD_WELL
    LEFT OUTER JOIN CD_DATUM ON (CD_WELL.well_id = CD_DATUM.well_id)
    WHERE
    (((CD_HOLE_SECT.sect_type_code LIKE '%OH%' ) AND
    (CD_HOLE_SECT_GROUP.phase LIKE '%ACTUAL%' ))) AND
    ((CD_HOLE_SECT_GROUP.well_id = CD_HOLE_SECT.well_id AND
    CD_HOLE_SECT_GROUP.wellbore_id = CD_HOLE_SECT.wellbore_id AND
    CD_HOLE_SECT_GROUP.hole_sect_group_id = CD_HOLE_SECT.hole_sect_group_id)
    AND (CD_WELLBORE.well_id = CD_HOLE_SECT_GROUP.well_id AND
    CD_WELLBORE.wellbore_id = CD_HOLE_SECT_GROUP.wellbore_id) AND
    (CD_WELL.well_id = CD_WELLBORE.well_id) AND (CD_SITE.site_id =
    CD_WELL.site_id) AND (DM_EVENT.well_id = CD_HOLE_SECT_GROUP.well_id AND
    DM_EVENT.event_id = CD_HOLE_SECT_GROUP.event_id) AND (CD_WELL.well_id =
    DM_EVENT.well_id)) AND (( ( {'{fn UCASE( CD_DATUM.is_default )}'} = 'Y' ) OR (
    CD_DATUM.datum_id IS NULL ))) AND
    CD_WELL.well_id='{well_id}'
    ORDER BY
    4 ASC, 5 ASC, 6 ASC
    """
    return QRY


def get_update_phase_qry(activity_id, well_id, phase):
    UPDATE_QRY = f"""
    UPDATE dm_activity SET activity_phase='{phase}'
    WHERE activity_id='{activity_id}' and well_id='{well_id}';
    """
    return UPDATE_QRY


def get_asignar_P_qry():
    QRY="""
    UPDATE DM_ACTIVITY SET
    DM_ACTIVITY.activity_class='P'
    WHERE DM_ACTIVITY.activity_class IS NULL
    """
    return QRY


def get_update_phase_mob():
    QRY="""
    UPDATE DM_ACTIVITY
    SET activity_phase='0100'
    WHERE (select event_code from dm_event e
    where e.event_id=dm_activity.event_id and e.well_id=dm_activity.well_id) IN ('MOB','MOV');
    """
    return QRY


def get_update_phase_ocm():
    QRY="""
    UPDATE DM_ACTIVITY
    SET activity_phase='0012'
    WHERE (select event_code from dm_event e
    where e.event_id=dm_activity.event_id and e.well_id=dm_activity.well_id) IN ('OCM','REM');
    """
    return QRY


def get_update_phase_aba():
    QRY="""
    UPDATE DM_ACTIVITY
    SET activity_phase='0013'
    WHERE (select event_code from dm_event e
    where e.event_id=dm_activity.event_id and e.well_id=dm_activity.well_id) IN ('ABA','ABN');
    """
    return QRY


def get_update_phase_services():
    QRY="""
    UPDATE DM_ACTIVITY
    SET activity_phase='0015'
    WHERE (select event_code from dm_event e
    where e.event_id=dm_activity.event_id and e.well_id=dm_activity.well_id) NOT IN ('OCM','ODR','REM','MOB','MOV','ABA','ABN');
    """
    return QRY