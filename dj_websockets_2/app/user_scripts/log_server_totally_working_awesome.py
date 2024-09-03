import logging

# from logging.handlers import StreamRequestHandler, ThreadingTCPServer
# from logging import handlers
import socketserver
import asyncio
import websockets
import pickle
import struct
import socket


# class LogRecordStreamHandler(logging.handlers.StreamRequestHandler):
class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    """
    Handler for a streaming logging request.
    LogRecordStreamHandler:
        Handles incoming log records from the SocketHandler.
        Unpickles the log records and formats them.
        Broadcasts the formatted log messages to all connected WebSocket clients using the broadcast_to_clients function.

    """

    # Additional code added to the original snippet
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("LogRecordStreamHandler initialized")

    def handle(self):
        """
        Handles multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format.
        """
        # while True:
        #     chunk = self.connection.recv(4)
        #     if len(chunk) < 4:
        #         break
        #     slen = struct.unpack(">L", chunk)[0]
        #     chunk = self.connection.recv(slen)
        #     while len(chunk) < slen:
        #         chunk += self.connection.recv(slen - len(chunk))
        #     obj = self.unPickle(chunk)
        #     record = logging.makeLogRecord(obj)
        #     asyncio.run(self.broadcast(record))
        self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack(">L", chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk += self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            record = logging.makeLogRecord(obj)
            asyncio.run(self.broadcast(record))

    def unPickle(self, data):
        return pickle.loads(data)

    async def broadcast(self, record):
        # message = self.format(record)
        self.formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        print(f"Broadcasting message: {record}")
        message = self.formatter.format(record)
        await broadcast_to_clients(message)


# class LogRecordSocketReceiver(logging.handlers.ThreadingTCPServer):
class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
    """
    Simple TCP socket-based logging receiver.
    LogRecordSocketReceiver:
    A TCP server that listens for incoming log records on a specified host and port (localhost:9999).
    Manages connected WebSocket clients.

    Listens on ws://localhost:6789 for client connections.
    When a client connects, it is registered to receive broadcasted log message

    """

    allow_reuse_address = True

    def __init__(self, host="localhost", port=9999, handler=LogRecordStreamHandler):
        super().__init__((host, port), handler)
        self.loop = asyncio.get_event_loop()
        self.clients = set()

    def start_server(self):
        print(f"Starting log server on {self.server_address}")
        server_thread = threading.Thread(target=self.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    async def register_client(self, websocket):
        self.clients.add(websocket)
        print(f"Client added to register_client : {websocket}")
        print(f"All websocket clients           : {self.clients}")
        try:
            await websocket.wait_closed()
        finally:
            self.clients.remove(websocket)


async def broadcast_to_clients(message):
    """
    Asynchronously sends log messages to all registered WebSocket clients.
    Use asyncio.gather instead of asyncio.wait to handle sending messages concurrently without delay.
    """
    if log_server.clients:
        # await asyncio.wait([client.send(message) for client in log_server.clients])
        await asyncio.gather(*[client.send(message) for client in log_server.clients])


# Initialize the log server
log_server = LogRecordSocketReceiver()


# Start WebSocket server
async def websocket_handler(websocket, path):
    await log_server.register_client(websocket)


def start_servers():
    """
    The start_servers function starts both the log server and the WebSocket server concurrently.
    """
    log_server.start_server()
    ws_server = websockets.serve(websocket_handler, "localhost", 6789)
    print("WebSocket server started on ws://localhost:6789")
    asyncio.get_event_loop().run_until_complete(ws_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    """
    The log server runs in a separate thread to handle blocking I/O operations without hindering the asynchronous WebSocket operations.
    """
    import threading

    start_servers()
