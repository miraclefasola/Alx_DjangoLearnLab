from django.shortcuts import render
from .serializers import BookSerializer
from rest_framework.generics import ListAPIView
from .models import Book

class BookList(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
