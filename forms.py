from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SelectMultipleField, StringField, DateField, SubmitField, TextAreaField,  IntegerField, widgets
from wtforms.validators import DataRequired, NumberRange


class ObraForm(FlaskForm):
    nombre_obra = StringField('Nombre de la Obra', validators=[DataRequired()])
    descripcion_obra = TextAreaField('Descripción de la Obra')
    fecha_inicio = DateField('Fecha de Inicio', validators=[DataRequired()])
    submit = SubmitField('Guardar')

class PartidaForm(FlaskForm):
    nombre_partida = StringField('Nombre de la Partida', validators=[DataRequired()])
    descripcion_partida = TextAreaField('Descripción de la Partida')
    unidad_medida_id = SelectField('Unidad de Medida', coerce=int)  # coerce=int para convertir el valor a entero
    rendimiento = FloatField('Rendimiento', validators=[DataRequired()])
    submit = SubmitField('Guardar')

class ManoObraForm(FlaskForm):
    nombre_mano_de_obra = StringField('Nombre', validators=[DataRequired()])
    descripcion_mano_de_obra = TextAreaField('Descripción')
    costo_hora = FloatField('Costo por Hora')
    submit = SubmitField('Guardar')

class HerramientaForm(FlaskForm):
    nombre_herramienta = StringField('Nombre', validators=[DataRequired()])
    descripcion_herramienta = TextAreaField('Descripción')
    costo_alquiler_dia = FloatField('Costo de Alquiler por Día')
    submit = SubmitField('Guardar')

class MaterialForm(FlaskForm):
    nombre_material = StringField('Nombre', validators=[DataRequired()])
    descripcion_material = TextAreaField('Descripción')
    unidad_medida_id = SelectField('Unidad de Medida', coerce=int)  # coerce=int para convertir el valor a entero
    precio_unitario = FloatField('Precio Unitario', validators=[DataRequired()])
    submit = SubmitField('Guardar')
class CantidadHorasForm(FlaskForm):
    cantidad_horas = FloatField('Cantidad de Horas', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar')

class CantidadDiasForm(FlaskForm):
    cantidad_dias = IntegerField('Cantidad de Días', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar')

class CantidadMaterialForm(FlaskForm):
    cantidad = FloatField('Cantidad', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar')





class AsignarManoObraForm(FlaskForm):
    mano_de_obra = SelectMultipleField('Mano de Obra', choices=[], coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
    cantidad_horas = FloatField("Cantidad de Horas", validators=[NumberRange(min=0)])
    submit = SubmitField('Asignar Mano de Obra')

class AsignarHerramientasForm(FlaskForm):
        herramientas = SelectMultipleField('Herramientas', choices=[], coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
        cantidad_dias = IntegerField("Cantidad de Días", validators=[NumberRange(min=0)])
        submit = SubmitField('Asignar Herramientas')

class AsignarMaterialesForm(FlaskForm):
        materiales = SelectMultipleField('Materiales', choices=[], coerce=int, widget=widgets.ListWidget(prefix_label=False), option_widget=widgets.CheckboxInput())
        cantidad = FloatField("Cantidad", validators=[NumberRange(min=0)])
        submit = SubmitField('Asignar Materiales')