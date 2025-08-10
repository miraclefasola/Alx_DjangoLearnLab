from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from bookshelf.views import *

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name= 'login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', Register.as_view(), name= 'register'),
    path('dashboard/', Dashboard.as_view(), name= 'dashboard'),
    path('bookview/', BookView.as_view(), name='book_view'),
    path('bookcreate/', BookCreate.as_view(), name='create_book'),
    path('editbook/', BookUpdate.as_view(), name='edit_book'),
    path('bookdelete/', BookDelete.as_view(), name= 'delete_book')
]
