from django import forms
from django.contrib import admin
from apps.role.models import AccessRole
from django.contrib.admin.widgets import FilteredSelectMultiple
from common.helpers import (module_perm, SS_MODULE_PERMISSIONS,
                            COM_MODULE_PERMISSIONS)
from custom_admin import ss_admin_site, company_admin_site


class AccessRoleAdminForm(forms.ModelForm):
    # Create a list of choices based on the new structure
    role_permissions = forms.MultipleChoiceField(
        choices=[
            (f"{module['module']}:{perm[0]}", perm[1])
            for module in SS_MODULE_PERMISSIONS
            for perm in module['permissions']
        ],
        widget=FilteredSelectMultiple("Permissions", is_stacked=False),
        required=False,
    )

    class Meta:
        model = AccessRole
        fields = ["name", "description", "role_permissions"]


class AccessRoleAdmin(admin.ModelAdmin):
    form = AccessRoleAdminForm 
    list_display = ["name","id", "role_permissions"]
    
    def has_change_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_super_user: 
            return True
        else:
            return module_perm("role", user, "update")
        
    def has_view_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_super_user: 
            return True
        else:
            return module_perm("role", user, "view")
            


    def has_add_permission(self, request):
        user = request.user
        if user.is_super_user: 
            return True
        else:
            return module_perm("role", user, "add")

    def has_delete_permission(self, request, obj=None):
        # Check if the user has permission to delete the object
        user = request.user
        if user.is_super_user: 
            return True
        else:
            return module_perm("role", user, "delete")




ss_admin_site.register(AccessRole, AccessRoleAdmin)

class AccessRoleSpecificAdminForm(forms.ModelForm):
    # Create a list of choices based on the new structure
    role_permissions = forms.MultipleChoiceField(
        choices=[
            (f"{module['module']}:{perm[0]}", perm[1])
            for module in COM_MODULE_PERMISSIONS
            for perm in module['permissions']
        ],
        widget=FilteredSelectMultiple("Permissions", is_stacked=False),
        required=False,
    )

    class Meta:
        model = AccessRole
        fields = ["name", "description", "role_permissions"]


class AccessRoleSpecificAdmin(admin.ModelAdmin):
    form = AccessRoleSpecificAdminForm 
    list_display = ["name","id", "role_permissions"]

    def save_model(self, request, obj, form, change):
    # Save the object initially to generate obj.id
        super().save_model(request, obj, form, change)

    # Check if this is a new invitation being added (not an update)
        if not change:
            obj.company_id = request.user.company_id
            obj.save()

    def get_queryset(self, request):
        user = request.user
        return super().get_queryset(request).filter(company_id=user.company_id)
    
    def has_change_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner: 
            return True
        else:
            return module_perm("role", user, "update")
        
    def has_view_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner: 
            return True
        else:
            return module_perm("role", user, "view")
            

    def has_add_permission(self, request):
        user = request.user
        if user.is_company_owner: 
            return True
        else:
            return module_perm("role", user, "add")

    def has_delete_permission(self, request, obj=None):
        # Check if the user has permission to delete the object
        user = request.user
        if user.is_company_owner: 
            return True
        else:
            return module_perm("role", user, "delete")

company_admin_site.register(AccessRole, AccessRoleSpecificAdmin)