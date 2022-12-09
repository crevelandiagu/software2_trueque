from flask_login import LoginManager

from app.domain.auth.repositories.user_repository import UserRepository

def init_auth_module(app):
    login_manager = LoginManager()
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        '''Used to reload the user object from the user ID stored in the session'''
        user_repo = UserRepository()
        return user_repo.get_user_by_id(user_id)