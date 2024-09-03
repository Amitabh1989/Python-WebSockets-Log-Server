import logging
import time
from logging.handlers import SocketHandler
import random

rand_num = random.randint(1, 1000)


def main():
    # Configure the logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the minimum logging level

    # Create a formatter with the desired format
    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d %(levelname)-8s %(module)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler for logging to a file
    file_handler = logging.FileHandler("HISTORYlistener.log")
    file_handler.setFormatter(formatter)
    file_handler.flush = (
        lambda: None
    )  # Add flush method to ensure logs are written immediately
    logger.addHandler(file_handler)

    # Stream handler for logging to the console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Create a socket handler
    # socket_handler = logging.handlers.SocketHandler(
    socket_handler = SocketHandler(
        "localhost", 9999
    )  # Replace with your log server address and port
    logger.addHandler(socket_handler)

    for i in range(200):
        logger.info(
            f"Hello, world! We are live logging via websockets {i} :  random_id : {rand_num}"
        )
        time.sleep(0.2)


if __name__ == "__main__":
    main()


"""
In the context of your code, the `SocketHandler` is designed to send log messages to a remote logging server over a network socket. This is useful when you want to centralize log collection from multiple sources, such as in a production environment where logs from various servers or applications are aggregated in one place.

### **Development Scenario:**
When you're running everything on your laptop, both the logging server and the script sending logs can run on the same machine. Here’s how you might set this up:

1. **Local Setup:**
   - **Log Server:** You can run a simple logging server on your laptop that listens for incoming log messages on a specific port (e.g., 9999).
   - **Log Client (your script):** The script will send logs to this server running locally.

   ```python
   socket_handler = logging.handlers.SocketHandler('localhost', 9999)
   ```

   - `'localhost'` refers to your local machine, and `9999` is the port where your logging server is listening.

### **Production Scenario:**
In a production environment, you might have your test script running on one server and a logging server running on a different machine. Here's how you would set it up:

1. **Log Server:**
   - The logging server could be running on a different machine, say with IP address `192.168.1.100`, listening on port `9999`.

2. **Log Client (your script):**
   - The script running on another server will send logs to this remote logging server.

   ```python
   socket_handler = logging.handlers.SocketHandler('192.168.1.100', 9999)
   ```

   - `'192.168.1.100'` is the IP address of the logging server, and `9999` is the port it's listening on.

### **Example Logging Server in Python:**
You can run a simple logging server using Python's `SocketServer`. Here's an example:

```python
import logging
import logging.handlers
import socketserver

class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            try:
                record = self.connection.recv(1024)
                if not record:
                    break
                print(record.decode('utf-8'))
            except:
                break

class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, host='localhost', port=9999, handler=LogRecordStreamHandler):
        super().__init__((host, port), handler)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    server = LogRecordSocketReceiver()
    print("Starting log server on port 9999...")
    server.serve_forever()
```

- **Development:**
  - Run this script on your laptop (`localhost`) to listen on port `9999`.
  - Your test script with `socket_handler = logging.handlers.SocketHandler('localhost', 9999)` will send logs to it.

- **Production:**
  - Deploy this server on your designated log server machine.
  - Replace `'localhost'` with the server's IP address (`'192.168.1.100'`) in your script's `SocketHandler`.

### **Summary:**
- **Development:** Use `'localhost'` and `9999` to log locally.
- **Production:** Replace `'localhost'` with the IP address of your remote log server, and make sure the port matches.

This setup will allow you to seamlessly move from local development to a production environment where logs are centralized on a remote server.

"""
