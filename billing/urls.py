from django.urls import path

from billing.views import SubscriptionView


urlpatterns = [path("subscription/", SubscriptionView.as_view(), name="subscription")]