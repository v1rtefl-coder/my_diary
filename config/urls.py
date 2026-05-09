from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="6-минутный дневник API",
        default_version='v1',
        description="API для личного дневника успеха по методике 6-минутного дневника",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@diary.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Web интерфейс
    path('', include('accounts.urls')),
    path('entries/', include('entries.urls')),

    # API endpoints
    path('api/', include('accounts.api_urls')),
    path('api/entries/', include('entries.api_urls')),

    # Swagger документация
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

