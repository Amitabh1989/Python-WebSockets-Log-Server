# import logging

# # from logging.handlers import QueueListener, StreamHandler, FileHandler
# from logging.handlers import QueueListener
# from logging import StreamHandler, FileHandler
# from queue import Queue


# def setup_listener(queue):
#     # Set up handlers where logs will be sent
#     console_handler = StreamHandler()
#     console_handler.setLevel(logging.DEBUG)
#     console_handler.setFormatter(
#         logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
#     )

#     file_handler = FileHandler("output.log")
#     file_handler.setLevel(logging.DEBUG)
#     file_handler.setFormatter(
#         logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
#     )

#     # Set up the QueueListener with the handlers
#     listener = QueueListener(queue, console_handler, file_handler)
#     listener.start()

#     return listener


# if __name__ == "__main__":
#     log_queue = Queue()
#     listener = setup_listener(log_queue)

#     # Keep the listener running to process incoming log messages
#     try:
#         while True:
#             pass
#     except KeyboardInterrupt:
#         listener.stop()


import logging
from logging.handlers import QueueHandler, QueueListener
from logging import StreamHandler, FileHandler
from multiprocessing import Process, Queue
import time
from test_logging import 


def logging_producer(queue):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    queue_handler = QueueHandler(queue)
    logger.addHandler(queue_handler)

    for i in range(10):
        logger.info(f"Logging message {i}")
        time.sleep(1)


def logging_consumer(queue):
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )

    file_handler = FileHandler("output.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )

    listener = QueueListener(queue, console_handler, file_handler)
    listener.start()

    try:
        while True:
            pass  # Keeps the listener alive
    except KeyboardInterrupt:
        listener.stop()


if __name__ == "__main__":
    log_queue = Queue()

    consumer_process = Process(target=logging_consumer, args=(log_queue,))
    consumer_process.start()

    producer_process = Process(target=logging_producer, args=(log_queue,))
    producer_process.start()

    producer_process.join()
    consumer_process.terminate()
