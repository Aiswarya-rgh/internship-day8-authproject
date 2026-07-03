from django.urls import path

from .views import RegisterAPIView, ProfileAPIView

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
)

urlpatterns = [

    path("signup/", RegisterAPIView.as_view()),

    path("login/", TokenObtainPairView.as_view()),

    path("refresh/", TokenRefreshView.as_view()),

    path("profile/", ProfileAPIView.as_view()),

    path("employer/", EmployerDashboard.as_view()),

    path("candidate/", CandidateDashboard.as_view()),

    path("admin-panel/", AdminDashboard.as_view()),

]