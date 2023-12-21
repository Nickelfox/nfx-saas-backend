from django.contrib import admin
from apps.role.models import AccessRole
from common.helpers import (
    module_perm,
    ss_available_role_permissions,
    com_available_role_permissions,
)
from .models import User
from django.contrib.auth.hashers import make_password
from custom_admin import ss_admin_site, company_admin_site


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_company_owner")
    list_filter = ("is_active", "is_company_owner")
    ordering = ("email",)
    readonly_fields = ("is_company_owner",)
    fields = (
        "full_name",
        "email",
        "role",
        "phone_number",
        "designation",
        "company",
        "is_company_owner",
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fields_to_hide = []

        # Check if the ForeignKey 'role' and 'company' are None
        if obj:
            if obj.role is None:
                fields_to_hide.append("role")
            if obj.company is None:
                fields_to_hide.append("company")

        # Exclude the fields that need to be hidden
        fieldsets[0][1]["fields"] = [
            field
            for field in fieldsets[0][1]["fields"]
            if field not in fields_to_hide
        ]

        return fieldsets

    def save_model(self, request, obj, form, change):
        if not change:  # Only apply this when adding a new user
            # Encode the password using make_password before saving
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "role":
            obj = request._obj_
            if obj:
                kwargs["queryset"] = AccessRole.objects.filter(
                    company_id=obj.company_id
                )
            else:
                kwargs["queryset"] = AccessRole.objects.filter(
                    company_id__exact=None
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        # Store the object being edited in the request
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)

    def has_change_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_super_user:
            return True
        else:
            edit_perm = module_perm("user", user, "update")
            if not edit_perm:
                return False
            else:
                if (
                    obj and obj.is_super_user
                ):  # Check if the object is associated with a superuser
                    return False
                if (
                    user.role.role_permissions != ss_available_role_permissions
                ) and (
                    obj
                    and obj.role.role_permissions
                    == ss_available_role_permissions
                ):  # Compare with all available role permissions
                    return False  # Superadmins cannot be deleted
                return True

    def has_view_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_super_user:
            return True
        else:
            return module_perm("user", user, "view")

    def has_add_permission(self, request):
        user = request.user
        if user.is_super_user:
            return True
        else:
            return module_perm("user", user, "add")

    def has_delete_permission(self, request, obj=None):
        # Check if the user has permission to delete the object
        user = request.user
        if user.is_super_user:
            return True
        else:
            del_perm = module_perm("user", user, "delete")
            if not del_perm:
                return False
            else:
                if (
                    obj and obj.is_super_user
                ):  # Check if the object is associated with a superuser
                    return False
                if (
                    user.role.role_permissions != ss_available_role_permissions
                ) and (
                    obj
                    and obj.role.role_permissions
                    == ss_available_role_permissions
                ):  # Compare with all available role permissions
                    return False  # Superadmins cannot be deleted
                return True


class CustomUserSpecificAdmin(admin.ModelAdmin):
    list_display = ("email", "is_company_owner")
    list_filter = ("is_active", "is_company_owner")
    ordering = ("email",)
    readonly_fields = ("is_company_owner",)
    fields = (
        "full_name",
        "email",
        "role",
        "phone_number",
        "designation",
        "is_company_owner",
    )

    def get_queryset(self, request):
        user = request.user
        return super().get_queryset(request).filter(company=user.company_id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "role":
            user = request.user
            kwargs["queryset"] = AccessRole.objects.filter(
                company_id=user.company_id
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:  # Only apply this when adding a new user
            # Encode the password using make_password before saving
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner:
            return True
        # if obj and (user.id == obj.id):
        #     return True
        else:
            edit_perm = module_perm("user", user, "update")
            if not edit_perm:
                return False
            else:
                if obj and obj.is_company_owner:
                    return False
                if (
                    user.role.role_permissions
                    != com_available_role_permissions
                ) and (
                    obj
                    and obj.role.role_permissions
                    == com_available_role_permissions
                ):
                    return False
            return True

    def has_view_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("user", user, "view")

    def has_add_permission(self, request):
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("user", user, "add")

    def has_delete_permission(self, request, obj=None):
        # Check if the user has permission to delete the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            del_perm = module_perm("user", user, "delete")
            if not del_perm:
                return False
            else:
                if obj and obj.is_company_owner:
                    return False
                if (
                    user.role.role_permissions
                    != com_available_role_permissions
                ) and (
                    obj
                    and obj.role.role_permissions
                    == com_available_role_permissions
                ):
                    return False
            return True


ss_admin_site.register(User, CustomUserAdmin)
company_admin_site.register(User, CustomUserSpecificAdmin)
