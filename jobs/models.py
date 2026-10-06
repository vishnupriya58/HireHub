from django.db import models
from accounts.models import User


class Company(models.Model):
    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="companies"
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    skills = models.TextField(
        help_text="Enter skills separated by commas"
    )
    location = models.CharField(max_length=100, blank=True)
    experience_required = models.PositiveIntegerField(default=0)
    salary = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title