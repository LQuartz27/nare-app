from datetime import datetime
import os
import pandas as pd
import re
import io



files_folder = os.path.join(os.getcwd(), 'app','static', 'xlfiles')
if not os.path.exists(files_folder):
    os.mkdir(files_folder)


def create_taladros_dailys_excel(engine_edm, wellname, TALADROS_QRY, DAILY_OPS_QRY):
    
    taladros_df = pd.read_sql(TALADROS_QRY, engine_edm)
    
    daily_ops_df = pd.read_sql(DAILY_OPS_QRY, engine_edm)
    
    daily_ops_df['EVENTO'] = daily_ops_df['SIGLA'] + ' ' + daily_ops_df['EVENT_START_DATE'].dt.strftime('%m/%d/%Y')
    
    daily_ops_df_cols = daily_ops_df.columns.tolist()
    daily_ops_df_cols = daily_ops_df_cols[:2] + daily_ops_df_cols[-1:] + daily_ops_df_cols[4:-1]
    
    daily_ops_df = daily_ops_df[daily_ops_df_cols]
    
    output = io.BytesIO()
    filename = f"{wellname}_TALADROS_DAILY_OPS.xlsx"

    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    taladros_df.to_excel(writer, sheet_name='TALADROS', index=False)
    daily_ops_df.to_excel(writer, sheet_name='DAILY_OPS', index=False)

    workbook  = writer.book

    headers_format = workbook.add_format({'bold': True})
    descript_format = workbook.add_format({'text_wrap':True})
    no_descript_format = workbook.add_format({'align':'center',
                                              'valign':'bottom'})

    descript_width = 80
    normal_width = 17.43
    proveedor_width = 35.4

    for sheet in writer.sheets:
        if sheet == 'TALADROS':
            worksheet = writer.sheets[sheet]

            worksheet.set_row(0,None, cell_format=headers_format)
            worksheet.set_column(0,2, width=normal_width, cell_format=no_descript_format)
            worksheet.set_column(3,3, width=proveedor_width, cell_format=no_descript_format)
            worksheet.set_column(4,6, width=normal_width, cell_format=no_descript_format)
            
        elif sheet == 'DAILY_OPS':
            
            worksheet = writer.sheets[sheet]

            worksheet.set_row(0,None, cell_format=headers_format)
            worksheet.set_column(0,6, width=normal_width, cell_format=no_descript_format)
            worksheet.set_column(7,7, width=descript_width, cell_format=descript_format)

    writer.save()
    output.seek(0)
    
    return output, filename

