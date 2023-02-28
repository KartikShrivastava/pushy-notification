from pywebpush import webpush, WebPushException

from apps.subscribers.models.subscriber import Subscriber
from apps.notifications.models.payload import Payload
import os
import json


class NotificationService:
    def _create_subscription_info_dict(self, subscriber):
        subscription_info = {
            'endpoint': subscriber.endpoint_url,
            'keys': {
                'p256dh': subscriber.p256dh_key,
                'auth': subscriber.auth_key
            }
        }
        return subscription_info

    def _create_notification_payload_json(self, payload):
        payload_data = {
            'title': payload.title,
            'message': payload.body
        }
        return json.dumps(payload_data)

    def _create_vapid_claims_dict(self):
        vapid_claims = {
            'sub': 'mailto:john@doe.com'
        }
        return vapid_claims

    def send_bulk_notifications(self, subscriber_ids, payload_id):
        try:
            for subscriber_id in subscriber_ids:
                subscriber = Subscriber.objects.get(subscriber_id=subscriber_id)
                subscription_info = self._create_subscription_info_dict(
                                        subscriber=subscriber)

                payload = Payload.objects.get(payload_id=payload_id)
                payload_data = self._create_notification_payload_json(payload=payload)

                vapid_claims = self._create_vapid_claims_dict()

                PRIVATE_VAPID_KEY = os.getenv('PRIVATE_VAPID_KEY')

                webpush(subscription_info=subscription_info,
                        data=payload_data,
                        vapid_private_key=PRIVATE_VAPID_KEY,
                        vapid_claims=vapid_claims)
        except WebPushException as e:
            if e.response and e.response.json():
                respponse = e.response.json()
                print(respponse)
