from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Author(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=300)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="book_author"
    )

    def __str__(self):
        return self.title


# implementation of a token once a user instance is created so they can access the api through a call
@receiver(post_save, sender=User)
def _post_save_receiver(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
