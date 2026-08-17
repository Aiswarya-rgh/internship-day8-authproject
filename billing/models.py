from django.db import models
from django.conf import settings
from django.utils import timezone


class SubscriptionPlan(models.Model):

    FREE = "FREE"
    PRO = "PRO"
    ENTERPRISE = "ENTERPRISE"

    PLAN_CHOICES = (
        (FREE, "Free"),
        (PRO, "Pro"),
        (ENTERPRISE, "Enterprise"),
    )

    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"

    BILLING_CHOICES = (
        (MONTHLY, "Monthly"),
        (YEARLY, "Yearly"),
    )

    name = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    billing_period = models.CharField(
        max_length=20,
        choices=BILLING_CHOICES,
        default=MONTHLY
    )

    # -------------------------------
    # JOB POSTING LIMIT
    # -------------------------------

    job_post_limit = models.PositiveIntegerField(
        default=0,
        help_text="0 means no job posting allowed."
    )

    unlimited_job_posts = models.BooleanField(
        default=False
    )

    # -------------------------------
    # PAID FEATURES
    # -------------------------------

    premium_analytics = models.BooleanField(
        default=False
    )

    ai_matching = models.BooleanField(
        default=False
    )

    ai_interview_evaluation = models.BooleanField(
        default=False
    )

    ai_analytics = models.BooleanField(
        default=False
    )

    # -------------------------------
    # PLAN STATUS
    # -------------------------------

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class UserSubscription(models.Model):

    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"

    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (EXPIRED, "Expired"),
        (CANCELLED, "Cancelled"),
        (PENDING, "Pending"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )

    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.PROTECT,
        related_name="subscriptions"
    )

    start_date = models.DateTimeField()

    end_date = models.DateTimeField()

    # -------------------------------
    # GRACE PERIOD
    # -------------------------------

    grace_period_end = models.DateTimeField(
        null=True,
        blank=True,
        help_text=(
            "Optional date/time until which paid access "
            "is allowed after subscription expiry."
        )
    )

    # -------------------------------
    # SUBSCRIPTION STATUS
    # -------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    auto_renew = models.BooleanField(
        default=False
    )

    # -------------------------------
    # CANDIDATE ACCESS LIMIT
    # -------------------------------

    candidate_access_limit = models.PositiveIntegerField(
        default=0,
        help_text=(
            "0 means no candidate access unless "
            "unlimited_candidate_access is enabled."
        )
    )

    unlimited_candidate_access = models.BooleanField(
        default=False
    )

    # -------------------------------
    # TIMESTAMPS
    # -------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # -------------------------------
    # ACCESS VALIDATION
    # -------------------------------

    def is_access_valid(self):

        now = timezone.now()

        # Subscription must be active
        if self.status != self.ACTIVE:
            return False

        # Normal subscription period
        if self.end_date > now:
            return True

        # Grace period after expiry
        if (
            self.grace_period_end
            and self.grace_period_end > now
        ):
            return True

        return False

    # -------------------------------
    # AUTOMATIC EXPIRY
    # -------------------------------

    def check_and_expire(self):

        now = timezone.now()

        if (
            self.status == self.ACTIVE
            and self.end_date <= now
            and (
                not self.grace_period_end
                or self.grace_period_end <= now
            )
        ):

            self.status = self.EXPIRED
            self.save(
                update_fields=[
                    "status",
                    "updated_at"
                ]
            )

            return True

        return False

    def __str__(self):

        return (
            f"{self.user.email} - "
            f"{self.plan.name}"
        )


class PaymentTransaction(models.Model):

    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

    STATUS_CHOICES = (
        (PENDING, "Pending"),
        (SUCCESS, "Success"),
        (FAILED, "Failed"),
        (REFUNDED, "Refunded"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payment_transactions"
    )

    subscription = models.ForeignKey(
        UserSubscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    transaction_id = models.CharField(
        max_length=255,
        unique=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    payment_method = models.CharField(
        max_length=50,
        blank=True
    )

    payment_date = models.DateTimeField(
        null=True,
        blank=True
    )

    failure_reason = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    gateway_order_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )

    gateway_payment_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )

    gateway_signature = models.CharField(
        max_length=512,
        blank=True
    )

    def __str__(self):

        return (
            f"{self.transaction_id} - "
            f"{self.status}"
        )


class BillingHistory(models.Model):

    SUBSCRIPTION_STARTED = "SUBSCRIPTION_STARTED"
    SUBSCRIPTION_RENEWED = "SUBSCRIPTION_RENEWED"
    PAYMENT_COMPLETED = "PAYMENT_COMPLETED"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    SUBSCRIPTION_CANCELLED = "SUBSCRIPTION_CANCELLED"

    EVENT_CHOICES = (
        (
            SUBSCRIPTION_STARTED,
            "Subscription Started"
        ),
        (
            SUBSCRIPTION_RENEWED,
            "Subscription Renewed"
        ),
        (
            PAYMENT_COMPLETED,
            "Payment Completed"
        ),
        (
            PAYMENT_FAILED,
            "Payment Failed"
        ),
        (
            SUBSCRIPTION_CANCELLED,
            "Subscription Cancelled"
        ),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="billing_history"
    )

    subscription = models.ForeignKey(
        UserSubscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="billing_history"
    )

    event_type = models.CharField(
        max_length=40,
        choices=EVENT_CHOICES
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.user.email} - "
            f"{self.event_type}"
        )