from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import NotificationLog

import threading
import time


def send_email_background(
    subject,
    template_name,
    context,
    recipient_email
):

    retries = 3

    while retries > 0:

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

            return

        except Exception as e:

            NotificationLog.objects.create(
                recipient=recipient_email,
                subject=subject,
                status="Failed",
                error_message=str(e)
            )

            retries -= 1

            print(f"Retry Left: {retries}")

            time.sleep(2)

    print("Email Sending Failed")


def send_notification_email(
    subject,
    template_name,
    context,
    recipient_email
):

    thread = threading.Thread(
        target=send_email_background,
        args=(
            subject,
            template_name,
            context,
            recipient_email,
        ),
        daemon=True
    )

    thread.start()