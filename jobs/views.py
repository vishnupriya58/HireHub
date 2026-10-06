from django.shortcuts import render, redirect
from .forms import CompanyForm, JobForm
from .models import Company, Job
from applications.models import Application


def create_company(request):

    if request.method == "POST":
        form = CompanyForm(request.POST)

        if form.is_valid():
            company = form.save(commit=False)
            company.recruiter = request.user
            company.save()

            return redirect("jobs:create_job")

    else:
        form = CompanyForm()

    return render(
        request,
        "jobs/create_company.html",
        {"form": form}
    )


def create_job(request):

    companies = Company.objects.filter(
        recruiter=request.user
    )

    if request.method == "POST":
        form = JobForm(request.POST)

        if form.is_valid():

            job = form.save(commit=False)

            company_id = request.POST.get("company")

            job.company = Company.objects.get(
                id=company_id,
                recruiter=request.user
            )

            job.save()

            return redirect("jobs:my_jobs")

    else:
        form = JobForm()

    return render(
        request,
        "jobs/create_job.html",
        {
            "form": form,
            "companies": companies
        }
    )


def my_jobs(request):

    jobs = Job.objects.filter(
        company__recruiter=request.user
    )

    return render(
        request,
        "jobs/my_jobs.html",
        {"jobs": jobs}
    )


def job_list(request):

    jobs = Job.objects.filter(
        is_active=True
    ).order_by("-created_at")

    return render(
        request,
        "jobs/job_list.html",
        {"jobs": jobs}
    )


def job_detail(request, job_id):

    job = Job.objects.get(
        id=job_id,
        is_active=True
    )

    return render(
        request,
        "jobs/job_detail.html",
        {"job": job}
    )


def job_applicants(request, job_id):

    job = Job.objects.get(
        id=job_id,
        company__recruiter=request.user
    )

    applications = Application.objects.filter(
        job=job
    ).select_related(
        "applicant"
    ).order_by(
        "-match_percentage"
    )

    for application in applications:

        resume = application.applicant.resumes.order_by(
            "-uploaded_at"
        ).first()

        matched_skills = []
        missing_skills = []

        if resume and resume.extracted_text:

            resume_text = resume.extracted_text.lower()

            job_skills = [
                skill.strip()
                for skill in job.skills.split(",")
                if skill.strip()
            ]

            for skill in job_skills:

                if skill.lower() in resume_text:
                    matched_skills.append(skill)
                else:
                    missing_skills.append(skill)

        application.matched_skills = matched_skills
        application.missing_skills = missing_skills

    return render(
        request,
        "jobs/job_applicants.html",
        {
            "job": job,
            "applications": applications
        }
    )




def update_application_status(request, application_id):

    application = Application.objects.get(
        id=application_id,
        job__company__recruiter=request.user
    )

    if request.method == "POST":

        status = request.POST.get("status")

        if status in ["SHORTLISTED", "REJECTED"]:

            application.status = status
            application.save()

    return redirect(
        "jobs:job_applicants",
        job_id=application.job.id
    )
    