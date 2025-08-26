from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User= get_user_model()
class UserSerializer(serializers.ModelSerializer):    
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        # create user with hashed password
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"]
        )
        # create token
        Token.objects.create(user=user)
        return user
    
    ["serializers.CharField()", "get_user_model().objects.create_user"]