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
from rest_framework.permissions import AllowAny


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
