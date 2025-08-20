import django_filters
from rest_framework.filters import BaseFilterBackend
from .models import Book

class BookCustomFilter(django_filters.FilterSet):
    class Meta:
        model= Book
        fields= {'title':['iexact', 'icontains'],
                  "publication_year":['exact', 'range','lt','gt'],
                  "author__name":['iexact', 'icontains']}