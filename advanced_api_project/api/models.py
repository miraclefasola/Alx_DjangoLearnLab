from django.db import models

class Author(models.Model):
    name= models.CharField(max_length=500)

    def __str__(self):
        return self.name

class Book(models.Model):
    title= models.CharField(max_length=300)
    publication_year= models.IntegerField()
    author= models.ForeignKey(Author, on_delete=models.CASCADE, related_name='book-author')

    def __str__(self):
        return self.title