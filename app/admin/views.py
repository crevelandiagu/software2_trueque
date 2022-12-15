from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for, flash

from app.models import Usuarios, Elementos, Trueques, SolicitudLogistica as SolicitudesLogisticas
from app.models import Notificaciones
from flask_sqlalchemy import SQLAlchemy
from app.admin.usuario import Usuario
from app.admin.elemento import Elemento
from app.admin.trueque import Trueque
from app.admin.solicitudlogistica import SolicitudLogistica
from app.admin.notificacion import Notificacion
from datetime import date
import json

db = SQLAlchemy()
admin = Blueprint('admin', __name__)

@admin.route('/')
def root():
    loggedIn, firstName, noOfItems, notMessages = getLoginDetails()

    itemData = Elementos.query.filter(
        Elementos.trocador != session.get('id',-1),
        Elementos.estado == 'sin-asignar'
    ).all()

    if len(itemData) > 9:
        itemData = itemData[0:9]
    return render_template('index.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, notMessages=notMessages)


@admin.route("/login", methods = ['POST', 'GET'])
def login():
    error = ''
    if request.method == 'POST':
        us = Usuario(
            email=request.form['inputEmail'],
            contrasena=request.form['inputPassword']
        )
        usuario = Usuarios.query.filter(
            Usuarios.email == us.get_email(),
            Usuarios.contrasena == us.validar_hash()
        ).first()
        db.session.commit()

        if usuario:
            session['email'] = usuario.email
            session['id'] = usuario.id
            session['role'] = usuario.role

            return redirect(url_for('admin.root'))
        else:
            error = 'Invalid UserId / Password'
    return render_template('login.html', error=error)

@admin.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('admin.root'))
    else:
        return render_template('login.html', error='')

@admin.route("/registerationForm")
def registrationForm():
    return render_template("register.html")

@admin.route("/register", methods = ['GET', 'POST'])
def register():
    error = ''
    if request.method == 'POST':
        try:

            usuario = Usuario(request.form['nombre'],
                              request.form['email'],
                              request.form['password'],
                              request.form['departamento'],
                              request.form['municipio'],
                              request.form['direccion'])

            password = usuario.encriptar_clave(request.form['cpassword'])

            nuevo_usuario = Usuarios(
                    nombre=usuario.get_nombre(),
                    email=usuario.get_email(),
                    contrasena=password,
                    departamento=usuario.get_departamento(),
                    municipio=usuario.get_municipio(),
                    direccion=usuario.get_direccion())


            db.session.add(nuevo_usuario)
            db.session.commit()

            flash("Registered Successfully")
        except Exception as e:
            print(e)
            return {"mensaje": f"Error {e}"}
        return redirect(url_for('admin.root'))

@admin.route("/profile")
def profileForm():
    if 'email' not in session:
        return redirect(url_for('admin.loginForm'))

    return render_template("profile.html", profileData='profileData')

@admin.route("/logout")
def logout():
    session.pop('email', None)
    session.pop('id', None)
    session.pop('role', None)
    session.clear()
    return redirect(url_for('admin.root'))


def getLoginDetails():

    if 'email' not in session:
        loggedIn = False
        firstName = ''
        noOfItems = 0
        notMessages = []
    else:

        loggedIn = session['role']
        usuario = Usuarios.query.filter(Usuarios.email == session['email']).first()
        if usuario is None:
            loggedIn = False
            firstName = ''
            noOfItems = 0
            notMessages = []
        else:
            firstName = usuario.nombre
            notificacion = Notificaciones.query.filter(
                Notificaciones.usuario == session['id'],
                Notificaciones.estado == 'enviado'
            ).all()

            noOfItems = len(notificacion)
            notMessages = notificacion

    return (loggedIn, firstName, noOfItems, notMessages)


@admin.route("/add")
def add():
    loggedIn, firstName, noOfItems, notMessages = getLoginDetails()
    return render_template('addEditElement.html',
                           categories=list(),
                           loggedIn=loggedIn,
                           firstName=firstName,
                           noOfItems=noOfItems,
                           notMessages=notMessages)

@admin.route('/myElements')
def myElements():
    loggedIn, firstName, noOfItems, notMessages = getLoginDetails()

    itemData = Elementos.query.filter(
            Elementos.trocador == session['id'],
            Elementos.estado == 'sin-asignar'
        ).all()

    existItem = True
    if len(itemData) == 0:
        existItem = False
    else:
        itemData = itemData[0:9]

    return render_template('elements.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName,
                           noOfItems=noOfItems, existItem=existItem, notMessages=notMessages)

@admin.route("/addElement", methods=["GET", "POST"])
def addElement():
    if request.method == "POST":

        nombre = request.form['nombre']

        el = Elemento(
            nombre=request.form['nombre'],
            precio_estimado=float(request.form['precio_estimado']),
            descripcion = request.form['descripcion'],
            categoria = 5,
            imagen_url = request.files['imagen_url'],
            trocador=session['id']
            )

        nuevo_elemento = Elementos(
            nombre=el.get_nombre(),
            precio_estimado=el.get_precio_estimado(),
            descripcion=el.get_descripcion(),
            imagen_url=el.get_imagen_url(),
            categoria=el.get_categoria(),
            trocador=el.get_trocador()
        )
        # Elementos.insertar(nuevo_usuario)
        db.session.add(nuevo_elemento)
        db.session.commit()

        flash("Elemento creado correctamente")
    return redirect(url_for('admin.root'))

@admin.route("/saveElement", methods=["GET", "POST"])
def saveElement():
    if request.method == "POST":

        el = Elemento(
            nombre=request.form['nombre'],
            precio_estimado=float(request.form['precio_estimado']),
            descripcion = request.form['descripcion'],
            categoria = 5,
            imagen_url = request.files['imagen_url'],
            trocador=session['id']
            )
        db.session.query(Elementos)\
            .filter(Elementos.id == request.form['id'])\
            .update({
                Elementos.nombre:el.get_nombre(),
                Elementos.precio_estimado:el.get_precio_estimado(),
                Elementos.descripcion:el.get_descripcion(),
                Elementos.imagen_url:el.get_imagen_url(),
                Elementos.categoria:el.get_categoria(),
                Elementos.trocador:el.get_trocador()
        }, synchronize_session=False)
        db.session.commit()
        flash("Elemento editado correctamente")
    return redirect(url_for('admin.myElements'))

@admin.route('/editElement/<int:elementId>')
def editElements(elementId):
    loggedIn, firstName, noOfItems,notMessages = getLoginDetails()

    itemData2 = Elementos.query.filter(
            Elementos.id == elementId
    ).all()
    db.session.commit()


    existItem = True
    if len(itemData2) == 0:
        existItem = False
        itemData=[]
    else:
        itemData= itemData2[0]
    return render_template('addEditElement.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName,
                           noOfItems=noOfItems, existItem=existItem, notMessages=notMessages)

@admin.route("/pujar/<int:elementId>")

def pujar(elementId):
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems, notMessages = getLoginDetails()
    email = session['email']

    products = Elementos.query.filter(
        Elementos.id == elementId,
    ).all()
    itemData = Elementos.query.filter(
            Elementos.trocador == session['id'],
            Elementos.estado == 'sin-asignar'
        ).all()
    totalPrice = 0

    existItem = False
    if len(itemData) > 0:
        existItem = True

    return render_template("pujar.html",
                           products = products,
                           misElementos = itemData,
                           totalPrice=totalPrice,
                           existItem=existItem,
                           loggedIn=loggedIn,
                           firstName=firstName,
                           noOfItems=noOfItems,
                           notMessages=notMessages)

@admin.route("/savePuja", methods=["GET", "POST"])
def savePuja():
    if request.method == "POST":

        el = Trueque(
            elemento_oferta=request.form['elemento_oferta'],
            elemento_puja=request.form['elemento_puja'],
            usuario_ofertador=request.form['usuario_ofertador'],
            usuario_pujador=session['id']
        )

        db.session.query(Elementos).filter(Elementos.id == request.form['elemento_oferta']) \
            .update({
            Elementos.estado: 'proceso'
        }, synchronize_session=False)
        db.session.commit()

        db.session.query(Elementos).filter(Elementos.id == request.form['elemento_puja']) \
            .update({
            Elementos.estado: 'proceso'
        }, synchronize_session=False)
        db.session.commit()

        nuevo_trueque = Trueques(
            elemento_oferta=el.get_elemento_oferta(),
            elemento_puja=el.get_elemento_puja(),
            usuario_ofertador=el.get_usuario_ofertador(),
            usuario_pujador=el.get_usuario_pujador()
        )

        db.session.add(nuevo_trueque)
        db.session.commit()

        obj_notificacion = Notificacion(
            mensaje='Ha recibido una solicitud de oferta, para ver mas diríjase a mis ofertas',
            estado='enviado',
            usuario_ofertador=request.form['usuario_ofertador'],
            usuario_pujador=session['id']
        )

        nuevo_notificacion = Notificaciones(
            mensaje=obj_notificacion.get_mensaje(),
            estado=obj_notificacion.get_estado(),
            usuario=obj_notificacion.get_usuario_ofertador(),
            url='myOferts'
        )

        db.session.add(nuevo_notificacion)
        db.session.commit()

        flash("puja enviada correctamente")
    return redirect(url_for('admin.root'))

@admin.route('/myOferts')
def myOferts():
    loggedIn, firstName, noOfItems, notMessages = getLoginDetails()

    itemData = Trueques.query.filter(
        Trueques.usuario_ofertador == session['id'],
        Trueques.estado == 'iniciado'
    ).all()
    result_dict = [u.__dict__ for u in itemData]


    for x in range(len(result_dict)):

        result_dict[x]['elemento_puja_propiedades'] = Elementos.query.filter(
                Elementos.id == result_dict[x]['elemento_puja']
            ).first()
        result_dict[x]['elemento_oferta_propiedades'] = Elementos.query.filter(
                Elementos.id == result_dict[x]['elemento_oferta']
            ).first()
        usuario_pujador_nombre = Usuarios.query.filter(
            Usuarios.id == result_dict[x]['usuario_pujador']
        ).first()
        result_dict[x]['usuario_pujador_nombre'] = usuario_pujador_nombre.nombre
        result_dict[x]['usuario_pujador_id'] = usuario_pujador_nombre.id


    existItem = True
    if len(itemData) == 0:
        existItem = False
    else:
        itemData = itemData[0:9]

    return render_template('misOfertas.html', itemData=result_dict, loggedIn=loggedIn, firstName=firstName,
                           noOfItems=noOfItems, existItem=existItem, notMessages=notMessages)

@admin.route('/myPujas')
def myPujas():
    loggedIn, firstName, noOfItems, notMessages = getLoginDetails()

    itemData = Trueques.query.filter(
        Trueques.usuario_pujador == session['id'],
        Trueques.estado == 'iniciado'
    ).all()
    result_dict = [u.__dict__ for u in itemData]


    for x in range(len(result_dict)):

        result_dict[x]['elemento_puja_propiedades'] = Elementos.query.filter(
                Elementos.id == result_dict[x]['elemento_puja']
            ).first()
        result_dict[x]['elemento_oferta_propiedades'] = Elementos.query.filter(
                Elementos.id == result_dict[x]['elemento_oferta']
            ).first()
        usuario_pujador_nombre = Usuarios.query.filter(
            Usuarios.id == result_dict[x]['usuario_pujador']
        ).first()
        result_dict[x]['usuario_pujador_nombre'] = usuario_pujador_nombre.nombre
        result_dict[x]['usuario_pujador_id'] = usuario_pujador_nombre.id


    existItem = True
    if len(itemData) == 0:
        existItem = False
    else:
        itemData = itemData[0:9]

    return render_template('misPujas.html', itemData=result_dict, loggedIn=loggedIn, firstName=firstName,
                           noOfItems=noOfItems, existItem=existItem, notMessages=notMessages)


@admin.route('/saveTrueque', methods=["GET", "POST"])
def saveTrueque():
    if request.method == "POST":


        db.session.query(Trueques).filter(Trueques.id == request.form['trueque_id']) \
            .update({
            Trueques.estado: 'proceso'
        }, synchronize_session=False)
        db.session.commit()

        db.session.query(Notificaciones)\
            .filter(Notificaciones.usuario == session['id'], Notificaciones.url == 'myOferts')\
            .update({
            Notificaciones.estado: 'leido'
        }, synchronize_session=False)
        db.session.commit()

        obj_solicitud_logistica = SolicitudLogistica(
            operador_logistico=1,
            estado='iniciado',
            trueque=request.form['trueque_id']
        )
        nueva_logistica = SolicitudesLogisticas(
            operador_logistico=obj_solicitud_logistica.get_operador_logistico(),
            estado=obj_solicitud_logistica.get_estado(),
            trueque=obj_solicitud_logistica.get_trueque()
        )

        db.session.add(nueva_logistica)
        db.session.commit()

        obj_notificacion = Notificacion(
            mensaje='Su puja ha sido aceptada, para ver el proceso puede ir a mis trueques',
            estado='enviado',
            usuario_ofertador=session['id'],
            usuario_pujador=request.form['usuario_pujador_id']
        )

        nuevo_notificacion = Notificaciones(
            mensaje=obj_notificacion.get_mensaje(),
            estado=obj_notificacion.get_estado(),
            usuario=obj_notificacion.get_usuario_pujador(),
            url='myTrueques'
        )

        db.session.add(nuevo_notificacion)
        db.session.commit()

        itemData = {
            "elemento_puja_propiedades_nombre":request.form['elemento_puja_propiedades_nombre'],
            "elemento_puja_propiedades_imagen_url":request.form['elemento_puja_propiedades_imagen_url'],
            "elemento_oferta_propiedades_nombre":request.form['elemento_oferta_propiedades_nombre'],
            "elemento_oferta_propiedades_imagen_url":request.form['elemento_oferta_propiedades_imagen_url'],
            "fecha":str(date.today()),
        }

    return redirect(url_for('admin.myInvoice', itemData=json.dumps(itemData)))

@admin.route('/myInvoice')
def myInvoice():
    loggedIn, firstName, noOfItems, notMessages = getLoginDetails()
    itemData = request.args['itemData']


    existItem = True
    if len(itemData) == 0:
        existItem = False

    return render_template('invoice.html', itemData=json.loads(itemData), loggedIn=loggedIn, firstName=firstName,
                           noOfItems=noOfItems, existItem=existItem, notMessages=notMessages)

@admin.route('/Logisticas')
def Logisticas():
    loggedIn, firstName, noOfItems, notMessages = getLoginDetails()

    solicitudes_logisticas_query = list(SolicitudesLogisticas.query.all())

    itemData = list()


    for x in range(len(solicitudes_logisticas_query)):
        Trueques_query = Trueques.query.filter(
            Trueques.id == solicitudes_logisticas_query[x].trueque
        ).first()
        usuario_pujador = Usuarios.query.filter(
            Usuarios.id == Trueques_query.usuario_pujador
        ).first()
        usuario_ofertador = Usuarios.query.filter(
            Usuarios.id == Trueques_query.usuario_ofertador
        ).first()

        itemData.append(
            {
                'id': solicitudes_logisticas_query[x].id,
                'puja_nombre': usuario_pujador.nombre,
                'puja_direccion': usuario_pujador.direccion,
                'ofertado_nombre': usuario_ofertador.nombre,
                'ofertado_direccion': usuario_ofertador.direccion,

                'cobro': "10.000",
                'estado': solicitudes_logisticas_query[x].estado
            }
        )


    existItem = True
    if len(itemData) == 0:
        existItem = False
    else:
        itemData = itemData[0:9]

    return render_template('logistica.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName,
                           noOfItems=noOfItems, existItem=existItem, notMessages=notMessages)

@admin.route("/saveLogistica", methods=["GET", "POST"])
def saveLogistica():
    if request.method == "POST":

        obj_solicitud_logistica = SolicitudLogistica(
            estado = request.form['estado'],
            operador_logistico = session['id'],
            numero_solicitud = request.form['id']
        )

        db.session.query(SolicitudesLogisticas).filter(SolicitudesLogisticas.id == obj_solicitud_logistica.get_numero_solicitud()) \
            .update({
            SolicitudesLogisticas.estado: obj_solicitud_logistica.get_estado()
        }, synchronize_session=False)
        db.session.commit()

        flash("Logistica Actualizada correctamente")
    return redirect(url_for('admin.Logisticas'))

@admin.route('/myTrueques')
def myTrueques():
    loggedIn, firstName, noOfItems, notMessages = getLoginDetails()

    solicitudes_logisticas_query = list(SolicitudesLogisticas.query.all())
    itemData = list()

    db.session.query(Notificaciones) \
        .filter(Notificaciones.usuario == session['id'], Notificaciones.url == 'myTrueques') \
        .update({
        Notificaciones.estado: 'leido'
    }, synchronize_session=False)
    db.session.commit()

    for x in range(len(solicitudes_logisticas_query)):
        Trueques_query = Trueques.query.filter(
            Trueques.id == solicitudes_logisticas_query[x].trueque
        ).first()
        usuario_pujador = Usuarios.query.filter(
            Usuarios.id == Trueques_query.usuario_pujador
        ).first()
        usuario_ofertador = Usuarios.query.filter(
            Usuarios.id == Trueques_query.usuario_ofertador
        ).first()
        elemeto_pujador = Elementos.query.filter(
            Elementos.id == Trueques_query.elemento_puja
        ).first()
        elemeto_ofertado = Elementos.query.filter(
            Elementos.id == Trueques_query.elemento_oferta
        ).first()

        itemData.append(
            {
                'id': x,
                'puja_nombre': usuario_pujador.nombre,
                'puja_elemento': elemeto_pujador.nombre,
                'ofertado_nombre': usuario_ofertador.nombre,
                'ofertado_elemento': elemeto_ofertado.nombre,
                'cobro': "10.000",
                'estado': solicitudes_logisticas_query[x].estado
            }
        )


    existItem = True
    if len(itemData) == 0:
        existItem = False
    else:
        itemData = itemData[0:9]

    return render_template('trueques.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName,
                           noOfItems=noOfItems, existItem=existItem, notMessages=notMessages)
