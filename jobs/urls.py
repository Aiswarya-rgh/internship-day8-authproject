from django.urls import path
from .views import (
    JobCreateAPIView,
    JobUpdateAPIView,
    JobListAPIView,
    JobStatusAPIView,
    PublicJobListAPIView,
)
urlpatterns = [
    path("create/",JobCreateAPIView.as_view()),
    path("list/",JobListAPIView.as_view()),
    path("edit/<int:pk>/",JobUpdateAPIView.as_view()),
    path("status/<int:pk>/", JobStatusAPIView.as_view()),
    path("public/",PublicJobListAPIView.as_view()),
]