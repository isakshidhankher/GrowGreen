"""
ASGI config for GrowGreen project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
import django
from asgiref.sync import sync_to_async
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GrowGreen.settings')
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chatv2.routing
# await sync_to_async(django.setup, thread_sensitive=True)()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chatv2.routing.websocket_urlpatterns
        )
    ),
})



