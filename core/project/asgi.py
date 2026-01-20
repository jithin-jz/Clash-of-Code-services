import os
import django

# Tell Django which settings module to use.
# This must be set before calling django.setup().
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Initialize Django. This loads settings, apps, and models.
# Required before importing anything that depends on Django internals.
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.middleware import JWTAuthMiddleware
from chat.routing import websocket_urlpatterns

# ASGI application entry point.
# ProtocolTypeRouter routes connections based on their protocol type.
application = ProtocolTypeRouter({
    # Standard HTTP requests (Django views, REST APIs, etc.)
    "http": get_asgi_application(),

    # WebSocket connections.
    # Requests are first passed through JWTAuthMiddleware
    # to authenticate the user using a JWT token,
    # then routed to the appropriate WebSocket consumer.
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})
