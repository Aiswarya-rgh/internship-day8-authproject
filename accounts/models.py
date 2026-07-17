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
    is_flagged = models.BooleanField(default=False)
    def __str__(self):
        return self.email
    
class Employer(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="employer_profile"
    )

    company_location = models.CharField(max_length=200, blank=True)
          #day 11 additional  fields 
    company_name=models.CharField(max_length=200,blank=True)
    company_domain=models.CharField(max_length=200,blank=True)
    company_size=models.CharField(max_length=100,blank=True)
    is_company_verified=models.BooleanField(default=False)

    def __str__(self):
        return self.user.email 

class Candidate(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="candidate_profile"
    )

    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
        #day 11 additional  fields 
    skills=models.TextField(blank=True)
    education=models.CharField(max_length=200,blank=True)
    experience=models.PositiveIntegerField(default=0)
    expected_salary=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    def __str__(self):
        return self.user.email
class AdminAuditLog(models.Model):

    admin = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    action = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin.email} - {self.action}"