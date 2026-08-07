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
    PlatformStatsAPIView,
    UserGrowthAPIView,
    JobActivityAPIView,
    RankedCandidatesAPIView,
    BatchATSProcessingAPIView,
    EmployerOverrideAPIView,
    EmployerApplicantListAPIView,
    TestEmailAPIView,
  
    
)

from .transcript_views import (
    SaveTranscriptAPIView,

)

from .interview_views import (
    StartInterviewAPIView,
    SubmitAnswerAPIView,
    RetrieveScoreAPIView,
    NextQuestionAPIView,
)
from .report_views import CandidateReportAPIView
from .scheduling_views import ScheduleInterviewAPIView,RescheduleInterviewAPIView,ConfirmInterviewAPIView
from .reminder_views import ReminderLogAPIView

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
    path("admin/platform-stats/",PlatformStatsAPIView.as_view(),name="platform-stats",), 
    path("admin/user-growth/",UserGrowthAPIView.as_view(),name="user-growth",),
    path("admin/job-activity/",JobActivityAPIView.as_view(),name="job-activity",),
    path("job/<int:job_id>/ranking/",RankedCandidatesAPIView.as_view(),name="ranked-candidates",),
    path("process-batch/",BatchATSProcessingAPIView.as_view()),
    path("applications/<int:application_id>/override/",EmployerOverrideAPIView.as_view()),
    path("job/<int:job_id>/applicants/",EmployerApplicantListAPIView.as_view()),
    path("test-email/",TestEmailAPIView.as_view(),name="test-email",),
    path("save-transcript/",SaveTranscriptAPIView.as_view()),
    path("submit-answer/",SubmitAnswerAPIView.as_view()),
    path("start-interview/<str:session_id>/",StartInterviewAPIView.as_view(),),
    path("submit-answer/",SubmitAnswerAPIView.as_view(),),
    path("scores/<int:session_id>/",RetrieveScoreAPIView.as_view(),),
    path("next-question/<str:session_id>/",NextQuestionAPIView.as_view(),),
    path("schedule-interview/",ScheduleInterviewAPIView.as_view()),
    path("reschedule-interview/",RescheduleInterviewAPIView.as_view(),name="reschedule-interview",),
    path("confirm-interview/",ConfirmInterviewAPIView.as_view(),name="confirm-interview",),
    path("reminder-logs/",ReminderLogAPIView.as_view(),name="reminder-logs"),
    path("candidate-report/<int:application_id>/",CandidateReportAPIView.as_view(),),

]
