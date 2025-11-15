"""
ASGI config for Prompt2Action AI Agent Platform
Author: Cavin Otieno

It exposes the ASGI callable as a module-level variable named ``application``.
Supports both HTTP and WebSocket protocols for real-time communication.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# Import routing after Django initialization
from agents import routing as agents_routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                agents_routing.websocket_urlpatterns
            )
        )
    ),
})
