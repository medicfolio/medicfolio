# medicfolio/urls.py 

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('', include('home.urls', namespace='home')),
]

# Manejo de errores personalizados (si tienes vistas de errores configuradas)
handler403 = 'users.views.error_403'
handler404 = 'users.views.error_404'
handler500 = 'users.views.error_500'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
