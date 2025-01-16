from app import db  # Importa la instancia de db creada en app.py

class Obra(db.Model):
    __tablename__ = 'obra'
    id_obra = db.Column(db.Integer, primary_key=True)
    nombre_obra = db.Column(db.String(100), nullable=False)
    descripcion_obra = db.Column(db.Text)
    cliente_nombre = db.Column(db.String(100))
    fecha_inicio = db.Column(db.Date)
    gastos_administrativos = db.Column(db.Date)
    partidas = db.relationship('ObraPartida', back_populates='obra', lazy='dynamic')  # Relación con Partidas

class Partida(db.Model):
    __tablename__ = 'partida'
    id_partida = db.Column(db.Integer, primary_key=True)
    nombre_partida = db.Column(db.String(100), nullable=False)
    descripcion_partida = db.Column(db.Text)
    unidad_medida_id = db.Column(
        db.Integer,
        db.ForeignKey('unidad_medida.id_unidad_medida', name='fk_partida_unidad_medida')
    )
    rendimiento = db.Column(db.Integer)
    obras = db.relationship('ObraPartida', back_populates='partida', lazy='dynamic')  # Relación con Obras
    mano_de_obra = db.relationship('PartidasManoDeObra', backref='partida', lazy=True)
    herramientas = db.relationship('PartidasHerramientas', backref='partida', lazy=True)
    materiales = db.relationship('PartidasMateriales', backref='partida', lazy=True)
    unidad_medida = db.relationship('UnidadMedida', backref='partidas')

    #unidad_medida = db.relationship('UnidadMedida', back_populates="partida", uselist=False, single_parent=True)

#    def __repr__(self):
#        return f"<Partida(id={self.id_partida}, nombre={self.nombre_partida}, um={self.unidad_medida})>"

class ObraPartida(db.Model):
    __tablename__ = 'obras_partidas'
    id = db.Column(db.Integer, primary_key=True)
    id_partida = db.Column(db.Integer, db.ForeignKey('partida.id_partida', name='fk_obras_partidas_partida'), nullable=False)
    id_obra = db.Column(db.Integer, db.ForeignKey('obra.id_obra', name='fk_obras_partidas_obra'), nullable=False)
    partida = db.relationship('Partida', back_populates='obras')
    obra = db.relationship('Obra', back_populates='partidas')

class ManoDeObra(db.Model):
    __tablename__ = 'mano_de_obra'
    id_mano_de_obra = db.Column(db.Integer, primary_key=True)
    nombre_mano_de_obra = db.Column(db.String(100), nullable=False)
    descripcion_mano_de_obra = db.Column(db.Text)
    costo_hora = db.Column(db.Float)

    partidas_mano_de_obra = db.relationship('PartidasManoDeObra', backref='mano_de_obra')

class Herramienta(db.Model):
    __tablename__ = 'herramienta'
    id_herramienta = db.Column(db.Integer, primary_key=True)
    nombre_herramienta = db.Column(db.String(100), nullable=False)
    descripcion_herramienta = db.Column(db.Text)
    costo_alquiler_dia = db.Column(db.Float)

    partidas_herramientas = db.relationship('PartidasHerramientas', backref='herramienta')


class Material(db.Model):
    __tablename__ = 'material'
    id_material = db.Column(db.Integer, primary_key=True)
    nombre_material = db.Column(db.String(100), nullable=False)
    descripcion_material = db.Column(db.Text)
    unidad_medida_id = db.Column(
        db.Integer,
        db.ForeignKey('unidad_medida.id_unidad_medida', name='fk_material_unidad_medida'),
        nullable=False
    )
    precio_unitario = db.Column(db.Float)
    fecha_registro = db.Column(db.Date)

    unidad_medida = db.relationship('UnidadMedida', backref='materiales')
    partidas_materiales = db.relationship('PartidasMateriales', backref='material')

    #persona = db.relationship('Persona', back_populates="ventas", uselist=False, single_parent=True)


    #def __repr__(self):
    #    return f"<Partida(id={self.id_partida}, nombre={self.nombre_partida})>"

class PartidasManoDeObra(db.Model):
    __tablename__ = 'partidas_mano_de_obra'
    id = db.Column(db.Integer, primary_key=True)
    id_partida = db.Column(db.Integer, db.ForeignKey('partida.id_partida', name='fk_partidas_mano_de_obra_partida'), nullable=False)
    id_mano_de_obra = db.Column(db.Integer, db.ForeignKey('mano_de_obra.id_mano_de_obra', name='fk_partidas_mano_de_obra_mano_de_obra'), nullable=False)
    cantidad = db.Column(db.Float)

class PartidasHerramientas(db.Model):
    __tablename__ = 'partidas_herramientas'
    id = db.Column(db.Integer, primary_key=True)
    id_partida = db.Column(db.Integer, db.ForeignKey('partida.id_partida', name='fk_partidas_herramientas_partida'), nullable=False)
    id_herramienta = db.Column(db.Integer, db.ForeignKey('herramienta.id_herramienta', name='fk_partidas_herramientas_herramienta'), nullable=False)
    cantidad = db.Column(db.Float)

class PartidasMateriales(db.Model):
    __tablename__ = 'partidas_materiales'
    id = db.Column(db.Integer, primary_key=True)
    id_partida = db.Column(db.Integer, db.ForeignKey('partida.id_partida', name='fk_partidas_materiales_partida'), nullable=False)
    id_material = db.Column(db.Integer, db.ForeignKey('material.id_material', name='fk_partidas_materiales_material'), nullable=False)
    cantidad = db.Column(db.Float)

    #partida = db.relationship('Partida', backref='partidas_materiales')

    def __repr__(self):
        return f"<P_Material(id={self.id_material}, partida={self.partida}, material={self.material.nombre_material}, material={self.cantidad})>"

class UnidadMedida(db.Model):
    __tablename__ = 'unidad_medida'
    id_unidad_medida = db.Column(db.Integer, primary_key=True)
    nombre_unidad_medida = db.Column(db.String(100), nullable=False)
    # Relación
    #partidas = db.relationship('Partida', backref='unidad_medida')

#    def __repr__(self):
#        return f"<UnidadMedida(id={self.id_unidad_medida}, nombre={self.nombre_unidad_medida})>"
