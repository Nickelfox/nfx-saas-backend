from django.contrib import admin
from apps.department.models import Department
from apps.user.models import User
from apps.project.models import Project, ProjectMember
from custom_admin import company_admin_site
from apps.team.models import Team
from common.helpers import module_perm
from django.contrib.admin.widgets import FilteredSelectMultiple
from common.constants import Days_choice
from django import forms

# Register your models here.


class TeamSpecificAdminForm(forms.ModelForm):
    # Create a list of choices based on the Days_choice enumeration
    work_days = forms.MultipleChoiceField(
        choices=[(day.value, day.label) for day in Days_choice],
        widget=FilteredSelectMultiple("Work Days", is_stacked=False),
        required=False,
        initial=[
            "MON",
            "TUE",
            "WED",
            "THU",
            "FRI",
        ],  # Set default values for work_days
    )

    class Meta:
        model = Team
        fields = [
            "capacity",  # Add the 'capacity' field
            "work_days",
            "user",
            "department",
        ]

    def clean(self):
        cleaned_data = super().clean()
        # Set a default value for the "capacity" field if it's not provided
        if "capacity" not in cleaned_data:
            cleaned_data["capacity"] = 8
        return cleaned_data


class ProjectInline(admin.TabularInline):
    model = ProjectMember
    fields = [
        "project",
    ]
    readonly_fields = [
        "project",
    ]
    extra = 0
    classes = ("collapse",)
    can_delete = False
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("team", user, "update")

    def has_view_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("team", user, "view")

    def has_add_permission(self, request, obj=None):
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("team", user, "add")

    def has_delete_permission(self, request, obj=None):
        # Check if the user has permission to delete the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("team", user, "delete")


class TeamSpecificAdmin(admin.ModelAdmin):
    inlines = [ProjectInline]
    form = TeamSpecificAdminForm
    list_display = [
        "id",
        "capacity",
        "department",
        "work_days",
    ]
    list_filter = ("department",)

    def save_model(self, request, obj, form, change):
        # Save the object initially to generate obj.id
        super().save_model(request, obj, form, change)

        # Check if this is a new invitation being added (not an update)
        if not change:
            obj.company_id = request.user.company_id
            obj.save()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "department":
            user = request.user
            kwargs["queryset"] = Department.objects.filter(
                company_id=user.company_id
            )
        if db_field.name == "user":
            user = request.user
            kwargs["queryset"] = User.objects.filter(company=user.company_id)
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
            return module_perm("team", user, "update")

    def has_view_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("team", user, "view")

    def has_add_permission(self, request):
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("team", user, "add")

    def has_delete_permission(self, request, obj=None):
        # Check if the user has permission to delete the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("team", user, "delete")


company_admin_site.register(Team, TeamSpecificAdmin)
