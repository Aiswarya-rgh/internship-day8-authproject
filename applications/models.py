from django.db import models
from accounts.models import Candidate
from jobs.models import Job

# Create your models here.
class Application(models.Model):
    APPLIED = "Applied"
    REVIEWING = "Reviewing"
    SHORTLISTED = "Shortlisted"
    REJECTED = "Rejected"
    HIRED = "Hired"

    STATUS_CHOICES = (
        (APPLIED,"Applied"),
        (REVIEWING,"Reviewing"),
        (SHORTLISTED,"Shortlisted"),
        (REJECTED,"Rejected"),
        (HIRED,"Hired")
    )
    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE,related_name="applications")
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name="applications")
    resume_snapshot = models.FileField(upload_to="application_resumes/")
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=APPLIED)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate.user.username} - {self.job.title}"