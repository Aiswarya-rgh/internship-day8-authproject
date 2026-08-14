from django.contrib import admin

from .models import (
    SubscriptionPlan,
    UserSubscription,
    PaymentTransaction,
    BillingHistory,
)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "billing_period",
        "job_post_limit",
        "unlimited_job_posts",
        "premium_analytics",
        "ai_matching",
        "ai_interview_evaluation",
        "ai_analytics",
        "is_active",
    )

    list_filter = (
        "name",
        "billing_period",
        "is_active",
    )


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "plan",
        "status",
        "start_date",
        "end_date",
        "auto_renew",
    )

    list_filter = (
        "status",
        "plan",
        "auto_renew",
    )

    search_fields = (
        "user__email",
    )


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_id",
        "user",
        "amount",
        "status",
        "payment_method",
        "payment_date",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_method",
    )

    search_fields = (
        "transaction_id",
        "user__email",
    )


@admin.register(BillingHistory)
class BillingHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "event_type",
        "amount",
        "subscription",
        "created_at",
    )

    list_filter = (
        "event_type",
    )

    search_fields = (
        "user__email",
    )