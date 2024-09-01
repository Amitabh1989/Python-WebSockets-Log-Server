from django.urls import path
from .consumers import EchoAsyncConsumer, EchoSyncConsumer, MyConsumer

websocket_urlpatterns = [
    path("ws/sc/", EchoSyncConsumer.as_asgi()),
    path("ws/ac/", EchoAsyncConsumer.as_asgi()),
    path("ws/log/", MyConsumer.as_asgi()),
]
