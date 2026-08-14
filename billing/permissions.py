from django.utils import timezone

from rest_framework.permissions import BasePermission

from .models import UserSubscription


class HasActiveSubscription(BasePermission):
    """
    Allows access only when the user has an active subscription.
    """

    message = "An active subscription is required to access this feature."

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return UserSubscription.objects.filter(
            user=request.user,
            status=UserSubscription.ACTIVE,
            end_date__gt=timezone.now(),
        ).exists()


class HasPremiumAnalytics(BasePermission):
    """
    Allows access only to users whose active plan
    includes premium analytics.
    """

    message = "Premium analytics requires a paid subscription."

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return UserSubscription.objects.filter(
            user=request.user,
            status=UserSubscription.ACTIVE,
            end_date__gt=timezone.now(),
            plan__premium_analytics=True,
        ).exists()


class HasAIAnalytics(BasePermission):
    """
    Enterprise-level AI analytics access.
    """

    message = "AI analytics requires an Enterprise subscription."

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return UserSubscription.objects.filter(
            user=request.user,
            status=UserSubscription.ACTIVE,
            end_date__gt=timezone.now(),
            plan__ai_analytics=True,
        ).exists()

class HasAIAnalytics(BasePermission):
    message = "AI analytics requires an Enterprise subscription."

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return UserSubscription.objects.filter(
            user=request.user,
            status=UserSubscription.ACTIVE,
            end_date__gt=timezone.now(),
            plan__ai_analytics=True,
        ).exists()
class HasAIMatching(BasePermission):
    """
    Allows access only to users whose active subscription
    includes AI matching.
    """

    message = "AI matching requires a subscription that includes AI matching."

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return UserSubscription.objects.filter(
            user=request.user,
            status=UserSubscription.ACTIVE,
            end_date__gt=timezone.now(),
            plan__ai_matching=True,
        ).exists()

class HasAIInterviewEvaluation(BasePermission):
    """
    Allows access only to users whose active subscription
    includes AI interview evaluation.
    """

    message = "AI interview evaluation requires a subscription that includes this feature."

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return UserSubscription.objects.filter(
            user=request.user,
            status=UserSubscription.ACTIVE,
            end_date__gt=timezone.now(),
            plan__ai_interview_evaluation=True,
        ).exists()