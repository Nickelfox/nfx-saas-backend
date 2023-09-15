# myapp/middleware.py

from django.conf import settings


class CustomLoginRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Your custom logic to determine the redirect URL here
        if request.user.is_authenticated:
            if request.user.company is not None:
                settings.LOGIN_REDIRECT_URL = '/company-admin/'  # Set the URL for company admin
            else:
                settings.LOGIN_REDIRECT_URL = '/ss-admin/'  # Set the URL for default admin

        response = self.get_response(request)
        return response
