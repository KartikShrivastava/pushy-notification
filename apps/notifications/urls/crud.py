from django.urls import path

from apps.notifications.views.crud import NotificationPayloadCRUDView
from apps.notifications.views.bulk_notification_events import SendBulkNotificationsView


urlpatterns = [
    path('notifications/payloads/', NotificationPayloadCRUDView.as_view()),
    path('notifications/', SendBulkNotificationsView.as_view()),
]
