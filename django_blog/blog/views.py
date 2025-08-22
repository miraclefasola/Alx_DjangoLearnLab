from django.shortcuts import render
from .forms import Register, PostForm
from django.views.generic.edit import CreateView
from django.views.generic import (
    TemplateView,
    ListView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Post
from django.core.exceptions import ValidationError, PermissionDenied


class RegisterView(CreateView):
    form_class = Register
    template_name = "blog/register.html"
    model = "User"
    success_url = reverse_lazy("login")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "blog/profile.html"
    redirect_field_name = "next"


# view for profile update
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "blog/profile_update.html"
    fields = ["username", "email"]
    success_url = reverse_lazy("profile")
    redirect_field_name = "next"

    # overriding get_object here because ususally and update views expect a pk but we want it to reture the logged in user
    def get_object(self, queryset=None):
        return self.request.user


class PostListView(ListView):
    template_name = "blog/post_list.html"
    model = Post
    context_object_name = "posts"
    ordering = ["-created_at"]
    redirect_field_name = "next"


class PostCreate(LoginRequiredMixin,CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"
    success_url = reverse_lazy("posts")
    redirect_field_name = "next"
    

    def form_valid(self, form):
        form.instance.author = self.request.user  # auto-assign logged-in user
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("posts")
    template_name = "blog/post_create.html"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    def handle_no_permission(self):
        raise PermissionDenied("Only authors can edit their own post")



class DeletePost(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = reverse_lazy("posts")
    template_name = "blog/post_confirm_delete.html"

    def test_func(self):
        post= self.get_object()
        return self.request.user == post.author
    
    def handle_no_permission(self):
        raise PermissionDenied('Only authors can delete their own post')

    # def delete(self, request, *args, **kwargs):
    #     post = self.get_object()
    #     if post.author == request.user:
    #         return super().delete(request, *args, **kwargs)
    #     raise PermissionDenied("only post author can delete post")
    
class PostDetailView( DetailView):
    model= Post
    redirect_field_name='next'
    template_name='blog/post_detail.html'
#
["from django.contrib.auth.decorators import login_required"]