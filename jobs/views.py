from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from accounts.permissions import IsEmployer
from .models import Job
from .serializers import (
    JobSerializer,
    JobListSerializer,)

# Create your views here.
class JobCreateAPIView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated,IsEmployer]
    
    def perform_create(self, serializer):
        serializer.save(
            employer=self.request.user.employer_profile
        )

class JobListAPIView(generics.ListAPIView):
    serializer_class =  JobSerializer
    permission_classes = [IsAuthenticated,IsEmployer]
    def get_queryset(self):
        return Job.objects.filter(
            employer=self.request.user.employer_profile
        )
    
class JobUpdateAPIView(generics.UpdateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated,IsEmployer]
    queryset = Job.objects.all()
    def get_queryset(self):
        return Job.objects.filter(
            employer=self.request.user.employer_profile
        )

class JobStatusAPIView(generics.UpdateAPIView):

    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        return Job.objects.filter(
            employer=self.request.user.employer_profile
        )

    def patch(self, request, *args, **kwargs):
        job = self.get_object()

        if job.status == "Open":
            job.status = "Closed"
        else:
            job.status = "Open"

        job.save()

        return Response({
            "message": f"Job status changed to {job.status}"
        })

class PublicJobListAPIView(generics.ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = [IsAuthenticated]

    queryset = Job.objects.filter(status="Open")

    filter_backends = [DjangoFilterBackend,SearchFilter]

    filterset_fields = [
        "location",
        "job_type",
        "experience",
    ]

    search_fields = [
        "title",
        "description",
        "skills"
    ]

    def get_queryset(self):
        queryset = Job.objects.filter(status="Open")
        skill = self.request.query_params.get("skill")
        if skill:
            queryset = queryset.filter(
                skills__icontains=skill
            )
        salary = self.request.query_params.get("salary")
        if salary:
            queryset = queryset.filter(
                salary_min__lte=salary,
                salary_max__gte=salary
            )
        return queryset

class FeaturedJobListAPIView(generics.ListAPIView):

    serializer_class = JobListSerializer
    permission_classes = [IsAuthenticated]

    queryset = Job.objects.filter(
        status="Open",
        featured=True
    )

class LatestJobListAPIView(generics.ListAPIView):

    serializer_class = JobListSerializer
    permission_classes = [IsAuthenticated]

    queryset = Job.objects.filter(
        status="Open"
    ).order_by("-created_at")

