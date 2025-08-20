from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

# router= DefaultRouter()
# router.register(r"books", BookView, basename='book_view')
# router.register(r'authors', AuthorView, basename='author_view')
urlpatterns = [
    path("books/", BookListView.as_view(), name="book_list"),
    path("books/create/", BookCreateView.as_view(), name="book_create"),
    path("books/detail/<int:ok>/", BookDetailView.as_view(), name="detail_view"),
    path("books/update/<int:pk>/", BookUpdateView.as_view(), name="book_update"),
    path("books/delete/<int:pk>/", BookDeleteView.as_view(), name="book_delete"),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
]
