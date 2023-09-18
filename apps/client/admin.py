from django.contrib import admin
from custom_admin import company_admin_site
from apps.client.models import Client
from common.helpers import module_perm
# Register your models here.


class ClientSpecificAdmin(admin.ModelAdmin):

    list_display = ["name","id"]
    fields = ["name"]

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
            return module_perm("client", user, "update")

    def has_view_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner: 
            return True
        else:
            return module_perm("client", user, "view")

    def has_add_permission(self, request):
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("client", user, "add")

    def has_delete_permission(self, request, obj=None):
        # Check if the user has permission to delete the object
        user = request.user
        if user.is_company_owner: 
            return True
        else:
            return module_perm("client", user, "delete")


company_admin_site.register(Client, ClientSpecificAdmin)
