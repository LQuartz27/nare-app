import json
import requests
from flask import Flask, flash, redirect, render_template, request, url_for

from app.api import *
from app.database import *
from app.api.queries import *

from app.forms import *

# template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
# print(__file__)
# print(template_dir)
# template_dir = os.path.join(template_dir, 'templates')
# print(template_dir)

app = Flask(__name__) 
app.config['SECRET_KEY'] = 'PyTmKoIeRfD67.2VbQ'
app.register_blueprint(api_blueprint)

@app.route('/')
def hello_world():  # put application's code here
    return redirect('/home')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/deleteCompStatus', methods=['GET', 'POST'])
def comp_status():

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


@app.route('/ajusteMDs', methods=['GET', 'POST'])
def ajustar_md():

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


@app.route('/ajusteProfEventos', methods=['GET', 'POST'])
def ajuste_prof_eventos():

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

        return redirect(url_for('ajuste_prof_eventos'))

    return render_template('ajuste_prof_eventos.html', **context)


@app.route('/preprocesamientoDDR', methods=['GET', 'POST'])
def preprocesamiento_ddr():

    ROOT = request.url_root

    form = PreprocesamientoDDRForm()

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

        preprocesar_ddr_url = ROOT + \
            url_for('api.preprocesar_ddr', wellname=nombrepozo)

        response = requests.get(preprocesar_ddr_url)
        num_registros_antes = json.loads(response.content.decode("utf-8"))['num_registros_antes']
        num_registros_despues = json.loads(response.content.decode("utf-8"))['num_registros_despues']

        flash('Antes: {} registros'.format(num_registros_antes))
        flash('Despues: {} registros'.format(num_registros_despues))

        return redirect(url_for('preprocesamiento_ddr'))

    return render_template('preprocesamiento_ddr.html', **context)


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
