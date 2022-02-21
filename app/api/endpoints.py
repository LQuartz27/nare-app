from urllib import response
from flask import jsonify, request
from itsdangerous import json
from sqlalchemy import create_engine, text
from . import api_blueprint
from .queries import *

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

    # print('QUERY RESULTS.')
    # print(type(data))
    # print(data)

    well_id = data[0][0]

    response = {'WELL COMMON NAME': wellname,
                'WELL ID': well_id}

    return jsonify(response)


@api_blueprint.route('/delcomponentstatus/<string:well_id>', methods=['GET'])
def del_component_status(well_id):

    engine = create_engine(connection_url)

    BORRAR_COMP_STATUS_QUERY = get_borrado_component_status_query(well_id)
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

    engine = create_engine(connection_url)

    with engine.connect() as connection:
        trans = connection.begin()
        try:
            cursor_borrado_result = connection.execute(text(BORRAR_COMP_STATUS_QUERY))
            useless_count = cursor_borrado_result.rowcount
            trans.commit()
        except:
            trans.rollback()
            raise Exception('No se logró eliminar los component status del pozo')

    print(f'Useless DELETE count: {useless_count}')

    response = {"num_registros_afectados": row_count}

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