from django.urls import reverse
from django.contrib import admin
from apps.role.models import AccessRole
from common.helpers import module_perm
from .models import User, Invitation
from django.contrib.auth.hashers import make_password
from custom_admin import ss_admin_site, company_admin_site
from squad_spot.settings import HOST_URL


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email', 'role',
                    'invite_link', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('fullname', 'email')
    readonly_fields = ('invite_link',)
    fields = ('fullname', 'email', 'role',
              'invite_link', 'is_active')

    def save_model(self, request, obj, form, change):
        # Save the object initially to generate obj.id
        super().save_model(request, obj, form, change)

        # Check if this is a new invitation being added (not an update)
        if not change:
            # Generate the invite_link based on id of new invitation
            new_uuid = obj.id  # obj.id is the default UUID

            invite_link = f"{HOST_URL}{reverse('user:accept_invitation', args=[str(new_uuid)])}"
            obj.invite_link = invite_link
            obj.save()

    def has_change_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_super_user:
            return True
        else:
            return module_perm("user", user, "update")

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
            return module_perm("user", user, "delete")


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_company_owner')
    list_filter = ( 'is_active', 'is_company_owner')
    ordering = ('email',)
    readonly_fields = (
                       'is_company_owner',)
    fields = ('full_name',
              'email',
              'role',
              'phone_number',
              'designation',
              'company',
              'is_company_owner',
              )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fields_to_hide = []

        # Check if the ForeignKey 'role' and 'company' are None
        if obj:
            if obj.role is None:
                fields_to_hide.append('role')
            if obj.company is None:
                fields_to_hide.append('company')

        # Exclude the fields that need to be hidden
        fieldsets[0][1]['fields'] = [field for field in fieldsets[0][1]['fields'] if field not in fields_to_hide]

        return fieldsets

    def save_model(self, request, obj, form, change):
        if not change:  # Only apply this when adding a new user
            # Encode the password using make_password before saving
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_super_user:
            return True
        else:
            return module_perm("user", user, "update")

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
            return module_perm("user", user, "delete")


class InvitationSpecificAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'email', 'role',
                    'invite_link', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('fullname', 'email')
    readonly_fields = ('invite_link',)
    fields = ('fullname', 'email', 'role',
              'invite_link', 'is_active')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'role':
            user = request.user
            kwargs['queryset'] = AccessRole.objects.filter(
                company_id=user.company_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        # Save the object initially to generate obj.id
        super().save_model(request, obj, form, change)

        # Check if this is a new invitation being added (not an update)
        if not change:
            # Generate the invite_link based on id of new invitation
            new_uuid = obj.id  # obj.id is the default UUID
            invite_link = f"{HOST_URL}{reverse('user:accept_invitation', args=[str(new_uuid)])}"

            # Update the invite_link in the model and save it again
            obj.invite_link = invite_link
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
            return module_perm("invitation", user, "update")

    def has_view_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("invitation", user, "view")

    def has_add_permission(self, request):
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("invitation", user, "add")

    def has_delete_permission(self, request, obj=None):
        # Check if the user has permission to delete the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("invitation", user, "delete")


class CustomUserSpecificAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_company_owner')
    list_filter = ( 'is_active', 'is_company_owner')
    ordering = ('email',)
    readonly_fields = (
                       'is_company_owner',)
    fields = ('full_name',
              'email',
              'role',
              'phone_number',
              'designation',
              'is_company_owner',
              )

    def get_queryset(self, request):
        user = request.user
        return super().get_queryset(request).filter(company=user.company_id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'role':
            user = request.user
            kwargs['queryset'] = AccessRole.objects.filter(
                company_id=user.company_id)
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
        else:
            return module_perm("user", user, "update")

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
            return module_perm("user", user, "delete")


ss_admin_site.register(User, CustomUserAdmin)
ss_admin_site.register(Invitation, InvitationAdmin)

company_admin_site.register(User, CustomUserSpecificAdmin)
company_admin_site.register(Invitation, InvitationSpecificAdmin)
