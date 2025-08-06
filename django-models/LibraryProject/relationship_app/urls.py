from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    
    path('booklist/', views.book, name='book_list'),
    path('libraryview/', views.LibararyView.as_view(), name='Library')
]
