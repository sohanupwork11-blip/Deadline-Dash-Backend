from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from billing.models import Subscription


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        read_only_fields = ("id",)

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Subscription.objects.create(user=user)
        return user