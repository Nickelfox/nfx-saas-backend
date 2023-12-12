from django.contrib import admin
from django.urls import path
from apps.department.resources import DepartmentResource
from apps.user.models import User
from custom_admin import company_admin_site
from apps.department.models import Department
from apps.team.models import Team
from common.helpers import module_perm
from import_export.admin import ImportExportModelAdmin
from django.http import HttpResponse
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.datavalidation import DataValidation


class TeamMemberInline(admin.TabularInline):
    model = Team
    extra = 0
    max_num = 0
    readonly_fields = [
        "work_days",
    ]
    fields = [
        "capacity",
        "emp_id",
        "work_days",
        "user",
    ]
    can_delete = False
    show_change_link = True

    def get_queryset(self, request):
        user = request.user
        return super().get_queryset(request).filter(company_id=user.company_id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            user = request.user
            kwargs["queryset"] = User.objects.filter(
                company_id=user.company_id
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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


class DeparmentSpecificAdmin(ImportExportModelAdmin):
    change_list_template = "company_admin/department_change_list.html"
    resource_class = DepartmentResource
    inlines = [TeamMemberInline]
    list_display = ["name", "id"]
    list_filter = ("name",)
    fields = ["name"]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.company_id = request.user.company_id
            instance.save()
        formset.save_m2m()

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

    def get_urls(self):
        urls = super(DeparmentSpecificAdmin, self).get_urls()
        my_urls = [
            path(
                "download_template/department/",
                self.download_template,
                name="department_custom_view",
            ),
        ]
        return my_urls + urls

    def download_template(self, request):
        # Create a workbook in-memory
        wb = Workbook()
        ws = wb.active
        headers = ["name"]
        ws.append(headers)

        # Create an HttpResponse with Excel content type
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Set the response headers for file attachment
        response[
            "Content-Disposition"
        ] = "attachment; filename=department_template.xlsx"

        # Save the workbook directly to the response
        wb.save(response)

        return response

    def has_change_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("department", user, "update")

    def has_view_permission(self, request, obj=None):
        # Check if the user has permission to change the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("department", user, "view")

    def has_add_permission(self, request):
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("department", user, "add")

    def has_delete_permission(self, request, obj=None):
        # Check if the user has permission to delete the object
        user = request.user
        if user.is_company_owner:
            return True
        else:
            return module_perm("department", user, "delete")


company_admin_site.register(Department, DeparmentSpecificAdmin)
