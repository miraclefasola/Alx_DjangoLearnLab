from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

User = get_user_model()


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name="posts", on_delete=models.PROTECT)
    tags = TaggableManager()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_user"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]


    def __str__(self):
        return self.name
