from rest_framework import serializers

from .models import (
    SubscriptionPlan,
    UserSubscription,
    PaymentTransaction,
    BillingHistory,
)


class SubscriptionPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionPlan
        fields = "__all__"


class UserSubscriptionSerializer(serializers.ModelSerializer):

    plan_name = serializers.CharField(
        source="plan.name",
        read_only=True
    )

    class Meta:
        model = UserSubscription
        fields = [
            "id",
            "plan",
            "plan_name",
            "start_date",
            "end_date",
            "status",
            "auto_renew",
        ]


class PaymentTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentTransaction
        fields = "__all__"
        read_only_fields = [
            "user",
            "created_at",
        ]


class BillingHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingHistory
        fields = "__all__"
        read_only_fields = [
            "user",
            "created_at",
        ]