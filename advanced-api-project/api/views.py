from django.shortcuts import render
from .models import Book, Author
from rest_framework.viewsets import ModelViewSet
from .serializers import BookSerializer, AuthorSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import PageNumberPagination
from .filters import BookCustomFilter
from rest_framework.authentication import TokenAuthentication

class BookListView(generics.ListAPIView):
    queryset= Book.objects.all()
    serializer_class=BookSerializer
    permission_classes= [IsAuthenticatedOrReadOnly]
    filter_backends= [BookCustomFilter,SearchFilter,OrderingFilter]
    search_fields= ('author', 'title')
    ordering_fields= ['title']
    pagination_class= PageNumberPagination
    pagination_class.size= 2
    authentication_classes= [TokenAuthentication]

class BookCreateView(generics.CreateAPIView):
    queryset= Book.objects.all()
    serializer_class= BookSerializer
    permission_classes= [IsAdminUser]
    authentication_classes= [TokenAuthentication]
    

class BookDetailView(generics.RetrieveAPIView):
    queryset= Book.objects.all()
    serializer_class=BookSerializer
    lookup_field= 'pk'
    permission_classes= [IsAuthenticated]
    authentication_classes= [TokenAuthentication]

class BookDeleteView(generics.DestroyAPIView):
    queryset= Book.objects.all()
    serializer_class=BookSerializer
    lookup_field= 'pk'
    permission_classes= [IsAdminUser]
    authentication_classes= [TokenAuthentication]

class BookUpdateView(generics.UpdateAPIView):
    queryset= Book.objects.all()
    serializer_class=BookSerializer
    lookup_field= 'pk'
    permission_classes= [IsAuthenticated]
    authentication_classes= [TokenAuthentication]