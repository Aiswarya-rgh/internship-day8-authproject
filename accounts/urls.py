from django.urls import path

from .views import (RegisterAPIView, ProfileAPIView,EmployerDashboard,CandidateDashboard,AdminDashboard,EmployerProfileAPIView,CandidateProfileAPIView,)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterAPIView,
    ProfileAPIView,
    EmployerDashboard,
    CandidateDashboard,
    AdminDashboard,
    ResumeUploadAPIView
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


]