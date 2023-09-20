# myapp/middleware.py

from django.shortcuts import render
from apps.company.models import Company
from common.constants import (
    SQUAD_SPOT_ADMIN_ROUTE_NAME,
    COMPANY_ADMIN_ROUTE_NAME,
    ApplicationMessages,
)


class CustomLoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Your custom logic to determine the redirect URL here
        host = request.get_host()
        parts = host.split(".")
        if len(parts) == 2:
            company = parts[0]
            if company:
                if f"{SQUAD_SPOT_ADMIN_ROUTE_NAME}" in request.path:
                    return render(
                        request,
                        "unauthorized_access.html",
                        {"error_message": ApplicationMessages.COMPANY_INVALID},
                        status=401,
                    )

            # Validate company
            valid_company = Company.objects.filter(
                name__iexact=company.replace("-", " ").lower()
            ).exists()
            if not valid_company:
                return render(request, "invalid_route.html", status=404)

        else:
            company = None
            if (
                f"{SQUAD_SPOT_ADMIN_ROUTE_NAME}" not in request.path
                and f"{COMPANY_ADMIN_ROUTE_NAME}" in request.path
            ):
                return render(
                    request,
                    "unauthorized_access.html",
                    {"error_message": ApplicationMessages.COMPANY_INVALID},
                    status=401,
                )

        if request.user.is_authenticated:
            if (
                company
                and request.user.company.name.replace(" ", "-").lower()
                != company
            ):
                return render(request, "invalid_route.html", status=404)
        response = self.get_response(request)
        return response
