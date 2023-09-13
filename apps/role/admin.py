from django import forms
from django.contrib import admin
from apps.role.models import AccessRole
from apps.role import forms as role_forms
import os
from django.conf import settings
from django.utils.safestring import mark_safe
from django.forms.widgets import CheckboxSelectMultiple
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelMultipleChoiceField

from common.helpers import module_perm
from custom_admin import ss_admin_site, company_admin_site


MODULE_PERMISSIONS = [
   {
       'module': 'User',
       'permissions': [
           ('view', 'Users View'),
           ('add', 'Users Add'),
           ('update', 'Users Update'),
           ('delete', 'Users Delete'),
       ],
   },
   {
       'module': 'Invitation',
       'permissions': [
           ('view', 'Invitations View'),
           ('add', 'Invitations Add'),
           ('update', 'Invitations Update'),
           ('delete', 'Invitations Delete'),
       ],
   },
   {
       'module': 'Role',
       'permissions': [
           ('view', 'Roles View'),
           ('add', 'Roles Add'),
           ('update', 'Roles Update'),
           ('delete', 'Roles Delete'),
       ],
   },
   {
       'module': 'Company',
       'permissions': [
           ('view', 'Companies View'),
           ('add', 'Companies Add'),
           ('update', 'Companies Update'),
           ('delete', 'Companies Delete'),
       ],
   },
   # Add more modules and permissions as needed
]

class AccessRoleAdminForm(forms.ModelForm):
    # Create a list of choices based on the new structure
    role_permissions = forms.MultipleChoiceField(
        choices=[
            (f"{module['module']}:{perm[0]}", perm[1])
            for module in MODULE_PERMISSIONS
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


class AccessRoleSpecificAdmin(admin.ModelAdmin):
    form = AccessRoleAdminForm 
    list_display = ["name","id", "role_permissions"]
    
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