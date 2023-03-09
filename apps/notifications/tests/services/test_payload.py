from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.notifications.services.payload import PayloadService


class TestPayloadServices(TestCase):
    def test_create_payload_successful_creation(self):
        request_data = {'title': 'Pushy notification title',
                        'body': 'Notification body can be a bit more longer'}
        payload = PayloadService.create_payload(request_data=request_data)
        self.assertEqual(payload['title'], request_data['title'])
        self.assertEqual(payload['body'], request_data['body'])

    def test_create_payload_throws_exception_for_empty_title(self):
        request_data = {'title': '',
                        'body': 'Notification body can be a bit more longer'}
        self.assertRaises(ValidationError, PayloadService.create_payload,
                          request_data=request_data)

    def test_create_payload_throws_exception_for_empty_body(self):
        request_data = {'title': 'Pushy notification title',
                        'body': ''}
        self.assertRaises(ValidationError, PayloadService.create_payload,
                          request_data=request_data)
