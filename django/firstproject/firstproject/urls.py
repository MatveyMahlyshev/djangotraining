from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from firstproject import settings
from men.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('men.urls')),
    path('', include('api.urls')),
    path('users/', include('users.urls', namespace='users')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('social-auth/', include('social_django.urls', namespace='social'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found