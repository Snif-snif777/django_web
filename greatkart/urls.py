from django.contrib import admin
from django.urls import include, path
from . import view

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view.home, name="home"),
    path('store/', include('store.urls')),
    path('carts/', include('carts.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
