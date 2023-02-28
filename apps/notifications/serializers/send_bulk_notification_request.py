from rest_framework import serializers

from apps.subscribers.models.subscriber import Subscriber
from apps.notifications.models.payload import Payload


class SendBulkNotificationRequestSerializer(serializers.Serializer):
    subscriber_ids = serializers.ListField(child=serializers.UUIDField())
    payload_id = serializers.UUIDField()

    def validate_subscriber_ids(self, value):
        if len(value) == 0:
            raise serializers.ValidationError('No subscribers found in request')

        for subscriber_id in value:
            try:
                Subscriber.objects.get(subscriber_id=subscriber_id)
            except Subscriber.DoesNotExist:
                raise serializers.ValidationError('Invalid subscriber_id', subscriber_id)
        return value

    def validate_payload_id(self, value):
        try:
            Payload.objects.get(payload_id=value)
        except Payload.DoesNotExist:
            raise serializers.ValidationError('Invalid payload_id', value)
        return value
