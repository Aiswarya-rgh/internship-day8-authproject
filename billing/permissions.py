from django.utils import timezone

from rest_framework.permissions import BasePermission

from .models import UserSubscription


def get_active_subscription(user):
    """
    Return the user's currently usable subscription.

    Access is allowed when:
    1. Subscription status is ACTIVE and end_date has not passed.
    2. Subscription has expired but is still inside its grace period.
    """

    if not user or not user.is_authenticated:
        return None

    subscription = (
        UserSubscription.objects
        .filter(
            user=user,
            status=UserSubscription.ACTIVE,
        )
        .select_related("plan")
        .order_by("-end_date")
        .first()
    )

    if not subscription:
        return None

    now = timezone.now()

    # Normal subscription period
    if subscription.end_date and subscription.end_date > now:
        return subscription

    # Grace period
    if (
        subscription.grace_period_end
        and subscription.grace_period_end > now
    ):
        return subscription

    return None


class HasActiveSubscription(BasePermission):

    message = (
        "An active subscription is required "
        "to access this feature."
    )

    def has_permission(self, request, view):

        subscription = get_active_subscription(
            request.user
        )

        return subscription is not None


class HasPremiumAnalytics(BasePermission):

    message = (
        "Premium analytics requires a "
        "subscription that includes this feature."
    )

    def has_permission(self, request, view):

        subscription = get_active_subscription(
            request.user
        )

        if not subscription:
            return False

        return subscription.plan.premium_analytics


class HasAIAnalytics(BasePermission):

    message = (
        "AI analytics requires a subscription "
        "that includes AI analytics."
    )

    def has_permission(self, request, view):

        subscription = get_active_subscription(
            request.user
        )

        if not subscription:
            return False

        return subscription.plan.ai_analytics


class HasAIMatching(BasePermission):

    message = (
        "AI matching requires a subscription "
        "that includes AI matching."
    )

    def has_permission(self, request, view):

        subscription = get_active_subscription(
            request.user
        )

        if not subscription:
            return False

        return subscription.plan.ai_matching


class HasAIInterviewEvaluation(BasePermission):

    message = (
        "AI interview evaluation requires a "
        "subscription that includes this feature."
    )

    def has_permission(self, request, view):

        subscription = get_active_subscription(
            request.user
        )

        if not subscription:
            return False

        return subscription.plan.ai_interview_evaluation


class HasUnlimitedJobPosts(BasePermission):

    message = (
        "Unlimited job posting requires a "
        "subscription that includes unlimited job posts."
    )

    def has_permission(self, request, view):

        subscription = get_active_subscription(
            request.user
        )

        if not subscription:
            return False

        return subscription.plan.unlimited_job_posts


class HasUnlimitedCandidateAccess(BasePermission):

    message = (
        "Unlimited candidate access requires "
        "an eligible subscription."
    )

    def has_permission(self, request, view):

        subscription = get_active_subscription(
            request.user
        )

        if not subscription:
            return False

        return subscription.unlimited_candidate_access