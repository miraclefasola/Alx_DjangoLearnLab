import django_filters
from rest_framework.filters import BaseFilterBackend
from .models import Book

class BookCustomFilter(BaseFilterBackend):
    class Meta:
        model= Book
        fields= {'title':['iexact', 'icontains'],
                  "publication_year":['exact', 'range','lt','gt']}