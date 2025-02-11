from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from accounts.views import password_reset_confirm_view
from django.conf.urls.static import static
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="RapidJob API",
        default_version='v1',
        description="API documentation for RapidJob",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@rapidjob.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/auth/', include('djoser.urls.authtoken')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/accounts/', include('accounts.urls')),
    # path('jobs/', include('jobs.urls')),
    path('api/messages/', include('messages.urls')),
    
    path('auth/users/reset_password_confirm/<uid>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),
    path("api/accounts/", include("accounts.urls")),
    path('api/jobs/', include('jobs.urls')),
    path('api/application/', include('applications.urls') ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)