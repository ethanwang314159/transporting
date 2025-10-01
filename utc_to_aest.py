from datetime import datetime
import pytz

def UTCtoAEST(inp):
    try:
        AESTzone = pytz.timezone('Australia/Sydney')
        UTC = datetime.strptime(inp, "%Y-%m-%dT%H:%M:%SZ")
        UTC = pytz.utc.localize(UTC)
        AEST = UTC.astimezone(AESTzone)
        return AEST.strftime('%Y/%m/%d %H:%M:%S')
    except ValueError as e:
        return f"Error: Invalid timestamp format. Expected format: YYYY-MM-DDTHH:MM:SSZ. Details: {e}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    inp = input("Input a UTC timestamp: ")
    result = UTCtoAEST(inp)
    print(result)
else:
    print('UTC to AEST module imported')