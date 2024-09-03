import logging
import logging.handlers
import asyncio
import websockets
import pickle
import struct


class LogRecordStreamHandler(logging.handlers.StreamRequestHandler):
    """Handler for a streaming logging request."""

    def handle(self):
        """
        Handles multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format.
        """
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
        message = self.format(record)
        await broadcast_to_clients(message)


class LogRecordSocketReceiver(logging.handlers.ThreadingTCPServer):
    """
    Simple TCP socket-based logging receiver.
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
        try:
            await websocket.wait_closed()
        finally:
            self.clients.remove(websocket)


async def broadcast_to_clients(message):
    if log_server.clients:
        await asyncio.wait([client.send(message) for client in log_server.clients])


# Initialize the log server
log_server = LogRecordSocketReceiver()


# Start WebSocket server
async def websocket_handler(websocket, path):
    await log_server.register_client(websocket)


def start_servers():
    log_server.start_server()
    ws_server = websockets.serve(websocket_handler, "localhost", 6789)
    print("WebSocket server started on ws://localhost:6789")
    asyncio.get_event_loop().run_until_complete(ws_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    import threading

    start_servers()
