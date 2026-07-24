from django.db import models
from accounts.models import Candidate
from jobs.models import Job

# Create your models here.
class Application(models.Model):
    APPLIED = "Applied"
    SHORTLISTED = "Shortlisted"
    INTERVIEW = "Interview Scheduled"
    REJECTED = "Rejected"
    SELECTED = "Selected"

    STATUS_CHOICES = (
    (APPLIED, "Applied"),
    (SHORTLISTED, "Shortlisted"),
    (INTERVIEW, "Interview Scheduled"),
    (REJECTED, "Rejected"),
    (SELECTED, "Selected"),
)

    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE,related_name="applications")
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name="applications")
    resume_snapshot = models.FileField(upload_to="application_resumes/")
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=APPLIED)
    status_updated_at = models.DateTimeField(auto_now=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    ats_score = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    class Meta:

        unique_together = ("candidate", "job")

        indexes = [

            models.Index(fields=["candidate"]),

            models.Index(fields=["job"]),

            models.Index(fields=["status"]),

            models.Index(fields=["ats_score"]),

            models.Index(fields=["applied_at"]),

        ]

    def __str__(self):
        return f"{self.candidate.user.username} - {self.job.title}"

class SavedJob(models.Model):
    candidate = models.ForeignKey("accounts.Candidate",on_delete=models.CASCADE)
    job = models.ForeignKey("jobs.Job",on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["candidate","job"]
    
    def __str__(self):
        return f"{self.candidate.user.username} saved {self.job.title}"
    
   
class NotificationLog(models.Model):

    recipient = models.EmailField()

    subject = models.CharField(max_length=255)

    status = models.CharField(max_length=30)

    error_message = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        indexes = [

            models.Index(fields=["recipient"]),

            models.Index(fields=["status"]),

            models.Index(fields=["created_at"]),

        ]

    def __str__(self):

        return self.recipient          