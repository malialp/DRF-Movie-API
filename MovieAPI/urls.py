from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.api.urls')),
    path('auth', obtain_auth_token, name='auth')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)