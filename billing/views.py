from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import (
    SubscriptionPlan,
    UserSubscription,
    PaymentTransaction,
    BillingHistory,
)

from .serializers import (
    SubscriptionPlanSerializer,
    UserSubscriptionSerializer,
    PaymentTransactionSerializer,
    BillingHistorySerializer,
)


class SubscriptionPlanListAPIView(APIView):

    permission_classes = []

    def get(self, request):
        plans = SubscriptionPlan.objects.filter(
            is_active=True
        )

        serializer = SubscriptionPlanSerializer(
            plans,
            many=True
        )

        return Response({
            "success": True,
            "plans": serializer.data
        })


class MySubscriptionAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        subscription = (
            UserSubscription.objects
            .filter(
                user=request.user,
                status=UserSubscription.ACTIVE,
                end_date__gt=timezone.now(),
            )
            .select_related("plan")
            .first()
        )

        if not subscription:
            return Response({
                "success": True,
                "has_active_subscription": False,
                "subscription": None,
            })

        serializer = UserSubscriptionSerializer(
            subscription
        )

        return Response({
            "success": True,
            "has_active_subscription": True,
            "subscription": serializer.data,
        })


class MyPaymentsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        payments = PaymentTransaction.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = PaymentTransactionSerializer(
            payments,
            many=True
        )

        return Response({
            "success": True,
            "payments": serializer.data
        })


class MyBillingHistoryAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        history = BillingHistory.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = BillingHistorySerializer(
            history,
            many=True
        )

        return Response({
            "success": True,
            "billing_history": serializer.data
        })