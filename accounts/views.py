from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, ResumeForm, ProfileForm
from .models import Profile
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

import pdfplumber
from docx import Document


def extract_resume_text(file):

    if file.name.lower().endswith(".pdf"):
        text = ""

        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    elif file.name.lower().endswith(".docx"):
        document = Document(file)

        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    elif file.name.lower().endswith(".txt"):
        return file.read().decode("utf-8")

    return ""


def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("accounts:login")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


class UserLoginView(LoginView):

    template_name = "accounts/login.html"


@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Profile updated successfully!"
            )

            return redirect("accounts:profile")

    else:
        form = ProfileForm(
            instance=profile
        )

    resume_count = request.user.resumes.count()

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            "resume_count": resume_count
        }
    )


@login_required
def dashboard(request):

    if request.user.role.upper() == "RECRUITER":

        from jobs.models import Job
        from applications.models import Application

        jobs_count = Job.objects.filter(
            company__recruiter=request.user
        ).count()

        applications_count = Application.objects.filter(
            job__company__recruiter=request.user
        ).count()

        shortlisted_count = Application.objects.filter(
            job__company__recruiter=request.user,
            status="SHORTLISTED"
        ).count()

        return render(
            request,
            "accounts/recruiter_dashboard.html",
            {
                "jobs_count": jobs_count,
                "applications_count": applications_count,
                "shortlisted_count": shortlisted_count
            }
        )

    resume_count = request.user.resumes.count()

    application_count = request.user.applications.count()

    return render(
        request,
        "accounts/dashboard.html",
        {
            "resume_count": resume_count,
            "application_count": application_count
        }
    )


@login_required
def upload_resume(request):

    if request.method == "POST":

        form = ResumeForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            resume = form.save(
                commit=False
            )

            resume.user = request.user

            resume.extracted_text = extract_resume_text(
                resume.file
            )

            resume.save()

            return redirect(
                "accounts:dashboard"
            )

    else:
        form = ResumeForm()

    return render(
        request,
        "accounts/upload_resume.html",
        {"form": form}
    )


@login_required
def applicant_profile(request, user_id):

    from .models import User

    applicant = User.objects.get(
        id=user_id,
        role="APPLICANT"
    )

    profile, created = Profile.objects.get_or_create(
        user=applicant
    )

    resumes = applicant.resumes.order_by(
        "-uploaded_at"
    )

    return render(
        request,
        "accounts/applicant_profile.html",
        {
            "applicant": applicant,
            "profile": profile,
            "resumes": resumes
        }
    )