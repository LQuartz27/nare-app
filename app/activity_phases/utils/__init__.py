def asign_phase(well_activities_df, well_hole_sections_df):
    
    asigned_phases = []
    
    for idx, row_serie in well_activities_df.iterrows():
        
        activity_date = row_serie['time_from']
        well_id = row_serie['well_id']
        
        min_section_end_date = min(well_hole_sections_df['date_sect_start'])
        min_phase = well_hole_sections_df.loc[well_hole_sections_df['date_sect_start']==min_section_end_date,
                                              'activity_drl_phase'].values[0]
        
        max_section_end_date = max(well_hole_sections_df['date_sect_end'])
        max_phase = well_hole_sections_df.loc[well_hole_sections_df['date_sect_end']==max_section_end_date,
                                              'activity_drl_phase'].values[0]
        
        start_cond = well_hole_sections_df['date_sect_start'] <= activity_date
        end_cond = activity_date < well_hole_sections_df['date_sect_end']
        
        matched_section_serie = well_hole_sections_df[start_cond & end_cond]
        # print(type(matched_section_serie))
        # print(activity_date)
        # display(matched_section_serie)
        try:
            if activity_date >= max_section_end_date:
                asigned_phase = max_phase
            elif activity_date < min_section_end_date:
                asigned_phase = min_phase
                # print(f'Fecha hora por debajo del minimo: {activity_date}')
            else:
                asigned_phase = matched_section_serie.iloc[0]['activity_drl_phase']
        except:
            print(f'VALOR A REVISAR WELL_ID: {well_id} | FECHA: {activity_date} | MIN: {min_section_end_date} | MAX: {max_section_end_date}')
            asigned_phase = 'Revisar'

        # print(asigned_phase)

        asigned_phases.append(asigned_phase)
        
    return asigned_phases


def ajustar_hole_sections(well_hole_sections_df):
    max_section_end_date = max(well_hole_sections_df['date_sect_end'])
    well_hole_sections_df['shifted_start'] = well_hole_sections_df['date_sect_start'].shift(-1).fillna(max_section_end_date)
    well_hole_sections_df['shift_comparison'] = well_hole_sections_df['shifted_start'] == well_hole_sections_df['date_sect_end']
    well_hole_sections_df['adjusted_end'] = well_hole_sections_df.apply(lambda row: row['shifted_start']\
                                                    if not row['shift_comparison'] else row['date_sect_end'],
                                                    axis=1)
    
    return well_hole_sections_df[['well_common_name','sect_type_code','activity_drl_phase',
                                  'date_sect_start','date_sect_end','hole_name','shifted_start',
                                  'shift_comparison','adjusted_end']]
    
    
def write_log_separator(log_file):
    with open(log_file, 'a') as log:
        log.write('\n{}\n'.format('='*100))