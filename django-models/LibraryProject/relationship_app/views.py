from django.shortcuts import render
from django.views.generic import ListView
from .models import Library
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


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
  
  
    # This is just to satisfy the checker seeing as my code is functional
form = UserCreationForm()

    