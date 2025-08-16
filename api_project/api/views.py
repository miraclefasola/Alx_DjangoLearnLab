from django.shortcuts import render
from .serializers import BookSerializer
from rest_framework import generics, viewsets
from .models import Book
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class BookList(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset= Book.objects.all()
    lookup_field= 'pk'
    #permission_classes= [IsAuthenticatedOrReadOnly]