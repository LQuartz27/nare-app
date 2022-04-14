from datetime import datetime
from fileinput import filename
import os
import pandas as pd
import re
import sys
import shutil

# PATRONES PARA REUNIONES PRE OPERACIONES
safety_meets_pattern = r"SAFETY|MEETING|PRE[-_ ]OPER.*"

# PATRONES PARA ACTIVIDADES RELACIONADAS CON DRILLING
spud_pattern = r".*SPUD.*|PRE[- ]*SPUD"
drill_pattern = r"DRILLED|DRILLING|P[/ ]?U.*BHA|M[/ ]+U.*BHA|R[/ ]?U.*BHA|DRILLING +BHA|DIRECTIONAL TOOL[S]?|DIRECTIONAL +BHA|ROTATING.*FT|SLIDING.*FT"
td_pattern = r"TD|LANDING POINT"
drill_cement = r"DRILL.*OUT.*CEM.*"

# PATRONES PARA ACTIVIDADES RELACIONADAS CON CEMENTING
cementing_job_pattern = r"CEMENT.*JOB|CEMENT.*TOOLS|CEMENT PLUG|BALANCED PLUG|CEMENT SLURRY|CEMENTING|SLURRY"
plugs_pattern = r"BOTTOM PLUG.*TOP PLUG"
woc_pattern = r"WOC|W.?O.?C|WAITING ?ON ?CEMENT"

# PATRONES PARA ACTIVIDADES RELACIONADAS CON CORRIDA DE CASING
run_casing_pattern = r"CSG|CASING|R[AU]+N ?CASING|RIH .* ?CASING|RIH .* CSG|CSG.*TOOLS| CASING.*TOOLS"
shoes_pattern = r"PACKER SHOE|CSG SHOE|CASING SHOE|WASH DOWN SHOE|FLOAT SHOE|FLOATING SHOE"
run_liner_pattern = r"LINER|R[AU]+N ?LINER|R[AU]+N ?MESH|ASSEMBLY COMPLETION|ASSY COMPLETION|SLOTTED.*LINER"

# PATRONES PARA ACTIVIDADES RELACIONADAS CON CORRIDA DE REGISTROS  CASTV-CBL-GR-CCL
logging_job_pattern = r"LOGGING|E[- _]LOGS?|CASED HOLE|OPEN HOLE"

# PATRONES PARA ACTIVIDADES RELACIONADAS CON BAJADA DE SLA/TUBING
tubing_pattern = r"TUBING|TBG"
pumps_pattern = r"PCP|SBP|BARREL|ROD|STATOR|ROTOR|PLUNGER"

# PATRONES PARA ACTIVIDADES RELACIONADAS CON GRAVEL PACK
underreamer_pattern = r"UNDER.*REAMER"
enlarging_pattern = r"ENLARGED?.*HOLE|ENLARGING.*HOLE|ENLARGE"
gravel_packing_pattern = r"GRAVEL ?PACKING|GRAVEL|PACKING|SXS"

# PATRONES RELACIONADOS CON ESTIMULACIONES
stim_job_pattern = r"STIMULATION|STIMULATION JOB|PICKLING|NEUTRAL RETURNS"
acids_pattern = r"ACID TREATMENT|ACID|ACID AND FORMATION"

# PATRONES RELACIONADOS CON SETTING TOOL
setting_tool_pattern = r"SET+ING {0,3}TOOL"


# COMPILACION DE LOS PATRONES EN SUS CATEGORIAS
meetings_pattern = '|'.join([safety_meets_pattern])

perfo_pattern = '|'.join([meetings_pattern, spud_pattern, drill_pattern, td_pattern, drill_cement])

cementing_pattern = '|'.join([cementing_job_pattern,plugs_pattern, woc_pattern])

csg_pattern = '|'.join([run_casing_pattern, run_liner_pattern])

logging_pattern = '|'.join([logging_job_pattern])

tbg_sla_pattern = '|'.join([tubing_pattern, pumps_pattern])

gravel_pack_pattern = '|'.join([underreamer_pattern, enlarging_pattern, gravel_packing_pattern])

stimulation_pattern = '|'.join([stim_job_pattern, acids_pattern])

setting_tool_pattern = '|'.join([setting_tool_pattern])



meetings_regex = re.compile(meetings_pattern, re.I)
perfo_regex = re.compile(perfo_pattern, re.I)
cementing_regex = re.compile(cementing_pattern, re.I)
csg_regex = re.compile(csg_pattern, re.I)
logging_regex = re.compile(logging_pattern, re.I)
tbg_sla_regex = re.compile(tbg_sla_pattern, re.I)
gravel_pack_regex = re.compile(gravel_pack_pattern, re.I)
stimulation_regex = re.compile(stimulation_pattern, re.I)
setting_tool_regex = re.compile(setting_tool_pattern, re.I)


# COMPILACION DE LOS PATRONES EN SUS CATEGORIAS
meetings_pattern = '|'.join([safety_meets_pattern])

perfo_pattern = '|'.join([meetings_pattern, spud_pattern, drill_pattern, td_pattern, drill_cement])

cementing_pattern = '|'.join([cementing_job_pattern, woc_pattern])

csg_pattern = '|'.join([run_casing_pattern, run_liner_pattern])

logging_pattern = '|'.join([logging_job_pattern])

tbg_sla_pattern = '|'.join([tubing_pattern, pumps_pattern])

gravel_pack_pattern = '|'.join([underreamer_pattern, enlarging_pattern, gravel_packing_pattern])

stimulation_pattern = '|'.join([stim_job_pattern, acids_pattern])

setting_tool_pattern = '|'.join([setting_tool_pattern])



meetings_regex = re.compile(meetings_pattern, re.I)
perfo_regex = re.compile(perfo_pattern, re.I)
cementing_regex = re.compile(cementing_pattern, re.I)
csg_regex = re.compile(csg_pattern, re.I)
logging_regex = re.compile(logging_pattern, re.I)
tbg_sla_regex = re.compile(tbg_sla_pattern, re.I)
gravel_pack_regex = re.compile(gravel_pack_pattern, re.I)
stimulation_regex = re.compile(stimulation_pattern, re.I)
setting_tool_regex = re.compile(setting_tool_pattern, re.I)

def crear_excel_actividades_segmentadas(engine_edm, TIME_SUMMARY_QRY, wellname):
    
    now = datetime.now()
    time_str = now.timestamp()
    
    ts_df = pd.read_sql(TIME_SUMMARY_QRY, engine_edm)
    
    drilling_df = ts_df[ts_df['DESCRIPCION'].str.contains(perfo_regex)]
    cementing_df = ts_df[ts_df['DESCRIPCION'].str.contains(cementing_regex)]
    casing_df = ts_df[ts_df['DESCRIPCION'].str.contains(csg_regex)]
    logging_df = ts_df[ts_df['DESCRIPCION'].str.contains(logging_regex)]
    tbg_sla_df = ts_df[ts_df['DESCRIPCION'].str.contains(tbg_sla_regex)]
    gravel_pack_df = ts_df[ts_df['DESCRIPCION'].str.contains(gravel_pack_regex)]
    stimulation_df = ts_df[ts_df['DESCRIPCION'].str.contains(stimulation_regex)]
    setting_tool_df = ts_df[ts_df['DESCRIPCION'].str.contains(setting_tool_regex)]
    
    if setting_tool_df.shape[0] > 0:
        indexes = setting_tool_df.index
        print(indexes)
        last_index = indexes[-1]
        setting_tool_df = pd.concat([setting_tool_df, ts_df.iloc[last_index+1:]])
    
    filename = f"{wellname}_{str(time_str).replace('.','')}.xlsx"
    
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    drilling_df.to_excel(writer, sheet_name='DRILLING', index=False)
    cementing_df.to_excel(writer, sheet_name='CEMENTING', index=False)
    casing_df.to_excel(writer, sheet_name='CASING', index=False)
    logging_df.to_excel(writer, sheet_name='LOGGING', index=False)
    tbg_sla_df.to_excel(writer, sheet_name='TBG_SLA', index=False)
    gravel_pack_df.to_excel(writer, sheet_name='GRAVEL_PACK', index=False)
    stimulation_df.to_excel(writer, sheet_name='STIM', index=False)
    setting_tool_df.to_excel(writer, sheet_name='SETTING_TOOL', index=False)
    ts_df.to_excel(writer, sheet_name='TIME_SUMMARY', index=False)

    workbook  = writer.book

    headers_format = workbook.add_format({'bold': True})
    descript_format = workbook.add_format({'text_wrap':True})
    no_descript_format = workbook.add_format({'align':'center',
                                            'valign':'bottom'})

    descript_width = 80
    normal_width = 17.43

    for sheet in writer.sheets:
        worksheet = writer.sheets[sheet]
        
        worksheet.set_row(0,None, cell_format=headers_format)
        worksheet.set_column(0,6, width=normal_width, cell_format=no_descript_format)
        worksheet.set_column(7,7, width=descript_width, cell_format=descript_format)
        worksheet.set_column(8,9, width=normal_width, cell_format=no_descript_format)
        
    writer.save()
    writer.close()
    
    return filename
