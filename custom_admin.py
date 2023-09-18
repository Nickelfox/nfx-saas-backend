from django.contrib import admin
from django.urls import path


class SSAdminSite(admin.AdminSite):
    site_header = "Squad Spot Admin Panel"
    index_title = 'Modules'                 # default: "Site administration"
    site_title = 'SS Admin'  # default: "Django site admin"


ss_admin_site = SSAdminSite(name="ss-admin")


class CompanyAdminSite(admin.AdminSite):
    site_header = "Company Admin Panel"
    index_title = 'Modules'                 # default: "Site administration"
    site_title = 'Company Admin'  # default: "Django site admin"

    def index(self, request, extra_context=None):
        # Get the user's company name from the URL parameter if not provided
        company_name = request.user.company.name if request.user.company else None

        # Dynamically set the site header and title based on the company_name
        if company_name:
            self.site_header = f"{company_name.upper()} Squad Spot Panel"
            self.site_title = f"{company_name.upper()} Admin"

        return super().index(request, extra_context=extra_context)


company_admin_site = CompanyAdminSite(name="company_admin")
