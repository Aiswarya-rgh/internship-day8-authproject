from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Q
from .email_service import send_notification_email

from .models import Application,SavedJob
from .serializers import (
    ApplicationSerializer,
    ApplicationHistorySerializer,
    ApplicationStatusSerializer,
    SavedJobSerializer,
)

from jobs.models import Job
from jobs.serializers import JobListSerializer

from accounts.permissions import IsCandidate, IsEmployer,IsAdmin
from accounts.models import CustomUser, Employer, Candidate

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
class ApplicantListAPIView(generics.ListAPIView):

    serializer_class = ApplicationHistorySerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    search_fields = ["candidate__user__username"]

    def get_queryset(self):

        job_id = self.kwargs["job_id"]

        return Application.objects.filter(
            job__id=job_id,
            job__employer=self.request.user.employer_profile
        )

from rest_framework.views import APIView

class EmployerDashboardAPIView(APIView):

    permission_classes = [IsAuthenticated, IsEmployer]

    def get(self, request):

        employer = request.user.employer_profile

        jobs = Job.objects.filter(employer=employer)

        total_jobs = jobs.count()

        total_applications = Application.objects.filter(
            job__employer=employer
        ).count()

        shortlisted = Application.objects.filter(
            job__employer=employer,
            status="Shortlisted"
        ).count()

        if total_applications > 0:
            shortlist_ratio = round(
                (shortlisted / total_applications) * 100,
                2
            )
        else:
            shortlist_ratio = 0

        return Response({
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "shortlisted_candidates": shortlisted,
            "shortlist_ratio": f"{shortlist_ratio}%"
        })
class SaveJobAPIView(generics.CreateAPIView):

    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def post(self, request):

        candidate = request.user.candidate_profile
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

        if SavedJob.objects.filter(
            candidate=candidate,
            job=job
        ).exists():
            return Response(
                {
                    "success": False,
                    "message": "Job already saved."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        saved_job = SavedJob.objects.create(
            candidate=candidate,
            job=job
        )

        serializer = SavedJobSerializer(saved_job)

        return Response(
            {
                "success": True,
                "message": "Job saved successfully.",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
class SavedJobListAPIView(generics.ListAPIView):

    serializer_class = SavedJobSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def get_queryset(self):

        return SavedJob.objects.filter(
            candidate=self.request.user.candidate_profile
        )
class InterviewStatusAPIView(generics.ListAPIView):

    serializer_class = ApplicationHistorySerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def get_queryset(self):

        candidate = self.request.user.candidate_profile

        return Application.objects.filter(
            candidate=candidate,
            status="Interview Scheduled"
        )
class MatchingJobsAPIView(generics.ListAPIView):

    serializer_class = JobListSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def get_queryset(self):

        candidate = self.request.user.candidate_profile

        skills = candidate.skills

        return Job.objects.filter(
            status="Open",
            skills__icontains=skills
        )


class SkillSuggestionAPIView(generics.ListAPIView):

    serializer_class = JobListSerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def get_queryset(self):

        candidate = self.request.user.candidate_profile

        skills = [
            skill.strip()
            for skill in candidate.skills.split(",")
            if skill.strip()
        ]

        query = Q()

        for skill in skills:
            query |= Q(skills__icontains=skill)

        return Job.objects.filter(
            status="Open"
        ).filter(query).distinct()
class ApplicationTimelineAPIView(generics.ListAPIView):

    serializer_class = ApplicationHistorySerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def get_queryset(self):

        return Application.objects.filter(
            candidate=self.request.user.candidate_profile
        ).order_by("-applied_at")
class StatusNotificationAPIView(generics.ListAPIView):

    serializer_class = ApplicationHistorySerializer
    permission_classes = [IsAuthenticated, IsCandidate]

    def get_queryset(self):

        return Application.objects.filter(
            candidate=self.request.user.candidate_profile
        ).exclude(
            status="Applied"
        )
class PlatformStatsAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):

        return Response({
            "total_users": CustomUser.objects.count(),
            "total_employers": Employer.objects.count(),
            "total_candidates": Candidate.objects.count(),
            "total_jobs": Job.objects.count(),
            "total_applications": Application.objects.count(),
        })
class UserGrowthAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):

        return Response({
            "total_users": CustomUser.objects.count(),
            "total_employers": Employer.objects.count(),
            "total_candidates": Candidate.objects.count(),
        })
class JobActivityAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):

        total_jobs = Job.objects.count()

        open_jobs = Job.objects.filter(
            status="Open"
        ).count()

        closed_jobs = Job.objects.filter(
            status="Closed"
        ).count()

        total_applications = Application.objects.count()

        return Response({
            "total_jobs": total_jobs,
            "open_jobs": open_jobs,
            "closed_jobs": closed_jobs,
            "total_applications": total_applications
        })

class RankedCandidatesAPIView(APIView):

    permission_classes = [IsAuthenticated, IsEmployer]

    def get(self, request, job_id):

        employer = request.user.employer_profile

        applications = (
            Application.objects
            .filter(job__id=job_id, job__employer=employer)
            .order_by("-ats_score")
        )

        data = []

        for application in applications:

            data.append({

                "candidate": application.candidate.user.email,

                "status": application.status,

                "ats_score": application.ats_score

            })

        return Response(data)
class BatchATSProcessingAPIView(APIView):

    permission_classes = [IsAuthenticated, IsEmployer]

    def post(self, request):

        applications = Application.objects.filter(
            status="Applied"
        )

        count = applications.count()

        return Response({
            "success": True,
            "message": f"{count} applications processed successfully."
        })
class EmployerOverrideAPIView(APIView):

    permission_classes = [IsAuthenticated, IsEmployer]

    def patch(self, request, application_id):

        try:

            application = Application.objects.get(
                id=application_id,
                job__employer=request.user.employer_profile
            )

        except Application.DoesNotExist:

            return Response(
                {"message": "Application not found."},
                status=404
            )

        application.status = request.data.get("status")

        application.save()

        return Response({

            "success": True,

            "message": "Application status updated manually.",

            "status": application.status

        })
class EmployerApplicantListAPIView(APIView):

    permission_classes = [IsAuthenticated, IsEmployer]

    def get(self, request, job_id):

        employer = request.user.employer_profile

        applications = (
            Application.objects
            .filter(
                job__id=job_id,
                job__employer=employer
            )
            .select_related(
                "candidate__user",
                "job"
            )
            .order_by("-ats_score")
        )

        applicants = []

        for application in applications:

            applicants.append({

                "candidate": application.candidate.user.email,

                "job": application.job.title,

                "status": application.status,

                "ats_score": application.ats_score,

                "applied_at": application.applied_at,

                "resume": application.resume_snapshot.url
                if application.resume_snapshot else None

            })

        return Response({

            "success": True,

            "message": "Applicants fetched successfully.",

            "count": len(applicants),

            "data": applicants

        })


class TestEmailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        send_notification_email(

            subject="Application Submitted",

            template_name="emails/application_submitted.txt",

            context={
                "candidate_name": request.user.username,
                "job_title": "Python Developer"
            },

            recipient_email=request.user.email
            

        )

        return Response({
            "success": True,
            "message": "Application email sent successfully."
        })
    