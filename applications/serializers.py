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
        ]
class ApplicationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
  