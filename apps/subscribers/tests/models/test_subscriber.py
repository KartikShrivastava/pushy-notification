from django.test import TestCase

from apps.subscribers.services.subscriber import SubscriberService


class TestSubscriberModel(TestCase):
    def setUp(self):
        self.validated_data = {'endpoint_url': 'https://fcm.googleapis.com/fcm/send/e-s0cN3uKzQ:APA91bF7FMhiKaweoRovSoz6bVYuDEFR2o4aCU9zCWjbRzoBWI1-KkV7M197JeyiZQuIm-Kg8St9UvHaElEg4lL028xA709bSeKLDrOYs2ghLKpKyWd4tZU6XGE0J5rbzq-xtxig0hsb',  # noqa: E501
                               'expiration_time': None,
                               'p256dh_key': 'BJthaLnJBkVtwe1SSAIbzSqm8A4vFw8P4SaF3yvmOW1IXzx4yUIvbmp4NVsuA5d0SBOVVUHfwYuak6CUJE1Qr9g',  # noqa: E501
                               'auth_key': 'vDfqsQPFWabqpmeFFv6EEg'}

    def test_string_representation_id(self):
        subscriber = SubscriberService.create_subscriber(validated_data=self.validated_data)
        self.assertEqual(str(subscriber), str(subscriber.subscriber_id))
