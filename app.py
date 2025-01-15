from flask import Flask, flash, render_template, Blueprint,abort,request, redirect, url_for
from jinja2 import TemplateNotFound

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import AsignarHerramientasForm, AsignarManoObraForm, AsignarMaterialesForm, CantidadDiasForm, CantidadHorasForm, CantidadMaterialForm, HerramientaForm, MaterialForm, ObraForm, PartidaForm, ManoObraForm # Importa tus formularios
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta' # Cambiar por una clave segura
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Configura la base de datos
db = SQLAlchemy(app)
migrate = Migrate(app, db) # Inicializa Flask-Migrate


# Importar los modelos DESPUÉS de inicializar db
from models import Obra, Partida, ManoDeObra, Herramienta, Material, PartidasManoDeObra, PartidasHerramientas, PartidasMateriales, UnidadMedida

datos = {
  "sistema": "GMDESING APP",
  "usuario": "Leonardo Méndez",
  "perfil": "Administrador",
  "imagen":"perfil.png"
}

@app.route('/obras')
def index():
    obras = Obra.query.all()
    return render_template('obras.html', obras=obras, datos=datos) # Pasa las obras a la plantilla

@app.route('/obras/crear', methods=['GET', 'POST'])
def crear_obra():
    form = ObraForm()
    if form.validate_on_submit():
        nueva_obra = Obra(nombre_obra=form.nombre_obra.data, descripcion_obra=form.descripcion_obra.data, fecha_inicio=form.fecha_inicio.data)
        db.session.add(nueva_obra)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('crear_obra.html', form=form, datos=datos)

@app.route('/obra/<int:id_obra>') # Ruta para ver detalles de una obra y sus partidas
def ver_obra(id_obra):
    obra = Obra.query.get_or_404(id_obra)
    return render_template('ver_obra.html', obra=obra, datos=datos)

@app.route('/obra/<int:id_obra>/partida/crear', methods=['GET', 'POST'])
def crear_partida_obra(id_obra):
    obra = Obra.query.get_or_404(id_obra)
    form = PartidaForm()
    if form.validate_on_submit():
        nueva_partida = Partida(
            nombre_partida=form.nombre_partida.data,
            descripcion_partida=form.descripcion_partida.data,
            id_obra=id_obra  # Asocia la partida a la obra
        )
        db.session.add(nueva_partida)
        db.session.commit()
        flash('Partida creada exitosamente', 'success') # Mensaje flash
        return redirect(url_for('ver_obra', id_obra=id_obra)) # Redirige a la vista de la obra
    return render_template('crear_partida.html', form=form, obra=obra, datos=datos) # Pasa la obra a la plantilla

@app.route('/obra/editar/<int:id_obra>', methods=['GET', 'POST'])
def editar_obra(id_obra):
    obra = Obra.query.get_or_404(id_obra)
    form = ObraForm(obj=obra) # Pre-carga el formulario con los datos de la obra
    if form.validate_on_submit():
        obra.nombre_obra = form.nombre_obra.data
        obra.descripcion_obra = form.descripcion_obra.data
        obra.fecha_inicio = form.fecha_inicio.data
        db.session.commit()
        flash('Obra actualizada correctamente.', 'success')
        return redirect(url_for('index'))
    return render_template('crear_obra.html', form=form, edit=True, obra_id=id_obra, datos=datos) # Reutiliza crear_obra.html

@app.route('/obra/eliminar/<int:id_obra>', methods=['GET'])
def eliminar_obra(id_obra):
    obra = Obra.query.get_or_404(id_obra)
    db.session.delete(obra)
    db.session.commit()
    flash('Obra eliminada correctamente.', 'success')
    return redirect(url_for('index'))

#Ruta para ver partida
@app.route('/partidas')
def listar_partidas():
    partidas = Partida.query.all()
    return render_template('listar_partidas.html', partidas_lista=partidas,datos=datos)

@app.route('/ver_partida/<int:id>', methods=['GET', 'POST'])
def ver_partida(id):
    #partida = Partida.query.get(id)
    partida = Partida.query.get_or_404(id)
    materiales = Material.query.order_by("nombre_material").all()  # Obtener materiales
    herramientas = Herramienta.query.order_by("nombre_herramienta").all()  # Obtener herramientas
    mano_de_obra = ManoDeObra.query.order_by("nombre_mano_de_obra").all()  # Obtener mano de obra 
    #materiales = PartidasMateriales.query.filter_by(id_partida=id).all()  # Obtener materiales de la partida
    #herramientas = PartidasHerramientas.query.filter_by(id_partida=id).all()  # Obtener herramientas de la partida
    #mano_de_obra = PartidasManoDeObra.query.filter_by(id_partida=id).all()  # Obtener mano de obra de la partida

    if request.method == 'POST':
        if 'agregar_material' in request.form:
            nuevo_material = PartidasMateriales(id_material=request.form['id_material'], id_partida=id, cantidad = 1)
            db.session.add(nuevo_material)
            db.session.commit()
            flash('Material agregado exitosamente.', 'success')
        elif 'agregar_herramienta' in request.form:
            herramienta_id = request.form['herramienta_id']
            herramienta = Herramienta.query.get(herramienta_id)
            partida.herramientas.append(herramienta)  # Asociar la herramienta a la partida
            db.session.commit()
            flash('Herramienta agregada exitosamente.', 'success')
        elif 'agregar_mano_de_obra' in request.form:
            nueva_mano_de_obra = ManoDeObra(nombre_trabajador=request.form['nombre_trabajador'], partida_id=id)
            db.session.add(nueva_mano_de_obra)
            db.session.commit()
            flash('Mano de obra agregada exitosamente.', 'success')


    return render_template('ver_partida.html', partida=partida, materiales=materiales, herramientas=herramientas, mano_de_obra=mano_de_obra, datos=datos)

@app.route('/partida/crear', methods=['GET', 'POST'])
def crear_partida():
    form = PartidaForm()
    # Cargar las unidades de medida desde la base de datos
    unidades = UnidadMedida.query.all()
    form.unidad_medida_id.choices = [(unidad.id_unidad_medida, unidad.nombre_unidad_medida) for unidad in unidades]
    if form.validate_on_submit():
        partida = Partida(
            nombre_partida=form.nombre_partida.data,
            descripcion_partida=form.descripcion_partida.data,
            unidad_medida_id=form.unidad_medida_id.data,
            rendimiento=form.rendimiento.data
        )
        db.session.add(partida)
        db.session.commit()
        flash('Partida creada.', 'success')
        return redirect(url_for('listar_partidas'))
    return render_template('crear_partida.html', form=form, datos=datos)

@app.route('/partida/editar/<int:id_partida>', methods=['GET', 'POST'])
def editar_partida(id_partida):
    partida = Partida.query.get_or_404(id_partida)
    print("Partida:",partida)

    form = PartidaForm(obj=partida)
    # Cargar las unidades de medida desde la base de datos
    unidades = UnidadMedida.query.all()
    form.unidad_medida_id.choices = [(unidad.id_unidad_medida, unidad.nombre_unidad_medida) for unidad in unidades]
    if form.validate_on_submit():
        partida.nombre_partida = form.nombre_partida.data
        partida.descripcion_partida = form.descripcion_partida.data
        partida.unidad_medida_id=form.unidad_medida_id.data
        partida.rendimiento=form.rendimiento.data
        db.session.commit()
        flash('Parida actualizada.', 'success')
        return redirect(url_for('listar_partidas'))
    return render_template('crear_partida.html', form=form, datos=datos) # Reutiliza la plantilla de creación

@app.route('/partida/eliminar/<int:id_partida>')
def eliminar_partida(id_partida):
    partida = Partida.query.get_or_404(id_partida)
    db.session.delete(partida)
    db.session.commit()
    flash('Partida eliminada.', 'success')
    return redirect(url_for('listar_partidas'))

@app.route('/partida/<int:id_partida>/mano_obra/crear', methods=['GET', 'POST'])
def crear_mano_obra(id_partida):
    partida = Partida.query.get_or_404(id_partida)
    form = ManoObraForm()
    if form.validate_on_submit():
        mano_obra_existente = ManoDeObra.query.filter_by(descripcion_mano_obra=form.descripcion_mano_obra.data).first()
        if mano_obra_existente:
            # Si ya existe la mano de obra, busca la relación en la tabla intermedia
            partida_mano_obra_existente = PartidasManoDeObra.query.filter_by(id_partida=id_partida, id_mano_obra=mano_obra_existente.id_mano_obra).first()
            if partida_mano_obra_existente:
                flash('Esta mano de obra ya está agregada a esta partida.', 'warning')
                return redirect(url_for('ver_partida', id_partida=id_partida))
            else:
                nueva_relacion = PartidasManoDeObra(id_partida=id_partida, id_mano_obra=mano_obra_existente.id_mano_obra, cantidad_horas=0)
                db.session.add(nueva_relacion)
                db.session.commit()
                flash('Mano de obra agregada a la partida.', 'success')
                return redirect(url_for('ver_partida', id_partida=id_partida))
        else:
            nueva_mano_obra = ManoDeObra(
                descripcion_mano_obra=form.descripcion_mano_obra.data,
                costo_hora=form.costo_hora.data
            )
            db.session.add(nueva_mano_obra)
            db.session.commit()
            nueva_relacion = PartidasManoDeObra(id_partida=id_partida, id_mano_obra=nueva_mano_obra.id_mano_obra, cantidad_horas=0)
            db.session.add(nueva_relacion)
            db.session.commit()
            flash('Mano de obra creada y agregada a la partida.', 'success')
            return redirect(url_for('ver_partida', id_partida=id_partida))

    return render_template('crear_mano_obra.html', form=form, partida=partida, datos=datos)

# Rutas para Materiales
@app.route('/partida/<int:id_partida>/material/crear', methods=['GET', 'POST'])
def crear_material_partida(id_partida):
    partida = Partida.query.get_or_404(id_partida)
    form = MaterialForm()
    if form.validate_on_submit():
        material_existente = Material.query.filter_by(nombre_material=form.nombre_material.data).first()
        if material_existente:
            partida_material_existente = PartidasMateriales.query.filter_by(id_partida=id_partida, id_material=material_existente.id_material).first()
            if partida_material_existente:
                flash('Este material ya está agregado a esta partida.', 'warning')
                return redirect(url_for('ver_partida', id_partida=id_partida))
            else:
                nueva_relacion = PartidasMateriales(id_partida=id_partida, id_material=material_existente.id_material, cantidad=0)
                db.session.add(nueva_relacion)
                db.session.commit()
                flash('Material agregado a la partida.', 'success')
                return redirect(url_for('ver_partida', id_partida=id_partida))
        else:
            nuevo_material = Material(
                nombre_material=form.nombre_material.data,
                unidad_medida=form.unidad_medida.data,
                precio_unitario=form.precio_unitario.data
            )
            db.session.add(nuevo_material)
            db.session.commit()
            nueva_relacion = PartidasMateriales(id_partida=id_partida, id_material=nuevo_material.id_material, cantidad=0)
            db.session.add(nueva_relacion)
            db.session.commit()
            flash('Material creado y agregado a la partida.', 'success')
            return redirect(url_for('ver_partida', id_partida=id_partida))
    return render_template('crear_material_partida.html', form=form, partida=partida, datos=datos)

@app.route('/partida/<int:id_partida>/mano_obra/<int:id_mano_obra>/editar', methods=['GET', 'POST'])
def editar_mano_obra_partida(id_partida, id_mano_obra):
    partida_mano_obra = PartidasManoDeObra.query.filter_by(id_partida=id_partida, id_mano_obra=id_mano_obra).first_or_404()
    form = CantidadHorasForm(obj=partida_mano_obra) # Pre-carga el formulario con los datos existentes
    if form.validate_on_submit():
        partida_mano_obra.cantidad_horas = form.cantidad_horas.data
        db.session.commit()
        flash('Cantidad de horas actualizada.', 'success')
        return redirect(url_for('ver_partida', id_partida=id_partida))
    return render_template('editar_cantidad.html', form=form, elemento="horas de mano de obra", partida=partida_mano_obra.partida)

@app.route('/partida/<int:id_partida>/herramienta/<int:id_herramienta>/editar', methods=['GET', 'POST'])
def editar_herramienta_partida(id_partida, id_herramienta):
    partida_herramienta = PartidasHerramientas.query.filter_by(id_partida=id_partida, id_herramienta=id_herramienta).first_or_404()
    form = CantidadDiasForm(obj=partida_herramienta)
    if form.validate_on_submit():
        partida_herramienta.cantidad_dias = form.cantidad_dias.data
        db.session.commit()
        flash('Cantidad de días actualizada.', 'success')
        return redirect(url_for('ver_partida', id_partida=id_partida))
    return render_template('editar_cantidad.html', form=form, elemento="días de herramienta", partida=partida_herramienta.partida)

@app.route('/partida/<int:id_partida>/material/<int:id_material>/editar', methods=['GET', 'POST'])
def editar_material_partida(id_partida, id_material):
    partida_material = PartidasMateriales.query.filter_by(id_partida=id_partida, id_material=id_material).first_or_404()
    form = CantidadMaterialForm(obj=partida_material)
    if form.validate_on_submit():
        partida_material.cantidad = form.cantidad.data
        db.session.commit()
        flash('Cantidad de material actualizada.', 'success')
        return redirect(url_for('ver_partida', id_partida=id_partida))
    return render_template('editar_cantidad.html', form=form, elemento="cantidad de material", partida=partida_material.partida)

# Rutas para Mano de Obra
@app.route('/mano_de_obra')
def listar_mano_de_obra():
    mano_de_obra_lista = ManoDeObra.query.all()
    return render_template('listar_mano_de_obra.html', mano_de_obra_lista=mano_de_obra_lista, datos=datos)

@app.route('/mano_de_obra/crear', methods=['GET', 'POST'])
def crear_mano_de_obra():
    form = ManoObraForm()
    if form.validate_on_submit():
        mano_de_obra = ManoDeObra(
            nombre_mano_de_obra=form.nombre_mano_de_obra.data,
            descripcion_mano_de_obra=form.descripcion_mano_de_obra.data,
            costo_hora=form.costo_hora.data
        )
        db.session.add(mano_de_obra)
        db.session.commit()
        flash('Mano de obra creada.', 'success')
        return redirect(url_for('listar_mano_de_obra'))
    return render_template('crear_mano_de_obra.html', form=form, datos=datos)

@app.route('/partida/<int:id_partida>/asignar_mano_de_obra', methods=['GET', 'POST'])
def asignar_mano_de_obra(id_partida):
    partida = Partida.query.get_or_404(id_partida)
    form = AsignarManoObraForm()
    form.mano_de_obra.choices = [(mo.id_mano_de_obra, mo.nombre_mano_de_obra) for mo in ManoDeObra.query.all()]
    if form.validate_on_submit():
        manos_de_obra_seleccionadas = [ManoDeObra.query.get(id_mo) for id_mo in form.mano_de_obra.data]
        for mano_de_obra in manos_de_obra_seleccionadas:
            relacion_existente = PartidasManoDeObra.query.filter_by(id_partida=id_partida, id_mano_de_obra=mano_de_obra.id_mano_de_obra).first()
            if relacion_existente:
                relacion_existente.cantidad_horas = form.cantidad_horas.data
                flash(f'Se actualizo la cantidad de horas para {mano_de_obra.nombre_mano_de_obra}', 'success')
            else:
                nueva_relacion = PartidasManoDeObra(id_partida=id_partida, id_mano_de_obra=mano_de_obra.id_mano_de_obra, cantidad_horas=form.cantidad_horas.data)
                db.session.add(nueva_relacion)
                flash(f'Se asigno {mano_de_obra.nombre_mano_de_obra} a la partida', 'success')
        db.session.commit()
        return redirect(url_for('ver_partida', id_partida=id_partida))
    return render_template('asignar_mano_de_obra.html', form=form, partida=partida)

@app.route('/mano_de_obra/editar/<int:id_mano_de_obra>', methods=['GET', 'POST'])
def editar_mano_de_obra(id_mano_de_obra):
    mano_de_obra = ManoDeObra.query.get_or_404(id_mano_de_obra)
    form = ManoObraForm(obj=mano_de_obra)
    if form.validate_on_submit():
        mano_de_obra.nombre_mano_de_obra = form.nombre_mano_de_obra.data
        mano_de_obra.descripcion_mano_de_obra = form.descripcion_mano_de_obra.data
        mano_de_obra.costo_hora = form.costo_hora.data
        db.session.commit()
        flash('Mano de obra actualizada.', 'success')
        return redirect(url_for('listar_mano_de_obra'))
    return render_template('crear_mano_de_obra.html', form=form, datos=datos) # Reutiliza la plantilla de creación

@app.route('/mano_de_obra/eliminar/<int:id_mano_de_obra>')
def eliminar_mano_de_obra(id_mano_de_obra):
    mano_de_obra = ManoDeObra.query.get_or_404(id_mano_de_obra)
    db.session.delete(mano_de_obra)
    db.session.commit()
    flash('Mano de obra eliminada.', 'success')
    return redirect(url_for('listar_mano_de_obra'))

# Rutas para Material
@app.route('/materiales')
def listar_materiales():
    materiales_lista = Material.query.all()
    return render_template('listar_materiales.html', materiales_lista=materiales_lista, datos=datos)

@app.route('/material/crear', methods=['GET', 'POST'])
def crear_material():
    form = MaterialForm()
    # Cargar las unidades de medida desde la base de datos
    unidades = UnidadMedida.query.all()
    form.unidad_medida_id.choices = [(unidad.id_unidad_medida, unidad.nombre_unidad_medida) for unidad in unidades]
    if form.validate_on_submit():
        material = Material(
            nombre_material=form.nombre_material.data,
            descripcion_material=form.descripcion_material.data,
            unidad_medida_id=form.unidad_medida_id.data,
            precio_unitario=form.precio_unitario.data
        )
        db.session.add(material)
        db.session.commit()
        flash('Material creado.', 'success')
        return redirect(url_for('listar_materiales'))
    return render_template('crear_material.html', form=form, datos=datos)

@app.route('/partida/<int:id_partida>/asignar_material', methods=['GET', 'POST'])
def asignar_material(id_partida):
    partida = Partida.query.get_or_404(id_partida)
    form = AsignarMaterialesForm()
    form.materiales.choices = [(ma.id_material, ma.nombre_material) for ma in Material.query.all()]
    if form.validate_on_submit():
        materiales_seleccionados = [Material.query.get(id_ma) for id_ma in form.materiales.data]
        for material in materiales_seleccionados:
            relacion_existente = PartidasMateriales.query.filter_by(id_partida=id_partida, id_material=material.id_material).first()
            if relacion_existente:
                relacion_existente.cantidad = form.cantidad.data
                flash(f'Se actualizo la cantidad de horas para {material.nombre_material}', 'success')
            else:
                nueva_relacion = PartidasManoDeObra(id_partida=id_partida, id_material=material.id_material, cantidad=form.cantidad.data)
                db.session.add(nueva_relacion)
                flash(f'Se asigno {material.nombre_material} a la partida', 'success')
        db.session.commit()
        return redirect(url_for('ver_partida', id_partida=id_partida))
    return render_template('asignar_material.html', form=form, partida=partida, datos=datos)

@app.route('/material/editar/<int:id_material>', methods=['GET', 'POST'])
def editar_material(id_material):
    material = Material.query.get_or_404(id_material)
    form = MaterialForm(obj=material)
    if form.validate_on_submit():
        material.nombre_material = form.nombre_material.data
        material.descripcion_material = form.descripcion_material.data
        material.unidad_medida = form.unidad_medida.data
        material.precio_unitario = form.precio_unitario.data
        db.session.commit()
        flash('Material actualizado.', 'success')
        return redirect(url_for('listar_materiales'))
    return render_template('crear_material.html', form=form, datos=datos) # Reutiliza la plantilla de creación

@app.route('/material/eliminar/<int:id_material>')
def eliminar_material(id_material):
    material = Material.query.get_or_404(id_material)
    db.session.delete(material)
    db.session.commit()
    flash('Material  eliminado.', 'success')
    return redirect(url_for('listar_materiales'))

# Rutas para Herramientas
@app.route('/herramientas')
def listar_herramientas():
    herramientas_lista = Herramienta.query.all()
    return render_template('listar_herramientas.html', herramientas_lista=herramientas_lista, datos=datos)

@app.route('/herramienta/crear', methods=['GET', 'POST'])
def crear_herramienta():
    form = HerramientaForm()
    if form.validate_on_submit():
        herramienta = Herramienta(
            nombre_herramienta=form.nombre_herramienta.data,
            descripcion_herramienta=form.descripcion_herramienta.data,
            costo_alquiler_dia=form.costo_alquiler_dia.data,
        )
        db.session.add(herramienta)
        db.session.commit()
        flash('Herramienta creada.', 'success')
        return redirect(url_for('listar_herramientas'))
    return render_template('crear_herramienta.html', form=form, datos=datos)

@app.route('/partida/<int:id_partida>/asignar_herramienta', methods=['GET', 'POST'])
def asignar_herramienta(id_partida):
    partida = Partida.query.get_or_404(id_partida)
    form = AsignarHerramientasForm()
    form.herramientas.choices = [(he.id_herramienta, he.nombre_herramienta) for he in Herramienta.query.all()]
    if form.validate_on_submit():
        herramientas_seleccionadas = [Herramienta.query.get(id_he) for id_he in form.herramientas.data]
        for herramienta in herramientas_seleccionadas:
            relacion_existente = PartidasHerramientas.query.filter_by(id_partida=id_partida, id_herramienta=herramienta.id_herramienta).first()
            if relacion_existente:
                relacion_existente.cantidad_dias = form.cantidad_dias.data
                flash(f'Se actualizo la cantidad de Días para {herramienta.nombre_herramienta}', 'success')
            else:
                nueva_relacion = PartidasHerramientas(id_partida=id_partida, id_herramienta=herramienta.id_herramienta, cantidad_dias=form.cantidad_dias.data)
                db.session.add(nueva_relacion)
                flash(f'Se asigno {herramienta.nombre_herramienta} a la partida', 'success')
        db.session.commit()
        return redirect(url_for('ver_partida', id_partida=id_partida))
    return render_template('asignar_herramienta.html', form=form, partida=partida, datos=datos)

@app.route('/herramienta/editar/<int:id_herramienta>', methods=['GET', 'POST'])
def editar_herramienta(id_herramienta):
    herramienta = Herramienta.query.get_or_404(id_herramienta)
    form = HerramientaForm(obj=herramienta)
    if form.validate_on_submit():
        herramienta.nombre_herramienta = form.nombre_herramienta.data
        herramienta.descripcion_herramienta = form.descripcion_herramienta.data
        herramienta.costo_alquiler_dia = form.costo_alquiler_dia.data
        db.session.commit()
        flash('Herramienta actualizada.', 'success')
        return redirect(url_for('listar_herramientas'))
    return render_template('crear_herramienta.html', form=form, datos=datos) # Reutiliza la plantilla de creación

@app.route('/herramienta/eliminar/<int:id_herramienta>')
def eliminar_herramienta(id_herramienta):
    herramienta = Herramienta.query.get_or_404(id_herramienta)
    db.session.delete(herramienta)
    db.session.commit()
    flash('Herramienta eliminada.', 'success')
    return redirect(url_for('listar_herramientas'))

@app.route('/')
def home():
    return render_template('index.html', active_route='/', datos=datos)

@app.route('/about')
def about():
    return render_template('index.html', active_route='/about', datos=datos)

@app.route('/contact')
def contact():
    return render_template('index.html', active_route='/contact', datos=datos)

@app.route('/dashboard')
def dashboard():
    return render_template('index.html', active_route='/dashboard', datos=datos)

@app.route('/settings')
def settings():
    return render_template('test.html', active_route='/settings', datos=datos)

@app.route('/profile')
def profile():
    return render_template('index.html', active_route='/profile', datos=datos)

if __name__ == '__main__':
    with app.app_context(): # Esencial para crear la base de datos
        db.create_all() # Crea las tablas en la base de datos
    app.run(debug=True)

