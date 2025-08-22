from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your models here.
class Post(models.Model):
    title= models.CharField(max_length=200)
    content= models.TextField()
    published_date= models.DateTimeField(auto_now_add=True)
    author= models.ForeignKey(User, related_name='posts', on_delete=models.PROTECT)

    def __str__(self):
        return self.title