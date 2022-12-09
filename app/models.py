import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()


class Usuarios(db.Model):

    __tablename__ = 'usuarios'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(150), unique=True, nullable=False)
    email: str = db.Column(db.String(150), unique=True, nullable=False)
    contrasena: str = db.Column(db.Text, nullable=False)
    departamento: str = db.Column(db.String(150), unique=True, nullable=False)
    municipio: str = db.Column(db.String(150), unique=True, nullable=False)
    direccion: str = db.Column(db.String(150), unique=True, nullable=False)
    # Relationships
    elemento = db.relationship('Elementos', cascade='all, delete, delete-orphan')
    # notificacion = db.relationship('Notificaciones', cascade='all, delete, delete-orphan')

class Trueques(db.Model, UserMixin):

    __tablename__ = 'trueques'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Relationships
    usuario_pujador: int = db.Column(db.Integer, db.ForeignKey('elementos.id'))
    usuario_ofeertador: int = db.Column(db.Integer, db.ForeignKey('elementos.id'))

    estado: str = db.Column(db.String(50), unique=True, nullable=False, default="iniciado")
    elemento_puja: int = db.Column(db.Integer, unique=True)
    elemento_oferta: int = db.Column(db.Integer, unique=True)
    precio_puja: int = db.Column(db.Integer, unique=True)

    created_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now,
                              onupdate=datetime.datetime.now)

    puja = db.relationship("Elementos", foreign_keys=[usuario_pujador])
    oferta = db.relationship("Elementos", foreign_keys=[usuario_ofeertador])

    solicitud_logistica = db.relationship('SolicitudLogistica', cascade='all, delete, delete-orphan')


class Elementos(db.Model):

    __tablename__ = 'elementos'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre: str = db.Column(db.String(50), unique=True, nullable=False)
    descripcion: str = db.Column(db.String(250), unique=True, nullable=False)
    imagen_url: str = db.Column(db.String(150), unique=True, nullable=False)
    categoria: str = db.Column(db.String(50), unique=True, nullable=False)
    trocador: int = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    created_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now,
                                     onupdate=datetime.datetime.now)




class SolicitudLogistica(db.Model):

    __tablename__ = 'solicitud_logistica'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estado: str = db.Column(db.String(50), unique=True, nullable=False)
    operador_logistico: int = db.Column(db.Integer, unique=True)
    trueque: int = db.Column(db.Integer, db.ForeignKey('trueques.id'))
    created_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now,
                                     onupdate=datetime.datetime.now)


class Notificaciones(db.Model):

    __tablename__ = 'notificaciones'

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mensaje: str = db.Column(db.String(150), unique=True, nullable=False)

    usuario_pujador: int = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario_ofeertador: int = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    created_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now,
                                     onupdate=datetime.datetime.now)

    pujador = db.relationship("Usuarios", foreign_keys=[usuario_pujador])
    ofeertador = db.relationship("Usuarios", foreign_keys=[usuario_ofeertador])




class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuarios
        include_relationships = True
        load_instance = True
