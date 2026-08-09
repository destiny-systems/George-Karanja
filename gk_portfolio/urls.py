from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')),
]

# Serve media files even when DEBUG=False.
# Not ideal for large-scale production, but fine for this project's current size.
# For real production scale, switch to cloud storage (e.g. Cloudinary or AWS S3).
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
