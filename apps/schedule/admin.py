from django.contrib import admin
from apps.project.models import ProjectMember
from apps.schedule.models import Schedule
from apps.team.models import Team
from apps.client.models import Client
from custom_admin import company_admin_site
from common.helpers import module_perm


# Register your models here.


class ScheduleSpecificAdmin(admin.ModelAdmin):
    list_display = [
        "project_member",
        "start_at",
        "end_at",
        "id",
        "schedule_type",
    ]
    list_filter = (
        "start_at",
        "end_at",
    )
    fields = [
        "project_member",
        "start_at",
        "end_at",
        "notes",
        "assigned_hour",
        "schedule_type",
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project_member":
            user = request.user
            kwargs["queryset"] = ProjectMember.objects.filter(
                project__company_id=user.company_id
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        user = request.user
        return (
            super()
            .get_queryset(request)
            .filter(project_member__project__company_id=user.company_id)
        )

    def has_change_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("schedule", user, "update")

    def has_view_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("schedule", user, "view")

    def has_add_permission(self, request):
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("schedule", user, "add")

    def has_delete_permission(self, request, obj=None):
        # Check if the user has permission to delete the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("schedule", user, "delete")


company_admin_site.register(Schedule, ScheduleSpecificAdmin)
