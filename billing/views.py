from django.utils import timezone
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .permissions import get_active_subscription
from .services import RazorpayService, FeatureAccessService
from .permissions import get_active_subscription

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


class CreatePaymentOrderAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        plan_id = request.data.get("plan_id")

        if not plan_id:

            return Response(
                {
                    "success": False,
                    "message": "plan_id is required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            plan = SubscriptionPlan.objects.get(
                id=plan_id,
                is_active=True,
            )

        except SubscriptionPlan.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Subscription plan not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if plan.price <= 0:

            return Response(
                {
                    "success": False,
                    "message": "Free plans do not require payment.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            order, payment = RazorpayService.create_order(
                request.user,
                plan,
            )

        except Exception as exc:

            return Response(
                {
                    "success": False,
                    "message": "Unable to create payment order.",
                    "error": str(exc),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "success": True,
                "order": {
                    "id": order["id"],
                    "amount": order["amount"],
                    "currency": order["currency"],
                },
                "payment_id": payment.id,
                "razorpay_key_id": settings.RAZORPAY_KEY_ID,
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyPaymentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        order_id = request.data.get(
            "razorpay_order_id"
        )

        payment_id = request.data.get(
            "razorpay_payment_id"
        )

        signature = request.data.get(
            "razorpay_signature"
        )

        if not all([
            order_id,
            payment_id,
            signature,
        ]):

            return Response(
                {
                    "success": False,
                    "message": (
                        "Payment verification data "
                        "is incomplete."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            payment = RazorpayService.verify_payment(
                request.user,
                order_id,
                payment_id,
                signature,
            )

        except PaymentTransaction.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Payment order not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception:

            return Response(
                {
                    "success": False,
                    "message": (
                        "Payment signature verification failed."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": True,
                "message": "Payment verified successfully.",
                "payment": PaymentTransactionSerializer(
                    payment
                ).data,
            },
            status=status.HTTP_200_OK,
        )
class SubscriptionValidationAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        subscription = get_active_subscription(request.user)

        if not subscription:
            return Response({
                "success": True,
                "has_active_subscription": False,
                "subscription": None,
                "features": {},
                "usage": {},
            })

        plan = subscription.plan

        job_usage = FeatureAccessService.get_job_post_usage(
            request.user
        )

        candidate_usage = (
            FeatureAccessService.get_candidate_access_usage(
                request.user
            )
        )

        return Response({
            "success": True,
            "has_active_subscription": True,

            "subscription": {
                "id": subscription.id,
                "plan": plan.name,
                "status": subscription.status,
                "start_date": subscription.start_date,
                "end_date": subscription.end_date,
                "grace_period_end": (
                    subscription.grace_period_end
                ),
                "auto_renew": subscription.auto_renew,
            },

            "features": {
                "premium_analytics": plan.premium_analytics,
                "ai_matching": plan.ai_matching,
                "ai_interview_evaluation": (
                    plan.ai_interview_evaluation
                ),
                "ai_analytics": plan.ai_analytics,
                "unlimited_job_posts": (
                    plan.unlimited_job_posts
                ),
                "unlimited_candidate_access": (
                    subscription.unlimited_candidate_access
                ),
            },

            "usage": {
                "jobs": job_usage,
                "candidates": candidate_usage,
            },
        })