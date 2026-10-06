from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        APPLICANT = "APPLICANT", "Applicant"
        RECRUITER = "RECRUITER", "Recruiter"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.APPLICANT,
    )

    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    full_name = models.CharField(max_length=150, blank=True)
    headline = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    experience_years = models.PositiveIntegerField(default=0)

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.full_name or self.user.username


class Resume(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="resumes"
    )

    file = models.FileField(upload_to="resumes/")
    extracted_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.uploaded_at:%Y-%m-%d}"