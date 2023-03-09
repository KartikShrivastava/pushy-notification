from rest_framework.test import APITestCase
from apps.subscribers.models.subscriber import Subscriber
from apps.subscribers.services.subscriber import SubscriberService
from apps.subscribers.tests.factories.subscriber_request import SubscriberRequestFactory


class TestSubscriberView(APITestCase):
    def setUp(self):
        request_data = SubscriberRequestFactory()
        self.subscriber = SubscriberService.create_subscriber(request_data=request_data)

    def tearDown(self):
        Subscriber.objects.all().delete()

    def test_get_method_returns_valid_subscribers(self):
        url = '/subscribers/'

        response = self.client.get(url)
        expected_count = Subscriber.objects.all().count()
        response_count = len(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_count, expected_count)

    def test_post_method_inserts_subscriber_successfully(self):
        url = '/subscribers/'
        data = SubscriberRequestFactory()

        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['endpoint_url'], data['endpoint_url'])
        self.assertEqual(response.data['p256dh_key'], data['p256dh_key'])
        self.assertEqual(response.data['auth_key'], data['auth_key'])

    def test_post_method_returns_bad_response_for_invalid_data(self):
        url = '/subscribers/'
        # incorrect key name
        data_1 = SubscriberRequestFactory()
        endpoint_url = data_1.pop('endpoint_url')
        data_1['endpoint'] = endpoint_url
        # empty endpoint
        data_2 = data_1
        data_2['endpoint_url'] = ''

        response_1 = self.client.post(url, data=data_1, format='json')
        response_2 = self.client.post(url, data=data_2, format='json')

        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(response_2.status_code, 400)
