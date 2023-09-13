from django.contrib import admin
from django.urls import path


class SSAdminSite(admin.AdminSite):
    site_header = "SS Admin Panel"
    index_title = 'Modules'                 # default: "Site administration"
    site_title = 'SS Admin' # default: "Django site admin"

# Create an instance of the custom admin site
ss_admin_site = SSAdminSite()


class CompanyAdminSite(admin.AdminSite):
    site_header = "Company Admin Panel"
    index_title = 'Modules'                 # default: "Site administration"
    site_title = 'Company Admin' # default: "Django site admin"

    def index(self, request, company_name=None, extra_context=None):
        # Get the user's company name from the URL parameter if not provided
        if company_name is None and 'company_name' in request.resolver_match.kwargs:
            company_name = request.resolver_match.kwargs['company_name']

        # Dynamically set the site header and title based on the company_name
        if company_name:
            self.site_header = f"{company_name.upper()} Squad Spot Panel"
            self.site_title = f"{company_name.upper()} Admin"

        return super().index(request, extra_context)

company_admin_site = CompanyAdminSite(name = "company_admin")
