
def init_models():
    '''Initialize the database models'''
    import app.domain.auth.models as auth
    import app.domain.blogs.models as blogs


def install_extensions(app):
    '''Install flask extensions in the app'''

    # Flask-SQLAlchemy
    from app.database import init_db
    init_db(app)

    # Flask-Login
    from app.domain.auth import init_auth_module
    init_auth_module(app)

    # Flask-Principal
    from flask_principal import Principal, identity_loaded, UserNeed, RoleNeed
    Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        from flask_login import current_user
        # Set the identity user object
        identity.user = current_user

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Update the identity with the roles that the user provides
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                for permission in role.permissions:
                    identity.provides.add(RoleNeed(permission.name))


    # Flask-Security

    # Bcrypt

    # Flask-Mail

    # Flask-Bootstrap

    # Flask-Moment

    # Flask-Babel

    # Flask-Admin

    # Flask-Cache

    # Flask-Restless

    # Flask-Assets

    # Flask-Script

    # Flask-Migrate

    # Flask-DebugToolbar

    # Flask-Webpack

    # Flask-Themes


def register_blueprints_in_app(app, ip_addr: str = None, server_port: int = None):
    '''Register the routes of each module in the app'''
    from flask import render_template

    @app.get("/")
    def index():
        data: dict = dict(
            name="John Doe",
            ip_address = f'{ip_addr}:{server_port}',
        )
        return render_template('hello.html', data=data)


    @app.get("/about")
    def about():
        return "<p>About</p>"


    from .auth.controllers import auth_controller
    app.register_blueprint(auth_controller.bp)

    from app import printers
    app.register_blueprint(printers.bp)

    from .blogs.controllers import blogs_controller
    app.register_blueprint(blogs_controller.bp)

    from .admin.controllers import manage_user_roles_controller
    app.register_blueprint(manage_user_roles_controller.bp)

    return app


from urllib.parse import urlparse, urljoin
from flask import request

def is_safe_url(target):
    '''Validate the target url is safe to redirect to'''
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
