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
