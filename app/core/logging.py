import logging
import os

LOG_FILE_PATH = "/www/wwwlogs/python/recall_api/gunicorn_error.log"

def setup_logging():
    # Ensure the log directory exists
    log_dir = os.path.dirname(LOG_FILE_PATH)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE_PATH)
        ]
    )