from django.shortcuts import render
from .models import Book, Author
from rest_framework.viewsets import ModelViewSet
from .serializers import BookSerializer, AuthorSerializer

class BookView(ModelViewSet):
    queryset= Book.objects.all()
    serializer_class=BookSerializer

class AuthorView(ModelViewSet):
    queryset= Author.objects.all()
    serializer_class= AuthorSerializer
