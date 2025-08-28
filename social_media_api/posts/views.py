from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from posts.models import *
from posts.serializers import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import filters, DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
class PostViewSet(ModelViewSet):
    model = Post
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 3
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["created_at", "updated_at"]
    search_fields = ["title", "content"]

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if request.method in SAFE_METHODS:
            return
        if request.user != obj.author:
            raise PermissionDenied("only author can edit their own post")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    model = Comment
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ["created_at", "updated_at"]
    filterset_fields = ["post"]

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if request.method in SAFE_METHODS:
            return
        if request.user != obj.author:
            raise PermissionDenied("only author can edit their own post")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedView(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    authentication_classes = [IsAuthenticated]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        current_user = self.request.user
        following_list = current_user.following.all()
        feed_queryset = Post.objects.filter(author__in=following_list).order_by(
            "-created_at"
        )
        return feed_queryset


from rest_framework.views import APIView
from rest_framework.permissions import SAFE_METHODS
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class LikeView(ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def like(self):
        actor = self.request.user
        target = self.get_object()
        if Like.objects.filter(user=actor, post=target).exists():
            return Response({"detail": "You have already liked this post"})
        Like.objects.create(user=actor, post=target)

        # response formatting
        if target.author == actor:
            return Response({"detail": "You have just liked your own post"})
        return Response({"detail": f"You have just liked {target.author}'s post"})

    @action(detail=True, methods=["post"])
    def Unlike(self):
        actor = self.request.user
        target = self.get_object()
        if not Like.objects.filter(user=actor, post=target).exists():
            return Response({"detail": "you haven't liked this post"})
        Like.objects.filter(user=actor, post=target).delete()
        if target.author == actor:
            return Response({"detail": "You have unliked your own post"})
        return Response({"detail": f"You have unliked {target.author}'s post"})


class LikeAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        actor = request.user

        if Like.objects.filter(user=actor, post=post).exists():
            return Response({"detail": "You have already liked this post"})
        Like.objects.create(user=actor, post=post)

        if post.author == actor:
            return Response({"detail": "You have just liked your own post"})
        elif post.author != actor:
            
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                content_type=ContentType.objects.get_for_model(post),
                object_id=post.id,
            )

            return Response({"detail": f"You have just liked {post.author}'s post"})
        else:
            return Response({"detail": "error"})


class UnlikeAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        actor = request.user
        target = get_object_or_404(Post, pk=pk)

        if not Like.objects.filter(user=actor, post=target).exists():
            return Response({"detail": "you haven't liked this post"})

        if target.author == actor:
            Like.objects.filter(user=actor, post=target).delete()
            return Response({"detail": "You have just unliked your own post"})
        elif target.author != actor:
            Like.objects.filter(user=actor, post=target).delete()
            return Response({"detail": f"You have just unliked {target.author}'s post"})
        else:
            return Response({"detail": "error"})

