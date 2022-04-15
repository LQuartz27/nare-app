from flask import Blueprint, jsonify
from .ajuste_fases import *

activity_phases_blueprint = Blueprint('activityPhases', __name__, url_prefix='/activityPhases')

@activity_phases_blueprint.route('/<string:wellname>', methods=['GET'])
def asignar_activity_phases(wellname):
    asignar_activity_phases(wellname)
    
    response = {"change": f"Se asignaron activity phases para el pozo {wellname}"}

    return jsonify(response)