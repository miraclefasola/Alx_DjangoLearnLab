from rest_framework import serializers
from posts.models import *
from rest_framework.serializers import StringRelatedField


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "created_at", "updated_at"]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "created_at",
            "updated_at",
            "comment",
        ]

    def validate(self, validated_data):
        if len(validated_data["title"]) > 200:
            raise serializers.ValidationError(
                {"title": "title can't be more than 200 characters"}
            )
        return validated_data


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    post = serializers.ReadOnlyField(source="post.title")

    class Meta:
        model = Like
        fields = ["id", "user", "post", "created_at"]
