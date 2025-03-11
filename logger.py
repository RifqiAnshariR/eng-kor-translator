import logging
import os
import sys

# Pastikan stdout menggunakan UTF-8 sebelum digunakan
sys.stdout.reconfigure(encoding="utf-8")

# Setup log directory and file
LOG_DIR = "log"
LOG_NAME = "app.log"

LOG_FILE = os.path.join(LOG_DIR, LOG_NAME)

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create file handler to store logs
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")  # Tambahkan encoding utf-8
file_handler.setLevel(logging.DEBUG)

# Create console handler for output in terminal
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Create a formatter and add it to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_logger():
    return logger
