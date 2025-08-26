from django.contrib import admin
from accounts.models import *

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "username", "email"]


admin.site.register(CustomUser, UserAdmin)
