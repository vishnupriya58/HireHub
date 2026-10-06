from django.urls import path
from . import views

app_name = "applications"

urlpatterns = [
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("my-applications/", views.my_applications, name="my_applications"),
]