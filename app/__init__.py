import json
import requests
import logging
import traceback
from flask import (Flask, flash, redirect, render_template,
                   request, url_for, Response, send_file)

from app.api import *
from app.api.preprocesado_ddr import *
from app.database import *
from app.api.queries import *
from app.activity_phases import *

from app.forms import *

cwd = os.getcwd()
LOGS_FOLDER = os.path.join(cwd, 'logs')

if not os.path.exists(LOGS_FOLDER):
    os.mkdir(LOGS_FOLDER)

file_basename = os.path.basename(__file__)
filename = file_basename.split('.')[0]
log_file = os.path.join(LOGS_FOLDER, '{}.log'.format(filename))
log_file_path = os.path.abspath(log_file)

logging.basicConfig(filename=log_file_path,
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    datefmt='%Y/%m/%d %H:%M:%S')

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'PyTmKoIeRfD67.2VbQ'
app.register_blueprint(api_blueprint)
app.register_blueprint(activity_phases_blueprint)


@app.route('/')
def hello_world():  # put application's code here
    return redirect('/home')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/error')
def error_page():
    return render_template('404.html')


@app.route('/ajustarProfundidades', methods=['GET', 'POST'])
def ajustar_profundidades():
    return render_template('ajustar_profundidades.html')


@app.route('/ajusteTDEventos', methods=['GET', 'POST'])
def ajustar_prof_eventos():
    try:
        ROOT = request.url_root

        form = AjusteProfEventosForm()

        context = {
            'form': form,
        }

        if form.validate_on_submit():
            nombrepozo = form.nombrepozo.data
            new_td = form.td.data

            get_well_id_url = ROOT + url_for('api.wellid', wellname=nombrepozo)

            response = requests.get(get_well_id_url)
            data = json.loads(response.content.decode("utf-8"))
            well_id = data['WELL ID']

            print('NOMBRE DEL POZO')
            print(nombrepozo)
            print('WELL ID')
            print(well_id)
            print('NUEVA TD')
            print(new_td)

            ajustar_profs_eventos_url = ROOT + \
                url_for('api.ajustar_profs_eventos')

            print(ajustar_profs_eventos_url)

            response = requests.get(ajustar_profs_eventos_url, params={"new_td": new_td,
                                                            "well_id":well_id
                                                            }
                                    )
            num_registros_actualizados = json.loads(response.content.decode("utf-8"))['num_registros_afectados']

            flash(f'Se actualizaron {num_registros_actualizados} registros')

            return redirect(url_for('ajustar_prof_eventos'))

        return render_template('ajuste_prof_eventos.html', **context)
    
    except Exception as e:
        print(e)
        logging.error(e)
        logging.info('TRACE BACK FOUND:')
        logging.error(traceback.format_exc())
        return redirect(url_for('error_page'))


@app.route('/ajusteMDsCurrent', methods=['GET', 'POST'])
def ajustar_md_current():
    try:
        ROOT = request.url_root
        # print('REQUEST ROOT: {}'.format(ROOT))

        form = AjusteMDsForm()

        context = {
            'form': form,
        }

        if form.validate_on_submit():
            nombrepozo = form.nombrepozo.data
            delta = form.delta.data

            get_well_id_url = ROOT + url_for('api.wellid', wellname=nombrepozo)

            response = requests.get(get_well_id_url)
            data = json.loads(response.content.decode("utf-8"))
            well_id = data['WELL ID']

            print('NOMBRE DEL POZO')
            print(nombrepozo)
            print('WELL ID')
            print(well_id)
            print('DELTA')
            print(delta)

            ajustar_MDs_url = ROOT + \
                url_for('api.ajustar_MDs_current')

            print(ajustar_MDs_url)

            response = requests.get(ajustar_MDs_url, params={"delta": delta,
                                                            "well_id":well_id
                                                            }
                                    )
            num_registros_actualizados = json.loads(response.content.decode("utf-8"))['num_registros_afectados']

            flash(f'Se actualizaron {num_registros_actualizados} registros')

            return redirect(url_for('ajustar_md_current'))

        return render_template('ajustar_md_current.html', **context)
    
    except Exception as e:
        print(e)
        logging.error(e)
        logging.info('TRACE BACK FOUND:')
        logging.error(traceback.format_exc())
        return redirect(url_for('error_page'))

@app.route('/ajusteMDsFromTo', methods=['GET', 'POST'])
def ajustar_md_from_to():
    try:
        ROOT = request.url_root
        # print('REQUEST ROOT: {}'.format(ROOT))

        form = AjusteMDsForm()

        context = {
            'form': form,
        }

        if form.validate_on_submit():
            nombrepozo = form.nombrepozo.data
            delta = form.delta.data

            get_well_id_url = ROOT + url_for('api.wellid', wellname=nombrepozo)

            response = requests.get(get_well_id_url)
            data = json.loads(response.content.decode("utf-8"))
            well_id = data['WELL ID']

            print('NOMBRE DEL POZO')
            print(nombrepozo)
            print('WELL ID')
            print(well_id)
            print('DELTA')
            print(delta)

            ajustar_MDs_url = ROOT + \
                url_for('api.ajustar_MDs_from_to')

            print(ajustar_MDs_url)

            response = requests.get(ajustar_MDs_url, params={"delta": delta,
                                                            "well_id":well_id
                                                            }
                                    )
            num_registros_actualizados = json.loads(response.content.decode("utf-8"))['num_registros_afectados']

            flash(f'Se actualizaron {num_registros_actualizados} registros')

            return redirect(url_for('ajustar_md_from_to'))

        return render_template('ajustar_md_from_to.html', **context)
    
    except Exception as e:
        print(e)
        logging.error(e)
        logging.info('TRACE BACK FOUND:')
        logging.error(traceback.format_exc())
        return redirect(url_for('error_page'))

@app.route('/ajusteMDsSurvey', methods=['GET', 'POST'])
def ajustar_md_survey():
    try:
        ROOT = request.url_root
        # print('REQUEST ROOT: {}'.format(ROOT))

        form = AjusteMDsForm()

        context = {
            'form': form,
        }

        if form.validate_on_submit():
            nombrepozo = form.nombrepozo.data
            delta = form.delta.data

            get_well_id_url = ROOT + url_for('api.wellid', wellname=nombrepozo)

            response = requests.get(get_well_id_url)
            data = json.loads(response.content.decode("utf-8"))
            well_id = data['WELL ID']

            print('NOMBRE DEL POZO')
            print(nombrepozo)
            print('WELL ID')
            print(well_id)
            print('DELTA')
            print(delta)

            ajustar_MDs_url = ROOT + \
                url_for('api.ajustar_MDs_survey')

            print(ajustar_MDs_url)

            response = requests.get(ajustar_MDs_url, params={"delta": delta,
                                                            "well_id":well_id
                                                            }
                                    )
            num_registros_actualizados = json.loads(response.content.decode("utf-8"))['num_registros_afectados']

            flash(f'Se actualizaron {num_registros_actualizados} registros')

            return redirect(url_for('ajustar_md_survey'))

        return render_template('ajustar_md_survey.html', **context)
    except Exception as e:
        print(e)
        logging.error(e)
        logging.info('TRACE BACK FOUND:')
        logging.error(traceback.format_exc())
        return redirect(url_for('error_page'))

@app.route('/ajusteMDs', methods=['GET', 'POST'])
def ajustar_md():
    try:
        ROOT = request.url_root
        # print('REQUEST ROOT: {}'.format(ROOT))

        form = AjusteMDsForm()

        context = {
            'form': form,
        }

        if form.validate_on_submit():
            nombrepozo = form.nombrepozo.data
            delta = form.delta.data

            get_well_id_url = ROOT + url_for('api.wellid', wellname=nombrepozo)

            response = requests.get(get_well_id_url)
            data = json.loads(response.content.decode("utf-8"))
            well_id = data['WELL ID']

            print('NOMBRE DEL POZO')
            print(nombrepozo)
            print('WELL ID')
            print(well_id)
            print('DELTA')
            print(delta)

            ajustar_MDs_url = ROOT + \
                url_for('api.ajustar_MDs')

            print(ajustar_MDs_url)

            response = requests.get(ajustar_MDs_url, params={"delta": delta,
                                                            "well_id":well_id
                                                            }
                                    )
            num_registros_actualizados = json.loads(response.content.decode("utf-8"))['num_registros_afectados']

            flash(f'Se actualizaron {num_registros_actualizados} registros')

            return redirect(url_for('ajustar_md'))

        return render_template('ajuste_md.html', **context)
    except Exception as e:
        print(e)
        logging.error(e)
        logging.info('TRACE BACK FOUND:')
        logging.error(traceback.format_exc())
        return redirect(url_for('error_page'))

@app.route('/deleteCompStatus', methods=['GET', 'POST'])
def comp_status():
    try:
        ROOT = request.url_root
        # print('REQUEST ROOT: {}'.format(ROOT))

        form = ProcesoMasivoPozoEspecificoForm()

        context = {
            'form': form,
        }

        if form.validate_on_submit():
            nombrepozo = form.nombrepozo.data

            get_well_id_url = ROOT + url_for('api.wellid', wellname=nombrepozo)

            response = requests.get(get_well_id_url)
            data = json.loads(response.content.decode("utf-8"))
            well_id = data['WELL ID']

            print('NOMBRE DEL POZO')
            print(nombrepozo)
            print('WELL ID')
            print(f'|{well_id}|')

            del_comp_status_url = ROOT + \
                url_for('api.del_component_status', well_id=well_id)

            response = requests.get(del_comp_status_url)
            num_registros_antes = json.loads(response.content.decode("utf-8"))['num_registros_antes']
            num_registros_despues = json.loads(response.content.decode("utf-8"))['num_registros_despues']

            flash('Antes: {} registros'.format(num_registros_antes))
            flash('Despues: {} registros'.format(num_registros_despues))

            return redirect(url_for('comp_status'))

        return render_template('component_status.html', **context)
    
    except Exception as e:
        print(e)
        logging.error(e)
        logging.info('TRACE BACK FOUND:')
        logging.error(traceback.format_exc())
        return redirect(url_for('error_page'))

@app.route('/preprocesamientoDDR', methods=['GET', 'POST'])
def preprocesar_ddr():
    try:
        ROOT = request.url_root

        form = PreprocesamientoDDRForm()

        context = {
            'form': form,
        }

        if form.validate_on_submit():
            nombrepozo = form.nombrepozo.data

            engine = create_engine(connection_url)
        
            TIME_SUMMARY_QRY = get_perfo_time_summary_qry(nombrepozo)
            
            output, filename = crear_excel_actividades_segmentadas(engine, text(TIME_SUMMARY_QRY), nombrepozo)

            return send_file(output, as_attachment=True, attachment_filename=filename)

        return render_template('preprocesamiento_ddr.html', **context)

    except Exception as e:
        print(e)
        logging.error(e)
        logging.info('TRACE BACK FOUND:')
        logging.error(traceback.format_exc())
        return redirect(url_for('error_page'))

@app.route('/asignarActivityPhases', methods=['GET', 'POST'])
def asignar_activity_phases():
    try:
        ROOT = request.url_root

        form = AisgnarFasesForm()

        context = {
            'form': form,
        }

        if form.validate_on_submit():
            nombrepozo = form.nombrepozo.data

            asignar_activity_phases_url = ROOT + \
                url_for('activityPhases.asignar_activity_phases', wellname=nombrepozo)
                
            response = requests.get(asignar_activity_phases_url)

            flash('Activity Phases asignadas!!')

            return redirect(url_for('asignar_activity_phases'))

        return render_template('asignar_activity_phases.html', **context)
    
    except Exception as e:
        print(e)
        logging.error(e)
        logging.info('TRACE BACK FOUND:')
        logging.error(traceback.format_exc())
        return redirect(url_for('error_page'))

@app.route('/preactualizacion', methods=['GET', 'POST'])
def preactualizacion():

    preactualizacion_form = PreActualizacionForm()

    wellcommon_names_choices, _ = get_well_common_names()
    print(wellcommon_names_choices)
    print(_)

    preactualizacion_form.nombrepozo.choices = wellcommon_names_choices
    context = {
        'preactualizacion_form': preactualizacion_form
    }

    if preactualizacion_form.validate_on_submit():
        nombrepozo = preactualizacion_form.nombrepozo.data
        td_pozo = preactualizacion_form.td_pozo.data
        elevacion_mesa = preactualizacion_form.elevacion_mesa.data
        elevacion_terreno = preactualizacion_form.elevacion_terreno.data
        geometria = preactualizacion_form.geometria.data

        print('nombrepozo', nombrepozo)
        print('td_pozo', td_pozo)
        print('elevacion_mesa', elevacion_mesa)
        print('elevacion_terreno', elevacion_terreno)
        print('geometria', geometria)

        return redirect(url_for('preactualizacion'))

    return render_template('preactualizacion.html', **context)
