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


# async def send_logs_to_websocket(consumer, script_path):
#     # Start the subprocess
#     process = subprocess.Popen(
#         [sys.executable, "-u", script_path],  # Run the script using Python
#         stdout=subprocess.PIPE,
#         stderr=subprocess.STDOUT,
#         text=True,
#         bufsize=1,  # Line-buffered output
#     )

#     loop = asyncio.get_event_loop()

#     async def read_logs():
#         while True:
#             # Read output line by line asynchronously
#             line = await loop.run_in_executor(None, process.stdout.readline)
#             if line:
#                 await consumer.send(
#                     {
#                         "type": "websocket.send",
#                         "text": json.dumps({"log_lines": line.strip()}),
#                     }
#                 )
#                 print(line, end="")  # Optional: Also print to the server console
#             else:
#                 break

#     # Run the read_logs coroutine
#     await read_logs()

#     process.stdout.close()
#     await loop.run_in_executor(None, process.wait)


import asyncio
import os

# C:\GitHub\Django-WebSockets\dj_websockets_2\HISTORYlistener.log


# async def send_logs_to_websocket(consumer):
#     """
#     This function reads logs from a log file and sends them over a WebSocket connection in real-time.
#     """
#     loop = asyncio.get_event_loop()
#     log_file_path = (
#         "C:\\GitHub\\Django-WebSockets\\dj_websockets_2\\HISTORYlistener.log"
#     )

#     async def read_logs():
#         with open(log_file_path, "r") as log_file:
#             print(f"Log file opened: {log_file_path}")
#             log_file.seek(0, os.SEEK_END)  # Move the cursor to the end of the file

#             while True:
#                 where = log_file.tell()
#                 line = log_file.readline()
#                 if not line:
#                     log_file.seek(where)
#                     await asyncio.sleep(0.1)
#                 else:
#                     await consumer.send(
#                         {
#                             "type": "websocket.send",
#                             "text": json.dumps({"log_lines": line.strip()}),
#                         }
#                     )
#                     print(line, end="")  # Optional: Also print to the server console

#     await read_logs()


async def send_logs_to_websocket(consumer):
    """
    This function reads logs from a log file and sends them over a WebSocket connection.
    """
    loop = asyncio.get_event_loop()
    log_file_path = os.path.join(
        "C:\GitHub\Django-WebSockets\dj_websockets_2\HISTORYlistener.log"
    )

    async def read_logs():
        with open(log_file_path, "r") as log_file:
            print(f"Log has been opened :{log_file}")
            # log_file.seek(
            #     0, 2
            # )  # Move the cursor to the end of the file to start reading new lines
            log_file.seek(0, os.SEEK_END)  # Move the cursor to the end of the file
            while True:
                # line = await loop.run_in_executor(None, log_file.readline)
                # line = log_file.readline()
                where = log_file.tell()
                line = log_file.readline()
                if line:
                    await consumer.send(
                        {
                            "type": "websocket.send",
                            "text": json.dumps({"log_lines": line.strip()}),
                        }
                    )
                    print(line, end="")  # Optional: Also print to the server console
                else:
                    print("No new line found, sleeping...")  # Debugging line
                    log_file.seek(where)
                    await asyncio.sleep(1)  # Poll the file every second for new logs

    await read_logs()


# apprioach like tail -f
# async def send_logs_to_websocket(consumer):
#     log_file_path = (
#         "C:\\GitHub\\Django-WebSockets\\dj_websockets_2\\HISTORYlistener.log"
#     )

#     async def follow(thefile):
#         thefile.seek(0, os.SEEK_END)
#         while True:
#             line = thefile.readline()
#             if not line:
#                 await asyncio.sleep(0.1)
#                 continue
#             yield line

#     async def read_logs():
#         with open(log_file_path, "r") as log_file:
#             async for line in follow(log_file):
#                 await consumer.send(
#                     {
#                         "type": "websocket.send",
#                         "text": json.dumps({"log_lines": line.strip()}),
#                     }
#                 )
#                 print(line, end="")  # Optional: Also print to the server console

#     await read_logs()
