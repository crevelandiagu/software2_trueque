from flask_principal import Permission, RoleNeed

class ManageRolesPermission(Permission):
    def __init__(self):
        # Use this code for many RoleNeeds in one Permission
        # needs = set()
        # for permission_name in RolesAndPermissionsRepository.permission_names:
        #     needs.add(RoleNeed(permission_name))
        # super(ManageRolesPermission, self).__init__(*needs)

        need = RoleNeed('manage_user_roles')
        super(ManageRolesPermission, self).__init__(need)


class EnterAdminPanelPermission(Permission):
    def __init__(self):
        need = RoleNeed('enter_admin_panel')
        super(EnterAdminPanelPermission, self).__init__(need)