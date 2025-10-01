import requests

url = 'https://transportnsw.info/api/trip/v1/departure-list-request'

params = {
    'date': '20251001',
    'debug': 'false',
    'depArrMacro': 'dep',
    'depType': 'stopEvents',
    'name': 'G2153190',
    'time': '1500',
    'type': 'stop',
    'accessible': 'false'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    if 'stopEvents' in data:
        stop_events = data['stopEvents'][:15]
        
        for stop_event in stop_events:
            unwanted_keys = ['isAccessible', 'transportation', 'location', 'id', 'alerts', 'isBookingRequired', 'onwardLocations', 'previousLocations', 'realtimeTripId', 'avmsTripId']
            
            for key in unwanted_keys:
                if key in stop_event:
                    del stop_event[key]

        data['stopEvents'] = stop_events
        print('Cleaned Data with First 15 Stop Events:', data)
    else:
        print('stopEvents not found in the response.')
else:
    print('Failed to retrieve data. Status code:', response.status_code)
