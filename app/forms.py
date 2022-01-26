from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError

def validate_dropdowns(form, field):
    if field.data == "None":
        raise ValidationError("Sorry, you haven't chosen an option")


class PreActualizacionForm(FlaskForm):
    nombrepozo = SelectField('NOMBRE DEL POZO',
                             choices=[(None, 'Well Common Name'),
                                      ('MOR BF 05', 'MOR BF 05'),
                                      ('MORC0002N', 'MORICHE N 02'),
                                      ('JAZM0001AN', 'JAZ AN 01')],
                             validators=[DataRequired(), validate_dropdowns])

    td_pozo = StringField('TD DEL POZO', validators=[DataRequired()])
    elevacion_mesa = StringField('ELEVACION DE LA MESA', validators=[DataRequired()])
    elevacion_terreno = StringField('ELEVACION DEL TERRENO', validators=[DataRequired()])
    #diametro_seccion_final = StringField('DIAMETRO ULTIMA SECCION DEL HUECO', validators=[DataRequired()])
    geometria = SelectField('GEOMETRIA DEL POZO',
                             choices=[(None, 'Geometría del Pozo'),('TIPO J', 'TIPO J'), ('TIPO S', 'TIPO S'),
                                      ('VERTICAL', 'VERTICAL'), ('HORIZONTAL','HORIZONTAL'),
                                      ('RE-ENTRADA','RE-ENTRADA'), ('MULTILAT','MULTILAT')],
                             validators=[DataRequired(), validate_dropdowns])

    consultar_btn = SubmitField('Consultar')
    preactualizar_btn = SubmitField('Pre Actualizar')


class TomaEvidenciaForm(FlaskForm):
    pass