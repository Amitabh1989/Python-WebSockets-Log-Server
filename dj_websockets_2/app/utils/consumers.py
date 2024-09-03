from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer
import websockets


# from utils.logging_utils import WebSocketHandler
# from .utils.logging_utils import WebSocketHandler
# import logging
from asgiref.sync import sync_to_async

# from .user_scripts.test_logging import setup_logger
# from queue import Queue


class EchoSyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print(
            f"Websocket connected Event : {event} -> message : {event.get('text', 'No message')} "
        )
        print(f"Channels : {self.channel_name}")
        print(f"Channels : {self.channel_layer}")
        self.send(
            {
                "type": "websocket.accept",
            }
        )

    def websocket_receive(self, event):
        print(
            f"Sync Websocket receive started :  : {event} -> message : {event.get('text', 'No message')} "
        )
        for i in range(10):
            self.send(
                {
                    "type": "websocket.send",
                    "text": json.dumps({"sync": f"Sync {i}"}),
                }
            )
            sleep(0.5)

    def websocket_disconnect(self, event):
        print(
            f"Sync Websocket disconnected Event : {event} -> message : {event.get('text', 'No message')} "
        )
        raise StopConsumer()


class EchoAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print(
            f"Async Websocket connected Event : {event} -> message : {event.get('text', 'No message')} "
        )
        await self.send(
            {
                "type": "websocket.accept",
            }
        )

    async def websocket_receive(self, event):
        print(
            f"Async Websocket receive started :  : {event} -> message : {event.get('text', 'No message')} "
        )
        for i in range(10):
            await self.send(
                {
                    "type": "websocket.send",
                    "text": json.dumps({"async": f"Async {i}"}),
                }
            )
            await asyncio.sleep(0.5)

    async def websocket_disconnect(self, event):
        print(
            f"Async Websocket disconnected Event : {event} -> message : {event.get('text', 'No message')} "
        )
        raise StopConsumer()


# class LogConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         self.running = True

#     async def disconnect(self, close_code):
#         self.running = False

#     async def receive(self, text_data):
#         await self.send(text_data)

#     async def send_logs(self, message):
#         await self.send(text_data=message)

from .log_framework import send_logs_to_websocket


# This works : Starts Scripts and Sends logs to client
class LogConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print(
            f"Websocket connected Event : {event} -> message : {event.get('text', 'No message')} "
        )
        print(f"Channels : {self.channel_name}")
        print(f"Channels : {self.channel_layer}")
        self.script_path = event.get("text", None)
        await self.send(
            {
                "type": "websocket.accept",
            }
        )
        self.channel_layer.group_add("livelogs", self.channel_name)
        # Now hook function to send logs here:
        # You can add channels to groups and everyone in that group will
        # see the logs real time

    async def send_logs(self, script_path):
        # await send_logs_to_websocket(self, script_path)
        await send_logs_to_websocket(self)

    async def websocket_receive(self, event):
        print(
            f"Websocket received message from client : {event} : Event text : {event.get('text')}"
        )
        message_text = event.get("text")
        message_data = json.loads(message_text)
        self.script_path = message_data.get("script_path")
        print(f"Script path : {self.script_path}")
        await self.send_logs(self.script_path)

        # await self.send(
        #     {
        #         "type": "websocket.send",
        #         "text": json.dumps({"log": event.get("text") + " from server"}),
        #     }
        # )

    async def websocket_disconnect(self, event):
        print(
            f"Websocket disconnected Event : {event} -> message : {event.get('text', 'No message')} "
        )
        self.channel_layer.group_discard("livelogs", self.channel_name)
        raise StopConsumer()


# from channels.generic.websocket import AsyncWebsocketConsumer
# import json


# class LogConsumerWebSockets(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         self.log_server_uri = "ws://localhost:6789"
#         self.log_server_connection = await websockets.connect(self.log_server_uri)

#         asyncio.create_task(self.forward_logs())

#     async def disconnect(self, close_code):
#         await self.log_server_connection.close()

#     async def forward_logs(self):
#         async for message in self.log_server_connection:
#             await self.send(text_data=message)
