import logging
import subprocess
import sys
from logging.handlers import QueueHandler, QueueListener, StreamHandler, FileHandler
from multiprocessing import Process, Queue
import argparse


def logging_consumer(queue, log_file):
    # Set up handlers where logs will be sent
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )

    file_handler = FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )

    # Set up the QueueListener with the handlers
    listener = QueueListener(queue, console_handler, file_handler)
    listener.start()

    try:
        while True:
            pass  # Keeps the listener alive
    except KeyboardInterrupt:
        listener.stop()


def logging_producer(queue, script, log_speed):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    queue_handler = QueueHandler(queue)
    logger.addHandler(queue_handler)

    # Run the script with log_speed argument
    process = subprocess.Popen(
        [sys.executable, script, "--log-speed", str(log_speed)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Log the output of the script
    for line in iter(process.stdout.readline, ""):
        logger.info(line.strip())

    process.stdout.close()
    process.wait()

    # Log any errors
    for line in iter(process.stderr.readline, ""):
        logger.error(line.strip())

    process.stderr.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Log consumer for running scripts and logging their output."
    )
    parser.add_argument(
        "--script", type=str, required=True, help="The script to run and log."
    )
    parser.add_argument(
        "--log-speed", type=float, default=1.0, help="Speed of logging in seconds"
    )
    parser.add_argument(
        "--logfile", type=str, default="output.log", help="The log file to write to."
    )

    args = parser.parse_args()

    log_queue = Queue()

    consumer_process = Process(target=logging_consumer, args=(log_queue, args.logfile))
    consumer_process.start()

    producer_process = Process(
        target=logging_producer, args=(log_queue, args.script, args.log_speed)
    )
    producer_process.start()

    producer_process.join()
    consumer_process.terminate()
