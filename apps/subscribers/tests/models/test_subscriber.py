from django.test import TestCase

from apps.subscribers.models.subscriber import Subscriber
from apps.subscribers.services.subscriber import SubscriberService


class TestSubscriberModel(TestCase):
    def setUp(self):
        self.request_data = {'endpoint_url': 'https://fcm.googleapis.com/fcm/send/e-s0cN3uKzQ:APA91bF7FMhiKaweoRovSoz6bVYuDEFR2o4aCU9zCWjbRzoBWI1-KkV7M197JeyiZQuIm-Kg8St9UvHaElEg4lL028xA709bSeKLDrOYs2ghLKpKyWd4tZU6XGE0J5rbzq-xtxig0hsb',  # noqa: E501
                             'expiration_time': None,
                             'p256dh_key': 'BJthaLnJBkVtwe1SSAIbzSqm8A4vFw8P4SaF3yvmOW1IXzx4yUIvbmp4NVsuA5d0SBOVVUHfwYuak6CUJE1Qr9g',  # noqa: E501
                             'auth_key': 'vDfqsQPFWabqpmeFFv6EEg'}

    def test_string_representation_returns_id(self):
        serialized_subscriber = SubscriberService.create_subscriber(
                                request_data=self.request_data)
        subscriber = Subscriber.objects.get(
                        subscriber_id=serialized_subscriber['subscriber_id'])
        self.assertEqual(str(subscriber), serialized_subscriber['subscriber_id'])
