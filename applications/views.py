from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Application
from .serializers import (
    ApplicationSerializer,
    ApplicationHistorySerializer,
    ApplicationStatusSerializer,
)

from jobs.models import Job
from jobs.serializers import JobListSerializer

from accounts.permissions import IsCandidate, IsEmployer


class ApplyJobAPIView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def post(self, request, *args, **kwargs):

        job_id = request.data.get("job")

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

        candidate = request.user.candidate_profile

        if job.status != "Open":
            return Response(
                {
                    "success": False,
                    "message": "This job is closed."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

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


class UpdateApplicationStatusAPIView(generics.UpdateAPIView):

    serializer_class = ApplicationStatusSerializer
    permission_classes = [IsAuthenticated, IsEmployer]
    queryset = Application.objects.all()

    def update(self, request, *args, **kwargs):

        application = self.get_object()

        new_status = request.data.get("status")

        allowed_transitions = {
            "Applied": [
                "Shortlisted",
                "Rejected"
            ],
            "Shortlisted": [
                "Interview Scheduled",
                "Rejected"
            ],
            "Interview Scheduled": [
                "Selected",
                "Rejected"
            ],
            "Selected": [],
            "Rejected": []
        }

        current_status = application.status

        if new_status not in allowed_transitions[current_status]:
            return Response(
                {
                    "success": False,
                    "message": f"Cannot move from {current_status} to {new_status}."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        application.status = new_status

        print(
            f"Employer {request.user.username} changed "
            f"Application {application.id} "
            f"status from {current_status} to {new_status}"
        )

        application.save()

        serializer = self.get_serializer(application)

        return Response(
            {
                "success": True,
                "message": "Application status updated successfully.",
                "data": serializer.data
            }
        )