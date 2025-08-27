📘 Social Media API – README
🔹 Setup
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

🔹 Authentication

Custom User model (email as USERNAME_FIELD).

Token authentication (/api-token-auth/).

Login supported with username or email.

🔹 Users & Follows

GET /users/ → List active users.

POST /follow/<user_id>/ → Follow user.

POST /unfollow/<user_id>/ → Unfollow user.

🔑 Rules:

Cannot follow/unfollow yourself.

Cannot follow twice / unfollow if not following.

🔹 Feed

GET /feed/ → Posts from followed users, ordered by newest (created_at).

🔹 Posts

GET /api/post/ → List all posts (paginated).

POST /api/post/ → Create post (author = current user).

GET/PUT/PATCH/DELETE /api/post/<id>/ → Manage post (author-only).

Nested comments included.

🔹 Comments

GET /api/comment/?post=<id> → List comments for post (paginated).

POST /api/comment/ → Add comment (author = current user).

PUT/PATCH/DELETE /api/comment/<id>/ → Manage comment (author-only).

🔹 Serializers
PostSerializer
class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["author", "title", "content", "created_at", "updated_at", "comment"]

    def validate(self, validated_data):
        if len(validated_data["title"]) > 200:
            raise serializers.ValidationError({"title": "title can't be more than 200 characters"})
        return validated_data

CommentSerializer
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = ["author", "content", "created_at", "updated_at"]

🔹 Permissions

All endpoints require IsAuthenticated.

Users can only update/delete their own posts & comments.

Follow/unfollow limited to own following list.