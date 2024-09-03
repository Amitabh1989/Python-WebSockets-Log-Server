from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer
import websockets
from asgiref.sync import sync_to_async


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


class LogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.log_server_uri = "ws://localhost:6789"
        self.log_server_connection = await websockets.connect(self.log_server_uri)

        asyncio.create_task(self.forward_logs())

    async def disconnect(self, close_code):
        await self.log_server_connection.close()

    async def forward_logs(self):
        async for message in self.log_server_connection:
            print(f"LogConsumer message : {message}")
            # await self.send(text_data=message)
            await self.send(text_data=json.dumps({"log_lines": message}))
