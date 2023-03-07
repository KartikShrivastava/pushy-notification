from django.forms import ValidationError
from apps.notifications.models.payload import Payload


class PayloadService:
    @classmethod
    def create_payload(cls, validated_data):
        if validated_data['title'] == '':
            raise ValidationError(message='Cannont insert payload with empty title')
        if validated_data['body'] == '':
            raise ValidationError(message='Cannot insert payload with empty body')

        inserted_payload = Payload.objects.create(**validated_data)
        return inserted_payload
