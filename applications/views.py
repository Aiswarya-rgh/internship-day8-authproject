from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Application
from .serializers import (
    ApplicationSerializer,
    ApplicationHistorySerializer,
)
from jobs.serializers import JobListSerializer

from jobs.models import Job
from accounts.permissions import IsCandidate


class ApplyJobAPIView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def post(self, request, *args, **kwargs):

        job_id = request.data.get("job")

        # Check if job exists
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Job not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Logged-in candidate
        candidate = request.user.candidate_profile

        # Check if job is open
        if job.status != "Open":
            return Response(
                {
                    "success": False,
                    "message": "This job is closed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prevent duplicate applications
        if Application.objects.filter(
            candidate=candidate,
            job=job
        ).exists():
            return Response(
                {
                    "success": False,
                    "message": "You have already applied for this job."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create application
        application = Application.objects.create(
            candidate=candidate,
            job=job,
            resume_snapshot=candidate.resume
        )

        serializer = ApplicationSerializer(application)

        return Response(
            {
                "success": True,
                "message": "Job applied successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
class ApplicationHistoryAPIView(generics.ListAPIView):

    serializer_class = ApplicationHistorySerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def get_queryset(self):

        candidate = self.request.user.candidate_profile

        return Application.objects.filter(
            candidate=candidate
        )
    
class AppliedJobListAPIView(generics.ListAPIView):

    serializer_class = JobListSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def get_queryset(self):

        candidate = self.request.user.candidate_profile

        return Job.objects.filter(
            applications__candidate=candidate
        )