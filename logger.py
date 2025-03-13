import logging
import os
import sys
from config import LOG_DIR, LOG_NAME

sys.stdout.reconfigure(encoding="utf-8")

LOG_FILE = os.path.join(LOG_DIR, LOG_NAME)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Store Logs
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Terminal Output
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Logs Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_logger():
    return logger
