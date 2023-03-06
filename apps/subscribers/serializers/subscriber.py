from rest_framework import serializers

from apps.subscribers.models.subscriber import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    endpoint_url = serializers.CharField(source='endpoint')
    expiration_time = serializers.DateTimeField(source='expirationTime')
    p256dh_key = serializers.CharField(source='keys.p256dh')
    auth_key = serializers.CharField(source='keys.auth')

    class Meta:
        model = Subscriber
        fields = ['endpoint_url', 'expiration_time', 'p256dh_key', 'auth_key']
