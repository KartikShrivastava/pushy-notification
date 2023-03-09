from rest_framework.test import APITestCase

from apps.notifications.models.payload import Payload
from apps.notifications.services.payload import PayloadService
from apps.notifications.tests.factories.payload_request import PayloadRequestFactory


class TestPayloadView(APITestCase):
    def setUp(self):
        self.request_data = PayloadRequestFactory()
        PayloadService.create_payload(request_data=self.request_data)

    def test_get_method_returns_valid_payloads(self):
        url = '/notifications/payloads/'

        response = self.client.get(url)
        expected_count = Payload.objects.all().count()
        response_count = len(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_count, expected_count)

    def test_post_method_inserts_payload_successfully(self):
        url = '/notifications/payloads/'
        data = self.request_data

        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['body'], data['body'])

    # TODO: Fix error not thrown when PayloadRequestFactory used in failing tests
    def test_post_method_returns_bad_response_for_invalid_data(self):
        url = '/notifications/payloads/'
        # incorrect/missing key
        data_1 = {'title': 'Test Title',
                  'message': 'Body value with message key'}
        data_2 = data_1
        # empty title value
        data_2['title'] = ''

        response_1 = self.client.post(url, data=data_1, format='json')
        response_2 = self.client.post(url, data=data_2, format='json')

        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(response_2.status_code, 400)
