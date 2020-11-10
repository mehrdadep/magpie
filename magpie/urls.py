from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from magpie.apps.files import api_urls
from magpie.apps.files import web_urls

admin.site.site_header = "MAGPIE"
admin.site.site_title = "Magpie"
admin.site.index_title = "Magpie"

urlpatterns = [
    path('health-check/', include('health_check.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('web/', include(web_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
