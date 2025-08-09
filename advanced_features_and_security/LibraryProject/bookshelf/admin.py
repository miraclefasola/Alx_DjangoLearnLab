from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author', 'publication_year')
    list_filter = ('author',)
    list_editable = ('author',)
    readonly_fields = ('title', 'publication_year')
    ordering = ('title',)
class CustomUserAdmin(admin.ModelAdmin):
    model=CustomUser
    fieldsets = UserAdmin.fieldsets +( (None,{'fields':('date_of_birth', 'profile_photo')}),)
    add_fieldsets=  UserAdmin.fieldsets+ ((None,{'fields':('date_of_birth', 'profile_photo')}),)
    list_display = ['username', 'email', 'date_of_birth', 'is_staff']
admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser,CustomUserAdmin )
