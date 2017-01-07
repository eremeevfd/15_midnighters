import requests
import pytz
from datetime import datetime


def load_attempts():
    pages = 1
    for page in range(pages):
        solution_attempts = requests.get('https://devman.org/api/challenges/solution_attempts/?page=2').json()
        yield solution_attempts['records']


def get_attempt_time(attempt):
    return pytz.utc.localize(datetime.fromtimestamp(attempt['timestamp']))


def get_time_zone(attempt):
    return pytz.timezone(attempt['timezone'])


def convert_time_according_to_time_zone(attempt_time, time_zone):
    return attempt_time.astimezone(time_zone)


def get_midnighters():
    midnighters = []
    for records in solution_attempts:
        for attempt in records:
            attempt_time = get_attempt_time(attempt)
            time_zone = get_time_zone(attempt)
            attempt_time_local = convert_time_according_to_time_zone(attempt_time, time_zone)
            if 0 < attempt_time_local.hour < 7:
                midnighters.append(attempt['username'])
    return midnighters


def output_midnighters_to_console(midnighters):
    print('List of Night Owls at DEVMAN.org: ')
    for midnighter in midnighters:
        print(midnighter)


if __name__ == '__main__':
    solution_attempts = load_attempts()
    midnighters = get_midnighters()
    output_midnighters_to_console(midnighters)