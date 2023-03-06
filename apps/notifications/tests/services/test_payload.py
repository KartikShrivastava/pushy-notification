from django.test import TestCase

from apps.notifications.services.payload import PayloadService


class TestPayloadServices(TestCase):
    def test_create_payload_successful_creation(self):
        validated_data = {'title': 'Pushy notification title',
                          'body': 'Notification body can be a bit more longer'}
        payload = PayloadService.create_payload(validated_data=validated_data)
        self.assertEqual(payload.title, validated_data['title'])
        self.assertEqual(payload.body, validated_data['body'])
