from django.urls import path

from apps.subscribers.views.crud import SubscriberCRUDView


urlpatterns = [
    path('subscribers/', SubscriberCRUDView.as_view()),
]
