"""
URL configuration for squad_spot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from custom_admin import (
    ss_admin_site,
    company_admin_site,
    restapi_ss_admin_site,
)

from django_api_admin.sites import site as rest_ss_site
from common.constants import (
    SQUAD_SPOT_ADMIN_ROUTE_NAME,
    COMPANY_ADMIN_ROUTE_NAME,
)

urlpatterns = [
    path(f"{COMPANY_ADMIN_ROUTE_NAME}/", company_admin_site.urls),
    path("user/", include("apps.user.urls")),
    path(f"{SQUAD_SPOT_ADMIN_ROUTE_NAME}/", ss_admin_site.urls),
    path("rest-ss-admin/", rest_ss_site.urls),
    path("restapi-ss-admin/", restapi_ss_admin_site.urls),
]
