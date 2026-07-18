from django.urls import path

from .views import (RegisterAPIView, ProfileAPIView,ResumeUploadAPIView,EmployerDashboard,CandidateDashboard,AdminDashboard,EmployerProfileAPIView,CandidateProfileAPIView,CandidateListAPIView,UserListAPIView,ApproveEmployerAPIView,BlockUserAPIView,FlagUserAPIView,AdminAuditLogAPIView,ResumeTextAPIView,)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path("signup/", RegisterAPIView.as_view()),

    path("login/", TokenObtainPairView.as_view()),

    path("refresh/", TokenRefreshView.as_view()),

    path("profile/", ProfileAPIView.as_view()),

    path("employer/", EmployerDashboard.as_view()),

    path("candidate/", CandidateDashboard.as_view()),

    path("admin-panel/", AdminDashboard.as_view()),

    path("employer-profile/", EmployerProfileAPIView.as_view()),

    path("candidate-profile/", CandidateProfileAPIView.as_view()),

    path("upload-resume/",ResumeUploadAPIView.as_view()),

    path("candidates/",CandidateListAPIView.as_view()),

    path("users/",UserListAPIView.as_view()),

    path("approve-employer/<int:pk>/",ApproveEmployerAPIView.as_view(),name="approve-employer",),

    path("block-user/<int:pk>/",BlockUserAPIView.as_view(),name="block-user",),
    
    path("flag-user/<int:pk>/",FlagUserAPIView.as_view(),name="flag-user",),
    
    path("admin-audit-logs/",AdminAuditLogAPIView.as_view(),name="admin-audit-logs",),

    path("resume-text/",ResumeTextAPIView.as_view(),name="resume-text",),
]

