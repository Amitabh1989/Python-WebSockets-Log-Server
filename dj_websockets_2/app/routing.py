from django.urls import path
from .consumers import (
    EchoAsyncConsumer,
    LogConsumer,
    EchoSyncConsumer,
    # LogConsumerWebSockets,
)

# MyConsumer

websocket_urlpatterns = [
    path("ws/sc/", EchoSyncConsumer.as_asgi()),
    path("ws/ac/", EchoAsyncConsumer.as_asgi()),
    path("ws/logs/", LogConsumer.as_asgi()),  # tcp based logger, new file
    # path("ws/logs/", LogConsumerWebSockets.as_asgi()),
    # path("ws/log/", MyConsumer.as_asgi()),
]
