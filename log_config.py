import logging
from logging.handlers import RotatingFileHandler


def setup_logging(log_file='app.log', log_level=logging.INFO):
    """
    Set up logging configuration for the application.

    Parameters:
    - log_file: Name of the file where logs will be saved.
    - log_level: The level of logging (e.g., logging.INFO, logging.DEBUG).
    """
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(log_level)  # Set the logging level

    # Define log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a console handler and set the format for console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Set up log rotation for the file handler (logs will be stored in 'log_file')
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10 * 1024 * 1024, backupCount=5
    )  # 10 MB size limit and 5 backup files
    file_handler.setFormatter(formatter)

    # Remove existing handlers to prevent duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Optional: Log rotating behavior or additional features
    logging.debug("Logging setup completed.")
