import pytz
import texts 
from datetime import datetime, timezone, timedelta
from dateutil.parser import parse


istanbul = pytz.timezone("Europe/Istanbul")

def get_days_of_week(day):
    
    weekday = day.weekday()
    dates=[]
    for i in range(weekday,6-weekday,-1):
        date = day - timedelta(i)
        date = f"{date.day}.{date.month}"
        dates.append(date)
    dates.append(f"{day.day}.{day.month}")
    for i in range(0,6-weekday):
        date = day + timedelta(i)
        date = f"{date.day}.{date.month}"
        dates.append(date)
    
    return dates 

def get_next_days(day, num_days=3):
    
    dates=[]
    dates.append(f"{day.day}.{day.month}")
    for i in range(0,num_days):
        date = day + timedelta(i)
        date = f"{date.day}.{date.month}"
        dates.append(date)
    
    return dates

def is_date(l, fuzzy=False):
    """
    """
    for string in l:
      try: 
          c = parse(string, fuzzy=fuzzy)
          return c

      except ValueError:
        pass

    return -1 

if __name__=="__main__":
    c=0
    if (c):
        print("ok")
    else:
        print("not")


