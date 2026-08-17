from django.urls import path

from .views import (
    SubscriptionPlanListAPIView,
    MySubscriptionAPIView,
    MyPaymentsAPIView,
    MyBillingHistoryAPIView,
    CreatePaymentOrderAPIView,
    VerifyPaymentAPIView,
    SubscriptionValidationAPIView,
)
from .webhook_views import RazorpayWebhookAPIView

urlpatterns = [
    path(
        "plans/",
        SubscriptionPlanListAPIView.as_view(),
        name="subscription-plans",
    ),

    path(
        "my-subscription/",
        MySubscriptionAPIView.as_view(),
        name="my-subscription",
    ),

    path(
        "payments/",
        MyPaymentsAPIView.as_view(),
        name="my-payments",
    ),

    path(
        "billing-history/",
        MyBillingHistoryAPIView.as_view(),
        name="billing-history",
    ),
    
    path(
    "payment/create-order/",
    CreatePaymentOrderAPIView.as_view(),
    name="create-payment-order",
    ),

    path(
    "payment/verify/",
    VerifyPaymentAPIView.as_view(),
    name="verify-payment",
    ),

    path(
    "payment/webhook/",
    RazorpayWebhookAPIView.as_view(),
    name="razorpay-webhook",
    ),

    path(
    "subscription/validate/",
    SubscriptionValidationAPIView.as_view(),
    name="subscription-validate",
   ),

    path(
    "subscription/validate/",
    SubscriptionValidationAPIView.as_view(),
    ),
]