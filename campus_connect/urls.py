"""
URL configuration for campus_connect project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # Users app (authentication)
    path('users/', include('users.urls')),
    
    # Items app (lost & found)
    path('items/', include('items.urls')),
    
    # Chat app (real-time messaging)
    path('chat/', include('chat.urls')),
    
    # Home page
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site headers
admin.site.site_header = "Campus Connect Admin"
admin.site.site_title = "Campus Connect Admin Portal"
admin.site.index_title = "Welcome to Campus Connect Administration"
