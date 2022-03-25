import requests
import time
import datetime
headers={'accept': 'application/json'}
payload={'power':'true'}
mario_API="http://mario.clients.shimley:8000/v1/strip/1/power"
luigi_API="http://luigi.clients.shimley:8000/v1/strip/1/power"
def timer():
    while True: 
        
        now = datetime.datetime.today().timetuple()
        if now.tm_hour == 18 and now.tm_min == 0:
            payload={'power':'true'}
            m=requests.put(mario_API, headers=headers,params=payload)
            l=requests.put(luigi_API, headers=headers,params=payload)
        if now.tm_hour == 2 and now.tm_min == 0:
            payload={'power':'false'}
            m=requests.put(mario_API, headers=headers,params=payload)
            l=requests.put(luigi_API, headers=headers,params=payload)
        if m.status_code!= 200:
            print("Mario looses a life!")
        if l.status_code!= 200:
            print("Luigi Looses a Life")
        time.sleep(59)
        
def main():
    timer()
    

