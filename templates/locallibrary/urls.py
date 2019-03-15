
from django.contrib import admin
from django.urls import path, include, re_path
from django.shortcuts import redirect
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', redirect_catalog),
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    re_path(r'^accounts/', include('django.contrib.auth.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
