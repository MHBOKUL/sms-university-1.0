from django.contrib import admin
from django.urls import path, include

# 🔥 media serve (DEV MODE ONLY)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🧠 core app routes
    path('', include('core.urls')),
    path("", include("accounts.urls")),

]

# 📁 MEDIA FILES (PDF download etc.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)