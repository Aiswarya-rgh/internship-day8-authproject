from rest_framework import serializers
from .models import (
    Application,
    SavedJob,
    AIAnswerEvaluation,
    AvailabilitySlot,
    InterviewSchedule,
    ReminderLog,
)

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = [
            "candidate",
            "status",
            "applied_at",
            "resume_snapshot",
            "status_updated_at",
        ]

class ApplicationHistorySerializer(serializers.ModelSerializer):
    candidate_name = serializers.CharField(
        source="candidate.user.username",
        read_only=True
    )
    class Meta:
        model = Application
        fields = "__all__"


class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["status"]

class SavedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJob
        fields = "__all__"
        read_only_fields =["candidate","saved_at"]

class AIAnswerEvaluationSerializer(serializers.ModelSerializer):

    class Meta:

        model = AIAnswerEvaluation

        fields = "__all__"

        read_only_fields = [

            "confidence_score",

            "ai_annotation",

            "relevance_score",

            "completeness_score",

            "keyword_score",

            "final_score",

            "created_at"

        ]

class AvailabilitySlotSerializer(serializers.ModelSerializer):

    class Meta:

        model = AvailabilitySlot

        fields = "__all__"

        read_only_fields = [
            "is_booked",
            "created_at",
        ]


class InterviewScheduleSerializer(serializers.ModelSerializer):

    candidate = serializers.CharField(
        source="application.candidate.user.username",
        read_only=True
    )

    job = serializers.CharField(
        source="application.job.title",
        read_only=True
    )

    interview_date = serializers.DateField(
        source="slot.available_date",
        read_only=True
    )

    start_time = serializers.TimeField(
        source="slot.start_time",
        read_only=True
    )

    end_time = serializers.TimeField(
        source="slot.end_time",
        read_only=True
    )

    class Meta:

        model = InterviewSchedule

        fields = [
            "id",
            "candidate",
            "job",
            "interview_date",
            "start_time",
            "end_time",
            "scheduled_by",
            "confirmation_status",
            "interview_status",
            "scheduled_at",
            "remarks",
        ]
class ReminderLogSerializer(serializers.ModelSerializer):

    class Meta:

        model=ReminderLog

        fields="__all__"