from PIL import ImageChops
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", lambda request: redirect("accounts:register")),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("jobs/", include("jobs.urls")),
    path("applications/", include("applications.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

handler404 = "core.views.custom_404"
handler500 = "core.views.custom_500"