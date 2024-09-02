# log_framework.py

import subprocess
import sys
import asyncio
import websockets
import json


# async def send_logs_to_websocket(uri):
#     async with websockets.connect(uri) as websocket:
#         process = subprocess.Popen(
#             [sys.executable, "-m", "pytest", "--log-cli-level=INFO"],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.STDOUT,
#             text=True,
#         )

#         for line in iter(process.stdout.readline, ""):
#             await websocket.send(line)
#             print(line, end="")  # Optional: Also print to console

#         process.stdout.close()
#         process.wait()


# if __name__ == "__main__":
#     asyncio.run(send_logs_to_websocket("ws://localhost:8001/ws/logs/"))


# Works but transmits only when script ends
# =============================================


# async def send_logs_to_websocket(consumer, script_path):
#     process = subprocess.Popen(
#         [sys.executable, "-u", script_path],  # Run the script using Python
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT,
#         text=True,
#         bufsize=1,  # Use line-buffering
#     )

#     # Read output line by line and send it over the WebSocket connection
#     for line in iter(process.stdout.readline, ""):
#         await consumer.send(
#             {"type": "websocket.send", "text": json.dumps({"log_lines": line.strip()})}
#         )
#         print(line, end="")  # Optional: Also print to the server console

#     process.stdout.close()
#     process.wait()


import asyncio
import json
import subprocess
import sys


async def send_logs_to_websocket(consumer, script_path):
    # Start the subprocess
    process = subprocess.Popen(
        [sys.executable, "-u", script_path],  # Run the script using Python
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,  # Line-buffered output
    )

    loop = asyncio.get_event_loop()

    async def read_logs():
        while True:
            # Read output line by line asynchronously
            line = await loop.run_in_executor(None, process.stdout.readline)
            if line:
                await consumer.send(
                    {
                        "type": "websocket.send",
                        "text": json.dumps({"log_lines": line.strip()}),
                    }
                )
                print(line, end="")  # Optional: Also print to the server console
            else:
                break

    # Run the read_logs coroutine
    await read_logs()

    process.stdout.close()
    await loop.run_in_executor(None, process.wait)
