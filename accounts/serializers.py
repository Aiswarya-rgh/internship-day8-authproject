import os
from rest_framework import serializers
from .models import CustomUser,Employer,Candidate


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "phone",
            "role",
            "password",
        )

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            phone=validated_data["phone"],
            role=validated_data["role"],
            password=validated_data["password"],
        )
        return user
    # Employer Profile Serializer
class EmployerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employer
        fields = [
            "company_name",
            "company_domain",
            "company_size",
            "is_company_verified",
        ]
# Candidate Profile Serializer
class CandidateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = [
            "skills",
            "education",
            "experience",
            "expected_salary",
        ]
#resume upload
import os
from rest_framework import serializers
from .models import Candidate

class ResumeUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        fields = ["resume"]

def validate_resume(self, value):

    if not value:
        raise serializers.ValidationError("Please select a resume file.")

    allowed_extensions = [".pdf", ".doc", ".docx"]

    extension = os.path.splitext(value.name)[1].lower()

    if extension not in allowed_extensions:
        raise serializers.ValidationError(
            "Only PDF, DOC and DOCX files are allowed."
        )

    if value.size > 5 * 1024 * 1024:
        raise serializers.ValidationError(
            "File size must be less than 5 MB."
        )

    return value