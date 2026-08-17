from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from billing.permissions import HasPremiumAnalytics

from .services import AnalyticsService
from accounts.permissions import IsEmployer
from security_hardening.throttles import PremiumAPIRateThrottle

class FunnelAPIView(APIView):

    permission_classes = [IsAuthenticated,HasPremiumAnalytics]

    def get(self, request):

        return Response({

            "success": True,

            "data": AnalyticsService.get_funnel_metrics()

        })


class JobPerformanceAPIView(APIView):

    permission_classes = [
    IsAuthenticated,
    HasPremiumAnalytics,
]

    def get(self, request):

        return Response({

            "success": True,

            "data": AnalyticsService.get_job_performance()

        })


class ConversionAPIView(APIView):

    permission_classes = [
    IsAuthenticated,
    HasPremiumAnalytics,
]

    def get(self, request):

        return Response({

            "success": True,

            "data": AnalyticsService.get_conversion_ratio()

        })


class TimeStatsAPIView(APIView):

    permission_classes = [IsAuthenticated,HasPremiumAnalytics]

    def get(self, request):

        return Response({

            "success": True,

            "data": AnalyticsService.get_time_based_stats()

        })


class RoleMetricsAPIView(APIView):

    permission_classes = [
    IsAuthenticated,
    HasPremiumAnalytics,
]

    def get(self, request):

        return Response({

            "success": True,

            "data": AnalyticsService.get_role_based_metrics()

        })

class AdvancedRecruiterAnalyticsAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsEmployer,
        HasPremiumAnalytics,
    ]

    def get(self, request):

        employer = request.user.employer_profile

        data = AnalyticsService.get_advanced_recruiter_analytics(
            employer
        )

        return Response(
            {
                "success": True,
                "report_type": "ADVANCED_RECRUITER_ANALYTICS",
                "data": data,
            }
        )


class RecruiterPremiumReportAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsEmployer,
        HasPremiumAnalytics,
    ]

    throttle_classes = [
        PremiumAPIRateThrottle,
    ]

    def get(self, request):

        employer = request.user.employer_profile

        hiring_efficiency = (
            AnalyticsService
            .get_hiring_efficiency_metrics(employer)
        )

        candidate_predictions = (
            AnalyticsService
            .get_candidate_success_predictions(employer)
        )

        return Response({
            "success": True,
            "report_type": "PREMIUM_RECRUITER_REPORT",
            "data": {
                "hiring_efficiency": hiring_efficiency,
                "candidate_success_predictions": (
                    candidate_predictions
                ),
            },
        })