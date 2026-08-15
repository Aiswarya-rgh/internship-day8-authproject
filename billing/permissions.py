from django.utils import timezone

from rest_framework.permissions import BasePermission

from .models import UserSubscription


class HasActiveSubscription(BasePermission):

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

    message = (
        "AI interview evaluation requires a subscription "
        "that includes this feature."
    )

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return UserSubscription.objects.filter(
            user=request.user,
            status=UserSubscription.ACTIVE,
            end_date__gt=timezone.now(),
            plan__ai_interview_evaluation=True,
        ).exists()