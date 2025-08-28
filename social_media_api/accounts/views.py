from django.shortcuts import render
from accounts.forms import *
from django.views.generic import CreateView, TemplateView, ListView, UpdateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

User = get_user_model()


class Register(CreateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "accounts/register.html"


class ProfileView(ListView):
    model = User
    template_name = "accounts/profile.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        followers_count = self.request.user.followers.count()
        context["followers"] = followers_count
        return context


class ProfileUpdate(UpdateView):
    model = User
    fields = ["first_name", "last_name", "email", "bio", "profile_picture"]
    template_name = "accounts/profile_update.html"
    success_url = reverse_lazy("profile")
    redirect_field_name = "next"

    def get_object(self, queryset=None):
        return self.request.user


from rest_framework.generics import CreateAPIView
from accounts.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated


class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user)
        data = serializer.data
        data["token"] = token.key

        return Response(data, status=201)


from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import SAFE_METHODS
from django.core.exceptions import PermissionDenied
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification

# List all users
class UsersView(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]

    #    @action(detail=True, methods=['POST'])  commenting it out because actin only works for routers and task is asking us to define custom urls
    def follow_user(self, request, user_id=None):
        user_to_follow = get_object_or_404(User, id=user_id)
        current_user = self.request.user
        if user_to_follow == self.request.user:
            return Response({"detail": "you cannot follow yourself"})
        elif current_user.following.filter(pk=user_to_follow.pk).exists():
            return Response({"detail": "already following this user"})
        else:
            current_user.following.add(user_to_follow)
            Notification.objects.create(
                recipient=user_to_follow,
                actor=request.user,
                verb="Followed",
                target_content_type=ContentType.objects.get_for_model(user_to_follow),
                target_object_id=user_to_follow.id,
            )
            return Response(
                {"detail": f"you've just followed {user_to_follow.username}"}
            )

    #    @action(detail=True, methods=["POST"])
    def unfollow_user(self, request, user_id=None):
        user_to_unfollow = get_object_or_404(User, id=user_id)
        current_user = self.request.user
        if not current_user.following.filter(pk=user_to_unfollow.pk).exists():
            return Response({"detail": "Can only unfollow users you are follwing"})
        elif user_to_unfollow == current_user:
            return Response({"detail": "You cannot unfollow yourself"})
        else:
            current_user.following.remove(user_to_unfollow)
            return Response(
                {"detail": f"you've just unfollowed {user_to_unfollow.username}"}
            )


# generics.GenericAPIView", "permissions.IsAuthenticated", "CustomUser.objects.all()"]
