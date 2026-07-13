from django.urls import path
from .views import (
    ApplyJobAPIView,
    ApplicationHistoryAPIView,
    AppliedJobListAPIView,
)


urlpatterns = [
    path("apply/",ApplyJobAPIView.as_view()),
    path("history/",ApplicationHistoryAPIView.as_view()),
    path(
    "applied-jobs/",
    AppliedJobListAPIView.as_view()
),
]
