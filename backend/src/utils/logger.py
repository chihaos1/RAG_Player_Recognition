import json
import logging.config
import pathlib
from datetime import datetime
from functools import wraps

logging_initialized = False

def setup_logging():
    global logging_initialized
    log_filename = pathlib.Path.cwd().parent / f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"

    if not logging_initialized:
        config_file = pathlib.Path.cwd().parent / "config/log_config.json"
        with open(config_file) as fhand:
            config = json.load(fhand)
            config["handlers"]["file"]["filename"] = log_filename
        logging_initialized = True

    
    logging.config.dictConfig(config)
    
def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        setup_logging()

        try:
            logging.info(f"Calling function: {func.__name__} with arguments: {args}, {kwargs}")
            result = func(*args, **kwargs)
            logging.info(f"Function -> {func.__name__} returned: {result}")
        except Exception as e:
            logging.warning(f"Function {func.__name__} failed with exception: {e}")
            raise e

        return result
    return wrapper