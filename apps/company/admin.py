from django.urls import reverse
from django.contrib import admin
# from django_restful_admin import admin as rest_admin
from apps.user.models import User
from common.helpers import module_perm
from .models import Company
from custom_admin import ss_admin_site
# restapi_ss_admin_site
from squad_spot.settings import HOST_URL


class CompanyAdmin(admin.ModelAdmin): 
    list_display = ("name", "owner_email", "invite_link", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "owner_email")
    readonly_fields = ("invite_link", "is_active")
    fields = ("name", "owner_name", "owner_email", "invite_link", "is_active")

    def regenerate_invitation(self, request, queryset):
        for company in queryset:
            user_obj = User.objects.filter(email=company.owner_email)
            if user_obj:
                user_obj.delete()
            rev_url = "user:accept_invitation"
            new_uuid = company.id
            company.invite_link = (
                f"{HOST_URL}{reverse(rev_url, args=[str(new_uuid)])}"
            )
            company.name = company.name.lower()
            company.is_active = False
            company.save()

    regenerate_invitation.short_description = "Regenerate Invitations"

    actions = [regenerate_invitation]

    def get_actions(self, request):
        actions = super().get_actions(request)
        user = request.user
        if not user.is_super_user and not module_perm(
            "company", user, "regenerate"
        ):
            actions.pop("regenerate_invitation", None)
        return actions

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            rev_url = "user:accept_invitation"
            new_uuid = obj.id
            invite_link = f"{HOST_URL}{reverse(rev_url, args=[str(new_uuid)])}"
            obj.name = obj.name.lower()
            obj.invite_link = invite_link
            obj.save()

    def has_change_permission(self, request, obj=None):
        user = request.user
        return user.is_super_user or module_perm("company", user, "update")

    def has_view_permission(self, request, obj=None):
        user = request.user
        return user.is_super_user or module_perm("company", user, "view")

    def has_add_permission(self, request):
        user = request.user
        return user.is_super_user or module_perm("company", user, "add")

    def has_delete_permission(self, request, obj=None):
        user = request.user
        return user.is_super_user or module_perm("company", user, "delete")


ss_admin_site.register(Company, CompanyAdmin)
# restapi_ss_admin_site.register(Company, RESTCompanyAdmin)
