from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, max_length=500)
    profile_picture = models.ImageField(
        default="default.jpeg", upload_to="profile_picture", null=True, blank=True
    )
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="user_followers", blank=True
    )
    following= models.ManyToManyField("self", symmetrical=False, related_name='user_following')
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    def __str__(self):
        return self.username


from django.db.models import Q
from django.contrib.auth.backends import BaseBackend
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def Tokengeneration(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UsernameOrEmail(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
