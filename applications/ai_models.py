from django.db import models
from accounts.models import Candidate
from jobs.models import Job


class AIInterviewSession(models.Model):

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE
    )

    session_id = models.CharField(
        max_length=100,
        unique=True
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    ended_at = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        default="In Progress"
    )

    transcript = models.JSONField(
       default=dict,
       blank=True
    )

    def __str__(self):
        return self.session_id


class AIQuestion(models.Model):

    session = models.ForeignKey(
        AIInterviewSession,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question_text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.question_text[:40]


class AIAnswer(models.Model):

    question = models.ForeignKey(
        AIQuestion,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    answer_text = models.TextField()

    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.answer_text[:40]


class CallLog(models.Model):

    session = models.OneToOneField(
        AIInterviewSession,
        on_delete=models.CASCADE
    )

    triggered_by = models.CharField(
        max_length=100
    )

    trigger_reason = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=30,
        default="Queued"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.session.session_id