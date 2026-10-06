from django.db import models
from accounts.models import User
from jobs.models import Job


class Application(models.Model):

    class Status(models.TextChoices):
        APPLIED = "APPLIED", "Applied"
        SHORTLISTED = "SHORTLISTED", "Shortlisted"
        REJECTED = "REJECTED", "Rejected"

    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.APPLIED
    )

    match_percentage = models.FloatField(
        default=0
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("applicant", "job")

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"