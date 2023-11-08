from rest_framework import serializers, status
from apps.user import models as user_models


class LoginSerializer(serializers.Serializer):
    """
    Login serializer
    """

    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = user_models.User
        exclude = ("password",)

    def validate_email(self, email):
        """will check email"""
        email = email.lower()
        return email
