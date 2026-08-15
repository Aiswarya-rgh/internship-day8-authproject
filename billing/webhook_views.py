import json
import hmac
import hashlib

from django.conf import settings
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PaymentTransaction


class RazorpayWebhookAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        webhook_signature = request.headers.get(
            "X-Razorpay-Signature"
        )

        if not webhook_signature:

            return Response(
                {
                    "success": False,
                    "message": "Missing webhook signature.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        expected_signature = hmac.new(
            settings.RAZORPAY_WEBHOOK_SECRET.encode(),
            request.body,
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(
            expected_signature,
            webhook_signature,
        ):

            return Response(
                {
                    "success": False,
                    "message": "Invalid webhook signature.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:

            payload = json.loads(
                request.body.decode("utf-8")
            )

        except json.JSONDecodeError:

            return Response(
                {
                    "success": False,
                    "message": "Invalid JSON payload.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        event = payload.get("event")

        if event == "payment.captured":

            payment_entity = (
                payload
                .get("payload", {})
                .get("payment", {})
                .get("entity", {})
            )

            payment_id = payment_entity.get("id")
            order_id = payment_entity.get("order_id")

            if order_id:

                payment = (
                    PaymentTransaction.objects
                    .filter(
                        gateway_order_id=order_id
                    )
                    .first()
                )

                if payment:

                    payment.gateway_payment_id = payment_id
                    payment.status = PaymentTransaction.SUCCESS
                    payment.payment_date = timezone.now()

                    payment.save(
                        update_fields=[
                            "gateway_payment_id",
                            "status",
                            "payment_date",
                        ]
                    )

        elif event == "payment.failed":

            payment_entity = (
                payload
                .get("payload", {})
                .get("payment", {})
                .get("entity", {})
            )

            order_id = payment_entity.get("order_id")

            if order_id:

                payment = (
                    PaymentTransaction.objects
                    .filter(
                        gateway_order_id=order_id
                    )
                    .first()
                )

                if payment:

                    payment.status = PaymentTransaction.FAILED

                    payment.failure_reason = (
                        payment_entity.get(
                            "error_description",
                            "Payment failed.",
                        )
                    )

                    payment.save(
                        update_fields=[
                            "status",
                            "failure_reason",
                        ]
                    )

        elif event in [
            "refund.created",
            "refund.processed",
        ]:

            refund_entity = (
                payload
                .get("payload", {})
                .get("refund", {})
                .get("entity", {})
            )

            payment_id = refund_entity.get(
                "payment_id"
            )

            if payment_id:

                payment = (
                    PaymentTransaction.objects
                    .filter(
                        gateway_payment_id=payment_id
                    )
                    .first()
                )

                if payment:

                    payment.status = (
                        PaymentTransaction.REFUNDED
                    )

                    payment.save(
                        update_fields=["status"]
                    )

        return Response(
            {
                "success": True,
                "message": "Webhook processed.",
            },
            status=status.HTTP_200_OK,
        )