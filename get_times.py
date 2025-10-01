import requests
from utc_to_aest import UTCtoAEST

def getTimes(time):
    url = 'https://transportnsw.info/api/trip/v1/departure-list-request'
    params = {
        'date': '20251001',
        'debug': 'false',
        'depArrMacro': 'dep',
        'depType': 'stopEvents',
        'name': 'G2153190',
        'time': time,
        'type': 'stop',
        'accessible': 'false'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        del data['version']
        if 'locations' in data:
            data['loc'] = {
                'name':data['locations'][0]['name'],
                'nick':data['locations'][0]['disassembledName'],
                'coord':data['locations'][0]['coord'],
                'suburb':data['locations'][0]['suburb'],
            }
            del data['locations']
        else:
            print('locations not found in the response.')

        if 'stopEvents' in data:
            stop_events = data['stopEvents'][:15]
            
            for stop_event in stop_events:
                unwanted_keys = ['isCancelled', 'isAccessible', 'transportation', 'location', 'id', 'alerts', 'isBookingRequired', 'onwardLocations', 'previousLocations', 'realtimeTripId', 'avmsTripId', 'isHighFrequency']
                
                for key in unwanted_keys:
                    if key in stop_event:
                        del stop_event[key]
                if stop_event["realtimeStatus"] == None:
                    stop_event["realtimeStatus"] = False
                else:
                    stop_event["realtimeStatus"] = True
                
                utc_keys = ['departureTime', 'departureTimePlanned', 'departureTimeEstimated', 'arrivalTimeEstimated', 'arrivalTimePlanned']
                for key in utc_keys:
                    if key in stop_event:
                        stop_event[key] = UTCtoAEST(stop_event[key])


            data['stopEvents'] = stop_events
            print(str(data).replace("'", '"'))
        else:
            print('stopEvents not found in the response.')
    else:
        print('Failed to retrieve data. Status code:', response.status_code)

getTimes('1732')