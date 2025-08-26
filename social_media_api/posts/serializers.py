from rest_framework import serializers
from posts.models import *
from rest_framework.serializers import StringRelatedField


class PostSerializer(serializers.ModelSerializer):
    author= serializers.StringRelatedField(read_only= True)
    class Meta:
        model= Post
        fields= ['author', 'title', 'content', 'created_at', 'updated_at']

    def validate(self, validated_data):
        if len(validated_data['title']) > 200:
            raise serializers.ValidationError({"title":"title can't be more than 200 characters"})
        return validated_data
    
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())


    class Meta:
        model= Comment
        fields=['author', 'post','content', 'created_at', 'updated_at']