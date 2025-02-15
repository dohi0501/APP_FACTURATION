
from django.contrib import admin
from django.urls import path, include
from gestion_factures.views import Custom_404

from django.conf.urls import handler404

handler404 = Custom_404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion_factures.urls')),
]
