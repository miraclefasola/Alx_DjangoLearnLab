from rest_framework import serializers
from .models import Notification
from django.core.exceptions import ValidationError


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source="actor.username")
    recipient = serializers.ReadOnlyField(source="recipient.username")
#    target = serializers.SerializerMethodField()

    class Meta:

        model = Notification
        fields = ["id", "actor", "verb", "recipient", "timestamp", "is_read"]
    # def get_target(self, obj):
    #     # Convert the target (GenericForeignKey) into a JSON-friendly string
    #     return str(obj.target)
    def validate_verb(self, value):

        if len(value) > 300:
            raise ValidationError("Action can't be more than 300")
        return value
