from django.urls import path

from .views import (
    SubscriptionPlanListAPIView,
    MySubscriptionAPIView,
    MyPaymentsAPIView,
    MyBillingHistoryAPIView,
)


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
]