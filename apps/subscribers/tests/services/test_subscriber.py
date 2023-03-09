from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.subscribers.services.subscriber import SubscriberService
from apps.subscribers.tests.factories.subscriber_request import SubscriberRequestFactory


class TestSubscriberService(TestCase):
    def setUp(self):
        self.request_data = SubscriberRequestFactory()

    def test_create_subscriber_successful_creation(self):
        subscriber = SubscriberService.create_subscriber(request_data=self.request_data)
        self.assertEqual(subscriber['endpoint_url'], self.request_data['endpoint_url'])
        # convert request_data datetime.datetime object to string format matching serializer
        self.assertEqual(subscriber['expiration_time'],
                         self.request_data['expiration_time']
                         .strftime('%Y-%m-%dT%H:%M:%SZ'))
        self.assertEqual(subscriber['p256dh_key'], self.request_data['p256dh_key'])
        self.assertEqual(subscriber['auth_key'], self.request_data['auth_key'])

    def test_create_subscriber_throws_exception_for_empty_endpoint(self):
        self.request_data['endpoint_url'] = ''
        self.assertRaises(ValidationError, SubscriberService.create_subscriber,
                          request_data=self.request_data)

    def test_create_subscriber_throws_exception_for_empty_p256dh_key(self):
        self.request_data['p256dh_key'] = ''
        self.assertRaises(ValidationError, SubscriberService.create_subscriber,
                          request_data=self.request_data)

    def test_create_subscriber_throws_exception_for_empty_auth_key(self):
        self.request_data['auth_key'] = ''
        self.assertRaises(ValidationError, SubscriberService.create_subscriber,
                          request_data=self.request_data)
