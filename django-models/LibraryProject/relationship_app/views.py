from django.shortcuts import render
from django.views.generic import ListView
from .models import Library
from django.views.generic.detail import DetailView


# Create your views here.
def list_books(request):
    return render(request, 'relationship_app/list_books.html', 'Book.objects.all()')

class LibraryDetailView(ListView):
    template_name= 'relationship_app/library_detail.html'
    model = Library
    context_object_name = 'book'
    