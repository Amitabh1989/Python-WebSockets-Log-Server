from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json


class EchoSyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print(
            f"Websocket connected Event : {event} -> message : {event.get('text', 'No message')} "
        )
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
                    "text": json.dumps({"message": event["text"], "sync": f"Sync {i}"}),
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
                    "text": json.dumps(
                        {"message": event["text"], "sync": f"Ayync {i}"}
                    ),
                }
            )
            await asyncio.sleep(0.5)

    async def websocket_disconnect(self, event):
        print(
            f"Async Websocket disconnected Event : {event} -> message : {event.get('text', 'No message')} "
        )
        raise StopConsumer()
