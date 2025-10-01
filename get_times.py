import requests
from datetime import datetime
from utc_to_aest import UTCtoAEST
from timefuncs import HHMM

def getTimes(time):
    url = 'https://transportnsw.info/api/trip/v1/departure-list-request'
    params = {
        'date': '20251001',
        'debug': 'false',
        'depArrMacro': 'dep',
        'depType': 'stopEvents',
        'name': 'G2153190',
        'time': time,
        'lines': 'nsw:14601: :H:sj2',
        'type': 'stop',
        'accessible': 'false'
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        del data['version']

        if 'locations' in data:
            data['loc'] = {
                'name': data['locations'][0]['name'],
                'nick': data['locations'][0]['disassembledName'],
                'coord': data['locations'][0]['coord'],
                'suburb': data['locations'][0]['suburb'],
            }
            del data['locations']

        if 'stopEvents' in data:
            stop_events = data['stopEvents'][:5]
            
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

            current_time = datetime.now()
            next_bus = None
            next_realtime_bus = None
            min_time_diff = float('inf')
            min_realtime_time_diff = float('inf')

            for stop_event in stop_events:
                dep_time_str = stop_event['departureTime']
                dep_time = datetime.strptime(dep_time_str, '%Y/%m/%d %H:%M:%S')

                time_diff = (dep_time - current_time).total_seconds()

                if time_diff > 0:
                    if time_diff < min_time_diff:
                        min_time_diff = time_diff
                        next_bus = stop_event

                    if stop_event['realtimeStatus'] and time_diff < min_realtime_time_diff:
                        min_realtime_time_diff = time_diff
                        next_realtime_bus = stop_event

            if next_bus:
                next_bus_time = next_bus['departureTime']
                next_bus_wait_time = divmod(min_time_diff, 60)
                print(f"Next bus departs at {next_bus_time} (in {int(next_bus_wait_time[0])} minutes {int(next_bus_wait_time[1])} seconds).")

            if next_realtime_bus:
                next_realtime_bus_time = next_realtime_bus['departureTime']
                next_realtime_bus_wait_time = divmod(min_realtime_time_diff, 60)
                print(f"Next bus with real-time status departs at {next_realtime_bus_time} (in {int(next_realtime_bus_wait_time[0])} minutes {int(next_realtime_bus_wait_time[1])} seconds).")
                print(f"Details of real-time bus: {next_realtime_bus}")
            else:
                print("No real-time bus available at this time.")
        else:
            print('stopEvents not found in the response.')
    else:
        print('Failed to retrieve data. Status code:', response.status_code)


getTimes(HHMM())