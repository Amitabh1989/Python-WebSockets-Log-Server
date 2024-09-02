# import logging
# from logging.handlers import QueueHandler
# from queue import Queue
# import time

# # ... rest of your script

# # Logging setup
# log_queue = Queue()
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# queue_handler = QueueHandler(log_queue)
# logger.addHandler(queue_handler)

# # Use the logger in your script
# logger.info("Starting script...")

# # ... your script logic here

# # Process log messages from the queue
# while True:
#     if not log_queue.empty():
#         log_record = log_queue.get()
#         print(f"Received log record: {log_record}")
#     time.sleep(0.1)

import logging
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
import time


def setup_logger(queue):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Set up the QueueHandler
    queue_handler = QueueHandler(queue)
    logger.addHandler(queue_handler)

    return logger


def log_messages(logger):
    for i in range(5):
        logger.info(f"Log message {i}")
        time.sleep(1)  # Simulate some processing time


if __name__ == "__main__":
    log_queue = Queue()
    logger = setup_logger(log_queue)
    log_messages(logger)
