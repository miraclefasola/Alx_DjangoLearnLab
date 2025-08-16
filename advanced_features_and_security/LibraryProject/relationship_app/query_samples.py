import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from .models import *

# book by author
# def books_by_author(author_name):
#     try:
#         author = Author.objects.get(name = author_name)
#         books = Book.objects.filter(author__name = author_name)


#         if books.exists():
#             for book in books:
#              print (f"{book.title} by {book.author.name}")
#         else:
#             print (f"{author_name} has no book in our database")
#     except Author.DoesNotExist:
#         print (f"{author_name} is not in our database")
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        for book in books:
            print(book.title)
    except Author.DoesNotExist:
        print(f"No author found with name {author_name}")


# For all books

# def book_in_library(library_name):
#     try:
#         library = Library.objects.get(name = library_name)
#         book = Book.objects.filter(library__name = library_name)
#         if not book.exists():
#             print(f"Book not present in {library_name}")
#         else:
#             for books in book:
#                 print(f"{books.title}")


#     except Library.DoesNotExist:
#         print (f"{library_name} does not exist in our database")


def books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        for book in books:
            print(book.title)
    except Library.DoesNotExist:
        print("Library not found")


# librarian for library
def retrieve_librarian(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f"{librarian} manages {library_name}")

    except Library.DoesNotExist:
        print(f"{library_name} does not exist")
    except Librarian.DoesNotExist:
        print(f"{library_name} has no librarian")
