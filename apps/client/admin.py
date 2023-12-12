from django.contrib import admin
from django.urls import path
from apps.client.resources import ClientResource
from custom_admin import company_admin_site
from apps.client.models import Client
from apps.project.models import Project
from common.helpers import module_perm
from import_export.admin import ImportExportModelAdmin
from django.http import HttpResponse
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.datavalidation import DataValidation


# Register your models here.


class ProjectInline(admin.TabularInline):
    model = Project
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
    ]
    extra = 0
    can_delete = False
    show_change_link = True

    def get_queryset(self, request):
        user = request.user
        return super().get_queryset(request).filter(company_id=user.company_id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "client":
            user = request.user
            kwargs["queryset"] = Client.objects.filter(
                company_id=user.company_id
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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

    def has_add_permission(self, request, obj=None):
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


class ClientSpecificAdmin(ImportExportModelAdmin):
    change_list_template = "company_admin/client_change_list.html"
    resource_class = ClientResource
    inlines = [ProjectInline]
    list_display = ["name", "id"]
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
        urls = super(ClientSpecificAdmin, self).get_urls()
        my_urls = [
            path(
                "download_template/client/",
                self.download_template,
                name="client_custom_view",
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
        ] = "attachment; filename=client_template.xlsx"

        # Save the workbook directly to the response
        wb.save(response)

        return response

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
