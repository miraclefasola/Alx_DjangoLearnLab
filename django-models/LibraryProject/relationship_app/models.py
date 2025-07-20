from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=300)
class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.ForeignKey(Author, on_delete= models.SET_NULL, null=True, blank=True)
class Library(models.Model):
    name = models.CharField(max_length=300)
    books= models.ManyToManyField(Book)
class Librarian(models.Model):
    name = models.CharField(max_length=300)
    library = models.OneToOneField(Library, on_delete=models.SET_NULL, null=True, blank= True)