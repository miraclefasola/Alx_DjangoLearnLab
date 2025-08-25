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
    path("post/new/", PostCreate.as_view(), name="post_create"),
    path("post/<int:pk>/update/", UpdatePost.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", DeletePost.as_view(), name="post_delete"),
    path("post/<int:pk>/detail/", PostDetailView.as_view(), name="post_detail"),
    # path("posts/<int:post_id>/comments/", CommentList.as_view(), name="list_comment"),
    # path(
    #     "post/<int:pk>/comments/new/",
    #     CommentCreateView.as_view(),
    #     name="create_comment",
    # ),
    path(
        "comment/<int:pk>/update/",
        CommentUpdateView.as_view(),
        name="edit_comment",
    ),
    path(
        "comment/<int:pk>/delete/",
        CommentDeleteView.as_view(),
        name="delete_comment",
    ),
    path("posts/tag/<slug:tag_slug>/", PostByTagListViewTagView.as_view(), name="tag_view"),
    path("posts/search/", PostSerachList.as_view(), name="search_list"),
]
