from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from jobs.models import Job
from .models import Application


def get_skill_match(job, resume_text):

    job_skills = [
        skill.strip()
        for skill in job.skills.split(",")
        if skill.strip()
    ]

    resume_text = resume_text.lower()

    matched_skills = []
    missing_skills = []

    for skill in job_skills:

        if skill.lower() in resume_text:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if not job_skills:
        percentage = 0
    else:
        percentage = (
            len(matched_skills) / len(job_skills)
        ) * 100

    return (
        round(percentage, 2),
        matched_skills,
        missing_skills
    )


def calculate_match(job, resume_text):

    percentage, matched_skills, missing_skills = get_skill_match(
        job,
        resume_text
    )

    return percentage


@login_required
def apply_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        is_active=True
    )

    if request.user.role != "APPLICANT":
        messages.error(
            request,
            "Only applicants can apply for jobs."
        )

        return redirect(
            "jobs:job_detail",
            job_id=job.id
        )

    application, created = Application.objects.get_or_create(
        applicant=request.user,
        job=job
    )

    resume = request.user.resumes.order_by(
        "-uploaded_at"
    ).first()

    if resume:

        percentage, matched_skills, missing_skills = get_skill_match(
            job,
            resume.extracted_text
        )

        application.match_percentage = percentage
        application.save()

    if created:

        messages.success(
            request,
            "Application submitted successfully!"
        )

    else:

        messages.info(
            request,
            "You have already applied for this job."
        )

    return redirect(
        "applications:my_applications"
    )


@login_required
def my_applications(request):

    applications = Application.objects.filter(
        applicant=request.user
    ).select_related(
        "job",
        "job__company"
    ).order_by(
        "-applied_at"
    )

    return render(
        request,
        "applications/my_applications.html",
        {
            "applications": applications
        }
    )