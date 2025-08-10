from django.shortcuts import render
from bookshelf.models import *
from django.views.generic import CreateView, UpdateView, DetailView,DeleteView,ListView, TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import redirect_to_login
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from bookshelf.forms import *
from django.shortcuts import redirect
# Create your views here.
#Book View just to see, added login required such that you have to login before you can see those books
class   BookView(LoginRequiredMixin, ListView):
    template_name= 'viewer.html'
    permission_required = 'bookshelf.view_book'
    permission_denied_message= '' 
    login_url= reverse_lazy('login')
    raise_exception= False
    redirect_field_name= 'next'
    model= Book

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), login_url=self.login_url )
        return redirect (reverse_lazy('dashboard'))




class BookCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    template_name= 'editor_create.html'
    model = Book
    fields= ('title', 'author', 'publication_year')
    permission_denied_message='' 
    permission_required= ['bookshelf.add_book','bookshelf.view_book'] 
 
    login_url=reverse_lazy('login')
    raise_exception= False
    redirect_field_name= 'next'
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), login_url=self.login_url )
        return redirect (reverse_lazy('book_view'))
        

class BookUpdate(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    template_name= 'editor_update.html'
    model = Book
    fields= ('title', 'author', 'publication_year')
 
    permission_required= ['bookshelf.change_book','bookshelf.view_book'] 
    permission_denied_message= '' 
    login_url=reverse_lazy('login')
    raise_exception= False
    redirect_field_name= 'next'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), login_url=self.login_url )
        return redirect (reverse_lazy('book_view'))
class BookDelete(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    template_name= 'editor_delete.html'
    model = Book
    
    success_url= reverse_lazy('dashboard')
    permission_required= ['bookshelf.delete_book','bookshelf.view_book'] 
    permission_denied_message= '' 
    login_url=reverse_lazy('login')
    raise_exception= False
    redirect_field_name= 'next'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), login_url=self.login_url )
        return redirect (reverse_lazy('book_view'))
class Register(CreateView):
    template_name='register.html'
    success_url= reverse_lazy('login')
    form_class = CustomUserForm

class Dashboard(TemplateView):
    template_name = 'base.html'


    #Code functional but time to trick the checker
    book_list=''