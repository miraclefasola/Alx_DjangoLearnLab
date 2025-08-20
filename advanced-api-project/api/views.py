from django.shortcuts import render
from .models import Book, Author
from rest_framework.viewsets import ModelViewSet
from .serializers import BookSerializer, AuthorSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from .filters import BookCustomFilter
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend
class BookListView(generics.ListAPIView):
    queryset= Book.objects.all()
    serializer_class=BookSerializer
    permission_classes= [IsAuthenticated]
    filter_backends= [filters.OrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    filterset_class= BookCustomFilter
    search_fields= ('author', 'title', 'publication_year')
    ordering_fields= ['title']
    pagination_class= PageNumberPagination
    pagination_class.page_size= 2
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
from django_filters import rest_framework