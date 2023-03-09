from django.test import TestCase

from apps.subscribers.models.subscriber import Subscriber
from apps.subscribers.services.subscriber import SubscriberService
from apps.subscribers.tests.factories.subscriber_request import SubscriberRequestFactory


class TestSubscriberModel(TestCase):
    def setUp(self):
        self.request_data = SubscriberRequestFactory()

    def test_string_representation_returns_id(self):
        serialized_subscriber = SubscriberService.create_subscriber(
                                request_data=self.request_data)
        subscriber = Subscriber.objects.get(
                        subscriber_id=serialized_subscriber['subscriber_id'])
        self.assertEqual(str(subscriber), serialized_subscriber['subscriber_id'])
