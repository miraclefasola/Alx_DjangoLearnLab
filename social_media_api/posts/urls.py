from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from posts.views import *

router = DefaultRouter()

router.register(r"post", PostViewSet, basename="post")
router.register(r"comment", CommentViewSet, basename="comment")

urlpatterns = [path("", include(router.urls))]
