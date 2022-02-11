from flask import Flask, redirect, render_template, url_for
import pyodbc
from sqlalchemy import create_engine, text
from app.forms import PreActualizacionForm
from app.api import *
from app.api.queries import *
from app.database import *
import os

# template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
# print(__file__)
# print(template_dir)
# template_dir = os.path.join(template_dir, 'templates')
# print(template_dir)

app = Flask(__name__)  # , template_folder=template_dir)
app.config['SECRET_KEY'] = 'PyTmKoIeRfD67.2VbQ'
app.register_blueprint(api_blueprint)

print(connection_url)
# print(engine)


@app.route('/')
def hello_world():  # put application's code here
    return redirect('/home')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/preactualizacion', methods=['GET', 'POST'])
def preactualizacion():
    engine = create_engine(connection_url)

    preactualizacion_form = PreActualizacionForm()

    wellcommon_names = [(None, 'Well Common Name')]

    with engine.connect() as connection:
        # WELL_COMMON_NAMES_QUERY
        result_cursor = connection.execute(text(WELL_COMMON_NAMES_QUERY))
        ddbb_wellnames_result = result_cursor.fetchall()
        ddbb_wellnames_list = [tupla[0] for tupla in ddbb_wellnames_result if tupla[0]]
        # print(type(ddbb_wellnames_list))
        print(ddbb_wellnames_list)

    wellcommon_names.extend(
        sorted([(wellname.strip(), wellname) for wellname in ddbb_wellnames_list], key=lambda variable: variable[0]))

    preactualizacion_form.nombrepozo.choices = wellcommon_names

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