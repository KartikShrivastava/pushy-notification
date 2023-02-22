from django.urls import path
from restAPI import views


urlpatterns = [
    path('subscribers/', views.SubscriberView.as_view()),
]
