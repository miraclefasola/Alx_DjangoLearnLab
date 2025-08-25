from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Post, Comment
from taggit.forms import TagWidget

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


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["title", "content", "tags"]
        widgets= {'tags':TagWidget()}

    def clean_title(self):
        title = " ".join(self.cleaned_data.get("title").split())
        if not title:
            raise ValidationError("TITLE IS REQUIRED")
        elif len(title) > 200:
            raise ValidationError("Title can only be 200 character")
        else:
            pass
        

    # def clean_content(self):
    #     content = self.cleaned_data.get("content")
    #     return content.strip()
from django.utils.html import strip_tags
import re
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]

    def clean_content(self):
        content = self.cleaned_data.get("content", "")
        if not content:
            raise ValidationError("Comment can't be empty")
        plain_content = strip_tags(content).strip()
        if re.search(r"(.)\1{21,}", plain_content):
            raise ValidationError("Content contains excessive repeated characters.")

    # 3. Word repetition (same word repeated more than 10 times in a row)
        if re.search(r"\b(\w+)(?:\s+\1){10,}\b", plain_content, flags=re.IGNORECASE):
            raise ValidationError("Content contains spam-like repeated words.")

        return content

