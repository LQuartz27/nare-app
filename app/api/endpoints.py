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

    with engine.connect() as connection:
        cursor_result = connection.execute(text(BORRAR_COMP_STATUS_QUERY))

    registros_afectados = cursor_result.rowcount

    response = {"num_registros_afectados": registros_afectados}

    return jsonify(response)


@api_blueprint.route('/ajustarMD')
def ajustar_MDs():

    engine = create_engine(connection_url)

    elev_mesa_0 = request.args.get('elev_mesa_0', None)
    elev_mesa_1 = request.args.get('elev_mesa_1', None)
    well_id = request.args.get('well_id', None)

    delta = elev_mesa_1 - elev_mesa_0

    AJUSTE_MD_QUERY = get_ajuste_MDs_query(delta, well_id)

    with engine.connect() as connection:
        cursor_result = connection.execute(text(AJUSTE_MD_QUERY))

    registros_afectados = cursor_result.rowcount

    response = {"num_registros_afectados": registros_afectados}

    return jsonify(response)
