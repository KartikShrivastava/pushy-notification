import json
import os
import uuid
from unittest import mock

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.utils import timezone

from apps.notifications.models.payload import Payload
from apps.notifications.services.notification import NotificationService
from apps.notifications.services.payload import PayloadService
from apps.subscribers.models.subscriber import Subscriber
from apps.subscribers.services.subscriber import SubscriberService


class TestNotificationServicePrivateFunctions(TestCase):
    def setUp(self):
        validated_data = {'endpoint_url': 'https://fcm.googleapis.com/fcm/send/e-s0cN3uKzQ:APA91bF7FMhiKaweoRovSoz6bVYuDEFR2o4aCU9zCWjbRzoBWI1-KkV7M197JeyiZQuIm-Kg8St9UvHaElEg4lL028xA709bSeKLDrOYs2ghLKpKyWd4tZU6XGE0J5rbzq-xtxig0hsb',  # noqa: E501
                          'expiration_time': timezone.now(),
                          'p256dh_key': 'BJthaLnJBkVtwe1SSAIbzSqm8A4vFw8P4SaF3yvmOW1IXzx4yUIvbmp4NVsuA5d0SBOVVUHfwYuak6CUJE1Qr9g',  # noqa: E501
                          'auth_key': 'vDfqsQPFWabqpmeFFv6EEg'}
        self.subscriber = SubscriberService.create_subscriber(validated_data=validated_data)

        validated_data = {'title': 'Pushy notification title',
                          'body': 'Notification body can be a bit more longer'}
        self.payload = PayloadService.create_payload(validated_data=validated_data)

    def test__create_subscription_info_dict_format_validity(self):
        subscription_info = NotificationService()._create_subscription_info_dict(
                            subscriber=self.subscriber)

        self.assertTrue('endpoint' in subscription_info)
        self.assertTrue('keys' in subscription_info)
        self.assertTrue('p256dh' in subscription_info['keys'])
        self.assertTrue('auth' in subscription_info['keys'])

    def test__create_notification_payload_json_format_validity(self):
        payload_data = NotificationService()._create_notification_payload_json(
                       payload=self.payload)
        payload_data_dict = json.loads(payload_data)

        self.assertTrue('title' in payload_data_dict)
        self.assertTrue('message' in payload_data_dict)

    def test__create_vapid_claims_dict_format_validity(self):
        vapid_claims = NotificationService()._create_vapid_claims_dict()

        self.assertTrue('sub' in vapid_claims)


class TestNotificationServicePublicFunctions(TestCase):
    def setUp(self):
        validated_data_1 = {'endpoint_url': 'https://fcm.googleapis.com/fcm/send/e-s0cN3uKzQ:APA91bF7FMhiKaweoRovSoz6bVYuDEFR2o4aCU9zCWjbRzoBWI1-KkV7M197JeyiZQuIm-Kg8St9UvHaElEg4lL028xA709bSeKLDrOYs2ghLKpKyWd4tZU6XGE0J5rbzq-xtxig0hsb',  # noqa: E501
                            'expiration_time': timezone.now(),
                            'p256dh_key': 'BJthaLnJBkVtwe1SSAIbzSqm8A4vFw8P4SaF3yvmOW1IXzx4yUIvbmp4NVsuA5d0SBOVVUHfwYuak6CUJE1Qr9g',  # noqa: E501
                            'auth_key': 'vDfqsQPFWabqpmeFFv6EEg'}
        subscriber_1 = SubscriberService.create_subscriber(validated_data=validated_data_1)

        validated_data_2 = {
            'endpoint_url': 'https://fcm.googleapis.com/fcm/send/fF8YFuWFGGM:APA91bE7zC7IdkTNO1sSk5nBytgK6JWPL0gf_sLvsfzoH24N_lSYDqF-0_fsxl-oYpSB3f6j1uVT-mzI0mnnjqaaotO7PoDFq20skCgC72K2fR0bPgUG-yic97jQa2vcgeo8y46rNElR',  # noqa: E501
            'expiration_time': None,
            'p256dh_key': 'BIDRHIvK7e8iUhJmOe7tGYCxnoLBXyGsdK83g4Th7PeoTZulPCb_tRn7-k6iKIfSVhNgDqEmyywlgb8lKaRuu2Y',  # noqa: E501
            'auth_key': 'JO52DmZYsGUdxsWMb0tsNA'}
        subscriber_2 = SubscriberService.create_subscriber(validated_data=validated_data_2)

        validated_data_3 = {'title': 'Pushy notification title',
                            'body': 'Notification body can be a bit more longer'}
        payload = PayloadService.create_payload(validated_data=validated_data_3)

        self.subscriber_ids = [subscriber_1.subscriber_id, subscriber_2.subscriber_id]
        self.payload_id = payload.payload_id

    @mock.patch('pushy_notification.celery.celery_app.send_task')
    def test_send_bulk_notifications_sends_notifications(self, mocked_func):
        subscriber_1 = Subscriber.objects.get(subscriber_id=self.subscriber_ids[0])
        subscriber_2 = Subscriber.objects.get(subscriber_id=self.subscriber_ids[1])
        payload = Payload.objects.get(payload_id=self.payload_id)
        subscription_info_1 = NotificationService()._create_subscription_info_dict(
                                subscriber=subscriber_1)
        subscription_info_2 = NotificationService()._create_subscription_info_dict(
                                subscriber=subscriber_2)
        subscription_infos = [subscription_info_1, subscription_info_2]
        payload_data = NotificationService()._create_notification_payload_json(
                        payload=payload)
        vapid_claims = NotificationService()._create_vapid_claims_dict()
        PRIVATE_VAPID_KEY = os.getenv('PRIVATE_VAPID_KEY')

        NotificationService().send_bulk_notifications(subscriber_ids=self.subscriber_ids,
                                                      payload_id=self.payload_id)

        mocked_func.assert_called()
        mocked_func.assert_has_calls(
            [mock.call('send_notification',
                       args=[subscription_info,
                             payload_data,
                             PRIVATE_VAPID_KEY,
                             vapid_claims]) for subscription_info in subscription_infos])

    @mock.patch('pushy_notification.celery.celery_app.send_task')
    def test_send_bulk_notification_raises_exception_for_invalid_subscriber_id(self,
                                                                               mocked_func):
        subscriber_ids = self.subscriber_ids
        subscriber_ids.append(uuid.uuid4())

        self.assertRaises(ObjectDoesNotExist, NotificationService().send_bulk_notifications,
                          subscriber_ids=subscriber_ids, payload_id=self.payload_id)

    @mock.patch('pushy_notification.celery.celery_app.send_task')
    def test_send_bulk_notification_raises_exception_for_invalid_payload_id(self,
                                                                            mocked_func):
        payload_id = uuid.uuid4()

        self.assertRaises(ObjectDoesNotExist, NotificationService().send_bulk_notifications,
                          subscriber_ids=self.subscriber_ids, payload_id=payload_id)
