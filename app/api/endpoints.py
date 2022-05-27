import json
from flask import jsonify, request, url_for, send_file
# from itsdangerous import json
import pandas as pd
import requests
from sqlalchemy import create_engine, text

from . import api_blueprint
from .queries import *
from .preprocesado_ddr import *
from .predecir_inicio_ocm import *

from app.database import *


@api_blueprint.route('/')
def api_root():
    return 'Api root'


@api_blueprint.route('/wellnames')
def well_names():
    _, wellnames_list = get_well_common_names()

    return jsonify(wellnames_list)


@api_blueprint.route('/wellid/<string:wellname>', methods=['GET'])
def wellid(wellname):
    print(wellname)
    engine = create_engine(connection_url)

    WELL_ID_QUERY = get_well_id_query(wellname)

    with engine.connect() as connection:
        result_cursor = connection.execute(text(WELL_ID_QUERY))
        data = result_cursor.fetchall()

    well_id = data[0][0]

    response = {'WELL COMMON NAME': wellname,
                'WELL ID': well_id}

    return jsonify(response)


@api_blueprint.route('/get_elevacion_mesa/<string:well_id>', methods=['GET'])
def get_elevacion_mesa(well_id):

    engine = create_engine(connection_url)

    ELEVACION_MESA_QRY = get_elevaciones_query(well_id)

    print(ELEVACION_MESA_QRY)

    with engine.connect() as connection:
        result_cursor = connection.execute(text(ELEVACION_MESA_QRY))
        data = result_cursor.fetchall()

    elevacion_mesa = data[0][0]
    elevacion_terreno = data[0][1]

    response = {'ELEVACION MESA': elevacion_mesa,
                'ELEVACION TERRENO':elevacion_terreno,
                'WELL ID': well_id}

    return jsonify(response)


@api_blueprint.route('/componentStatusRows', methods=['GET'])
def count_comp_status():
    well_id = request.args.get('well_id', None)

    engine = create_engine(connection_url)
    COMP_STATUS_COUNT_QUERY = get_compo_status_rows_query(well_id)

    with engine.connect() as connection:
        trans = connection.begin()
        try:
            cursor_conteo_result = connection.execute(text(COMP_STATUS_COUNT_QUERY))
            count_data = cursor_conteo_result.fetchall()
            row_count = count_data[0][0]
            trans.commit()
        except:
            trans.rollback()
            raise Exception('No se logró hacer el conteo de los registros de COMP STATUS')

    print(f'ROW COUNT: {row_count}')

    response = {'COMPONENT STATUS ROWS': row_count}

    return jsonify(response)


@api_blueprint.route('/delcomponentstatus/<string:well_id>', methods=['GET'])
def del_component_status(well_id):

    BORRAR_COMP_STATUS_QUERY = get_borrado_component_status_query(well_id)
    
    ROOT = request.url_root

    get_comp_status_rows_url = ROOT + \
            url_for('api.count_comp_status')

    print(get_comp_status_rows_url)

    response = requests.get(get_comp_status_rows_url, params={
                                                        "well_id":well_id
                                                    }
                            )

    row_count_prev = json.loads(response.content.decode("utf-8"))['COMPONENT STATUS ROWS']

    print(BORRAR_COMP_STATUS_QUERY)
    print(text(BORRAR_COMP_STATUS_QUERY))

    engine = create_engine(connection_url)

    with engine.connect() as connection:
        trans = connection.begin()
        try:
            # cursor_borrado_result = connection.execute("DELETE FROM CD_ASSEMBLY_COMP_STATUS_T WITH (READPAST) WHERE well_id = 'su8xOlmBS3'")
            cursor_borrado_result = connection.execute(text(BORRAR_COMP_STATUS_QUERY))

            trans.commit()
            
        except:
            trans.rollback()
            raise Exception('No se logró eliminar los component status del pozo')

    # print(f'Useless DELETE count: {useless_count}')
    # row_count = 1

    response = requests.get(get_comp_status_rows_url, params={
                                                        "well_id":well_id
                                                    }
                            )

    row_count_after = json.loads(response.content.decode("utf-8"))['COMPONENT STATUS ROWS']

    response = {"num_registros_antes": row_count_prev,
                "num_registros_despues":row_count_after}

    return jsonify(response)


@api_blueprint.route('/ajustarProfEventos/', methods=['GET'])
def ajustar_profs_eventos():
    engine = create_engine(connection_url)

    new_td = float(request.args.get('new_td', None))
    well_id = request.args.get('well_id', None)

    ROOT = request.url_root

    get_elevacion_mesa_url = ROOT + \
            url_for('api.get_elevacion_mesa', well_id=well_id)

    response = requests.get(get_elevacion_mesa_url)
    elevacion_mesa = json.loads(response.content.decode("utf-8"))['ELEVACION MESA']
    elevacion_terreno = json.loads(response.content.decode("utf-8"))['ELEVACION TERRENO']

    AJUSTAR_PROFS_EVENTOS_PERFO = get_ajustar_profundidades_eventos_perfo_qry(new_td, elevacion_mesa , elevacion_terreno, well_id)
    AJUSTAR_PROFS_EVENTOS_SUBSUELO = get_ajustar_profundidades_eventos_subsuelo_qry(new_td, elevacion_mesa , well_id)
    
    perfo_queries = AJUSTAR_PROFS_EVENTOS_PERFO.replace('\t','').split(';\n')
    subsuelo_queries = AJUSTAR_PROFS_EVENTOS_SUBSUELO.replace('\t','').split(';\n')
    
    all_queries = perfo_queries + subsuelo_queries

    registros_afectados = 0

    with engine.connect() as connection:
        for query in all_queries:
            if query:
                cursor_result = connection.execute(text(query))
                registros_afectados += cursor_result.rowcount

    print('registros_afectados', registros_afectados)

    response = {"num_registros_afectados": registros_afectados}

    return jsonify(response)


@api_blueprint.route('/ajustarMDCurrent')
def ajustar_MDs_current():

    engine = create_engine(connection_url)

    delta = float(request.args.get('delta', None))
    well_id = request.args.get('well_id', None)

    print(f'DELTA INSIDE API: {delta}')
    print(f'WELL ID: {well_id}')

    AJUSTE_MD_QUERY = get_ajuste_MDs_current_query(delta, well_id)

    all_queries = AJUSTE_MD_QUERY.split(';\n')

    registros_afectados = 0

    with engine.connect() as connection:
        for query in all_queries:
            print(query)
            print()
            cursor_result = connection.execute(text(query))
            registros_afectados += cursor_result.rowcount
    
    response = {"num_registros_afectados": registros_afectados}

    return jsonify(response)


@api_blueprint.route('/ajustarMDFromTo')
def ajustar_MDs_from_to():

    engine = create_engine(connection_url)

    delta = float(request.args.get('delta', None))
    well_id = request.args.get('well_id', None)

    print(f'DELTA INSIDE API: {delta}')
    print(f'WELL ID: {well_id}')

    AJUSTE_MD_QUERY = get_ajuste_MDs_from_to_query(delta, well_id)

    all_queries = AJUSTE_MD_QUERY.split(';\n')

    registros_afectados = 0

    with engine.connect() as connection:
        for query in all_queries:
            print(query)
            print()
            cursor_result = connection.execute(text(query))
            registros_afectados += cursor_result.rowcount
    
    response = {"num_registros_afectados": registros_afectados}

    return jsonify(response)


@api_blueprint.route('/ajustarMDSurvey')
def ajustar_MDs_survey():

    engine = create_engine(connection_url)

    delta = float(request.args.get('delta', None))
    well_id = request.args.get('well_id', None)

    print(f'DELTA INSIDE API: {delta}')
    print(f'WELL ID: {well_id}')

    AJUSTE_MD_QUERY = get_ajuste_MDs_survey_query(delta, well_id)

    all_queries = AJUSTE_MD_QUERY.split(';\n')

    registros_afectados = 0

    with engine.connect() as connection:
        for query in all_queries:
            print(query)
            print()
            cursor_result = connection.execute(text(query))
            registros_afectados += cursor_result.rowcount
    
    response = {"num_registros_afectados": registros_afectados}

    return jsonify(response)


@api_blueprint.route('/ajustarMD')
def ajustar_MDs():

    engine = create_engine(connection_url)

    delta = float(request.args.get('delta', None))
    well_id = request.args.get('well_id', None)

    print(f'DELTA INSIDE API: {delta}')
    print(f'WELL ID: {well_id}')

    AJUSTE_MD_QUERY = get_ajuste_MDs_query(delta, well_id)

    all_queries = AJUSTE_MD_QUERY.split(';\n')

    registros_afectados = 0

    with engine.connect() as connection:
        for query in all_queries:
            print(query)
            print()
            cursor_result = connection.execute(text(query))
            registros_afectados += cursor_result.rowcount
    
    response = {"num_registros_afectados": registros_afectados}

    return jsonify(response)


@api_blueprint.route('/predecirInicioOCM')
def predecir_inicio_OCM():

    engine = create_engine(connection_url)

    wellname = request.args.get('wellname', None)

    DATA_BASE_QUERY = get_prediccion_ocm_base_qry(wellname)

    base_df = pd.read_sql(text(DATA_BASE_QUERY), engine)
    base_df.sort_values(by=['Desde'],ascending=[1],inplace=True)

    fecha_ocm = predecir_modelo_deterministico(base_df, wellname)
    fecha_ocm_RF = predecir_RF(base_df, wellname)

    base_df['Operación'] = base_df['Operación'].str.upper()

    base_df['Desde'] = base_df['Desde'].dt.strftime('%m/%d/%Y %H:%M')
    base_df['Hasta'] = base_df['Hasta'].dt.strftime('%m/%d/%Y %H:%M')

    base_df['MDFrom'] = base_df['MDFrom'].round(1)
    base_df['MDto'] = base_df['MDto'].round(1)

    rows_num = base_df.shape[0]
    twenty_perc_rows = int(rows_num*0.17)

    print(base_df.info())
    print(base_df.head())

    needed_cols = ['Desde', 'Hasta','MDFrom','MDto','Operación']
    last_rows_df = base_df.tail(-twenty_perc_rows)[needed_cols]
    
    response = {"time_summary_df": last_rows_df.to_dict('split'),
                "prediccion_deterministica":fecha_ocm,
                "prediccion_RF":fecha_ocm_RF}

    return jsonify(response)


@api_blueprint.route('/insertar_OCM')
def insertar_OCM():

    engine = create_engine(connection_url)

    startdate = request.args.get('startdate', None)
    finaldate = request.args.get('finaldate', None)
    well_id = request.args.get('well_id', None)

    EVENTS_IDS_QRY = get_events_ids_qry()

    event_ids_df= pd.read_sql(text(EVENTS_IDS_QRY), engine)
    event_ids_list = event_ids_df["event_id"].tolist()

    neweventid = generar_event_id_valido(event_ids_list)

    INSERTAR_OCM_QUERY = get_insert_event_qry(well_id, neweventid, startdate, finaldate)

    with engine.connect() as connection:
        trans = connection.begin()
        try:
            cursor_insert_result = connection.execute(text(INSERTAR_OCM_QUERY))
            trans.commit()
            
        except:
            trans.rollback()
            raise Exception('No se logró insertar el evento OCM')
    
    response = {"event_id": neweventid,
                "status": 'Evento OCM Insertado con éxito'}

    return jsonify(response)