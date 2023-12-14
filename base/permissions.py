from rest_framework import permissions
from common.helpers import module_perm


class ModulePermission(permissions.BasePermission):
    """
    Custom permission class to check module-level permissions.
    """

    def has_permission(self, request, view):
        # Check if the user has the required module permission for the action
        action_mapping = {
            "list": "view",
            "create": "add",
            "partial_update": "update",
            "destroy": "delete",
            "retrieve": "view",
        }
        module_mapping = {
            "projectmember": "project_member",
            "client": "client",
            "user": "user",
            "department": "department",
            "project": "project",
            "team": "team",
            "schedule": "schedule",
        }
        user = request.user
        action = view.action
        module_name = view.basename.lower()
        permission_action = action_mapping[action]
        return user.is_company_owner or module_perm(
            module_mapping[module_name], user, permission_action
        )
