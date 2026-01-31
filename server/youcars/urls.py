from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# AVVAL urlpatterns ni yarating
urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("cars/", include("cars.urls")),
]

# KEYIN schema_view ni yarating va urlpatterns ni bering
schema_view = get_schema_view(
    openapi.Info(
        title="YourCars API",
        default_version="v1",
        description="API Documentation",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=urlpatterns,  # BU QATORNI QO'SHING
)

# KEYIN Swagger URL'larini qo'shing
urlpatterns += [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
