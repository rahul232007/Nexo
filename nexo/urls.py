from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('teacher/', include('teacher.urls')),
    path('student/', include('student.urls')),
    path('chat/', include('chatbot.urls')),
    path('global-chat/', include('communication.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

