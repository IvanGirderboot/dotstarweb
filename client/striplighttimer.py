import datetime
import time

import requests
HEADERS = {'accept': 'application/json'}
MARIO_API="http://mario.clients.shimley:8000/v1/strip/1/power"
LUIGI_API="http://luigi.clients.shimley:8000/v1/strip/1/power"
def timer():
       '''Turns LED strips on and off.'''
    while True: 
        
        now = datetime.datetime.today().timetuple()
        if now.tm_hour == 18 and now.tm_min == 0:
            payload = {'power':'true'}
            mario = requests.put(url=MARIO_API, headers=HEADERS, params=payload)
            luigi = requests.put(url=LUIGI_API, headers=HEADERS, params=payload)
        elif now.tm_hour == 2 and now.tm_min == 0:
            payload = {'power':'false'}
            mario = requests.put(url=MARIO_API, headers=HEADERS, params=payload)
            luigi = requests.put(url=LUIGI_API, headers=HEADERS, params=payload)
        else:
            time.sleep(59)
            continue
        if mario.status_code!= 200:
            print("Mario looses a life!")
        if luigi.status_code!= 200:
            print("Luigi Looses a Life")
        time.sleep(59)
        
if __name__ == "__main__":
    timer()
    

