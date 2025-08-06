from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Library


# Create your views here.
def book(request):
    return render(request, 'list_books.html')

class LibararyView(ListView):
    template_name= 'library_detail.html'
    model = Library
    context_object_name = 'book'
    