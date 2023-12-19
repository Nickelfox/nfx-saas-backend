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
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user or self.context["request"].user
        user_serializer = UserListSerializer(user)
        response = {
            "user": user_serializer.data,
        }
        response["user"]["token"] = data
        response["user"]["role_permissions"] = user.role.role_permissions
        return response
