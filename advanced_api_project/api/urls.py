from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router= DefaultRouter()
router.register(r"books", BookView, basename='book_view')
router.register(r'authors', AuthorView, basename='author_view')
urlpatterns = [path('api/', include (router.urls))

]
