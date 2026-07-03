from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    ADMIN = "Admin"
    EMPLOYER = "Employer"
    CANDIDATE = "Candidate"
    ROLE_CHOICES = (
        (ADMIN, "Admin"),
        (EMPLOYER, "Employer"),
        (CANDIDATE, "Candidate"),
    )
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=15)
    role=models.CharField(max_length=20,choices=ROLE_CHOICES)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.email
    
class Employer(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="employer_profile"
    )

    company_name = models.CharField(max_length=200, blank=True)
    company_location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.email 

class Candidate(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="candidate_profile"
    )

    skills = models.TextField(blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    def __str__(self):
        return self.user.email