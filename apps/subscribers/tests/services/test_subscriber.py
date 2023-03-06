from django.utils import timezone
from django.test import TestCase

from apps.subscribers.services.subscriber import SubscriberService


class TestSubscriberService(TestCase):
    def test_create_subscriber_successful_creation(self):
        validated_data = {'endpoint_url': 'https://fcm.googleapis.com/fcm/send/e-s0cN3uKzQ:APA91bF7FMhiKaweoRovSoz6bVYuDEFR2o4aCU9zCWjbRzoBWI1-KkV7M197JeyiZQuIm-Kg8St9UvHaElEg4lL028xA709bSeKLDrOYs2ghLKpKyWd4tZU6XGE0J5rbzq-xtxig0hsb',  # noqa: E501
                          'expiration_time': timezone.now(),
                          'p256dh_key': 'BJthaLnJBkVtwe1SSAIbzSqm8A4vFw8P4SaF3yvmOW1IXzx4yUIvbmp4NVsuA5d0SBOVVUHfwYuak6CUJE1Qr9g',  # noqa: E501
                          'auth_key': 'vDfqsQPFWabqpmeFFv6EEg'}
        subscriber = SubscriberService.create_subscriber(validated_data=validated_data)
        self.assertEqual(subscriber.endpoint_url, validated_data['endpoint_url'])
        self.assertEqual(subscriber.expiration_time, validated_data['expiration_time'])
        self.assertEqual(subscriber.p256dh_key, validated_data['p256dh_key'])
        self.assertEqual(subscriber.auth_key, validated_data['auth_key'])
