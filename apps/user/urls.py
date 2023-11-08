from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path(
        "invitation/accept/<uuid:uuid>/",
        views.AcceptInvitationView.as_view(),
        name="accept_invitation",
    ),
    path(
        "password_set_success/",
        views.PasswordSetSuccessView.as_view(),
        name="password_set_success",
    ),
    path(
        "login/",
        views.UserLoginAPIView.as_view(),
        name="post-admin-login",
    ),
    path("logout/", views.LogoutAPIView.as_view(), name="admin-logout"),
]
