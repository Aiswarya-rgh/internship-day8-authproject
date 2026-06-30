from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Customuser(AbstractUser):

    ROLE_CHOICES =(
        ("Admin","Admin"),
        ("Employer","Employer"),
        ("Candidate","Candidate"),
    )

    username=None
    email=models.EmailField(unique=True)
    phone=models.CharField(max_length=15)
    role=models.CharField(max_length=20,choices=ROLE_CHOICES)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    USERNAME_FIELD="email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email