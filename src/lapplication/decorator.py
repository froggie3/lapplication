import logging
import time
from contextlib import ContextDecorator

logger = logging.getLogger(__name__)


class timer(ContextDecorator):
    def __init__(self, name="timer"):
        self.timer_name = name
        self.start = float(0)

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, exc_type, exc, exc_tb):
        logger.debug(
            "[{}] time elapsed = {:.9f}s".format(
                self.timer_name, time.time() - self.start
            )
        )
