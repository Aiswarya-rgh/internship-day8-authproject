from django.db import models
from django.conf import settings


class AuditLog(models.Model):

    EVENT_TYPES = (
        ("APPLICATION", "Application"),
        ("ERROR", "Error"),
        ("AI", "AI Event"),
        ("USER", "User Action"),
        ("ADMIN", "Admin Action"),
        ("RETRY", "Retry"),
        ("SECURITY", "Security"),
    )

    STATUS_CHOICES = (
        ("SUCCESS", "Success"),
        ("FAILED", "Failed"),
        ("WARNING", "Warning"),
    )

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES
    )

    action = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="SUCCESS"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs"
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    failure_reason = models.TextField(
        blank=True,
        null=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    endpoint = models.CharField(
        max_length=500,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["event_type"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.event_type} - {self.action} - {self.status}"