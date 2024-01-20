import random
import time


def wait() -> None:
    wait_time = random.randint(40, 50) + random.random()  # Time between requests
    time.sleep(wait_time)
