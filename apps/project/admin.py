from django.contrib import admin
from apps.project.models import Project, ProjectMember
from apps.team.models import Team
from apps.client.models import Client
from custom_admin import company_admin_site
from common.helpers import module_perm

# Register your models here.


class MemberInline(admin.TabularInline):
    model = ProjectMember
    fields = [
        "member",
    ]
    extra = 0
    can_delete = False
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("project_member", user, "update")

    def has_view_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("project_member", user, "view")

    def has_add_permission(self, request, obj=None):
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("project_member", user, "add")

    def has_delete_permission(self, request, obj=None):
        # Check if the user has permission to delete the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("project_member", user, "delete")


class ProjectSpecificAdmin(admin.ModelAdmin):
    inlines = [MemberInline]
    list_display = ["project_name", "client", "start_date", "end_date", "id"]
    list_filter = (
        "client",
        "project_type",
    )
    fields = [
        "project_name",
        "project_code",
        "client",
        "start_date",
        "end_date",
        "project_type",
        "notes",
    ]

    def save_model(self, request, obj, form, change):
        # Save the object initially to generate obj.id
        super().save_model(request, obj, form, change)

        # Check if this is a new invitation being added (not an update)
        if not change:
            obj.company_id = request.user.company_id
            obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "client":
            user = request.user
            kwargs["queryset"] = Client.objects.filter(
                company_id=user.company_id
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        user = request.user
        return super().get_queryset(request).filter(company_id=user.company_id)

    def has_change_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("project", user, "update")

    def has_view_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("project", user, "view")

    def has_add_permission(self, request):
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("project", user, "add")

    def has_delete_permission(self, request, obj=None):
        # Check if the user has permission to delete the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("project", user, "delete")


company_admin_site.register(Project, ProjectSpecificAdmin)


class ProjectMemberSpecificAdmin(admin.ModelAdmin):
    list_display = [
        "project",
        "member",
    ]
    list_filter = (
        "project",
        "member",
    )
    fields = [
        "project",
        "member",
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project":
            user = request.user
            kwargs["queryset"] = Project.objects.filter(
                company_id=user.company_id
            )
        if db_field.name == "team":
            user = request.user
            kwargs["queryset"] = Team.objects.filter(
                company_id=user.company_id
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        user = request.user
        return (
            super()
            .get_queryset(request)
            .filter(project__company_id=user.company_id)
        )

    def has_change_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("project_member", user, "update")

    def has_view_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("project_member", user, "view")

    def has_add_permission(self, request):
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("project_member", user, "add")

    def has_delete_permission(self, request, obj=None):
        # Check if the user has permission to delete the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("project_member", user, "delete")


company_admin_site.register(ProjectMember, ProjectMemberSpecificAdmin)
