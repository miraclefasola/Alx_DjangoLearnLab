from django.urls import path
from .views import NotificationAPIVIEW

urlpatterns = [
    path("notifications/", NotificationAPIVIEW.as_view(), name="notifications"),
]
