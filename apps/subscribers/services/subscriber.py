from django.forms import ValidationError
from apps.subscribers.models.subscriber import Subscriber


class SubscriberService:
    @classmethod
    def create_subscriber(cls, validated_data):
        if validated_data['endpoint_url'] == '':
            raise ValidationError(message='Cannont insert subscriber with empty endpoint')
        if validated_data['p256dh_key'] == '':
            raise ValidationError(message='Cannot insert subscriber with empty p256dh key')
        if validated_data['auth_key'] == '':
            raise ValidationError(message='Cannot insert subscriber with empty auth key')

        inserted_subscriber = Subscriber.objects.create(**validated_data)
        return inserted_subscriber
