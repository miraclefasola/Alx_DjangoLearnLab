from django.contrib import admin
from blog.models import *
from django.utils.text import Truncator

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "published_date", "author", "display_tags"]

    # get querset redundant but inclluding it anyway as i dont ahve a custom queryset
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def display_tags(self, obj):
        if obj.tags.exists():
            return ", ".join(o.name for o in obj.tags.all())
        return "No Tags"

    def content(self, obj):
        return Truncator(obj.content).chars(50)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
