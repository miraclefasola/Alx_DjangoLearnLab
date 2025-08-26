from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.views import LogoutView, LoginView
from accounts.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("api/login", obtain_auth_token, name="api_token_auth"),
    path("login/", LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", Register.as_view(), name="register"),
    path("profile/",ProfileView.as_view() ,name='profile'),
    path('pofile_update/<int:pk>/', ProfileUpdate.as_view(), name='profile_update'),
    path(
        "reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change_done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path("api/register/", RegisterAPIView.as_view(), name="api-register")
]
