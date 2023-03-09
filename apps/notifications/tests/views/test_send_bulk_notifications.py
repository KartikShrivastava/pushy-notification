from rest_framework.test import APITestCase
from apps.notifications.services.payload import PayloadService

from apps.subscribers.services.subscriber import SubscriberService
import uuid
from unittest import mock


class TestSendBulkNotificationsView(APITestCase):
    def setUp(self):
        validated_data_1 = {'endpoint_url': 'https://fcm.googleapis.com/fcm/send/e-s0cN3uKzQ:APA91bF7FMhiKaweoRovSoz6bVYuDEFR2o4aCU9zCWjbRzoBWI1-KkV7M197JeyiZQuIm-Kg8St9UvHaElEg4lL028xA709bSeKLDrOYs2ghLKpKyWd4tZU6XGE0J5rbzq-xtxig0hsb',  # noqa: E501
                            'expiration_time': None,
                            'p256dh_key': 'BJthaLnJBkVtwe1SSAIbzSqm8A4vFw8P4SaF3yvmOW1IXzx4yUIvbmp4NVsuA5d0SBOVVUHfwYuak6CUJE1Qr9g',  # noqa: E501
                            'auth_key': 'vDfqsQPFWabqpmeFFv6EEg'}
        self.subscriber = SubscriberService.create_subscriber(
                            validated_data=validated_data_1)

        validated_data_2 = {'title': 'Pushy notification title',
                            'body': 'Notification body can be a bit more longer'}
        self.payload = PayloadService.create_payload(
                        validated_data=validated_data_2)

    @mock.patch('pushy_notification.celery.celery_app.send_task')
    def test_post_method_triggers_send_notification_successfully(self, mocked_func):
        url = '/notifications/'
        data = {'subscriber_ids': [self.subscriber.subscriber_id],
                'payload_id': self.payload.payload_id}

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data['message'],
                         'Web push notifications scheduled successfully')

    @mock.patch('pushy_notification.celery.celery_app.send_task')
    def test_post_method_returns_bad_status_for_invalid_data(self, mocked_func):
        url = '/notifications/'
        # incorrect key
        data_1 = {'subscribers': [self.subscriber.subscriber_id],
                  'payload_id': self.payload.payload_id}
        # incorrect subscriber_id
        data_2 = {'subscriber_ids': [uuid.uuid4()],
                  'payload_id': self.payload.payload_id}
        # incorrect payload_id
        data_3 = {'subscriber_ids': [self.subscriber.subscriber_id],
                  'payload_id': uuid.uuid4()}

        response_1 = self.client.post(url, data=data_1, format='json')
        response_2 = self.client.post(url, data=data_2, format='json')
        response_3 = self.client.post(url, data=data_3, format='json')

        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(response_3.status_code, 400)
