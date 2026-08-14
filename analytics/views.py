from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from billing.permissions import HasPremiumAnalytics

from .services import AnalyticsService


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