from rest_framework import serializers
from .models import Application

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

