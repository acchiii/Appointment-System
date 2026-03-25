from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from appointments.views import error404, error500
from  django.conf.urls import handler400, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('appointments.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = error404
handler500 = error500
