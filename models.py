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
    manos_obra = db.relationship('PartidasManoObra', backref='partida', lazy=True)
    herramientas = db.relationship('PartidasHerramientas', backref='partida', lazy=True)
    materiales = db.relationship('PartidasMateriales', backref='partida', lazy=True)

# ... (Modelos para ManoObra, Herramienta, Material, PartidasManoObra, PartidasHerramientas, PartidasMateriales siguiendo el esquema anterior)
class ManoObra(db.Model):
    id_mano_obra = db.Column(db.Integer, primary_key=True)
    descripcion_mano_obra = db.Column(db.String(255))
    costo_hora = db.Column(db.Float)
    partidas = db.relationship('PartidasManoObra', backref='mano_obra', lazy=True)

class Herramienta(db.Model):
    id_herramienta = db.Column(db.Integer, primary_key=True)
    nombre_herramienta = db.Column(db.String(255))
    costo_alquiler_dia = db.Column(db.Float)
    partidas = db.relationship('PartidasHerramientas', backref='herramienta', lazy=True)

class Material(db.Model):
    id_material = db.Column(db.Integer, primary_key=True)
    nombre_material = db.Column(db.String(255))
    unidad_medida = db.Column(db.String(50))
    precio_unitario = db.Column(db.Float)
    partidas = db.relationship('PartidasMateriales', backref='material', lazy=True)

class PartidasManoObra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_partida = db.Column(db.Integer, db.ForeignKey('partida.id_partida'))
    id_mano_obra = db.Column(db.Integer, db.ForeignKey('mano_obra.id_mano_obra'))
    cantidad_horas = db.Column(db.Float)

class PartidasHerramientas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_partida = db.Column(db.Integer, db.ForeignKey('partida.id_partida'))
    id_herramienta = db.Column(db.Integer, db.ForeignKey('herramienta.id_herramienta'))
    cantidad_dias = db.Column(db.Integer)

class PartidasMateriales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_partida = db.Column(db.Integer, db.ForeignKey('partida.id_partida'))
    id_material = db.Column(db.Integer, db.ForeignKey('material.id_material'))
    cantidad = db.Column(db.Float)