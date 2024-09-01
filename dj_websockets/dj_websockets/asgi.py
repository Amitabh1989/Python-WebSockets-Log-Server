"""
ASGI config for dj_websockets project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
import realtimeapp.routing

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_websockets.settings")


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(realtimeapp.routing.websocket_urlpatterns),
    }
)


# application = get_asgi_application()

# `application = get_asgi_application()` is a line of code in the ASGI
# configuration file that retrieves the ASGI application callable for the
# Django project. This callable is responsible for handling ASGI requests
# and routing them to the appropriate channels and consumers defined in
# the project. It essentially sets up the Django application to work with
# ASGI servers like Daphne for handling WebSocket connections and other
# asynchronous tasks.
