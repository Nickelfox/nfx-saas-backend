from apps.role.models import AccessRole
from common.models import BaseModel
from django.shortcuts import get_object_or_404
from django.http import Http404
from apps.user.models import Invitation, User
from apps.company.models import Company


def module_perm(name, user, perm):
    user_access = AccessRole.objects.filter(id=user.role_id)
    if not user_access :
        return False
    user_access = user_access.first()
    role_permissions = user_access.role_permissions
    module_permissions = [permission.split(':')[1] for permission in role_permissions if permission.startswith(f'{name.title()}:')]
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
