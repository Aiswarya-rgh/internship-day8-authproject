from django.http import JsonResponse

from .permissions import get_active_subscription


class PremiumAccessMiddleware:
    """
    Blocks access to URLs that require a paid/active subscription.

    Only URLs listed in PREMIUM_PATHS are protected.
    """

    PREMIUM_PATHS = [
    # Premium analytics
    "/api/analytics/funnel/",
    "/api/analytics/job-performance/",
    "/api/analytics/conversion/",
    "/api/analytics/time-stats/",
    "/api/analytics/role-metrics/",

    # AI matching
    "/api/applications/matching-jobs/",
    "/api/applications/skill-suggestions/",

    # AI interview features
    "/api/applications/start-interview/",
    "/api/applications/submit-answer/",
    "/api/applications/scores/",
    "/api/applications/next-question/",
    "/api/applications/save-transcript/",

    # Premium candidate report
    "/api/applications/candidate-report/",
]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Only protect configured premium URLs
        is_premium_url = any(
            request.path.startswith(path)
            for path in self.PREMIUM_PATHS
        )

        if not is_premium_url:
            return self.get_response(request)

        # Authentication check
        if not request.user.is_authenticated:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Authentication required."
                },
                status=401
            )

        # Subscription check
        subscription = get_active_subscription(request.user)

        if not subscription:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Active subscription required."
                },
                status=403
            )

        return self.get_response(request)