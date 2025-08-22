from django.shortcuts import render
from .forms import Register
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class RegisterView(CreateView):
    form_class = Register
    template_name = "blog/register.html"
    model = "User"
    success_url = reverse_lazy("login")


class ProfileView(TemplateView):
    template_name = "blog/profile.html"


class PostListView(ListView):
    template_name = "blog/posts.html"

#view for profile update
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "blog/profile_update.html"
    fields = ["username", "email"]
    success_url = reverse_lazy("profile")
#overriding get_object here because ususally and update views expect a pk but we want it to reture the logged in user    
    def get_object(self, queryset=None):
        return self.request.user
