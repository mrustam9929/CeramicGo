from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import path

from apps.bot.webhook import webhook as tg_webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tg-webhook/', tg_webhook)
]

# SWAGGER SCHEMES
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.unregister(Group)
admin.site.site_header = 'CeramicGo ADMIN'
admin.site.site_title = 'CeramicGO'
admin.site.index_title = 'ADMIN'
