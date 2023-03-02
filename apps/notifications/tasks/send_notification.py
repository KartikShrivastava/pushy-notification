from pywebpush import WebPushException, webpush

from pushy_notification.celery import celery_app


@celery_app.task(name='send_notification')
def send_notification(subscription_info, payload_data, vapid_private_key, vapid_claims):
    try:
        webpush(subscription_info=subscription_info,
                data=payload_data,
                vapid_private_key=vapid_private_key,
                vapid_claims=vapid_claims)
    except WebPushException as e:
        if e.response and e.response.json():
            respponse = e.response.json()
            raise respponse
        raise e
