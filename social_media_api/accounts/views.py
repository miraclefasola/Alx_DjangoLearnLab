from django.shortcuts import render
from accounts.forms import *
from django.views.generic import CreateView, TemplateView, ListView,UpdateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

User = get_user_model()


class Register(CreateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "accounts/register.html"

class ProfileView(ListView):
    model= User
    template_name='accounts/profile.html'
    context_object_name='users'

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        followers_count=self.request.user.followers.count()
        context['followers']= followers_count
        return context

class ProfileUpdate(UpdateView):
    model= User
    fields=['first_name', 'last_name', 'email', 'bio', 'profile_picture']
    template_name = "accounts/profile_update.html"
    success_url = reverse_lazy("profile")
    redirect_field_name = "next"

    def get_object(self, queryset=None):
        return self.request.user

