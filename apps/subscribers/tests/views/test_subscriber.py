from rest_framework.test import APITestCase
from apps.subscribers.models.subscriber import Subscriber
from apps.subscribers.services.subscriber import SubscriberService


class TestSubscriberView(APITestCase):
    def setUp(self):
        request_data = {'endpoint_url': 'https://fcm.googleapis.com/fcm/send/e-s0cN3uKzQ:APA91bF7FMhiKaweoRovSoz6bVYuDEFR2o4aCU9zCWjbRzoBWI1-KkV7M197JeyiZQuIm-Kg8St9UvHaElEg4lL028xA709bSeKLDrOYs2ghLKpKyWd4tZU6XGE0J5rbzq-xtxig0hsb',  # noqa: E501
                        'expiration_time': None,
                        'p256dh_key': 'BJthaLnJBkVtwe1SSAIbzSqm8A4vFw8P4SaF3yvmOW1IXzx4yUIvbmp4NVsuA5d0SBOVVUHfwYuak6CUJE1Qr9g',  # noqa: E501
                        'auth_key': 'vDfqsQPFWabqpmeFFv6EEg'}
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
        data = {
            "endpoint_url": "https://fcm.googleapis.com/fcm/send/fF8YFuWFGGM:APA91bE7zC7IdkTNO1sSk5nBytgK6JWPL0gf_sLvsfzoH24N_lSYDqF-0_fsxl-oYpSB3f6j1uVT-mzI0mnnjqaaotO7PoDFq20skCgC72K2fR0bPgUG-yic97jQa2vcgeo8y46rNElR",  # noqa: E501
            "expiration_time": None,
            "p256dh_key": "BIDRHIvK7e8iUhJmOe7tGYCxnoLBXyGsdK83g4Th7PeoTZulPCb_tRn7-k6iKIfSVhNgDqEmyywlgb8lKaRuu2Y",  # noqa: E501
            "auth_key": "JO52DmZYsGUdxsWMb0tsNA"
        }

        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['endpoint_url'], data['endpoint_url'])
        self.assertEqual(response.data['p256dh_key'], data['p256dh_key'])
        self.assertEqual(response.data['auth_key'], data['auth_key'])

    def test_post_method_returns_bad_response_for_invalid_data(self):
        url = '/subscribers/'
        # incorrect keys
        data_1 = {
            "endpoint_url": "https://fcm.googleapis.com/fcm/send/fF8YFuWFGGM:APA91bE7zC7IdkTNO1sSk5nBytgK6JWPL0gf_sLvsfzoH24N_lSYDqF-0_fsxl-oYpSB3f6j1uVT-mzI0mnnjqaaotO7PoDFq20skCgC72K2fR0bPgUG-yic97jQa2vcgeo8y46rNElR",  # noqa: E501
            "expiration_time": None,
            "keys": {
                "p256dh": "BIDRHIvK7e8iUhJmOe7tGYCxnoLBXyGsdK83g4Th7PeoTZulPCb_tRn7-k6iKIfSVhNgDqEmyywlgb8lKaRuu2Y",  # noqa: E501
                "auth": "JO52DmZYsGUdxsWMb0tsNA"
            }
        }
        # empty endpoint
        data_2 = data_1
        data_2['endpoint_url'] = ''

        response_1 = self.client.post(url, data=data_1, format='json')
        response_2 = self.client.post(url, data=data_2, format='json')

        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(response_2.status_code, 400)
