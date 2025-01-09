from app import db # Importa la instancia de db creada en app.py

class Obra(db.Model):
    id_obra = db.Column(db.Integer, primary_key=True)
    nombre_obra = db.Column(db.String(100), nullable=False)
    descripcion_obra = db.Column(db.Text)
    fecha_inicio = db.Column(db.Date)
    partidas = db.relationship('Partida', backref='obra', lazy=True) # Relación con Partidas

class Partida(db.Model):
    id_partida = db.Column(db.Integer, primary_key=True)
    id_obra = db.Column(db.Integer, db.ForeignKey('obra.id_obra'), nullable=False)
    nombre_partida = db.Column(db.String(100), nullable=False)
    descripcion_partida = db.Column(db.Text)
    manos_obra = db.relationship('PartidasManoDeObra', backref='partida', lazy=True)
    herramientas = db.relationship('PartidasHerramientas', backref='partida', lazy=True)
    materiales = db.relationship('PartidasMateriales', backref='partida', lazy=True)

# ... (Modelos para ManoObra, Herramienta, Material, PartidasManoObra, PartidasHerramientas, PartidasMateriales siguiendo el esquema anterior)
class ManoDeObra(db.Model):
    id_mano_de_obra = db.Column(db.Integer, primary_key=True)
    nombre_mano_de_obra = db.Column(db.String(100), nullable=False)
    descripcion_mano_de_obra = db.Column(db.Text)
    costo_hora = db.Column(db.Float)

class Herramienta(db.Model):
    id_herramienta = db.Column(db.Integer, primary_key=True)
    nombre_herramienta = db.Column(db.String(100), nullable=False)
    descripcion_herramienta = db.Column(db.Text)
    costo_alquiler_dia = db.Column(db.Float)

class Material(db.Model):
    id_material = db.Column(db.Integer, primary_key=True)
    nombre_material = db.Column(db.String(100), nullable=False)
    descripcion_material = db.Column(db.Text)
    unidad_medida = db.Column(db.String(20))
    precio_unitario = db.Column(db.Float)


# Tablas de unión (con nombres explícitos y clave primaria)
class PartidasManoDeObra(db.Model):
    __tablename__ = 'partidas_mano_de_obra'
    id = db.Column(db.Integer, primary_key=True)
    id_partida = db.Column(db.Integer, db.ForeignKey('partida.id_partida'), primary_key=True)
    id_mano_de_obra = db.Column(db.Integer, db.ForeignKey('mano_de_obra.id_mano_de_obra'), primary_key=True)
    cantidad_horas = db.Column(db.Float)

class PartidasHerramientas(db.Model):
    __tablename__ = 'partidas_herramientas'
    id = db.Column(db.Integer, primary_key=True)
    id_partida = db.Column(db.Integer, db.ForeignKey('partida.id_partida'), primary_key=True)
    id_herramienta = db.Column(db.Integer, db.ForeignKey('herramienta.id_herramienta'), primary_key=True)
    cantidad_dias = db.Column(db.Float)

class PartidasMateriales(db.Model):
    __tablename__ = 'partidas_materiales'
    id = db.Column(db.Integer, primary_key=True)
    id_partida = db.Column(db.Integer, db.ForeignKey('partida.id_partida'), primary_key=True)
    id_material = db.Column(db.Integer, db.ForeignKey('material.id_material'), primary_key=True)
    cantidad = db.Column(db.Float)