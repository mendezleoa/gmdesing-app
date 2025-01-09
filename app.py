from flask import Flask, flash, render_template, Blueprint,abort,request, redirect, url_for
from jinja2 import TemplateNotFound

from flask_sqlalchemy import SQLAlchemy
from forms import CantidadDiasForm, CantidadHorasForm, CantidadMaterialForm, HerramientaForm, MaterialForm, ObraForm, PartidaForm, ManoObraForm # Importa tus formularios
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta' # Cambiar por una clave segura
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Configura la base de datos
db = SQLAlchemy(app)

# Importar los modelos DESPUÉS de inicializar db
from models import Obra, Partida, ManoObra, Herramienta, Material, PartidasManoObra, PartidasHerramientas, PartidasMateriales

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
def crear_partida(id_obra):
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
@app.route('/partida/<int:id_partida>')
def ver_partida(id_partida):
    partida = Partida.query.get_or_404(id_partida)
    return render_template('ver_partida.html', partida=partida)

@app.route('/partida/<int:id_partida>/mano_obra/crear', methods=['GET', 'POST'])
def crear_mano_obra(id_partida):
    partida = Partida.query.get_or_404(id_partida)
    form = ManoObraForm()
    if form.validate_on_submit():
        mano_obra_existente = ManoObra.query.filter_by(descripcion_mano_obra=form.descripcion_mano_obra.data).first()
        if mano_obra_existente:
            # Si ya existe la mano de obra, busca la relación en la tabla intermedia
            partida_mano_obra_existente = PartidasManoObra.query.filter_by(id_partida=id_partida, id_mano_obra=mano_obra_existente.id_mano_obra).first()
            if partida_mano_obra_existente:
                flash('Esta mano de obra ya está agregada a esta partida.', 'warning')
                return redirect(url_for('ver_partida', id_partida=id_partida))
            else:
                nueva_relacion = PartidasManoObra(id_partida=id_partida, id_mano_obra=mano_obra_existente.id_mano_obra, cantidad_horas=0)
                db.session.add(nueva_relacion)
                db.session.commit()
                flash('Mano de obra agregada a la partida.', 'success')
                return redirect(url_for('ver_partida', id_partida=id_partida))
        else:
            nueva_mano_obra = ManoObra(
                descripcion_mano_obra=form.descripcion_mano_obra.data,
                costo_hora=form.costo_hora.data
            )
            db.session.add(nueva_mano_obra)
            db.session.commit()
            nueva_relacion = PartidasManoObra(id_partida=id_partida, id_mano_obra=nueva_mano_obra.id_mano_obra, cantidad_horas=0)
            db.session.add(nueva_relacion)
            db.session.commit()
            flash('Mano de obra creada y agregada a la partida.', 'success')
            return redirect(url_for('ver_partida', id_partida=id_partida))

    return render_template('crear_mano_obra.html', form=form, partida=partida, datos=datos)

# Rutas para Herramientas
@app.route('/partida/<int:id_partida>/herramienta/crear', methods=['GET', 'POST'])
def crear_herramienta(id_partida):
    partida = Partida.query.get_or_404(id_partida)
    form = HerramientaForm()
    if form.validate_on_submit():
        herramienta_existente = Herramienta.query.filter_by(nombre_herramienta=form.nombre_herramienta.data).first()
        if herramienta_existente:
            partida_herramienta_existente = PartidasHerramientas.query.filter_by(id_partida=id_partida, id_herramienta=herramienta_existente.id_herramienta).first()
            if partida_herramienta_existente:
                flash('Esta herramienta ya está agregada a esta partida.', 'warning')
                return redirect(url_for('ver_partida', id_partida=id_partida))
            else:
                nueva_relacion = PartidasHerramientas(id_partida=id_partida, id_herramienta=herramienta_existente.id_herramienta, cantidad_dias=0)
                db.session.add(nueva_relacion)
                db.session.commit()
                flash('Herramienta agregada a la partida.', 'success')
                return redirect(url_for('ver_partida', id_partida=id_partida))
        else:
            nueva_herramienta = Herramienta(
                nombre_herramienta=form.nombre_herramienta.data,
                costo_alquiler_dia=form.costo_alquiler_dia.data
            )
            db.session.add(nueva_herramienta)
            db.session.commit()
            nueva_relacion = PartidasHerramientas(id_partida=id_partida, id_herramienta=nueva_herramienta.id_herramienta, cantidad_dias=0)
            db.session.add(nueva_relacion)
            db.session.commit()
            flash('Herramienta creada y agregada a la partida.', 'success')
            return redirect(url_for('ver_partida', id_partida=id_partida))
    return render_template('crear_herramienta.html', form=form, partida=partida, datos=datos)

# Rutas para Materiales
@app.route('/partida/<int:id_partida>/material/crear', methods=['GET', 'POST'])
def crear_material(id_partida):
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
    return render_template('crear_material.html', form=form, partida=partida, datos=datos)

@app.route('/partida/<int:id_partida>/mano_obra/<int:id_mano_obra>/editar', methods=['GET', 'POST'])
def editar_mano_obra_partida(id_partida, id_mano_obra):
    partida_mano_obra = PartidasManoObra.query.filter_by(id_partida=id_partida, id_mano_obra=id_mano_obra).first_or_404()
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

