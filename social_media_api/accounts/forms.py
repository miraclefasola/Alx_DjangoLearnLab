from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password1",
            "password2",
        ]

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if User.objects.filter(email=email).exists():
    #         raise ValidationError("An account with this email exists")
    #     return email
    # def clean_username(self):
    #     username= self.cleaned_data.get('username')
    #     if User.objects.filter(username=username).exists():
    #         raise ValidationError("Username not available")
    #     return username
