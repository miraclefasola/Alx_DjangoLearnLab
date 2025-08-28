from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from django.core.exceptions import PermissionDenied
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from accounts.models import *
from posts.models import *
from .models import Notification
from .serializers import NotificationSerializer
from django.shortcuts import redirect
from django.conf import settings

User = get_user_model()


class NotificationAPIVIEW(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recipient = self.request.user
        notis = Notification.objects.filter(recipient=recipient).order_by(
            "is_read", "-timestamp"
        )
        serializer = NotificationSerializer(notis, many=True)
        notis.update(is_read=True)
        return Response(serializer.data)
