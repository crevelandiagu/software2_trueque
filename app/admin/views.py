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

db = SQLAlchemy()
admin = Blueprint('admin', __name__)

@admin.route('/')
def root():
    loggedIn, firstName, noOfItems = getLoginDetails()

    itemData = Elementos.query.filter(
        Elementos.trocador != session.get('id',-1),
        Elementos.estado != 'sin-asignar'
    ).all()

    if len(itemData) > 9:
        itemData = itemData[0:9]
        print(itemData)
    return render_template('index.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

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

        # try:
        #     existe = Usuarios.query.filter(Usuarios.email == request.form['email']).first()
        #     if existe is not None:
        #         error = "El usuario ya existe, pruebe con otro"
        #         return render_template('login.html', error=error)
        #
        #     nuevo_usuario = Usuarios(
        #         nombre=request.form['nombre'],
        #         email=request.form['email'],
        #         contrasena=request.form['password'],
        #         departamento=request.form['departamento'],
        #         municipio=request.form['municipio'],
        #         direccion=request.form['direccion']
        #     )
        #
        #     db.session.add(nuevo_usuario)
        #     db.session.commit()
        #     flash("Registered Successfully")
        # except Exception as e:
        #     print(e)
        #     return {"mensaje": f"Error {e}"}
        #

        return redirect(url_for('admin.root'))

@admin.route("/profile")
def profileForm():
    if 'email' not in session:
        return redirect(url_for('admin.loginForm'))

    return render_template("profile.html", profileData='profileData')

@admin.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('admin.root'))


def getLoginDetails():

    if 'email' not in session:
        loggedIn = False
        firstName = ''
        noOfItems = 0
    else:
        print(session['email'])
        loggedIn = True
        usuario = Usuarios.query.filter(Usuarios.email == session['email']).first()
        if usuario is None:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            firstName = usuario.nombre
            print("usuario")
            print(usuario)
            notificacion = Notificaciones.query.filter(Notificaciones.usuario_pujador == usuario.id).first()
            noOfItems = 3 # notificaciones futuras

    return (loggedIn, firstName, noOfItems)



@admin.route("/add")
def add():
    loggedIn, firstName, noOfItems = getLoginDetails()
    return render_template('addEditElement.html', categories=list(),  loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@admin.route('/myElements')
def myElements():
    loggedIn, firstName, noOfItems = getLoginDetails()

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
                           noOfItems=noOfItems, existItem=existItem)

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
    loggedIn, firstName, noOfItems = getLoginDetails()

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
                           noOfItems=noOfItems, existItem=existItem)

@admin.route("/pujar/<int:elementId>")
def pujar(elementId):
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
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
    if noOfItems > 0:
        existItem = True
    return render_template("pujar.html", products = products,misElementos = itemData, totalPrice=totalPrice, existItem=existItem, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@admin.route("/savePuja", methods=["GET", "POST"])
def savePuja():
    if request.method == "POST":

        print("request.form")
        print(request.form['prujaId'])
        print(request.form['ofertaId'])

        el = Trueque(
            elemento_oferta=request.form['elemento_oferta'],
            elemento_puja=request.form['elemento_puja'],
            usuario_ofertador=request.form['usuario_ofertador'],
            usuario_trocador=session['usuario_trocador']
        )
        nuevo_trueque= Trueques(
            elemento_oferta=el.get_elemento_oferta(),
            elemento_puja=el.get_elemento_puja(),
            usuario_ofertador=el.get_usuario_ofertador(),
            usuario_trocador=el.get_usuario_trocador()
        )
        # Elementos.insertar(nuevo_usuario)
        db.session.add(nuevo_trueque)
        db.session.commit()

        db.session.commit()
        flash("puja enviada correctamente")
    return redirect(url_for('admin.root'))