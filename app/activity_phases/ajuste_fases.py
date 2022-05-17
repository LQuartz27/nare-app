import pandas as pd
from .utils.DATABASE import *
from .utils.queries import *
from .utils import *


def asignar_activity_phases(wellname):
    edm_engine = create_engine(edm_connection_url)

    TIME_SUMMARY_QRY = get_time_summary_qry(wellname)

    activity_df = pd.read_sql(TIME_SUMMARY_QRY, edm_engine)
    activity_df = activity_df.sort_values(by=['well_id','time_from'],ascending=[1,1])

    well_ids = activity_df['well_id'].unique()

    hole_sections = []
    activities = []

    for well_id in well_ids:
        HUECOS_QRY = get_secciones_hueco_qry(well_id)
        
        well_hole_sections_df = pd.read_sql(HUECOS_QRY, edm_engine).sort_values(by=['date_sect_start'], ascending=[1])
        well_hole_sections_df = ajustar_hole_sections(well_hole_sections_df)
        
        hole_sections.append(well_hole_sections_df.copy())
        
        well_hole_sections_df['date_sect_end'] = well_hole_sections_df['adjusted_end']
        
        well_activities_df = activity_df[activity_df['well_id']==well_id].copy()
        
        asigned_phases = asign_phase(well_activities_df, well_hole_sections_df)
        
        well_activities_df['asigned_phase'] = asigned_phases
        
        activities.append(well_activities_df)
        
    
    full_hole_sections_df = pd.concat(hole_sections)
    full_activities_df = pd.concat(activities)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('OUTPUT.xlsx', engine='xlsxwriter')

    # Write each dataframe to a different worksheet.
    full_hole_sections_df.to_excel(writer, sheet_name='HOLE_SECTIONS',index=False)
    full_activities_df.to_excel(writer, sheet_name='ACTIVITIES',index=False)

    writer.save()
    writer.close()

    with edm_engine.connect() as con:
                
        ASIGNAR_P_QRY = get_asignar_P_qry()
        UPDATE_ACTIVITY_PHASES_MOB = get_update_phase_mob()
        UPDATE_ACTIVITY_PHASES_OCM = get_update_phase_ocm()
        UPDATE_ACTIVITY_PHASES_ABA = get_update_phase_aba()
        UPDATE_ACTIVITY_PHASES_SERVICES = get_update_phase_services()

        trans = con.begin()

        try:
            con.execute(ASIGNAR_P_QRY)
            con.execute(UPDATE_ACTIVITY_PHASES_MOB)
            con.execute(UPDATE_ACTIVITY_PHASES_OCM)
            con.execute(UPDATE_ACTIVITY_PHASES_ABA)
            con.execute(UPDATE_ACTIVITY_PHASES_SERVICES)

            trans.commit()
        except:
            trans.rollback()

            raise Exception('No se ejecutaron exitosamente los queries de asignacion de fases genéricos')

        try:
            for idx, row_serie in full_activities_df.iterrows():
                
                activity_id = row_serie['activity_id']
                well_id = row_serie['well_id']
                asigned_phase = row_serie['asigned_phase']

                update_q = get_update_phase_qry(activity_id, well_id, asigned_phase)
                con.execute(update_q)
        except:
            trans.rollback()
            raise Exception('No se logró asignar fase')
            
        trans.commit()
            
