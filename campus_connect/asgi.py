"""
ASGI config for campus_connect project with Django Channels.

Exposes the ASGI callable as a module-level variable named ``application``.
Supports both HTTP and WebSocket protocols.
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_connect.settings')

django_asgi_app = get_asgi_application()

# Import chat routing lazily to avoid app loading issues
try:
    from chat.routing import websocket_urlpatterns as chat_ws_urlpatterns
except Exception:
    chat_ws_urlpatterns = []

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(chat_ws_urlpatterns)
    ),
})
