from django.db import models
from accounts.models import Candidate
from jobs.models import Job
from .ai_models import *
from django.utils import timezone

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
    AI_QUEUED = "Queued"
    AI_PROGRESS = "In Progress"
    AI_COMPLETED = "Completed"
    AI_FAILED = "Failed"

    AI_STATUS_CHOICES = (
    (AI_QUEUED, "Queued"),
    (AI_PROGRESS, "In Progress"),
    (AI_COMPLETED, "Completed"),
    (AI_FAILED, "Failed"),
)

    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE,related_name="applications")
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name="applications")
    resume_snapshot = models.FileField(upload_to="application_resumes/")
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=APPLIED)
    status_updated_at = models.DateTimeField(auto_now=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    ats_score = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    ai_status = models.CharField(max_length=20,choices=AI_STATUS_CHOICES,default=AI_QUEUED)
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

class AIQuestionTemplate(models.Model):

    CATEGORY_CHOICES = (
        ("Introduction", "Introduction"),
        ("Experience", "Experience"),
        ("Skills", "Skills"),
        ("Availability", "Availability"),
        ("Salary", "Salary"),
    )

    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)

    question = models.TextField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.question[:40]}"

from jobs.models import Job

class JobQuestionMapping(models.Model):

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="question_mappings"
    )

    question = models.ForeignKey(
        AIQuestionTemplate,
        on_delete=models.CASCADE
    )

    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.job.title} -> {self.question.category}"

class AIAnswerEvaluation(models.Model):

    session = models.ForeignKey(
        AIInterviewSession,
        on_delete=models.CASCADE,
        related_name="evaluations"
    )

    question = models.ForeignKey(
        AIQuestionTemplate,
        on_delete=models.CASCADE
    )

    raw_answer = models.TextField()

    confidence_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    ai_annotation = models.TextField(
        blank=True,
        null=True
    )

    relevance_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    completeness_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    keyword_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    final_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.session.session_id} - {self.final_score}"

class AvailabilitySlot(models.Model):

    employer = models.ForeignKey(
        "accounts.Employer",
        on_delete=models.CASCADE,
        related_name="availability_slots"
    )

    role = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="available_slots"
    )

    available_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_booked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["available_date", "start_time"]

    def __str__(self):
        return f"{self.role.title} | {self.available_date} {self.start_time}"


class InterviewSchedule(models.Model):

    STATUS_CHOICES = (
        ("Scheduled", "Scheduled"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
        ("Rescheduled", "Rescheduled"),
    )

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name="interview_schedule"
    )

    slot = models.ForeignKey(
        AvailabilitySlot,
        on_delete=models.CASCADE,
        related_name="interviews"
    )

    scheduled_by = models.CharField(
        max_length=100,
        default="AI Scheduler"
    )

    confirmation_status = models.BooleanField(default=False)

    interview_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Scheduled"
    )

    scheduled_at = models.DateTimeField(
        default=timezone.now
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    reminder_24_sent = models.BooleanField(default=False)

    reminder_1hr_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.application.candidate.user.username} - {self.slot.available_date}"