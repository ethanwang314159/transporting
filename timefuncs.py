from datetime import datetime

def HHMM():
    HHMM = datetime.now().strftime('%H%M')
    return HHMM

if __name__ == "__main__":
    result = HHMM()
    print(result)
else:
    print('HHMM module imported')