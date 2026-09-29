from rest_framework import generics

from billing.models import Subscription
from billing.serializers import SubscriptionSerializer


class SubscriptionView(generics.RetrieveAPIView):
    serializer_class = SubscriptionSerializer

    def get_object(self):
        subscription, _ = Subscription.objects.get_or_create(user=self.request.user)
        return subscription