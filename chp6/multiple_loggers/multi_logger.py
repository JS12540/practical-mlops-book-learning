import logging
import sys

def setup_logging(log_file="app.log"):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # ---- STDOUT handler (INFO and below) ----
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)
    stdout_handler.setFormatter(formatter)

    # ---- STDERR handler (ERROR and above) ----
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.ERROR)
    stderr_handler.setFormatter(formatter)

    # ---- File handler (ALL levels) ----
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Avoid duplicate handlers if setup_logging is called twice
    logger.handlers.clear()

    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_logging("my_app.log")

logger.debug("Debug message (file only)")
logger.info("Info message (stdout + file)")
logger.warning("Warning message (stdout + file)")
logger.error("Error message (stderr + file)")
logger.critical("Critical message (stderr + file)")
