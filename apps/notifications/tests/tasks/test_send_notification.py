import os

from django.test import TestCase, override_settings

from apps.notifications.models.payload import Payload
from apps.notifications.services.notification import NotificationService
from apps.notifications.services.payload import PayloadService
from apps.notifications.tasks.send_notification import send_notification
from apps.subscribers.models.subscriber import Subscriber
from apps.subscribers.services.subscriber import SubscriberService


class TestSendNotificationTask(TestCase):
    def setUp(self):
        validated_data_1 = {'endpoint_url': 'https://fcm.googleapis.com/fcm/send/e-s0cN3uKzQ:APA91bF7FMhiKaweoRovSoz6bVYuDEFR2o4aCU9zCWjbRzoBWI1-KkV7M197JeyiZQuIm-Kg8St9UvHaElEg4lL028xA709bSeKLDrOYs2ghLKpKyWd4tZU6XGE0J5rbzq-xtxig0hsb',  # noqa: E501
                            'expiration_time': None,
                            'p256dh_key': 'BJthaLnJBkVtwe1SSAIbzSqm8A4vFw8P4SaF3yvmOW1IXzx4yUIvbmp4NVsuA5d0SBOVVUHfwYuak6CUJE1Qr9g',  # noqa: E501
                            'auth_key': 'vDfqsQPFWabqpmeFFv6EEg'}
        subscriber = SubscriberService.create_subscriber(validated_data=validated_data_1)

        validated_data_2 = {'title': 'Pushy notification title',
                            'body': 'Notification body can be a bit more longer'}
        payload = PayloadService.create_payload(validated_data=validated_data_2)

        self.subscriber_ids = [subscriber.subscriber_id]
        self.payload_id = payload.payload_id

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_send_notification_makes_call_to_webpush(self, mocked_func):
        subscriber = Subscriber.objects.get(subscriber_id=self.subscriber_ids[0])
        payload = Payload.objects.get(payload_id=self.payload_id)
        subscription_info = NotificationService()._create_subscription_info_dict(
                            subscriber=subscriber)
        subscription_infos = [subscription_info]
        payload_data = NotificationService()._create_notification_payload_json(
                        payload=payload)
        vapid_claims = NotificationService()._create_vapid_claims_dict()
        PRIVATE_VAPID_KEY = os.getenv('PRIVATE_VAPID_KEY')

        send_notification.delay(subscription_infos, payload_data,
                                PRIVATE_VAPID_KEY, vapid_claims)

        # TODO: Complete the impl to test celery task result and exceptions
