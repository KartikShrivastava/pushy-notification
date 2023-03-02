from apps.subscribers.models.subscriber import Subscriber
from apps.notifications.models.payload import Payload
import os
import json
from pushy_notification.celery import celery_app


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
                payload = Payload.objects.get(payload_id=payload_id)
                subscription_info = self._create_subscription_info_dict(
                                        subscriber=subscriber)
                payload_data = self._create_notification_payload_json(payload=payload)
                vapid_claims = self._create_vapid_claims_dict()
                PRIVATE_VAPID_KEY = os.getenv('PRIVATE_VAPID_KEY')

                async_task_result = celery_app.send_task('send_notification', args=[
                    subscription_info, payload_data, PRIVATE_VAPID_KEY, vapid_claims
                ])
                print(async_task_result.id)
        except Exception as e:
            raise e
