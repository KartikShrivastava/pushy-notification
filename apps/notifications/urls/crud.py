from django.urls import path

from apps.notifications.views.crud import NotificationPayloadCRUDView


urlpatterns = [
    path('notifications/payloads/', NotificationPayloadCRUDView.as_view())
]
