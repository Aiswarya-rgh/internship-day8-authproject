from rest_framework import serializers
from .models import Job

#to create and update jobs
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields =  "__all__"
        read_only_fields = ["employer","created_at","updated_at"]

#used for displaying jobs
class JobListSerializer(serializers.ModelSerializer):
     class Meta:
        model = Job
        fields = [
            "id",
            "title",
            "skills",
            "experience",
            "salary_min",
            "salary_max",
            "location",
            "job_type",
            "status",
        ]
        