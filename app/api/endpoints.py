from urllib import response
from flask import jsonify, request, url_for
from itsdangerous import json
from sqlalchemy import create_engine, text
from . import api_blueprint
from .queries import *
import requests

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

    # engine.dispose()

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
            # from sqlalchemy import Table, MetaData

            # metadata_obj = MetaData()
            # metadata_obj.reflect(connection)      

            # # print(metadata_obj.tables)
            # # print(metadata_obj.tables.keys())
            # CD_ASSEMBLY_COMP_STATUS = metadata_obj.tables['CD_ASSEMBLY_COMP_STATUS_T']

            # print(type(CD_ASSEMBLY_COMP_STATUS))
            # print(CD_ASSEMBLY_COMP_STATUS)

            # dele = CD_ASSEMBLY_COMP_STATUS.delete().where(CD_ASSEMBLY_COMP_STATUS.c.well_id == 'h9yJX1iFMu')
            # print(dele)
            # connection.execute(dele)
            # cursor_borrado_result = connection.execute(text(BORRAR_COMP_STATUS_QUERY))
            
            # print(type(cursor_borrado_result))
            # print(cursor_borrado_result)                                             
            # useless_count = cursor_borrado_result.rowcount
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


@api_blueprint.route('/ajustarMD')
def ajustar_MDs():

    engine = create_engine(connection_url)

    delta = float(request.args.get('delta', None))
    well_id = request.args.get('well_id', None)

    print(f'DELTA INSIDE API: {delta}')
    print(f'WELL ID: {well_id}')

    # delta = 10

    AJUSTE_MD_QUERY = get_ajuste_MDs_query(delta, well_id)
    print('QUERY A EJECUTAR:')
    print(AJUSTE_MD_QUERY)
    print(text(AJUSTE_MD_QUERY))

    with engine.connect() as connection:
        cursor_result = connection.execute(text(AJUSTE_MD_QUERY))

    registros_afectados = cursor_result.rowcount

    response = {"num_registros_afectados": registros_afectados}

    return jsonify(response)