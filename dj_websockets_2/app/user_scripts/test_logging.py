import logging
import time


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

    for i in range(200):
        logger.info(f"Hello, world! We are live logging via websockets {i}")
        time.sleep(0.2)


if __name__ == "__main__":
    main()
