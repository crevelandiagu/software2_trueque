import os
from flask_sqlalchemy import SQLAlchemy


db = None

def init_db(app):
    '''Initialize the database'''
    global db
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(app.instance_path, app.config.get('DATABASE_FILENAME'))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conversion.db'
    db = SQLAlchemy(app)

    from app.domain import init_models
    init_models()
    db.create_all()
        
    # Inserting default permissions
    from app.domain.auth.repositories.roles_perms_repository import RolesAndPermissionsRepository
    RolesAndPermissionsRepository.insert_default_permissions()
