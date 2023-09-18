# myapp/middleware.py

from django.conf import settings
from django.shortcuts import render, redirect
from apps.company.models import Company


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
                if 'ss-admin' in request.path:
                    # return HttpResponseForbidden("Unauthorized")
                    return render(request, 'unauthorized_access.html')

            # Validate company
            valid_company = Company.objects.filter(
                name__iexact=company.replace("-", " ").lower()).exists()
            if not valid_company:
                return render(request, 'invalid_route.html')

        else:
            company = None
            if 'ss-admin' not in request.path and 'admin' in request.path:
                return render(request, 'unauthorized_access.html')

        if request.user.is_authenticated:
            if company and request.user.company.name.replace(" ", "-").lower() != company:
                return render(request, 'invalid_route.html')
        response = self.get_response(request)
        return response
