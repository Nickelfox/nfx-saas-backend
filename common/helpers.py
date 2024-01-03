from apps.client.models import Client
from apps.project.models import Project
from apps.role.models import AccessRole
from common import constants


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
            ("regenerate", "Invitations Regenerate"),
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
            ("regenerate", "Invitations Regenerate"),
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
            ("regenerate", "Invitations Regenerate"),
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
    {
        "module": "Department",
        "permissions": [
            ("view", "Departments View"),
            ("add", "Departments Add"),
            ("update", "Departments Update"),
            ("delete", "Departments Delete"),
        ],
    },
    {
        "module": "Team",
        "permissions": [
            ("view", "Teams View"),
            ("add", "Teams Add"),
            ("update", "Teams Update"),
            ("delete", "Teams Delete"),
        ],
    },
    {
        "module": "Project",
        "permissions": [
            ("view", "Projects View"),
            ("add", "Projects Add"),
            ("update", "Projects Update"),
            ("delete", "Projects Delete"),
        ],
    },
    {
        "module": "Project_Member",
        "permissions": [
            ("view", "Project_Members View"),
            ("add", "Project_Members Add"),
            ("update", "Project_Members Update"),
            ("delete", "Project_Members Delete"),
        ],
    },
    {
        "module": "Schedule",
        "permissions": [
            ("view", "Schedules View"),
            ("add", "Schedules Add"),
            ("update", "Schedules Update"),
            ("delete", "Schedules Delete"),
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
    "Invitation:regenerate",
    "Role:view",
    "Role:add",
    "Role:update",
    "Role:delete",
    "Company:view",
    "Company:add",
    "Company:update",
    "Company:delete",
    "Company:regenerate",
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
    "Invitation:regenerate",
    "Role:view",
    "Role:add",
    "Role:update",
    "Role:delete",
    "Client:view",
    "Client:add",
    "Client:update",
    "Client:delete",
    "Department:view",
    "Department:add",
    "Department:update",
    "Department:delete",
    "Team:view",
    "Team:add",
    "Team:update",
    "Team:delete",
    "Project:view",
    "Project:add",
    "Project:update",
    "Project:delete",
    "Project_member:view",
    "Project_member:add",
    "Project_member:update",
    "Project_member:delete",
    "Schdeule:view",
    "Schdeule:add",
    "Schdeule:update",
    "Schdeule:delete",
]


def create_static_objs_on_company_gen(company_id):
    client_instance, created_client = Client.objects.get_or_create(
        name=constants.Schedule_type.TIME_OFF, company_id=company_id
    )
    role_instance, created_role = AccessRole.objects.get_or_create(
        name=constants.GeneralConstants.NO_ACCESS_ROLE, company_id=company_id
    )
    project_instance, created_project = Project.objects.get_or_create(
        project_name=constants.Schedule_type.TIME_OFF,
        client=client_instance,
        color_code=constants.Color_choice.Black,
        company_id=company_id,
    )
