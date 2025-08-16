from django.contrib.auth.forms import UserCreationForm
from bookshelf.models import *
from django.forms import forms


class CustomUserForm(UserCreationForm):
    class Meta:
        fields = ("username", "email", "password1", "password2")
        model = CustomUser


class ExampleForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    age = forms.IntegerField(required=True)
    email = forms.EmailField(max_length=200, required=False)
