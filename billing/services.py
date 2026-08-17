import uuid
from datetime import timedelta
from decimal import Decimal

import razorpay

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from .permissions import get_active_subscription

from .models import (
    SubscriptionPlan,
    UserSubscription,
    PaymentTransaction,
    BillingHistory,
)


class RazorpayService:

    @staticmethod
    def get_client():

        return razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET,
            )
        )

    @staticmethod
    def create_order(user, plan):

        if plan.price <= 0:
            raise ValueError(
                "Free plans do not require a payment order."
            )

        amount_paise = int(
            Decimal(plan.price) * Decimal("100")
        )

        receipt = (
            f"billing_{user.id}_"
            f"{uuid.uuid4().hex[:12]}"
        )

        client = RazorpayService.get_client()

        order = client.order.create(
            data={
                "amount": amount_paise,
                "currency": "INR",
                "receipt": receipt,
            }
        )

        payment = PaymentTransaction.objects.create(
            user=user,
            amount=plan.price,
            transaction_id=order["id"],
            gateway_order_id=order["id"],
            status=PaymentTransaction.PENDING,
            payment_method="razorpay",
        )

        return order, payment

    @staticmethod
    def verify_payment(
        user,
        order_id,
        payment_id,
        signature,
    ):

        client = RazorpayService.get_client()

        # Verify Razorpay signature first.
        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }
        )

        with transaction.atomic():

            payment = (
                PaymentTransaction.objects
                .select_for_update()
                .get(
                    user=user,
                    gateway_order_id=order_id,
                )
            )

            # Prevent duplicate verification.
            if payment.status == PaymentTransaction.SUCCESS:
                return payment

            payment.gateway_payment_id = payment_id
            payment.gateway_signature = signature
            payment.status = PaymentTransaction.SUCCESS
            payment.payment_date = timezone.now()

            payment.save(
                update_fields=[
                    "gateway_payment_id",
                    "gateway_signature",
                    "status",
                    "payment_date",
                ]
            )

            # Find the active subscription plan using
            # the amount associated with this payment.
            plan = (
                SubscriptionPlan.objects
                .filter(
                    price=payment.amount,
                    is_active=True,
                )
                .first()
            )

            if not plan:
                raise ValueError(
                    "Subscription plan for this payment was not found."
                )

            now = timezone.now()

            if plan.billing_period == SubscriptionPlan.YEARLY:
                end_date = now + timedelta(days=365)
            else:
                end_date = now + timedelta(days=30)

            subscription = UserSubscription.objects.create(
                user=user,
                plan=plan,
                start_date=now,
                end_date=end_date,
                status=UserSubscription.ACTIVE,
                auto_renew=False,
            )

            payment.subscription = subscription

            payment.save(
                update_fields=["subscription"]
            )

            BillingHistory.objects.create(
                user=user,
                subscription=subscription,
                event_type=BillingHistory.PAYMENT_COMPLETED,
                amount=payment.amount,
                description=(
                    f"Razorpay payment completed for "
                    f"{plan.name} subscription."
                ),
            )

            return payment

class FeatureAccessService:

    @staticmethod
    def can_post_job(user):
        """
        Check whether the employer can create another job.
        """

        subscription = get_active_subscription(user)

        if not subscription:
            return False

        plan = subscription.plan

        # Enterprise / unlimited plan
        if plan.unlimited_job_posts:
            return True

        employer = getattr(
            user,
            "employer_profile",
            None
        )

        if not employer:
            return False

        from jobs.models import Job

        current_job_count = Job.objects.filter(
            employer=employer
        ).count()

        return current_job_count < plan.job_post_limit

    @staticmethod
    def get_job_post_usage(user):
        """
        Return current job-post usage and remaining limit.
        """

        subscription = get_active_subscription(user)

        if not subscription:
            return {
                "allowed": False,
                "used": 0,
                "limit": 0,
                "remaining": 0,
                "unlimited": False,
            }

        plan = subscription.plan

        employer = getattr(
            user,
            "employer_profile",
            None
        )

        if not employer:
            return {
                "allowed": False,
                "used": 0,
                "limit": 0,
                "remaining": 0,
                "unlimited": False,
            }

        from jobs.models import Job

        used = Job.objects.filter(
            employer=employer
        ).count()

        if plan.unlimited_job_posts:
            return {
                "allowed": True,
                "used": used,
                "limit": None,
                "remaining": None,
                "unlimited": True,
            }

        limit = plan.job_post_limit
        remaining = max(limit - used, 0)

        return {
            "allowed": remaining > 0,
            "used": used,
            "limit": limit,
            "remaining": remaining,
            "unlimited": False,
        }

    @staticmethod
    def has_feature(user, feature_name):
        """
        Generic paid-feature checker.

        Example:
            FeatureAccessService.has_feature(
                user,
                "premium_analytics"
            )
        """

        subscription = get_active_subscription(user)

        if not subscription:
            return False

        plan = subscription.plan

        return bool(
            getattr(plan, feature_name, False)
        )

    @staticmethod
    def has_unlimited_candidate_access(user):
        """
        Check whether the user's subscription allows
        unlimited candidate access.
        """

        subscription = get_active_subscription(user)

        if not subscription:
            return False

        return subscription.unlimited_candidate_access

    @staticmethod
    def get_candidate_access_usage(user):
        """
        Return candidate-access limit information.
        """

        subscription = get_active_subscription(user)

        if not subscription:
            return {
                "allowed": False,
                "used": 0,
                "limit": 0,
                "remaining": 0,
                "unlimited": False,
            }

        limit = subscription.candidate_access_limit

        if subscription.unlimited_candidate_access:
            return {
                "allowed": True,
                "used": 0,
                "limit": None,
                "remaining": None,
                "unlimited": True,
            }

        # Candidate-access counting will be connected to
        # the application's candidate-access operation.
        return {
            "allowed": limit > 0,
            "used": 0,
            "limit": limit,
            "remaining": limit,
            "unlimited": False,
        }
    @staticmethod
    def deactivate_expired_subscriptions():
        """
        Mark subscriptions as EXPIRED when their grace period
        has also ended.
        """

        now = timezone.now()

        subscriptions = UserSubscription.objects.filter(
            status=UserSubscription.ACTIVE
        )

        expired_count = 0

        for subscription in subscriptions:

            # Still within normal subscription period
            if (
                subscription.end_date
                and subscription.end_date > now
            ):
                continue

            # Still within grace period
            if (
                subscription.grace_period_end
                and subscription.grace_period_end > now
            ):
                continue

            subscription.status = UserSubscription.EXPIRED

            subscription.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            expired_count += 1

        return expired_count