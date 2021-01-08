import time

default_time = time.time()
default_seconds = default_time - 600


def timer(seconds=default_seconds):
    timer = default_time - seconds
    return abs(timer)
