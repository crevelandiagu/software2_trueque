import os

from flask import Flask


def create_app(ip_addr: str = None, server_port: int = None, test_config=None):
    '''Creates and configures the app'''
    app = Flask(__name__, template_folder='templates', static_folder='templates/css')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        from app.config import config
        app.config.from_mapping(dict(config))
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from app.domain import install_extensions, register_blueprints_in_app
    install_extensions(app)
    register_blueprints_in_app(app, ip_addr, server_port)

    return app
