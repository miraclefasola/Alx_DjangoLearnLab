from rest_framework import serializers
from .models import Book, Author
from datetime import datetime,date

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields= '__all__'


    def validate_publication_year(self, value):
        if value > date.today().year:
            raise serializers.ValidationError("Publication Year cannot be in the future")
        return value
    

class AuthorSerializer(serializers.ModelSerializer):
    books= BookSerializer(read_only=True, many=True, source='book_author')
    class Meta:
        model= Author
        fields= ["name", "books"]

