from django.contrib import admin
from .models import Book


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_year")
    search_fields = ("title", "author", "publication_year")
    list_filter = ("author",)
    list_editable = ("author",)
    readonly_fields = ("title", "publication_year")
    ordering = ("title",)


admin.site.register(Book, BookAdmin)
