import requests
import pytz
from datetime import datetime
import logging


logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)


def load_attempts():
    page = 1
    pages = 1
    logger.info(pages)
    while page <= pages:
        payload = {'page': page}
        logger.info(payload)
        solution_attempts = requests.get('https://devman.org/api/challenges/solution_attempts/', params=payload).json()
        pages = solution_attempts['number_of_pages']
        yield solution_attempts['records']
        page += 1


def get_attempt_time(attempt):
    try:
        return pytz.utc.localize(datetime.fromtimestamp(attempt['timestamp']))
    except TypeError:
        return None


def get_time_zone(attempt):
    return pytz.timezone(attempt['timezone'])


def convert_time_according_to_time_zone(attempt_time, time_zone):
    try:
        return attempt_time.astimezone(time_zone)
    except AttributeError:
        return None


def get_midnighters():
    midnighters = set()
    midnight_hour = 0
    morning_hour = 7
    for records in solution_attempts:
        for attempt in records:
            attempt_time = get_attempt_time(attempt)
            time_zone = get_time_zone(attempt)
            attempt_time_local = convert_time_according_to_time_zone(attempt_time, time_zone)
            try:
                if midnight_hour < attempt_time_local.hour < morning_hour:
                    midnighters.add(attempt['username'])
            except AttributeError:
                pass
    return midnighters


def output_midnighters_to_console(midnighters):
    print('List of Night Owls at DEVMAN.org: ')
    for midnighter in midnighters:
        print(midnighter)


if __name__ == '__main__':
    solution_attempts = load_attempts()
    midnighters = get_midnighters()
    output_midnighters_to_console(midnighters)