from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class SuperAdminBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user  # Return the user object

        return None
