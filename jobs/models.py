from django.db import models
from accounts.models import Employer

# Create your models here.
class Job(models.Model):
    FULL_TIME="Full Time"
    PART_TIME="Part Time"
    INTERNSHIP="Internship"

    JOB_TYPE_CHOICES = (
        (FULL_TIME,"Full Time"),
        (PART_TIME,"Part Time"),
        (INTERNSHIP,"Internship"),
    )

    OPEN="Open"
    CLOSED="Closed"

    STATUS_CHOICES = (
        (OPEN,"Open"),
        (CLOSED,"Closed"),
    )

    employer = models.ForeignKey(Employer,on_delete=models.CASCADE,related_name="jobs")
    title = models.CharField(max_length=100,db_index=True)
    description = models.TextField()
    skills = models.TextField()
    experience = models.PositiveIntegerField()
    salary_min = models.DecimalField(max_digits=10,decimal_places=2)
    salary_max = models.DecimalField(max_digits=10,decimal_places=2)
    location = models.CharField(max_length=100,db_index=True)
    job_type = models.CharField(max_length=100,choices=JOB_TYPE_CHOICES)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default=OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
