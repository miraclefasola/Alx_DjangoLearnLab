from django.shortcuts import render
from .forms import Register, PostForm, CommentForm
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
from .models import Post, Comment
from django.core.exceptions import ValidationError, PermissionDenied
from django.views.generic.edit import FormMixin
from taggit.models import Tag
from django.shortcuts import get_object_or_404


class RegisterView(CreateView):
    form_class = Register
    template_name = "blog/register.html"
    model = User
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
    ordering = ["-published_date"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag_list"] = Tag.objects.all()
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create.html"
    success_url = reverse_lazy("posts")
    redirect_field_name = "next"

    def form_valid(self, form):
        form.instance.author = self.request.user  # auto-assign logged-in user
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy("posts")
    template_name = "blog/post_create.html"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        raise PermissionDenied("Only authors can edit their own post")


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("posts")
    template_name = "blog/post_confirm_delete.html"

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def handle_no_permission(self):
        raise PermissionDenied("Only authors can delete their own post")

    # def delete(self, request, *args, **kwargs):
    #     post = self.get_object()
    #     if post.author == request.user:
    #         return super().delete(request, *args, **kwargs)
    #     raise PermissionDenied("only post author can delete post")


class PostDetailView(FormMixin, DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["comments"] = self.object.post_comments.all().order_by(
            "-created_at"
        )  # Getting the comments related to the particular post bu using the self.object to reference the post and using the related name defined in models.py to reference the relationship
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("User must be logged in before dropping a comment")
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.get_object()
        form.save()
        return super().form_valid(form)


# class CommentList(ListView):
#     model= Comment
#     template_name= 'blog/post_detail.html'
#     context_object_name = "comments"
#     ordering = ["-created_at"]

#     def get_queryset(self):
#        post_id= self.kwargs.get('pk')
#        return Comment.objects.filter(post_id=post_id).order_by('-created_at')
# class CommentCreateView(LoginRequiredMixin,CreateView):
#     model= Comment
#     form_class= CommentForm
#     success_url=reverse_lazy('list_comment')
#     template_name='blog/post_detail.html'
#     redirect_field_name= 'next'

#     def form_valid(self, form):
#         form.instance.author= self.request.user
#         form.instance.post_id= self.kwargs['pk']
#         return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/post_detail.html"
    redirect_field_name = "next"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def handle_no_permission(self):
        raise PermissionDenied("only authors of comment can edit")


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/post_detail.html"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def handle_no_permission(self):
        raise PermissionDenied("Only authors of this comment can delete it")


class TagView(ListView):
    model = Post
    template_name = "blog/post_by_tag.html"
    context_object_name = "posts"

    def get_queryset(self):
        slug = self.kwargs.get("tag_slug")
        self.tag = get_object_or_404(Tag, slug=slug)
        queryset = Post.objects.filter(tags__slug=slug).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context


from django.db.models import Q


class PostSerachList(ListView):
    model = Post
    template_name = "blog/search.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        if query:
            q = (
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(tags__name__icontains=query)
            )

            # if query.isdigit():
            #     q |= Q(published_date__year__exact=int(query))
            return Post.objects.filter(q).distinct()
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context
