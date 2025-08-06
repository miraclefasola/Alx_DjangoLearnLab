from django.contrib import admin
from django.urls import path, include
import relationship_app.views as views 
from .views import list_books, LibraryDetailView, UserRegisterView, AdminView,MemberView,LibrarianView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView


# urlpatterns = [
    
#     path('list_books/', list_books, name='book_list'),
#     path('LibraryDetailView/', LibraryDetailView.as_view(), name='Library'),
#     path('register/', UserRegisterView.as_view(), name= "register"),
#     path('login/', auth_views.LoginView.as_view(template_name = 'relationship_app/login.html'), name='login'),
#     path('logout/', auth_views.LogoutView.as_view(template_name = 'relationship_app/logout.html'), name ='logout')
# ]




urlpatterns = [
    path('list_books/', views.list_books, name='book_list'),
    path('LibraryDetailView/', views.LibraryDetailView.as_view(), name='Library'),
    path('register/', views.UserRegisterView.as_view(), name="register"),  # 👈 views.register pattern
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),  # 👈 LoginView inline
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('admin-view/', AdminView.as_view(), name='admin_view'),
    path('librarian-view/', LibrarianView.as_view(), name='librarian_view'),
    path('member-view/', MemberView.as_view(), name='member_view'),
]
