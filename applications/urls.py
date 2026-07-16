from django.urls import path
from .views import (
    ApplyJobAPIView,
    ApplicationHistoryAPIView,
    AppliedJobListAPIView,
    UpdateApplicationStatusAPIView,
    ApplicantListAPIView,
    EmployerDashboardAPIView,
    SavedJobListAPIView,
    SaveJobAPIView,
    InterviewStatusAPIView,
    MatchingJobsAPIView,
    SkillSuggestionAPIView,
    ApplicationTimelineAPIView,
    StatusNotificationAPIView,
)


urlpatterns = [
    path("apply/",ApplyJobAPIView.as_view()),
    path("history/",ApplicationHistoryAPIView.as_view()),
    path("applied-jobs/",AppliedJobListAPIView.as_view()),
    path("status/<int:pk>/",UpdateApplicationStatusAPIView.as_view()),
    path("job/<int:job_id>/applicants/",ApplicantListAPIView.as_view()),
    path("employer-dashboard/",EmployerDashboardAPIView.as_view()),
    path("save-job/",SaveJobAPIView.as_view(),name="save-job",),
    path("saved-jobs/",SavedJobListAPIView.as_view(),name="saved-jobs",),
    path("interview-status/",InterviewStatusAPIView.as_view(),name="interview-status",),
    path("matching-jobs/",MatchingJobsAPIView.as_view(),name="matching-jobs",),
    path("skill-suggestions/",SkillSuggestionAPIView.as_view(),name="skill-suggestions",),
    path("timeline/",ApplicationTimelineAPIView.as_view(),name="application-timeline",),
    path("notifications/",StatusNotificationAPIView.as_view(),name="status-notifications",),
    
]
