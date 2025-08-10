from django.shortcuts import render
from django.views.generic import ListView
from .models import Library
from django.views.generic.detail import DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import *


# Create your views here.
def list_books(request):
    return render(request, 'relationship_app/list_books.html', 'Book.objects.all()')

class LibraryDetailView(ListView):
    template_name= 'relationship_app/library_detail.html'
    model = Library
    context_object_name = 'book'

class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')
  
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
class RoleRequiredMixin(LoginRequiredMixin):
    required_roles = []

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            
            return redirect_to_login(request.get_full_path())

        user_profile = getattr(user, 'userprofile', None)
        if user_profile and user_profile.role in self.required_roles:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied("You do not have permission to access this page.")

class AdminView(RoleRequiredMixin, TemplateView):
    template_name = 'relationship_app/admin_view.html'
    required_roles = ['Admin']

class LibrarianView(RoleRequiredMixin, TemplateView):
    template_name = 'relationship_app/librarian_view.html'
    required_roles = ['Librarian']

class MemberView(RoleRequiredMixin, TemplateView):
    template_name = 'relationship_app/member_view.html'
    required_roles = ['Member']

class BookAddView(PermissionRequiredMixin, RoleRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'published_date']
    template_name = 'relationship_app/book_form.html'
    permission_required = 'Book.add_book'
    required_roles = ['Admin', 'Librarian']
    success_url = reverse_lazy('book_list') 

class ChangeBookView(UpdateView, RoleRequiredMixin, PermissionRequiredMixin):
    permission_required = 'Book.change_book'
    required_roles = ['Admin', 'Librarian']
    template_name= ''
    model = Book
    fields = ['title', 'author', 'published_date']
    success_url = reverse_lazy('book_list') 

class DeleteBookView(DeleteView, RoleRequiredMixin, PermissionRequiredMixin):
    permission_required = 'Book.delete_book'
    required_roles = ['Admin', 'Librarian']
    template_name= ''
    model = Book
    fields = ['title', 'author', 'published_date']
    success_url = reverse_lazy('book_list') 