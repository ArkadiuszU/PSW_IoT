import requests
import json
from datetime import datetime
names = ["developer", "stop_bath" , "fixer"]

config_date = None

def PostCounter(name):
    response = requests.post("http://silgy.org:3030/api/counters", data={
        'name':  "{}".format(name)
    })
    if(response.status_code == 200): 
        print("API: success in counter up")
    else:
        print("API: fault in counter up")
    return response

def Post_IoT(name, temp, time, counter, status):
    response = requests.post("https://dweet.io/dweet/for/au", data={
    "actual_bath_name": "{}".format(name),
    "actual_bath_time":  time,
    "total_bath_counter": counter,
    "status" : status,
    "temp": [
         temp[0],     #"developer"
         temp[1],    #"fixer"
         temp[2]    #"stop_bath"       
        ]
}
)
    return response

def Get_settings():
    global config_date
    new_config = False
    for name in names:
        response = requests.get("http://silgy.org:3030/api/settings/{}".format(name))
        if(response.status_code == 200): 
            r = response.json()
            d = datetime.strptime(r["modified"], '%Y-%m-%d %H:%M:%S')
            if( config_date == None or config_date < d):
                config_date = d
                new_config = True
        else:
            print("API: fault in get settings")
    if(new_config):
        print("new configuration received [{}]".format(config_date))
            
    #Get_counter()
    
def Get_counter():
    response = requests.get("http://silgy.org:3030/getCounter")
    #response = requests.get("http://silgy.org:3030/api/settings/fixer")
    if(response.status_code == 200): 
        y = json.loads(response.text)
        return(y["counter"]) 
    else:
        print("API: fault in get counters")
        