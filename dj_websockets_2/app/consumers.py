from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer


# from utils.logging_utils import WebSocketHandler
from .utils.logging_utils import WebSocketHandler
import logging
from asgiref.sync import sync_to_async
from .user_scripts.test_logging import setup_logger


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


class WebSocketHandler(logging.Handler):
    def __init__(self, send_function):
        super().__init__()
        self.send_function = send_function

    def emit(self, record):
        try:
            log_entry = self.format(record)
            asyncio.run(
                self.send_function({"type": "websocket.send", "text": log_entry})
            )
        except Exception:
            self.handleError(record)


# class MyConsumer(AsyncWebsocketConsumer):

#     async def websocket_connect(self, event):
#         print(
#             f"Async Websocket connected Event : {event} -> message : {event.get('text', 'No message')} "
#         )
#         await self.send(
#             {
#                 "type": "websocket.accept",
#             }
#         )

#     async def websocket_receive(self, event):
#         print("I am here")
#         # from .user_scripts import test_logging

#         log_file = "test.log"
#         # Set up the logger and get the queue
#         self.logger, self.listener, self.log_queue = setup_logger(
#             log_file, send_function=self.send
#         )
#         print(f"Log setup done : {self.logger} -> {self.listener} -> {self.log_queue}")

#         # Read from the queue periodically
#         while True:
#             if not self.log_queue.empty():
#                 log_entry = self.log_queue.get()
#                 # Send the log entry through the WebSocket
#                 await self.send({"type": "websocket.send", "text": log_entry})
#             await asyncio.sleep(0.5)  # Adjust sleep time as needed

#     async def websocket_disconnect(self, close_code):
#         # Optionally remove the handler to clean up
#         for handler in self.logger.handlers[:]:
#             if isinstance(handler, WebSocketHandler):
#                 self.logger.removeHandler(handler)


class WebSocketHandler(logging.Handler):
    def __init__(self, send_function):
        super().__init__()
        self.send_function = send_function

    def emit(self, record):
        try:
            log_entry = self.format(record)
            # Schedule the send operation
            asyncio.create_task(
                self.send_function({"type": "websocket.send", "text": log_entry})
            )
        except Exception:
            self.handleError(record)


class MyConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        print(
            f"Async Websocket connected Event : {event} -> message : {event.get('text', 'No message')} "
        )
        await self.accept()  # Ensure we accept the connection first

        # Set up the logger and get the queue
        log_file = "test.log"
        self.logger, self.listener, self.log_queue = setup_logger(
            log_file, send_function=self.send
        )
        print(f"Log setup done : {self.logger} -> {self.listener} -> {self.log_queue}")

        # Start the log handling loop
        self.log_task = asyncio.create_task(self.handle_logs())

    async def handle_logs(self):
        print(f"IN handling loop : {vars(self.log_queue)}")
        while True:
            if not self.log_queue.not_empty():
                log_entry = self.log_queue.get()
                # Send the log entry through the WebSocket
                await self.send({"type": "websocket.send", "text": log_entry})
            await asyncio.sleep(0.5)  # Adjust sleep time as needed

    async def websocket_disconnect(self, close_code):
        # Stop the log handling loop
        self.log_task.cancel()

        # Clean up the logger
        for handler in self.logger.handlers[:]:
            if isinstance(handler, WebSocketHandler):
                self.logger.removeHandler(handler)

        # Ensure that all tasks are finished
        await self.log_task
