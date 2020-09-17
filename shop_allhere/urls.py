from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from app_shop import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('allhere.ru/', include('app_shop.urls')),
    path('allhere_in_russia/', include('allhere_in_russia.urls')),
    path('', RedirectView.as_view(url='/allhere.ru/', permanent=True)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler403 = views.handler403
handler404 = views.handler404
handler500 = views.handler500
