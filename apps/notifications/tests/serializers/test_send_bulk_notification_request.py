import uuid
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.notifications.serializers.send_bulk_notification_request import SendBulkNotificationRequestSerializer  # noqa: E501
from apps.notifications.services.payload import PayloadService
from apps.subscribers.services.subscriber import SubscriberService


class TestSendBulkNotificationRequestSerializer(TestCase):
    def setUp(self):
        validated_data_1 = {"endpoint_url": "https://fcm.googleapis.com/fcm/send/eoLdOURqrOk:APA91bHsMNZuJ2Df0Sy-yfNEHPyka7Md5Qi2xGepqtM5Wn07qqs11_E6bURjiEgSDLDPgo7YRlK9ZJ8-z0zJ14kLbvBVi4ZH35cZg_V9AS7Q2Ut4xYMxIHghCzaLyfXm_wxepPNv9aKL",  # noqa: E501
                            "expiration_time": None,
                            "p256dh_key": "BFhMLZUCjNsz0XZczzTMuC3lxeU09Krdl4FR1qoCF7q8Fz-OZ41nd3DwH17dlZAgp2pn6OCoBMgn_Hr0XaOepxA",  # noqa: E501
                            "auth_key": "3Yp8xGuTzT3MPG1EGzFSWg"}
        self.subscriber_1 = SubscriberService.create_subscriber(
                            validated_data=validated_data_1)

        validated_data_2 = {"subscriber_id": "b1508aa3-ea53-4f30-98ec-bb4d5217de72",
                            "endpoint_url": "https://fcm.googleapis.com/fcm/send/fQY6QXCiz-w:APA91bER2F8VNt0QmJ5lM3tUKkCORZwmHrNuwh5Riz1He3GdMOmh8mvfB68NkB85phFY4J_smaq7wIoGE-1KG1hb4qtr9lP0R6sFyT2GpiFqUyP538DWCQaiteD3fRX21vZB2ah_Fet9",  # noqa: E501
                            "expiration_time": None,
                            "p256dh_key": "BJWQevte81aYdpNnJ-LcDAbhOZxrkTXYY2DdI2gX9jOyR_4iWnZ300f64wGH8QRxM44X0BK9BNRYjM39U_Fn9yY",  # noqa: E501
                            "auth_key": "pwRPIiJJ7ydAzATZfO2yMQ"}
        self.subscriber_2 = SubscriberService.create_subscriber(
                            validated_data=validated_data_2)

        validated_data_3 = {'title': 'Pushy notification title',
                            'body': 'Notification body can be a bit more longer'}
        self.payload = PayloadService.create_payload(validated_data=validated_data_3)

    def test_perform_successful_validation(self):
        data = {'subscriber_ids': [f'{self.subscriber_1.subscriber_id}',
                                   f'{self.subscriber_2.subscriber_id}'],
                'payload_id': f'{self.payload.payload_id}'}

        request_serializer = SendBulkNotificationRequestSerializer(data=data)
        ret_val = request_serializer.is_valid(raise_exception=True)

        self.assertTrue(ret_val)

    def test_validate_subscriber_ids_raises_exception_for_invalid_data(self):
        # empty subscriber_ids
        data_1 = {'subscriber_ids': [],
                  'payload_id': f'{self.payload.payload_id}'}
        # invalid key
        data_2 = {'subscriber_id': [f'{self.subscriber_1.subscriber_id}'],
                  'payload_id': f'{self.payload.payload_id}'}
        # non-existing random subscriber_ids
        data_3 = {'subscriber_ids': [f'{uuid.uuid4()}'],
                  'payload_id': f'{self.payload.payload_id}'}

        request_serializer_1 = SendBulkNotificationRequestSerializer(data=data_1)
        request_serializer_2 = SendBulkNotificationRequestSerializer(data=data_2)
        request_serializer_3 = SendBulkNotificationRequestSerializer(data=data_3)

        self.assertRaises(ValidationError, request_serializer_1.is_valid,
                          raise_exception=True)
        self.assertRaises(ValidationError, request_serializer_2.is_valid,
                          raise_exception=True)
        self.assertRaises(ValidationError, request_serializer_3.is_valid,
                          raise_exception=True)

    def test_validate_payload_id_raises_exception_for_invalid_data(self):
        # empty payload_id
        data_1 = {'subscriber_ids': [f'{self.subscriber_1.subscriber_id}',
                                     f'{self.subscriber_2.subscriber_id}'],
                  'payload_id': ''}
        # invalid payload_id
        data_2 = {'subscriber_ids': [f'{self.subscriber_1.subscriber_id}',
                                     f'{self.subscriber_2.subscriber_id}'],
                  'payload_ids': f'{self.payload.payload_id}'}
        # non-existing random payload_id
        data_3 = {'subscriber_ids': [f'{self.subscriber_1.subscriber_id}',
                                     f'{self.subscriber_2.subscriber_id}'],
                  'payload_id': uuid.uuid4()}

        request_serializer_1 = SendBulkNotificationRequestSerializer(data=data_1)
        request_serializer_2 = SendBulkNotificationRequestSerializer(data=data_2)
        request_serializer_3 = SendBulkNotificationRequestSerializer(data=data_3)

        self.assertRaises(ValidationError, request_serializer_1.is_valid,
                          raise_exception=True)
        self.assertRaises(ValidationError, request_serializer_2.is_valid,
                          raise_exception=True)
        self.assertRaises(ValidationError, request_serializer_3.is_valid,
                          raise_exception=True)
