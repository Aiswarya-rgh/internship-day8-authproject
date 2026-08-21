

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import CustomUser
from jobs.models import Job
from applications.models import Application
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache

class EmployerApplicationTests(APITestCase):
    def setUp(self):
        cache.clear()
    def test_employer_can_view_applicants(self):

        employer = CustomUser.objects.create_user(
            username="employer1",
            email="employer@gmail.com",
            phone="9999999999",
            role="Employer",
            password="Employer@123"
        )

        candidate = CustomUser.objects.create_user(
            username="candidate1",
            email="candidate@gmail.com",
            phone="8888888888",
            role="Candidate",
            password="Candidate@123"
        )

        job = Job.objects.create(

            employer=employer.employer_profile,

            title="Python Developer",

            description="Backend",

            skills="Python,Django",

            experience=2,

            salary_min=30000,

            salary_max=50000,

            location="Kochi",

            job_type="Full Time"

        )

        resume = SimpleUploadedFile(
            "resume.pdf",
            b"Dummy Resume",
            content_type="application/pdf"
        )

        Application.objects.create(

            candidate=candidate.candidate_profile,

            job=job,

            resume_snapshot=resume

        )

        login = self.client.post(

            "/api/login/",

            {

                "username": "employer1",

                "password": "Employer@123"

            },

            format="json"

        )

        token = login.data["access"]

        self.client.credentials(

            HTTP_AUTHORIZATION=f"Bearer {token}"

        )

        response = self.client.get(

            f"/api/applications/job/{job.id}/applicants/"

        )

        self.assertEqual(

            response.status_code,

            status.HTTP_200_OK

        )
