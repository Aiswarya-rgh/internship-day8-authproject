import os
import tempfile

from django.core.files.storage import default_storage
from celery import shared_task
from django.utils import timezone
from applications.models import Application
from applications.ai_models import AIInterviewSession, CallLog
import time
from .utils import (
    extract_resume_text,
    clean_resume_text,
    tokenize_text,
    extract_skills,
    extract_email,
    extract_phone,
    extract_experience,
    extract_role,
    extract_education,
    calculate_resume_score,
)


@shared_task
def process_resume_task(file_path):

    temp_path = None

    try:
        # Download the private S3 file to a temporary local file
        extension = os.path.splitext(file_path)[1]

        with default_storage.open(file_path, "rb") as source_file:
            with tempfile.NamedTemporaryFile(
                suffix=extension,
                delete=False
            ) as temp_file:

                temp_path = temp_file.name
                temp_file.write(source_file.read())

        # Existing resume processing works with a local path
        text = extract_resume_text(temp_path)

        text = clean_resume_text(text)

        tokens = tokenize_text(text)

        skills = extract_skills(tokens)

        email = extract_email(text)

        phone = extract_phone(text)

        experience = extract_experience(text)

        role = extract_role(text)

        education = extract_education(text)

        score = calculate_resume_score(
            skills,
            experience,
            education
        )

        print("Resume Processed Successfully")

        print({
            "skills": skills,
            "email": email,
            "phone": phone,
            "experience": experience,
            "role": role,
            "education": education,
            "score": score
        })

    finally:
        # Remove temporary local copy
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

@shared_task(bind=True, max_retries=3)
def ai_resume_analysis_task(self, application_id):

    application = Application.objects.get(id=application_id)

    # Get the latest interview session
    session = AIInterviewSession.objects.filter(
        candidate=application.candidate,
        job=application.job
    ).latest("started_at")

    call_log = CallLog.objects.get(session=session)

    try:

        # Update AI status
        application.ai_status = Application.AI_PROGRESS
        application.save()

        # Update Call Log
        call_log.status = "In Progress"
        call_log.save()

        print("=================================")
        print("AI Resume Analysis Triggered")
        print(f"Application ID : {application.id}")

        # Simulate AI processing
        time.sleep(5)

        # AI Completed
        application.ai_status = Application.AI_COMPLETED
        application.save()

        call_log.status = "Completed"
        call_log.save()

        print("AI Analysis Completed")

        return {
            "status": "success",
            "message": "AI Resume Analysis Completed"
        }

    except Exception as exc:

        application.ai_status = Application.AI_FAILED
        application.save()

        call_log.status = "Failed"
        call_log.save()

        print("AI Task Failed. Retrying...")

        raise self.retry(exc=exc, countdown=10)
@shared_task
def periodic_system_check():

    print("=================================")
    print("Periodic Task Running")
    print(f"Current Time : {timezone.now()}")
    print("=================================")

    return "Periodic Task Executed Successfully"
