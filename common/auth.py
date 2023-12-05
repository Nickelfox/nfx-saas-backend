# from common import constants
# from apps.user import models as user_models
# from django.contrib.auth import get_user_model
# from rest_framework import status
# from rest_framework.exceptions import ValidationError
# from rest_framework_simplejwt.token_blacklist.management.commands import (
#     flushexpiredtokens,
# )
# from rest_framework_simplejwt.token_blacklist.models import (
#     BlacklistedToken,
#     OutstandingToken,
# )
# from common.constants import ApplicationMessages
# from django.utils import timezone
# from django.contrib.auth.hashers import check_password
# from apps.role import models as role_models

# Users = get_user_model()


# class AuthManager:
#     """This class deals with all type of users
#     for Login and SignUp

#     login function will return the token once user get Authenticated and they are static as well
#     """

#     model = Users

#     @staticmethod
#     def login_user_email(user_instance, password, data):
#         """User login via email and password and return token"""
#         if not user_instance.is_active:
#             raise ValidationError(
#                 constants.ApplicationMessages.USER_NOT_ACTIVE,
#                 status.HTTP_401_UNAUTHORIZED,
#             )
#         if check_password(password, user_instance.password):
#             user_instance.last_login = timezone.now()
#             token = user_instance.tokens()
#             user_instance.save()
#             # raise Exception(user_instance.id)
#             response = {
#                 "message": ApplicationMessages.SUCCESS,
#                 "tokens": token,
#                 "email": user_instance.email,
#                 "id": user_instance.id,
#                 "full_name": user_instance.full_name,
#             }
#             if user_instance.role:
#                 response["permissions"] = user_instance.role.role_permissions

#             return response
#         else:
#             raise ValidationError(ApplicationMessages.INVALID_PASSWORD)


# def logout_all_session(user):
#     """clear all the sessions of user
#     Here also delete the all user session info model data"""
#     OutstandingToken.objects.filter(user=user).delete()
