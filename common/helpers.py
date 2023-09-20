from apps.role.models import AccessRole
from apps.invitation.models import Invitation
from apps.company.models import Company


def module_perm(name, user, perm):
    user_access = AccessRole.objects.filter(id=user.role_id)
    if not user_access:
        return False
    user_access = user_access.first()
    role_permissions = user_access.role_permissions
    module_permissions = [
        permission.split(":")[1]
        for permission in role_permissions
        if permission.startswith(f"{name.title()}:")
    ]
    if f"{perm}" in module_permissions:
        return True
    return False


def get_object_from_models(id_value):
    model_classes = [Company, Invitation]  # Add your models here

    for model_class in model_classes:
        try:
            obj = model_class.objects.get(pk=id_value)
            model_name = model_class.__name__
            return model_name, obj
        except model_class.DoesNotExist:
            pass

    return None, None


SS_MODULE_PERMISSIONS = [
    {
        "module": "User",
        "permissions": [
            ("view", "Users View"),
            ("add", "Users Add"),
            ("update", "Users Update"),
            ("delete", "Users Delete"),
        ],
    },
    {
        "module": "Invitation",
        "permissions": [
            ("view", "Invitations View"),
            ("add", "Invitations Add"),
            ("update", "Invitations Update"),
            ("delete", "Invitations Delete"),
        ],
    },
    {
        "module": "Role",
        "permissions": [
            ("view", "Roles View"),
            ("add", "Roles Add"),
            ("update", "Roles Update"),
            ("delete", "Roles Delete"),
        ],
    },
    {
        "module": "Company",
        "permissions": [
            ("view", "Companies View"),
            ("add", "Companies Add"),
            ("update", "Companies Update"),
            ("delete", "Companies Delete"),
        ],
    },
]

COM_MODULE_PERMISSIONS = [
    {
        "module": "User",
        "permissions": [
            ("view", "Users View"),
            ("add", "Users Add"),
            ("update", "Users Update"),
            ("delete", "Users Delete"),
        ],
    },
    {
        "module": "Invitation",
        "permissions": [
            ("view", "Invitations View"),
            ("add", "Invitations Add"),
            ("update", "Invitations Update"),
            ("delete", "Invitations Delete"),
        ],
    },
    {
        "module": "Role",
        "permissions": [
            ("view", "Roles View"),
            ("add", "Roles Add"),
            ("update", "Roles Update"),
            ("delete", "Roles Delete"),
        ],
    },
    {
        "module": "Client",
        "permissions": [
            ("view", "Clients View"),
            ("add", "Clients Add"),
            ("update", "Clients Update"),
            ("delete", "Clients Delete"),
        ],
    },
]

ss_available_role_permissions = [
    "User:view",
    "User:add",
    "User:update",
    "User:delete",
    "Invitation:view",
    "Invitation:add",
    "Invitation:update",
    "Invitation:delete",
    "Role:view",
    "Role:add",
    "Role:update",
    "Role:delete",
    "Company:view",
    "Company:add",
    "Company:update",
    "Company:delete",
]

com_available_role_permissions = [
    "User:view",
    "User:add",
    "User:update",
    "User:delete",
    "Invitation:view",
    "Invitation:add",
    "Invitation:update",
    "Invitation:delete",
    "Role:view",
    "Role:add",
    "Role:update",
    "Role:delete",
    "Client:view",
    "Client:add",
    "Client:update",
    "Client:delete",
]
