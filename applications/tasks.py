from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .reminder_service import ReminderService
from .models import NotificationLog
from .models import ReminderLog

from audit_logs.services import AuditLogService


@shared_task(bind=True, max_retries=3)
def send_email_task(
    self,
    subject,
    template_name,
    context,
    recipient_email
):

    try:

        message = render_to_string(
            template_name,
            context
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )

        NotificationLog.objects.create(
            recipient=recipient_email,
            subject=subject,
            status="Success"
        )

        # Centralized application log
        AuditLogService.application(
            action="Email sent successfully",
            description=f"Email subject: {subject}"
        )

        print("Email Sent Successfully")

    except Exception as e:

        NotificationLog.objects.create(
            recipient=recipient_email,
            subject=subject,
            status="Failed",
            error_message=str(e)
        )

        # Centralized error log
        AuditLogService.error(
            action="Email sending failed",
            exception=e
        )

        # Centralized retry log
        AuditLogService.retry(
            action="Email retry",
            failure_reason=str(e)
        )

        print("Retrying Email...")

        raise self.retry(
            exc=e,
            countdown=2
        )


@shared_task(bind=True, max_retries=3)
def send_interview_reminders(self):

    reminders = ReminderService.get_pending_reminders()

    for interview, reminder_type in reminders:

        try:

            from .email_service import InterviewEmailService

            InterviewEmailService.send_reminder(
                interview,
                reminder_type
            )

            # Existing reminder log
            ReminderLog.objects.create(
                interview=interview,
                reminder_type=reminder_type,
                status="Success"
            )

            # Centralized AI/event log
            AuditLogService.ai_event(
                action="Interview reminder sent",
                description=f"Reminder type: {reminder_type}"
            )

        except Exception as exc:

            # Existing failure log
            ReminderLog.objects.create(
                interview=interview,
                reminder_type=reminder_type,
                status="Failed",
                failure_reason=str(exc)
            )

            # Centralized error log
            AuditLogService.error(
                action="Interview reminder failed",
                exception=exc
            )

            # Centralized retry log
            AuditLogService.retry(
                action="Interview reminder retry",
                failure_reason=str(exc)
            )

            raise self.retry(
                exc=exc,
                countdown=60
            )