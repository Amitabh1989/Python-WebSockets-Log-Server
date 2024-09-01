# # import pytest
# # import logging
# # import time
# # import random


# # # Set up a logger
# # def setup_logger(log_file, level=logging.INFO):
# #     logger = logging.getLogger(__name__)
# #     logger.setLevel(level)
# #     handler = logging.FileHandler(log_file)
# #     handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
# #     logger.addHandler(handler)
# #     return logger


# # @pytest.mark.parametrize(
# #     "log_speed", [0.1, 0.5, 1.0, 5.0, 10.0]
# # )  # Adjust logging speed here
# # def test_logging(log_speed):
# #     log_file = pytest.config.getoption("--log-file")
# #     logger = setup_logger(log_file)

# #     for _ in range(100):  # Adjust the range for more or fewer log entries
# #         logger.info(f"Logging gibberish: {random.choice(['foo', 'bar', 'baz', 'qux'])}")
# #         time.sleep(log_speed)  # Log at the specified speed

# #     # Simulate a pass/fail scenario
# #     assert random.choice([True, False]), "Simulated test failure"


# import pytest
# import time
# import random
# import controller
# from queue import Queue
# import logging
# from logging.handlers import QueueHandler, QueueListener

# log_queue = Queue()

# print(f"Controller version : {controller.get_version()}")


# # Set up a logger
# def setup_logger(log_file, level=logging.INFO):
#     # logger = logging.getLogger(__name__)
#     # logger.setLevel(level)
#     # handler = logging.FileHandler(log_file)
#     # logging.basicConfig(level=logging.INFO, handlers=[QueueHandler(log_queue)])

#     # handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
#     # logger.addHandler(handler)
#     # return logger
#     log_queue = Queue(-1)
#     queue_handler = QueueHandler(log_queue)

#     logger = logging.getLogger()
#     logger.addHandler(queue_handler)

#     console_handler = logging.StreamHandler()
#     formatter = logging.Formatter("%(threadName)s: %(message)s")
#     console_handler.setFormatter(formatter)

#     file_handler = logging.FileHandler("queue_example.log")
#     file_handler.setFormatter(formatter)

#     return logger

#     # listener = QueueListener(log_queue, console_handler, file_handler)
#     # listener.start()

#     # logger.warning('Look out!')

#     # listener.stop()


# @pytest.fixture
# def log_file(pytestconfig):
#     return pytestconfig.getoption("--log-file")


# @pytest.mark.parametrize(
#     # "log_speed", [0.1, 0.5, 1.0, 5.0, 10.0]
#     "log_speed",
#     [0.1, 0.5, 1.0, 5.0],
# )  # Adjust logging speed here
# def test_logging(log_speed, log_file):
#     logger = setup_logger(log_file)

#     for _ in range(1):  # Adjust the range for more or fewer log entries
#         logger.info(
#             f"Logging gibberish: {random.choice(['foo', 'bar', 'baz', 'qux'])} => Controller version : {controller.get_version()} "
#         )
#         time.sleep(log_speed)  # Log at the specified speed

#     # Simulate a pass/fail scenario
#     assert random.choice([True, False]), "Simulated test failure"


# ================================================


# import pytest
# import logging
# import time
# import random


# # Set up a logger
# def setup_logger(log_file, level=logging.INFO):
#     logger = logging.getLogger(__name__)
#     logger.setLevel(level)
#     handler = logging.FileHandler(log_file)
#     handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
#     logger.addHandler(handler)
#     return logger


# @pytest.mark.parametrize(
#     "log_speed", [0.1, 0.5, 1.0, 5.0, 10.0]
# )  # Adjust logging speed here
# def test_logging(log_speed):
#     log_file = pytest.config.getoption("--log-file")
#     logger = setup_logger(log_file)

#     for _ in range(100):  # Adjust the range for more or fewer log entries
#         logger.info(f"Logging gibberish: {random.choice(['foo', 'bar', 'baz', 'qux'])}")
#         time.sleep(log_speed)  # Log at the specified speed

#     # Simulate a pass/fail scenario
#     assert random.choice([True, False]), "Simulated test failure"


# import pytest
# import time
# import random
# import controller
# from queue import Queue
# import logging
# from logging.handlers import QueueHandler, QueueListener


# print(f"Controller version : {controller.get_version()}")


# # Set up a logger
# def setup_logger(log_file, level=logging.INFO):
#     logger = logging.getLogger(__name__)
#     logger.setLevel(level)
#     handler = logging.FileHandler(log_file)
#     handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
#     logger.addHandler(handler)
#     return logger


# @pytest.fixture
# def log_file(pytestconfig):
#     return pytestconfig.getoption("--log-file")


# @pytest.mark.parametrize(
#     "log_speed",
#     [0.1, 0.5, 1.0, 5.0],
# )  # Adjust logging speed here
# def test_logging(log_speed, log_file):
#     logger = setup_logger(log_file)

#     for _ in range(1):  # Adjust the range for more or fewer log entries
#         logger.info(
#             f"Logging gibberish: {random.choice(['foo', 'bar', 'baz', 'qux'])} => Controller version : {controller.get_version()} "
#         )
#         time.sleep(log_speed)  # Log at the specified speed

#     # Simulate a pass/fail scenario
#     assert random.choice([True, False]), "Simulated test failure"


# =======================================================


import pytest
import time
import random

# import controller
from queue import Queue
import logging
from logging.handlers import QueueHandler, QueueListener
from ..utils.logging_utils import (
    WebSocketHandler,
)  # Assuming WebSocketHandler is in utils/logging_utils.py


# Print controller version
# print(f"Controller version : {controller.get_version()}")


# Set up a logger
# def setup_logger(log_file, send_function=None, level=logging.INFO):
#     logger = logging.getLogger(__name__)
#     logger.setLevel(level)

#     # Create a file handler
#     file_handler = logging.FileHandler(log_file)
#     file_handler.setFormatter(
#         logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
#     )

#     # Create a queue handler for managing logs in a thread-safe manner
#     log_queue = Queue()
#     queue_handler = QueueHandler(log_queue)

#     logger.addHandler(queue_handler)
#     logger.addHandler(file_handler)

#     # Set up a listener to output logs from the queue to the file handler and WebSocket handler if provided
#     handlers = [file_handler]

#     if send_function:
#         websocket_handler = WebSocketHandler(send_function)
#         handlers.append(websocket_handler)

#     listener = QueueListener(log_queue, *handlers)
#     listener.start()

#     return logger, listener


def setup_logger(log_file=None, send_function=None, level=logging.INFO):
    logger = logging.getLogger(__name__)
    logger.setLevel(level)

    # Create a file handler only if log_file is provided
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        handlers = [file_handler]
    else:
        handlers = []

    # Create a queue handler for managing logs in a thread-safe manner
    log_queue = Queue()
    queue_handler = QueueHandler(log_queue)
    logger.addHandler(queue_handler)

    # Add WebSocket handler if send_function is provided
    if send_function:
        websocket_handler = WebSocketHandler(send_function)
        handlers.append(websocket_handler)

    # Start QueueListener if there are handlers
    if handlers:
        listener = QueueListener(log_queue, *handlers)
        listener.start()
    else:
        listener = None

    return logger, listener, log_queue


@pytest.fixture
def log_file(pytestconfig):
    log_file_path = pytestconfig.getoption("--log-file")
    # Provide a default path if none is provided
    if log_file_path is None:
        log_file_path = "default.log"
    return log_file_path


@pytest.mark.parametrize(
    "log_speed",
    [0.1, 0.5, 1.0, 5.0],
)  # Adjust logging speed here
def test_logging(log_speed, log_file, websocket_send_function=None):
    logger, listener, log_queue = setup_logger(
        log_file, send_function=websocket_send_function
    )

    try:
        for _ in range(10):  # Adjust the range for more or fewer log entries
            logger.info(
                f"Logging gibberish: {random.choice(['foo', 'bar', 'baz', 'qux'])} => Controller version "
            )
            time.sleep(log_speed)  # Log at the specified speed

        # Simulate a pass/fail scenario
        assert random.choice([True, False]), "Simulated test failure"
    finally:
        listener.stop()  # Ensure the listener is stopped when done
