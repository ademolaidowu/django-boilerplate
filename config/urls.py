"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .settings import base


admin.site.site_header = base.DJANGO_ADMIN_HEADER
admin.site.index_title = base.DJANGO_ADMIN_TITLE
admin.site.site_title = base.COMPANY_NAME


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("user/", include("app.user.urls", namespace="user")),
            ]
        ),
    ),
]

urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)


handler404 = "app.core.views.error_404"
handler500 = "app.core.views.error_500"
