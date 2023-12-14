from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from apps.invitation.models import Invitation
from common.constants import Invite_type, ApplicationMessages
from common.helpers import module_perm
from .models import User
from apps.company.models import Company
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .forms import AcceptInvitationForm
from django.contrib.auth.hashers import make_password
from squad_spot.settings import HOST_URL, COMPANY_ADMIN_URL
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework import views, status, viewsets, permissions, filters
from apps.user import serializers
from apps.user import models as user_models
from common.constants import ApplicationMessages
from django.contrib.auth import authenticate
from common import auth as user_auth
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.views import TokenObtainPairView
from common.constants import (
    COMPANY_ADMIN_ROUTE_NAME,
    SQUAD_SPOT_ADMIN_ROUTE_NAME,
)
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.views import TokenObtainPairView


class AcceptInvitationView(FormView):
    form_class = AcceptInvitationForm

    def get(self, request, uuid):
        valid_flag = True
        obj = Invitation.objects.filter(id=uuid)
        if obj:
            obj = obj.first()
        else:
            obj = Company.objects.filter(id=uuid).first()

        if (
            (
                obj.invite_type == Invite_type.INTERNAL
                or obj.invite_type == Invite_type.COMPANY
            )
            and (not obj.is_active)
        ) or (
            obj.invite_type == Invite_type.COMPANY_OWNER and (obj.is_active)
        ):
            valid_flag = False
            self.template_name = "unauthorized_access.html"
            return render(
                request,
                "unauthorized_access.html",
                {"error_message": ApplicationMessages.INVITATION_INVALID},
                status=401,
            )
        return render(
            request,
            "user/accept_invitation.html",
            {
                "form": self.form_class,
                "invitation": obj,
                "flag": valid_flag,
            },
            status=200,
        )

    def post(self, request, uuid):
        # Retrieve the invitation associated with the UUID
        company_name = ""
        obj = Invitation.objects.filter(id=uuid)
        if obj:
            obj = obj.first()
        else:
            obj = Company.objects.filter(id=uuid).first()

        if (
            obj.invite_type in [Invite_type.INTERNAL, Invite_type.COMPANY]
            and (not obj.is_active)
        ) or (
            obj.invite_type == Invite_type.COMPANY_OWNER and (obj.is_active)
        ):
            return render(
                request,
                "unauthorized_access.html",
                {"error_message": ApplicationMessages.INVITATION_INVALID},
                status=401,
            )

        # Create a new user with the provided email and password
        password = request.POST.get("password")
        encrpt_pswd = make_password(password)
        if obj.invite_type == Invite_type.COMPANY_OWNER:
            User.objects.create(
                full_name=obj.owner_name,
                email=obj.owner_email,
                company=obj,
                password=encrpt_pswd,
                is_staff=True,
                is_company_owner=True,
            )
            obj.is_active = True
            obj.invite_link = ""
            obj.save()
            company_name = obj.name.replace(" ", "-").lower()
        else:
            if obj.invite_type == Invite_type.COMPANY:
                com_obj = Company.objects.get(id=obj.company_id)
                company_name = com_obj.name.replace(" ", "-").lower()
            User.objects.create(
                full_name=obj.fullname,
                email=obj.email,
                role=obj.role,
                company=com_obj
                if obj.invite_type == Invite_type.COMPANY
                else None,
                password=encrpt_pswd,
                is_staff=True,
                is_company_owner=False,
            )
            obj.is_active = False
            obj.save()
        redirect_url = reverse("user:password_set_success")
        if company_name:
            redirect_url += f"?company_name={company_name}"

        return HttpResponseRedirect(redirect_url)  # Redirect to a success page


class PasswordSetSuccessView(TemplateView):
    template_name = "user/set_password_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company_name = self.request.GET.get("company_name")
        if company_name is not None:
            login_url = f"http://{company_name}.{COMPANY_ADMIN_URL}"
            # login_url = f"{HOST_URL}/{COMPANY_ADMIN_ROUTE_NAME}/"
        else:
            login_url = f"{HOST_URL}/ss-admin/"
            # login_url = f"{HOST_URL}/{SQUAD_SPOT_ADMIN_ROUTE_NAME}/"
        context["login_url"] = login_url
        return context


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Call the save method to get the response
            response = serializer.validated_data

            user_data = response

            # Customize the success response format
            data = {
                "status": status.HTTP_200_OK,
                "message": ApplicationMessages.LOGIN_SUCCESSFULLY,
                "error": False,
                "data": user_data,
            }

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle the exception for invalid credentials
            error_data = {
                "status": status.HTTP_401_UNAUTHORIZED,
                "message": ApplicationMessages.INVALID_PASSWORD,
                "error": True,
                "data": {},
            }
            return Response(error_data, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(views.APIView):
    """
    Logout  api view
    """

    permission_classes = [permissions.IsAuthenticated]
    user_model = user_models.User

    def delete(self, request, *args, **kwargs):
        """
        Delete session
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            user = self.user_model.objects.get(id=request.user.id)
            qs = OutstandingToken.objects.filter(user=user)
            if qs.exists():
                qs.delete()
                return Response(
                    {
                        "status": status.HTTP_200_OK,
                        "message": ApplicationMessages.LOGOUT_SUCCESSFULLY,
                        "error": False,
                        "data": {},
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                # Handle the case where qs is empty
                return Response(
                    {
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": ApplicationMessages.LOGOUT_FAILED_NO_TOKEN,
                        "error": True,
                        "data": {},
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except self.user_model.DoesNotExist:
            return Response(
                {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": ApplicationMessages.LOGOUT_FAILED,
                    "error": True,
                    "data": {},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserListSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]  # Add DjangoFilterBackend
    filterset_fields = [
        "id",
        "email",
        "role",
    ]  # Define the fields available for filtering

    # Define fields available for filtering and ordering
    ordering_fields = [
        "full_name",
        "email",
    ]
    search_fields = [
        "id",
        "full_name",
    ]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(company_id=user.company_id)

    def list(self, request):
        req_user = request.user
        if req_user.is_company_owner or module_perm("user", req_user, "view"):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(
                {
                    "status": ApplicationMessages.SUCCESS,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": "error",
                    "message": ApplicationMessages.PERMISSION_DENIED,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def retrieve(self, request, pk=None):
        instance = self.get_object()

        req_user = request.user
        if req_user.is_company_owner or module_perm("user", req_user, "view"):
            serializer = self.get_serializer(instance)
            return Response(
                {
                    "status": ApplicationMessages.SUCCESS,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": "error",
                    "message": ApplicationMessages.PERMISSION_DENIED,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def update(self, request, pk=None):
        instance = self.get_object()

        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "user", req_user, "update"
        ):
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {
                    "status": ApplicationMessages.SUCCESS,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": "error",
                    "message": ApplicationMessages.PERMISSION_DENIED,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

    def partial_update(self, request, pk=None):
        instance = self.get_object()

        req_user = request.user
        if req_user.is_company_owner or module_perm(
            "user", req_user, "update"
        ):
            serializer = self.get_serializer(
                instance, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {
                    "status": ApplicationMessages.SUCCESS,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": "error",
                    "message": ApplicationMessages.PERMISSION_DENIED,
                },
                status=status.HTTP_403_FORBIDDEN,
            )
