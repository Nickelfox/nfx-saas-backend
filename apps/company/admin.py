from django.urls import reverse
from django.contrib import admin
from common.helpers import module_perm
from .models import Company
from custom_admin import ss_admin_site
from squad_spot.settings import HOST_URL


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner_email',
                    'invite_link', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'owner_email')
    readonly_fields = ('invite_link','is_active',)
    fields = ('name','owner_name', 'owner_email',
                    'invite_link', 'is_active')
    
    def save_model(self, request, obj, form, change):
    # Save the object initially to generate obj.id
        super().save_model(request, obj, form, change)

    # Check if this is a new invitation being added (not an update)
        if not change:
            # Generate the invite_link based on the UUID (id) of the new invitation
            new_uuid = obj.id  # obj.id is the default UUID
            invite_link = f"{HOST_URL}{reverse('user:accept_invitation', args=[str(new_uuid)])}"
            # Update the invite_link in the model and save it again
            obj.invite_link = invite_link
            obj.save()
    
    
    def has_change_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_super_user: 
            return True
        else:
            return module_perm("company", user, "update")
            
    def has_view_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_super_user: 
            return True
        else:
            return module_perm("company", user, "view")

    def has_add_permission(self, request):
        user = request.user
        if user.is_super_user: 
            return True
        else:
            return module_perm("company", user, "add")

    def has_delete_permission(self, request, obj=None):
        # Check if the user has permission to delete the object
        user = request.user
        if user.is_super_user: 
            return True
        else:
            return module_perm("company", user, "delete")


ss_admin_site.register(Company, CompanyAdmin)
