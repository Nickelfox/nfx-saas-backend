from django.contrib import admin
from django.urls import reverse
from .models import Invitation
from apps.role.models import AccessRole
from common.constants import Invite_type
from common.helpers import module_perm
from custom_admin import ss_admin_site, company_admin_site

from squad_spot.settings import HOST_URL

# Register your models here.


class InvitationAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "role", "invite_link", "is_active")
    list_filter = ("is_active",)
    search_fields = ("fullname", "email")
    readonly_fields = ("invite_link",)
    fields = ("fullname", "email", "role", "invite_link", "is_active")

    def save_model(self, request, obj, form, change):
        # Save the object initially to generate obj.id
        super().save_model(request, obj, form, change)

        # Check if this is a new invitation being added (not an update)
        if not change:
            # Generate the invite_link based on id of new invitation
            new_uuid = obj.id  # obj.id is the default UUID
            rev_url = "user:accept_invitation"
            invite_link = f"{HOST_URL}{reverse(rev_url, args=[str(new_uuid)])}"
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


class InvitationSpecificAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "role", "invite_link", "is_active")
    list_filter = ("is_active",)
    search_fields = ("fullname", "email")
    readonly_fields = ("invite_link",)
    fields = ("fullname", "email", "role", "invite_link", "is_active")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "role":
            user = request.user
            kwargs["queryset"] = AccessRole.objects.filter(
                company_id=user.company_id
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        # Save the object initially to generate obj.id
        super().save_model(request, obj, form, change)

        # Check if this is a new invitation being added (not an update)
        if not change:
            # Generate the invite_link based on id of new invitation
            new_uuid = obj.id  # obj.id is the default UUID
            rev_url = "user:accept_invitation"
            invite_link = f"{HOST_URL}{reverse(rev_url, args=[str(new_uuid)])}"

            # Update the invite_link in the model and save it again
            obj.invite_link = invite_link
            obj.invite_type = Invite_type.COMPANY
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


ss_admin_site.register(Invitation, InvitationAdmin)
company_admin_site.register(Invitation, InvitationSpecificAdmin)
