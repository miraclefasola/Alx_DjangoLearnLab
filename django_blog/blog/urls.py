from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from blog.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login/", LoginView.as_view(template_name="blog/login.html"), name="login"),
    path(
        "logout/", LogoutView.as_view(template_name="blog/logout.html"), name="logout"
    ),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="home"),
    path("posts/", PostListView.as_view(), name="posts"),
    path("profile_update", ProfileUpdateView.as_view(), name="profile_update"),
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
    path("posts/new/", PostCreate.as_view(), name="create_post"),
    path("posts/edit/<int:pk>/", UpdatePost.as_view(), name="post_update"),
    path("posts/delete/<int:pk>/", DeletePost.as_view(), name="post_delete"),
    path('posts/detail/<int:pk>/', PostDetailView.as_view(), name='post_detail')
]
