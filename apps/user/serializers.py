from rest_framework import serializers, status
from apps.user import models as user_models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from common.constants import ApplicationMessages


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = (
            "id",
            "full_name",
            "email",
            "role",
            "phone_number",
            "designation",
        )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # You can add custom claims to the token if needed
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user or self.context["request"].user

        if user.is_authenticated:
            refresh = self.get_token(user)
            access = refresh.access_token

            user_serializer = UserListSerializer(user)
            data = {
                "user": user_serializer.data,
            }
            data["user"]["token"] = {
                "refresh": str(refresh),
                "access": str(access),
            }
            data["user"]["role_permissions"] = user.role.role_permissions
        else:
            data = {}
        # Remove top-level refresh and access tokens
        data.pop("refresh", None)
        data.pop("access", None)
        return data
