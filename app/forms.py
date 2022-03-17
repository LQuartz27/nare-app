from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError


def validate_dropdowns(form, field):
    if field.data == "None":
        raise ValidationError("Sorry, you haven't chosen an option")


class PreActualizacionForm(FlaskForm):
    nombrepozo = SelectField('NOMBRE DEL POZO',
                             validators=[DataRequired(), validate_dropdowns])

    td_pozo = StringField('TD DEL POZO', validators=[DataRequired()])
    elevacion_mesa = StringField(
        'ELEVACION DE LA MESA', validators=[DataRequired()])
    elevacion_terreno = StringField(
        'ELEVACION DEL TERRENO', validators=[DataRequired()])
    #diametro_seccion_final = StringField('DIAMETRO ULTIMA SECCION DEL HUECO', validators=[DataRequired()])
    geometria = SelectField('GEOMETRIA DEL POZO',
                            choices=[(None, 'Geometría del Pozo'), ('TIPO J', 'TIPO J'), ('TIPO S', 'TIPO S'),
                                     ('VERTICAL', 'VERTICAL'), ('HORIZONTAL',
                                                                'HORIZONTAL'),
                                     ('RE-ENTRADA', 'RE-ENTRADA'), ('MULTILAT', 'MULTILAT')],
                            validators=[DataRequired(), validate_dropdowns])

    consultar_btn = SubmitField('Consultar')
    preactualizar_btn = SubmitField('Pre Actualizar')


class ProcesoMasivoPozoEspecificoForm(FlaskForm):
    nombrepozo = StringField('NOMBRE DEL POZO', validators=[
                             DataRequired()], id='well-name')
    submit_btn = SubmitField('Borrar Status')


class AjusteMDsForm(FlaskForm):
    nombrepozo = StringField('NOMBRE DEL POZO', validators=[
                             DataRequired()], id='well-name')

    delta = StringField(
        'DELTA en MD', validators=[DataRequired()])
    
    submit_btn = SubmitField('Ajustar MDs')


class AjusteProfEventosForm(FlaskForm):
    nombrepozo = StringField('NOMBRE DEL POZO', validators=[
                             DataRequired()], id='well-name')

    td = StringField(
        'Nueva TD [ft]', validators=[DataRequired()])
    
    submit_btn = SubmitField('Ajustar Profs Props Eventos')


class PreprocesamientoDDRForm(FlaskForm):
    nombrepozo = StringField('NOMBRE DEL POZO', validators=[
                             DataRequired()], id='well-name')
    submit_btn = SubmitField('Generar Excel')
