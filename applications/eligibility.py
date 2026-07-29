from jobs.models import Job
from .models import Application
from django.utils import timezone

ATS_THRESHOLD = 70

def check_candidate_eligibility(application):

    # Rule 1
    if application.ats_score < ATS_THRESHOLD:
        return False, "ATS Score Below Threshold"

    # Rule 2
    if application.job.status != Job.OPEN:
        return False, "Job Closed"

    # Rule 3
    if application.status == Application.INTERVIEW:
        return False, "Interview Already Scheduled"

    # Rule 4 - Time Window Validation
    current_hour = timezone.localtime().hour

    if current_hour < 9 or current_hour >= 18:
        return False, "Outside AI Processing Hours"

    return True, "Eligible"