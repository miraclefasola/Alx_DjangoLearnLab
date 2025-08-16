from django.shortcuts import render
from .serializers import BookSerializer
from rest_framework import generics
from .models import Book

class BookList(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
