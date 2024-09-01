"""
ASGI config for dj_websockets_2 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application
import app.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_websockets_2.settings")

# application = get_asgi_application()


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter(app.routing.websocket_urlpatterns),
    }
)
