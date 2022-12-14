import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
db = SQLAlchemy()


class UsuariosMapper(db.Model):

    __tablename__ = 'usuarios'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(150), nullable=False)
    email: str = db.Column(db.String(150), unique=True, nullable=False)
    contrasena: str = db.Column(db.String(250), nullable=False)
    departamento: str = db.Column(db.String(150), nullable=False)
    municipio: str = db.Column(db.String(150), nullable=False)
    direccion: str = db.Column(db.String(150), nullable=False)
    role: str = db.Column(db.String(150), nullable=False, default="Trocador")
    # Relationships
    # elemento = db.relationship('Elementos', cascade='all, delete, delete-orphan')
    # notificacion = db.relationship('Notificaciones', cascade='all, delete, delete-orphan')

    def __init__(self, id: int = None,
                 nombre=None,
                 email=None,
                 contrasena=None,
                 departamento=None,
                 municipio=None,
                 direccion=None,
                 role=None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.contrasena = contrasena
        self.departamento = departamento
        self.municipio = municipio
        self.direccion = direccion
        self.role = role

    def insertar(self):
        db.session.add(self.__init__)
        db.session.commit()


class TruequesMapper(db.Model):

    __tablename__ = 'trueques'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Relationships
    usuario_pujador: int = db.Column(db.Integer, db.ForeignKey('elementos.id'))
    usuario_ofertador: int = db.Column(db.Integer, db.ForeignKey('elementos.id'))

    estado: str = db.Column(db.String(50), unique=True, nullable=False, default="iniciado")
    elemento_puja: int = db.Column(db.Integer, unique=True)
    elemento_oferta: int = db.Column(db.Integer, unique=True)
    precio_puja: int = db.Column(db.Integer, unique=True)

    created_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now,
                              onupdate=datetime.datetime.now)

    puja = db.relationship("ElementosMapper", foreign_keys=[usuario_pujador])
    oferta = db.relationship("ElementosMapper", foreign_keys=[usuario_ofertador])

    solicitud_logistica = db.relationship('SolicitudLogisticaMapper', cascade='all, delete, delete-orphan')


class ElementosMapper(db.Model):

    __tablename__ = 'elementos'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(50), nullable=False)
    descripcion: str = db.Column(db.String(250), nullable=False)
    imagen_url: str = db.Column(db.String(150), nullable=False)
    categoria: str = db.Column(db.String(50), nullable=False)
    precio_estimado: int = db.Column(db.Integer)
    trocador: int = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    estado: str = db.Column(db.String(50), nullable=False, default="sin-asignar")
    created_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now,
                                     onupdate=datetime.datetime.now)

class SolicitudLogisticaMapper(db.Model):

    __tablename__ = 'solicitud_logistica'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estado: str = db.Column(db.String(50), unique=True, nullable=False)
    operador_logistico: int = db.Column(db.Integer, unique=True)
    trueque: int = db.Column(db.Integer, db.ForeignKey('trueques.id'))
    created_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now,
                                     onupdate=datetime.datetime.now)


class NotificacionesMapper(db.Model):

    __tablename__ = 'notificaciones'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mensaje: str = db.Column(db.String(150), nullable=False)

    usuario: int = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    url: str = db.Column(db.String(150), nullable=False)
    estado: str = db.Column(db.String(150), nullable=False)

    created_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now,
                                     onupdate=datetime.datetime.now)

    fk_pujador = db.relationship("UsuariosMapper", foreign_keys=[usuario])





class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UsuariosMapper
        include_relationships = True
        load_instance = True
