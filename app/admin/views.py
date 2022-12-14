from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for, flash

from app.models import Usuarios, Elementos, Trueques
from app.models import Notificaciones
from flask_sqlalchemy import SQLAlchemy
from app.admin.usuario import Usuario
from app.admin.elemento import Elemento
from app.admin.trueque import Trueque
from app.admin.notificacion import Notificacion

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
        print(itemData)
    return render_template('index.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, notMessages=notMessages)

    # return render_template('index.html', itemData=[], loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryData=[])

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
            print("session['id']")
            print(session['id'])

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

            # Usuarios.insertar(nuevo_usuario)
            db.session.add(nuevo_usuario)
            db.session.commit()
            #
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
    session.clear()
    return redirect(url_for('admin.root'))


def getLoginDetails():

    if 'email' not in session:
        loggedIn = False
        firstName = ''
        noOfItems = 0
        notMessages = []
    else:
        print(session['email'])
        loggedIn = True
        usuario = Usuarios.query.filter(Usuarios.email == session['email']).first()
        if usuario is None:
            loggedIn = False
            firstName = ''
            noOfItems = 0
            notMessages = []
        else:
            firstName = usuario.nombre
            print("usuario")
            print(usuario)
            notificacion = Notificaciones.query.filter(
                Notificaciones.usuario == session['id'],
                Notificaciones.estado == 'enviado'
            ).all()

            noOfItems = len(notificacion)
            notMessages = notificacion

            print("notMessages")
            print(list(notMessages))

    return (loggedIn, firstName, noOfItems, notMessages)



@admin.route("/add")
def add():
    loggedIn, firstName, noOfItems, notMessages = getLoginDetails()
    return render_template('addEditElement.html', categories=list(),  loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, notMessages=notMessages)

@admin.route('/myElements')
def myElements():
    loggedIn, firstName, noOfItems, notMessages = getLoginDetails()

    itemData = Elementos.query.filter(
            Elementos.trocador == session['id'],
            Elementos.estado == 'sin-asignar'
        ).all()
    print(itemData)
    existItem = True
    if len(itemData) == 0:
        existItem = False
    else:
        itemData = itemData[0:9]
        print(itemData)
    return render_template('elements.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName,
                           noOfItems=noOfItems, existItem=existItem, notMessages=notMessages)

@admin.route("/addElement", methods=["GET", "POST"])
def addElement():
    if request.method == "POST":

        nombre = request.form['nombre']

        print("session['id']")
        print(session['id'])

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

        print("session['id']")
        print(session['id'])

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
    print('aqui')
    print(elementId)
    print(itemData2)

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
        Elementos.id == elementId
    ).all()
    itemData = Elementos.query.filter(
            Elementos.trocador == session['id']
        ).all()
    totalPrice = 0
    print(products)
    print("itemData")
    print(itemData)
    existItem = False
    if len(itemData) > 0:
        existItem = True
    print("existItem")
    print(existItem)
    return render_template("pujar.html", products = products,misElementos = itemData, totalPrice=totalPrice, existItem=existItem, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, notMessages=notMessages)

@admin.route("/savePuja", methods=["GET", "POST"])
def savePuja():
    if request.method == "POST":

        print("request.form")
        print(request.form)

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
        # Elementos.insertar(nuevo_usuario)
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
        # Elementos.insertar(nuevo_usuario)
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
    print("session['id']")
    print(session['id'])
    print("result_dict")

    print(result_dict)

    for x in range(len(result_dict)):
        print("x")
        print(x)
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


    existItem = True
    if len(itemData) == 0:
        existItem = False
    else:
        itemData = itemData[0:9]
        print(itemData)
    return render_template('misOfertas.html', itemData=result_dict, loggedIn=loggedIn, firstName=firstName,
                           noOfItems=noOfItems, existItem=existItem, notMessages=notMessages)\
#
# @admin.route('/myOferts')
# def myOferts():
#     loggedIn, firstName, noOfItems, notMessages = getLoginDetails()
#
#     itemData = Trueques.query.filter(
#         Trueques.usuario_ofertador == session['id'],
#         Trueques.estado == 'iniciado'
#     ).all()
#     result_dict = [u.__dict__ for u in itemData]
#     print("session['id']")
#     print(session['id'])
#     print("result_dict")
#
#     print(result_dict)
#
#     for x in range(len(result_dict)):
#         print("x")
#         print(x)
#         result_dict[x]['elemento_puja_propiedades'] = Elementos.query.filter(
#                 Elementos.id == result_dict[x]['elemento_puja']
#             ).first()
#         result_dict[x]['elemento_oferta_propiedades'] = Elementos.query.filter(
#                 Elementos.id == result_dict[x]['elemento_oferta']
#             ).first()
#         usuario_pujador_nombre = Usuarios.query.filter(
#             Usuarios.id == result_dict[x]['usuario_pujador']
#         ).first()
#         result_dict[x]['usuario_pujador_nombre'] = usuario_pujador_nombre.nombre
#
#
#     existItem = True
#     if len(itemData) == 0:
#         existItem = False
#     else:
#         itemData = itemData[0:9]
#         print(itemData)
#     return render_template('misOfertas.html', itemData=result_dict, loggedIn=loggedIn, firstName=firstName,
#                            noOfItems=noOfItems, existItem=existItem, notMessages=notMessages)
