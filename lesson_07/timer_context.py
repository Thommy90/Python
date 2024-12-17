import time
import logging
import math

from lesson_05.run import Price


class TimerContext:
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end_time = time.time()
        elapsed_time = round(self.end_time - self.start_time, 4)
        logging.info(f"Code block executed in {elapsed_time} seconds")


# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

with TimerContext():
    time.sleep(2)

tablet = Price(value=400, currency="USD")
keyboard = Price(value=30, currency="EUR")
with TimerContext():
    logging.info(keyboard + tablet)

with TimerContext():
    result = math.factorial(1000)
    logging.info(result)

with TimerContext():
    time.sleep(1.5)
