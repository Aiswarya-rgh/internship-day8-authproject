from django.urls import path

from .views import (
    FunnelAPIView,
    JobPerformanceAPIView,
    ConversionAPIView,
    TimeStatsAPIView,
    RoleMetricsAPIView,
)

urlpatterns = [

    path(
        "funnel/",
        FunnelAPIView.as_view()
    ),

    path(
        "job-performance/",
        JobPerformanceAPIView.as_view()
    ),

    path(
        "conversion/",
        ConversionAPIView.as_view()
    ),

    path(
        "time-stats/",
        TimeStatsAPIView.as_view()
    ),

    path(
        "role-metrics/",
        RoleMetricsAPIView.as_view()
    ),
]