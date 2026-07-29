from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .models import NotificationLog

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