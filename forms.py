from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, DateField, SubmitField, TextAreaField,  IntegerField
from wtforms.validators import DataRequired

class ObraForm(FlaskForm):
    nombre_obra = StringField('Nombre de la Obra', validators=[DataRequired()])
    descripcion_obra = StringField('Descripción de la Obra')
    fecha_inicio = DateField('Fecha de Inicio', validators=[DataRequired()])
    submit = SubmitField('Crear Obra')

class PartidaForm(FlaskForm):
    nombre_partida = StringField('Nombre de la Partida', validators=[DataRequired()])
    descripcion_partida = TextAreaField('Descripción de la Partida')
    submit = SubmitField('Crear Partida')

class ManoObraForm(FlaskForm):
    descripcion_mano_obra = StringField('Descripción del Trabajo', validators=[DataRequired()])
    costo_hora = FloatField('Costo por Hora', validators=[DataRequired()])
    submit = SubmitField('Agregar Mano de Obra')