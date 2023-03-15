from datetime import datetime, timezone
from time import sleep
import requests


TOKEN_PATH = "../resources/token.txt"
LIMIT_URL = "https://api.github.com/rate_limit"


def get_token_header():
    with open(TOKEN_PATH, "r") as token_file:
        token = token_file.readline()
        if token != "":
            return {"Authorization": "Bearer " + token}
    raise AssertionError("Token file could not be read")


def get_remaining_requests():
    reponse = requests.get(LIMIT_URL, headers=get_token_header()).json()
    remaining_requests = reponse['rate']['remaining']
    return remaining_requests


def get_time_of_reset():
    reponse = requests.get(LIMIT_URL, headers=get_token_header()).json()
    utc_timestamp = reponse['rate']['reset']
    reset_time = datetime.fromtimestamp(utc_timestamp, timezone.utc)
    return reset_time


def sleep_till(end: datetime):
    now = datetime.now(timezone.utc)
    till_reset = end - now
    seconds_till_reset = till_reset.seconds
    print(f"Out of requests, sleeping for: {str(till_reset)}")
    sleep(seconds_till_reset + 1)


def sleeper(number_of_requests: int = 1):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            if sleeper.remaining - number_of_requests == 0:
                sleep_till(get_time_of_reset())
                sleeper.remaining = get_remaining_requests()

            sleeper.remaining -= number_of_requests
            fn(*args, **kwargs)

        return wrapper
    return decorator


sleeper.remaining = get_remaining_requests()
