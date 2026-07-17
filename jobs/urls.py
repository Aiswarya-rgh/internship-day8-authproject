from django.urls import path
from .views import (
    JobCreateAPIView,
    JobUpdateAPIView,
    JobListAPIView,
    JobStatusAPIView,
    PublicJobListAPIView,
    FeaturedJobListAPIView,
    LatestJobListAPIView,
    AdminJobListAPIView,
    AdminJobStatusAPIView,
    AdminDeleteJobAPIView,

)
urlpatterns = [
    path("create/",JobCreateAPIView.as_view()),
    path("list/",JobListAPIView.as_view()),
    path("edit/<int:pk>/",JobUpdateAPIView.as_view()),
    path("status/<int:pk>/", JobStatusAPIView.as_view()),
    path("public/",PublicJobListAPIView.as_view()),
    path("featured/",FeaturedJobListAPIView.as_view()),
    path("latest/", LatestJobListAPIView.as_view()),
    path("admin/jobs/",AdminJobListAPIView.as_view(),name="admin-job-list",),
    path("admin/jobs/<int:pk>/delete/",AdminDeleteJobAPIView.as_view(),name="admin-delete-job",),
    path("admin/jobs/<int:pk>/status/",AdminJobStatusAPIView.as_view(),name="admin-job-status",),
]
























