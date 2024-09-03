# Django-WebSockets
Using Django Websockets for real time applications

if runserver does not detect asgi server, follow the link as below :

https://github.com/massover/asgi-runserver


Here's a detailed write-up for your socket-based log server project that you can use for GitHub:

---

# Socket-Based Log Server

## Overview

This project implements a real-time, socket-based log server designed to collect, process, and broadcast log messages to multiple clients via WebSockets. It provides a reliable mechanism for real-time log monitoring, enabling users to view logs as they are generated on a server. The server is built using Python’s asyncio for handling asynchronous tasks, ensuring that logs are transmitted to clients with minimal delay.

## Features

- **Real-Time Log Broadcasting:** The server collects logs from various sources and broadcasts them to all connected clients in real-time.
- **Asynchronous Log Handling:** Utilizes Python's asyncio to handle multiple clients concurrently, ensuring efficient and non-blocking communication.
- **WebSocket Communication:** Logs are sent to clients over WebSockets, providing a continuous, live feed of log messages.
- **Client Registration and Management:** Clients can connect and disconnect dynamically, with the server maintaining an updated list of active clients.
- **Immediate Log Flushing:** The server supports immediate flushing of logs to ensure that messages are delivered to clients as soon as they are available.

## Architecture

The project consists of several key components:

### 1. **LogRecordStreamHandler**
   - **Description:** This class is responsible for handling incoming log records from a TCP socket connection. It unpacks the log records, processes them, and then broadcasts them to all connected WebSocket clients.
   - **Key Methods:**
     - `handle()`: Handles the receipt and processing of log records.
     - `unPickle()`: Unpickles the log record data for further processing.
     - `broadcast()`: Broadcasts the processed log record to all connected clients.

### 2. **LogRecordSocketReceiver**
   - **Description:** A TCP server that listens for incoming log records on a specified host and port. It manages the lifecycle of connected WebSocket clients, ensuring that they receive log updates in real-time.
   - **Key Methods:**
     - `start_server()`: Starts the TCP server and handles incoming connections.
     - `register_client()`: Registers a new WebSocket client to receive log updates.

### 3. **WebSocket Handling**
   - **Description:** The project uses Python's `websockets` library to handle WebSocket connections. Clients connect to the server to receive live log updates.
   - **Key Methods:**
     - `websocket_handler()`: Manages client connections and broadcasts log messages.
     - `broadcast_to_clients()`: Sends log messages to all connected clients and flushes the output immediately.

### 4. **LogConsumer**
   - **Description:** An asynchronous WebSocket consumer that connects to a log server and forwards log messages to connected WebSocket clients.
   - **Key Methods:**
     - `connect()`: Establishes a WebSocket connection to the log server.
     - `disconnect()`: Handles the disconnection of a WebSocket client.
     - `forward_logs()`: Continuously forwards log messages from the log server to clients.

## Usage

### Prerequisites

- Python 3.7+
- Dependencies: `asyncio`, `websockets`, `logging`, `socketserver`

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/socket-log-server.git
   cd socket-log-server
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server

To start the log server and WebSocket server:

```bash
python log_server.py
```

This will start the TCP log server on `localhost:9999` and the WebSocket server on `ws://localhost:6789`. The log server will begin listening for incoming log records, and the WebSocket server will handle client connections.

### Example: Connecting a WebSocket Client

Clients can connect to the WebSocket server using any WebSocket client tool (e.g., `websocat`, `wscat`, or a custom client).

```bash
wscat -c ws://localhost:6789
```

Once connected, clients will start receiving live log messages as they are generated.

## Customization

### Configuring the Server

You can customize the host and port for the TCP log server and WebSocket server by modifying the `LogRecordSocketReceiver` and `websocket_handler` methods in `log_server.py`.

### Extending Functionality

This project is designed to be easily extensible. You can add more sophisticated log filtering, support for multiple log sources, or enhanced client management as needed.

## Troubleshooting

- **Logs Received in Bursts:** If clients are receiving logs in bursts rather than in real-time, consider disabling Nagle's algorithm by setting the `TCP_NODELAY` option on the socket connection.
- **Client Disconnections:** Ensure that the server is properly handling client disconnections by cleaning up and removing clients from the active list.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you encounter any bugs or have suggestions for new features.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---
