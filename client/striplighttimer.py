'''Example Timer Client'''
import datetime
import threading
import time

import requests

HEADERS = {'accept': 'application/json'}


def timer(on_hour, on_minute, off_hour, off_minute, host='http://localhost:8000', strip_id=1):
    '''Turns LED strips on and off.'''
    API_ADDRESS = f'/v1/strip/{strip_id}/power'
    host = host.rstrip('/')
    while True:
        now = datetime.datetime.today().timetuple()
        if now.tm_hour == on_hour and now.tm_min == on_minute:
            payload = {'power': 'true'}
            strip = requests.put(
                url=host + API_ADDRESS, headers=HEADERS, params=payload)

        elif now.tm_hour == off_hour and now.tm_min == off_minute:
            payload = {'power': 'false'}
            strip = requests.put(
                url=host + API_ADDRESS, headers=HEADERS, params=payload)

        else:
            time.sleep(59)
            continue
        if strip.status_code != 200:
            print("Mario looses a life!")
            print(strip.text)

        time.sleep(59)


if __name__ == "__main__":
    MARIO = "http://mario.clients.shimley:8000/"
    LUIGI = "http://luigi.clients.shimley:8000"

    mario = threading.Thread(target=timer, args=(18, 00, 2, 00, MARIO, 1))
    mario.start()

    luigi = threading.Thread(target=timer, args=(18, 00, 2, 00, LUIGI, 1))
    luigi.start()

    mario.join()
    luigi.join()
