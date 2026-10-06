from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("company/create/", views.create_company, name="create_company"),
    path("create/", views.create_job, name="create_job"),
    path("my-jobs/", views.my_jobs, name="my_jobs"),
    path("list/", views.job_list, name="job_list"),
    path("detail/<int:job_id>/", views.job_detail, name="job_detail"),
    path("applicants/<int:job_id>/", views.job_applicants, name="job_applicants"),
    path("application/<int:application_id>/status/", views.update_application_status, name="update_application_status"),
]