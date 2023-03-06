from rest_framework.test import APITestCase
from apps.subscribers.models.subscriber import Subscriber
from apps.subscribers.services.subscriber import SubscriberService


class TestSubscriberView(APITestCase):
    def setUp(self):
        validated_data = {'endpoint_url': 'https://fcm.googleapis.com/fcm/send/e-s0cN3uKzQ:APA91bF7FMhiKaweoRovSoz6bVYuDEFR2o4aCU9zCWjbRzoBWI1-KkV7M197JeyiZQuIm-Kg8St9UvHaElEg4lL028xA709bSeKLDrOYs2ghLKpKyWd4tZU6XGE0J5rbzq-xtxig0hsb',  # noqa: E501
                          'expiration_time': None,
                          'p256dh_key': 'BJthaLnJBkVtwe1SSAIbzSqm8A4vFw8P4SaF3yvmOW1IXzx4yUIvbmp4NVsuA5d0SBOVVUHfwYuak6CUJE1Qr9g',  # noqa: E501
                          'auth_key': 'vDfqsQPFWabqpmeFFv6EEg'}
        SubscriberService.create_subscriber(validated_data=validated_data)

    def tearDown(self):
        Subscriber.objects.all().delete()

    def test_get_method_returns_all_subscribers(self):
        url = '/subscribers/'

        response = self.client.get(url)
        expected_count = Subscriber.objects.all().count()
        response_count = len(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_count, expected_count)
