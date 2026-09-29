from rest_framework import serializers

from billing.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ("plan", "status", "current_period_start", "current_period_end", "created_at")
        read_only_fields = fields