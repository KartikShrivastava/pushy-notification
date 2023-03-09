from django.test import TestCase

from apps.notifications.models.payload import Payload
from apps.notifications.services.payload import PayloadService
from apps.notifications.tests.factories.payload_request import PayloadRequestFactory


class TestPayloadModel(TestCase):
    def test_string_representation_returns_id(self):
        request_data = PayloadRequestFactory()
        serialized_payload = PayloadService.create_payload(request_data=request_data)
        payload = Payload.objects.get(payload_id=serialized_payload['payload_id'])
        self.assertEqual(str(payload), serialized_payload['payload_id'])
