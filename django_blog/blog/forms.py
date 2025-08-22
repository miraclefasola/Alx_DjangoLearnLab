from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class Register(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

        def clean_email(self):
            email = self.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                raise ValidationError("Email has an account with us")
            return email
