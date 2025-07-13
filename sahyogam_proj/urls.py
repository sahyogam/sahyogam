from django.contrib import admin
from django.urls import path, include

# ✅ Required for media files in development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Login.urls')),
    path('register/', include('Registration.urls')),
    path('organization/', include('organization.urls')),
    path('volunteer/', include('volunteer.urls')),
    path('profile/', include('profile_page.urls')),
]

# ✅ Serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
