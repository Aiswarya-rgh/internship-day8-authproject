from django.db import transaction
from django.utils import timezone

from .models import (
    AvailabilitySlot,
    InterviewSchedule,
    Application,
)

from .email_service import InterviewEmailService


class InterviewSchedulingService:

    @staticmethod
    @transaction.atomic
    def schedule_interview(application):

        slot = AvailabilitySlot.objects.filter(
            role=application.job,
            is_booked=False
        ).order_by(
            "available_date",
            "start_time"
        ).first()

        if not slot:
            return None

        # Prevent scheduling in the past
        today = timezone.localdate()

        if slot.available_date < today:
            return None

        # Prevent duplicate interview for same application
        if InterviewSchedule.objects.filter(
            application=application,
            interview_status="Scheduled"
        ).exists():
            return None

        # Prevent overlapping interview for same employer
        conflict = InterviewSchedule.objects.filter(
            slot__employer=slot.employer,
            slot__available_date=slot.available_date,
            slot__start_time=slot.start_time,
        ).exists()

        if conflict:
            return None

        slot.is_booked = True
        slot.save()

        schedule = InterviewSchedule.objects.create(
            application=application,
            slot=slot,
            scheduled_by="AI Scheduler",
            confirmation_status=False,
            interview_status="Scheduled"
        )

        application.status = Application.INTERVIEW
        application.save()

        InterviewEmailService.send_confirmation(schedule)

        return schedule

    @staticmethod
    @transaction.atomic
    def reschedule_interview(schedule):

        # Release old slot
        old_slot = schedule.slot
        old_slot.is_booked = False
        old_slot.save()

        # Find next available slot
        new_slot = AvailabilitySlot.objects.filter(
            role=schedule.application.job,
            is_booked=False
        ).exclude(
            id=old_slot.id
        ).order_by(
            "available_date",
            "start_time"
        ).first()

        if not new_slot:
            old_slot.is_booked = True
            old_slot.save()
            return None

        # Prevent rescheduling to a past slot
        today = timezone.localdate()

        if new_slot.available_date < today:
            old_slot.is_booked = True
            old_slot.save()
            return None

        # Prevent overlapping interview for same employer
        conflict = InterviewSchedule.objects.filter(
            slot__employer=new_slot.employer,
            slot__available_date=new_slot.available_date,
            slot__start_time=new_slot.start_time
        ).exclude(
            id=schedule.id
        ).exists()

        if conflict:
            old_slot.is_booked = True
            old_slot.save()
            return None

        new_slot.is_booked = True
        new_slot.save()

        schedule.slot = new_slot
        schedule.interview_status = "Rescheduled"
        schedule.save()

        InterviewEmailService.send_confirmation(schedule)

        return schedule