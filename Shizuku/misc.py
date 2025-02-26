import logging
import time

_boot_ = time.time()


def dbb():
    global db
    db = {}
    logging.info(f"Local Database Initialized.")
