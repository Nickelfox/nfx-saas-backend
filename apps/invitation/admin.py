from django.contrib import admin
from django.urls import reverse
from apps.invitation.helpers import reinvite_user

from apps.user.models import User
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
    readonly_fields = ("invite_link", "is_active")
    fields = ("fullname", "email", "role", "invite_link", "is_active")

    def regenerate_invitation(self, request, queryset):
        for invitation in queryset:
            # Generate a new invite_link and send it to the email
            reinvite_user(invitation)

    regenerate_invitation.short_description = "Regenerate Invitations"

    actions = [regenerate_invitation]

    def get_actions(self, request):
        actions = super().get_actions(request)
        user = request.user
        if not user.is_super_user:
            if not module_perm("invitation", user, "regenerate"):
                actions.pop("regenerate_invitation", None)
        return actions

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
            obj.company_id = None
            obj.save()

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
            return module_perm("invitation", user, "update")

    def has_view_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_super_user:
            return True
        else:
            return module_perm("invitation", user, "view")

    def has_add_permission(self, request):
        user = request.user
        if user.is_super_user:
            return True
        else:
            return module_perm("invitation", user, "add")

    def has_delete_permission(self, request, obj=None):
        # Check if the user has permission to delete the object
        user = request.user
        if user.is_super_user:
            return True
        else:
            return module_perm("invitation", user, "delete")


class InvitationSpecificAdmin(admin.ModelAdmin):
    list_display = ("fullname", "email", "role", "invite_link", "is_active")
    list_filter = ("is_active",)
    search_fields = ("fullname", "email")
    readonly_fields = ("invite_link",)
    fields = ("fullname", "email", "role", "invite_link", "is_active")

    def regenerate_invitation(self, request, queryset):
        for invitation in queryset:
            # Generate a new invite_link and send it to the email
            user_obj = User.objects.filter(email=invitation.email)
            if user_obj:
                user_obj.delete()
            invitation.is_active = True
            invitation.save()
            # Send the new invite to the email (you should implement this part)

    regenerate_invitation.short_description = "Regenerate Invitations"

    actions = [regenerate_invitation]

    def get_actions(self, request):
        actions = super().get_actions(request)
        user = request.user
        if not user.is_company_owner:
            if not module_perm("invitation", user, "regenerate"):
                actions.pop("regenerate_invitation", None)
        return actions

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
