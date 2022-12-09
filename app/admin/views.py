from flask import Blueprint
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for, flash

from app.models import Usuarios
from app.models import Notificaciones
from flask_sqlalchemy import SQLAlchemy
from app.admin.elemento import Elemento
from app.admin.usuario import Usuario

db = SQLAlchemy()
admin = Blueprint('admin', __name__)

@admin.route('/')
def root():
    loggedIn, firstName, noOfItems = getLoginDetails()
    return render_template('index.html', itemData=[], loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryData=[])

@admin.route("/login", methods = ['POST', 'GET'])
def login():
    error = ''
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        usuario = Usuarios.query.filter(Usuarios.email == email,
                                       Usuarios.contrasena == password).first()
        db.session.commit()

        if usuario:
            session['email'] = email
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
            # usuario.set_nombre(request.form['usuario'])
            # usuario.set_email(request.form['email'])
            # usuario.set_contrasena(request.form['contrasena'])
            # usuario.set_departamento(request.form['departamento'])
            # usuario.set_municipio(request.form['municipio'])
            # usuario.set_direccion(request.form['direccion'])

            nuevo_usuario = Usuarios(
                    nombre=usuario.get_nombre(),
                    email=usuario.get_email(),
                    contrasena=usuario.get_contrasena(),
                    departamento=usuario.get_departamento(),
                    municipio=usuario.get_municipio(),
                    direccion=usuario.get_direccion()
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
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
    # with sqlite3.connect('database.db') as conn:
    #     cur = conn.cursor()
    #     cur.execute("SELECT userId, email, firstName, lastName, phone FROM users WHERE email = ?", (session['email'], ))
    #     profileData = cur.fetchone()
    # conn.close()
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
        loggedIn = True
        usuario = Usuarios.query.filter(Usuarios.email == session['email']).first()
        firstName = usuario.nombre
        notificacion = Notificaciones.query.filter(Notificaciones.usuario_pujador == usuario.id).first()
        # userId, firstName = cur.fetchone()
        # cur.execute("SELECT count(productId) FROM kart WHERE userId = ?", (userId, ))
        noOfItems = 3 # notificaciones futuras

    return (loggedIn, firstName, noOfItems)


@admin.route("/addItem", methods=["GET", "POST"])
def addItem():
    if request.method == "POST":
        elemento = Elemento(
            request.form['name'],
        )


        print(request.form)
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        stock = int(request.form['stock'])
        categoryId = int(request.form['category'])

        #Uploading image procedure
        image = request.files['image']
        # if image and allowed_file(image.filename):
        #     filename = secure_filename(image.filename)
        #     image.save(os.path.join(UPLOAD_FOLDER, filename))
        # imagename = filename
        # with sqlite3.connect('database.db') as conn:
        #     try:
        #         cur = conn.cursor()
        #         cur.execute('''INSERT INTO products (name, price, description, image, stock, categoryId) VALUES (?, ?, ?, ?, ?, ?)''', (name, price, description, imagename, stock, categoryId))
        #         conn.commit()
        #         msg="added successfully"
        #     except:
        #         msg="error occured"
        #         conn.rollback()
        # conn.close()
        # print(msg)
        return redirect(url_for('admin.root'))


@admin.route("/add")
def add():
    # with sqlite3.connect('database.db') as conn:
    #     cur = conn.cursor()
    #     cur.execute("SELECT categoryId, name FROM categories")
    #     categories = cur.fetchall()
    # conn.close()
    return render_template('add.html', categories=list())
