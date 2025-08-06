from django.contrib import admin
from django.urls import path, include

from .views import list_books, LibraryDetailView, UserRegisterView
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('list_books/', list_books, name='book_list'),
    path('LibraryDetailView/', LibraryDetailView.as_view(), name='Library'),
    path('register/', UserRegisterView.as_view(), name= "register"),
    path('login/', auth_views.LoginView.as_view(template_name = 'relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'relationship_app/logout.html'), name ='logout')
]
