import logging
import json


class WebSocketHandler(logging.Handler):
    def __init__(self, send_function):
        super().__init__()
        self.send_function = send_function

    def emit(self, record):
        log_entry = self.format(record)
        self.send_function(
            {
                "type": "websocket.send",
                "text": json.dumps({"log": log_entry}),
            }
        )
