import random
import time


def wait() -> None:
    wait_time = random.randint(30, 40) + random.random()  # Time between requests
    time.sleep(wait_time)
