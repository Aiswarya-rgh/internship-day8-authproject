from datetime import timedelta
from django.core.cache import cache
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status

from accounts.models import CustomUser
from jobs.models import Job
from billing.models import SubscriptionPlan, UserSubscription


class JobFlowTests(APITestCase):

    def setUp(self):
        cache.clear()

        self.employer = CustomUser.objects.create_user(
            username="employer1",
            email="employer@gmail.com",
            phone="9876543210",
            role="Employer",
            password="Employer@123"
        )

        plan = SubscriptionPlan.objects.create(
            name=SubscriptionPlan.PRO,
            job_post_limit=10,
            unlimited_job_posts=False,
        )

        UserSubscription.objects.create(
            user=self.employer,
            plan=plan,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            status=UserSubscription.ACTIVE,
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

    def test_employer_create_job(self):

        response = self.client.post(
            "/api/jobs/create/",
            {
                "title": "Python Developer",
                "description": "Backend Development",
                "skills": "Python,Django",
                "experience": 2,
                "salary_min": "30000.00",
                "salary_max": "50000.00",
                "location": "Kochi",
                "job_type": "Full Time"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Job.objects.count(),
            1
        )

        self.assertEqual(
            Job.objects.first().title,
            "Python Developer"
        )

    
    def test_candidate_can_view_public_jobs(self):

     employer = CustomUser.objects.create_user(
        username="employer2",
        email="emp2@gmail.com",
        phone="9876543211",
        role="Employer",
        password="Employer@123"
    )

     Job.objects.create(
        employer=employer.employer_profile,
        title="Python Developer",
        description="Backend",
        skills="Python,Django",
        experience=2,
        salary_min=30000,
        salary_max=50000,
        location="Kochi",
        job_type="Full Time",
        status="Open"
    )

     candidate = CustomUser.objects.create_user(
        username="candidate1",
        email="candidate@gmail.com",
        phone="9999999999",
        role="Candidate",
        password="Candidate@123"
    )

     login = self.client.post(
        "/api/login/",
        {
            "username": "candidate1",
            "password": "Candidate@123"
        },
        format="json"
    )

     token = login.data["access"]

     self.client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )

     response = self.client.get("/api/jobs/public/")

     self.assertEqual(response.status_code, status.HTTP_200_OK)
     self.assertEqual(response.data["count"], 1)
