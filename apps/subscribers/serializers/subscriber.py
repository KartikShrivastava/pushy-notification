from rest_framework import serializers

from apps.subscribers.models.subscriber import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['subscriber_id', 'endpoint_url', 'expiration_time', 'p256dh_key',
                  'auth_key']
