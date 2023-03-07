from django.test import TestCase

from apps.notifications.services.payload import PayloadService


class TestPayloadModel(TestCase):
    def test_string_representation_returns_id(self):
        validated_data = {'title': 'Pushy notification title',
                          'body': 'Notification body can be a bit more longer'}
        payload = PayloadService.create_payload(validated_data=validated_data)
        self.assertEqual(str(payload), str(payload.payload_id))
