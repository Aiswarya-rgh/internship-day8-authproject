from django.urls import path
from .views import (
    ApplyJobAPIView,
    ApplicationHistoryAPIView,
    AppliedJobListAPIView,
    UpdateApplicationStatusAPIView,
    ApplicantListAPIView,
    EmployerDashboardAPIView,

)


urlpatterns = [
    path("apply/",ApplyJobAPIView.as_view()),
    path("history/",ApplicationHistoryAPIView.as_view()),
    path("applied-jobs/",AppliedJobListAPIView.as_view()),
    path("status/<int:pk>/",UpdateApplicationStatusAPIView.as_view()),
    path("job/<int:job_id>/applicants/",ApplicantListAPIView.as_view()),
    path("employer-dashboard/",EmployerDashboardAPIView.as_view()
),
]
