from flask import Flask
from flask_cors import CORS
from app.admin import admin
from app.models import db

from flask_bootstrap import Bootstrap
ACTIVATE_ENDPOINTS = (('/', admin),)


app = Flask(__name__)
app.secret_key = 'dev'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])

Bootstrap(app)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///truequestundama.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True

db.init_app(app)

with app.app_context():
    db.create_all()

app_context = app.app_context()
app_context.push()
cors = CORS(app)


for url, blueprint in ACTIVATE_ENDPOINTS:
    app.register_blueprint(blueprint, url_prefix=url)




