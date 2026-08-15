import uuid
from datetime import timedelta
from decimal import Decimal

import razorpay

from django.conf import settings
from django.db import transaction
from django.utils import timezone

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