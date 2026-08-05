from django.utils import timezone
from datetime import timedelta

from .models import InterviewSchedule


class ReminderService:

    @staticmethod
    def get_pending_reminders():

        now = timezone.localtime()

        tomorrow = now.date() + timedelta(days=1)

        interviews = InterviewSchedule.objects.filter(
            interview_status="Scheduled",
            confirmation_status=False
        )

        reminders = []

        for interview in interviews:

            slot = interview.slot

            # Reminder one day before
            if (
                slot.available_date == tomorrow
                and not interview.reminder_24_sent
            ):
                reminders.append(
                    (
                        interview,
                        "24_HOURS"
                    )
                )

            # Reminder one hour before
            interview_datetime = timezone.make_aware(
                timezone.datetime.combine(
                    slot.available_date,
                    slot.start_time
                )
            )

            if (
                interview_datetime - now
            ) <= timedelta(hours=1):

                if not interview.reminder_1hr_sent:

                    reminders.append(
                        (
                            interview,
                            "1_HOUR"
                        )
                    )

        return reminders