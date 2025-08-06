from django.shortcuts import render
from django.views.generic import ListView
from .models import Library
from django.views.generic.detail import DetailView


# Create your views here.
def book(request):
    return render(request, 'relationship_app/list_books.html', 'Book.objects.all()')

class LibararyView(ListView):
    template_name= 'relationship_app/library_detail.html'
    model = Library
    context_object_name = 'book'
    