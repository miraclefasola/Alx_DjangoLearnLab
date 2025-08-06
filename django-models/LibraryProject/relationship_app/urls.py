from django.contrib import admin
from django.urls import path, include
from . import views
from .views import list_books, LibraryDetailView

urlpatterns = [
    
    path('list_books/', views.list_books, name='book_list'),
    path('LibraryDetailView/', views.LibraryDetailView.as_view(), name='Library')
]
