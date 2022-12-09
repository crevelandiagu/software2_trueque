from app.database import db
from app.domain.auth.models import Permission, Role, User

class RolesAndPermissionsRepository:
    permission_names: list = ['manage_user_roles', 'enter_admin_panel']


    def insert_role(self, name: str, permissions: list):
        role = Role(name=name)

        for permission_id in permissions:
            permission = Permission.query.filter_by(id=permission_id).first()
            role.permissions.append(permission)

        db.session.add(role)
        db.session.commit()
        db.session.close()


    def bind_user_with_roles(self, user: int, roles: list):
        # Deleting all roles from user
        user = User.query.filter_by(id=user).first()
        user.roles = []
        db.session.add(user)
        db.session.commit()

        # Binding user with roles
        for role_id in roles:
            role = Role.query.filter_by(id=role_id).first()
            user.roles.append(role)

        db.session.add(user)
        db.session.commit()
        db.session.close()


    @classmethod
    def insert_default_permissions(cls):
        for perm_name in cls.permission_names:
            permission = Permission.query.filter_by(name=perm_name).first()
            if not permission:
                permission = Permission(name=perm_name)
                db.session.add(permission)
                db.session.commit()

        permissions = Permission.query.all()
        role = Role.query.filter_by(name='admin').first()
        if not role:
            role = Role(name='admin')
        for permission in permissions:
            role.permissions.append(permission)

        db.session.add(role)
        db.session.commit()
        db.session.close()


    @staticmethod
    def get_permissions_choices() -> list:
        permissions = Permission.query.all()
        return [(permission.id, permission.name) for permission in permissions]


    @staticmethod
    def get_roles_created() -> list:
        roles = Role.query.all()
        return [(role.id, role.name) for role in roles]