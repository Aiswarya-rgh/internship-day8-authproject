# ************ only while using thread inteaqd of celery*************

# from django.core.mail import send_mail
# # from django.conf import settings
# # from django.template.loader import render_to_string
# # from .models import NotificationLog

# # import threading
# # import time


# # def send_email_background(
# #     subject,
# #     template_name,
# #     context,
# #     recipient_email
# # ):

# #     retries = 3

# #     while retries > 0:

# #         try:

# #             message = render_to_string(
# #                 template_name,
# #                 context
# #             )

# #             send_mail(
# #                 subject=subject,
# #                 message=message,
# #                 from_email=settings.DEFAULT_FROM_EMAIL,
# #                 recipient_list=[recipient_email],
# #                 fail_silently=False,
# #             )

# #             NotificationLog.objects.create(
# #                 recipient=recipient_email,
# #                 subject=subject,
# #                 status="Success"
# #             )

# #             print("Email Sent Successfully")

# #             return

# #         except Exception as e:

# #             NotificationLog.objects.create(
# #                 recipient=recipient_email,
# #                 subject=subject,
# #                 status="Failed",
# #                 error_message=str(e)
# #             )

# #             retries -= 1

# #             print(f"Retry Left: {retries}")

# #             time.sleep(2)

# #     print("Email Sending Failed")


# # def send_notification_email(
# #     subject,
# #     template_name,
# #     context,
# #     recipient_email
# # ):

# #     thread = threading.Thread(
# #         target=send_email_background,
# #         args=(
# #             subject,
# #             template_name,
# #             context,
# #             recipient_email,
# #         ),
# #         daemon=True
# #     )

# #     thread.start()

# ****using celery to send emqail*****
from .tasks import send_email_task
from django.core.mail import send_mail
from django.conf import settings

def send_notification_email(
    subject,
    template_name,
    context,
    recipient_email
):

    send_email_task.delay(
        subject,
        template_name,
        context,
        recipient_email
    )

class InterviewEmailService:

    @staticmethod
    def send_confirmation(schedule):

        candidate = schedule.application.candidate

        job = schedule.application.job

        subject = "Interview Scheduled Successfully"

        message = f"""
Hello {candidate.user.first_name},

Your interview has been scheduled.

Job Role : {job.title}

Date : {schedule.slot.available_date}

Time :
{schedule.slot.start_time} - {schedule.slot.end_time}

Please be available on time.

Best Regards,
AI Recruitment Team
"""

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [candidate.user.email],
            fail_silently=False,
        )

@staticmethod
def send_reminder(interview, reminder_type):

    subject = f"Interview Reminder ({reminder_type})"

    body = f"""
Hello {interview.application.candidate.user.first_name},

This is a reminder for your interview.

Job: {interview.application.job.title}

Date: {interview.slot.available_date}

Time: {interview.slot.start_time}

Please be available.

Regards,
AI Recruitment System
"""

    from .tasks import send_email_task

    send_email_task.delay(
        interview.application.candidate.user.email,
        subject,
        body
    )

    return True
@staticmethod
def send_voice_reminder(interview):

        print(
            f"Voice reminder queued for {interview.application.candidate.user.email}"
        )

        return True