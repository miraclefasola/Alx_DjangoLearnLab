from django.contrib.auth.forms import UserCreationForm
from bookshelf.models import *

class CustomUserForm(UserCreationForm):
    class Meta:
        fields= ('username', 'email', 'password1', 'password2') 
        model = CustomUser
    