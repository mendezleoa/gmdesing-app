from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, DateField, SubmitField, TextAreaField,  IntegerField
from wtforms.validators import DataRequired, NumberRange

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

class HerramientaForm(FlaskForm):
    nombre_herramienta = StringField('Nombre de la Herramienta', validators=[DataRequired()])
    costo_alquiler_dia = FloatField('Costo de Alquiler por Día')  # Opcional, puede ser None
    submit = SubmitField('Agregar Herramienta')

class MaterialForm(FlaskForm):
    nombre_material = StringField('Nombre del Material', validators=[DataRequired()])
    unidad_medida = StringField('Unidad de Medida (ej: kg, m2, unidad)', validators=[DataRequired()])
    precio_unitario = FloatField('Precio Unitario', validators=[DataRequired()])
    submit = SubmitField('Agregar Material')

class CantidadHorasForm(FlaskForm):
    cantidad_horas = FloatField('Cantidad de Horas', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar')

class CantidadDiasForm(FlaskForm):
    cantidad_dias = IntegerField('Cantidad de Días', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar')

class CantidadMaterialForm(FlaskForm):
    cantidad = FloatField('Cantidad', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar')