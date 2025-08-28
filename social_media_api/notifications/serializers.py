from rest_framework import serializers
from .models import Notification
from django.core.exceptions import ValidationError


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source="actor.username")
    recipient = serializers.ReadOnlyField(source="recipient.username")
    target = serializers.ReadOnlyField(source="target")

    class Meta:

        model = Notification
        fields = ["id", "actor", "target", "verb", "recipient", "timestamp", "is_read"]

    def validate_verb(self, value):

        if len(value) > 300:
            raise ValidationError("Action can't be more than 300")
        return value
