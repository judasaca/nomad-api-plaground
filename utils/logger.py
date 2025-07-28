from loguru import logger
import sys
import json
from time import time
from functools import wraps

# Configure loguru
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
#    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
#           "<level>{level: <8}</level> | "
#           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
#           "<level>{message}</level>"
)

# Optional: log to a file as JSON
#logger.add("debug.json", serialize=True, level="DEBUG")

# Timing decorator
def log_timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        logger.debug(f"🔄 Starting '{func.__name__}'...")
        result = func(*args, **kwargs)
        elapsed = time() - start
        logger.success(f"✅ Finished '{func.__name__}' in {elapsed:.3f}s")
        return result
    return wrapper

