from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .reminder_service import ReminderService


from .models import NotificationLog
from .models import ReminderLog
import time


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

        print("Email Sent Successfully")

    except Exception as e:

        NotificationLog.objects.create(
            recipient=recipient_email,
            subject=subject,
            status="Failed",
            error_message=str(e)
        )

        print("Retrying Email...")

        raise self.retry(
            exc=e,
            countdown=2
        )
from celery import shared_task


@shared_task(bind=True, max_retries=3)
def send_interview_reminders(self):

    from .email_service import InterviewEmailService


    reminders = ReminderService.get_pending_reminders()

    for interview, reminder_type in reminders:

        try:

            InterviewEmailService.send_reminder(
                interview,
                reminder_type
            )

            # Success Log
            ReminderLog.objects.create(
                interview=interview,
                reminder_type=reminder_type,
                status="Success"
            )

        except Exception as exc:

            # Failure Log
            ReminderLog.objects.create(
                interview=interview,
                reminder_type=reminder_type,
                status="Failed",
                failure_reason=str(exc)
            )

            raise self.retry(
                exc=exc,
                countdown=60
            )

