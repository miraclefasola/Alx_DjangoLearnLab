from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.
class Book(models.Model):
    title= models.CharField(max_length=200)
    author= models.CharField(max_length=100)
    publication_year= models.IntegerField()
    class Meta:
        permissions=(
            ('can_view', 'View'),
            ('can_create', 'Create'),
            ('can_edit', 'Edit'),
            ('can_delete', 'Delete')
            )
    
    
    def __str__(self):
        return f"{self.title} by {self.author}"

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Please input a username')
        if not email:
            raise ValueError('Please input your email')
        email= self.normalize_email(email=email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, email, password=None, **extra_fields ):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser', True)
        user= self.create_user(username=username,
                               email=email,
                               password=password, **extra_fields)
        if extra_fields.get("is_staff") is not True:
            raise ValueError('superuser must have staff level status')
        if extra_fields.get("is_superuser") is not True:
            raise ValueError('supersuser should have superuserstatus')
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    date_of_birth= models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(default='default.jpg', blank=True,null=True, upload_to='profile_photos/')
    email= models.EmailField(unique=True)

    objects= CustomUserManager()

    def __str__(self):
        return self.username