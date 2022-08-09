import time 
from datetime import date,datetime, timezone
from bs4 import BeautifulSoup
from urllib.request import urlopen
import db 
import re
import texts 
  
def fetch_meals():
    '''
    get meals of yemekhane for this month and if available for next 
    '''

    urls = ["https://yemekhane.boun.edu.tr/aylik-menu"]
    try:
        page = urlopen(urls[0])
    except: 
        return
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    urls.append(soup.find_all("li", {"class": "date-next"})[0].findChild("a")['href'])

    canteens = ["Öğle Yemeği","Akşam Yemeği"]
    meals_of_both_canteens = {canteens[0]: {}, 
                                canteens[1]: {}}
    for url in urls:
        try:
            page = urlopen(url)
        except: 
            return

        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        month = soup.find("h3").get_text()
        month = ''.join([i for i in month if not i.isdigit()]).strip()
        month_num = texts.get_month_num(month,"tr")
        s = soup.get_text()
        for day in range(1,32):
            date = str(day)+" "+month
            date_num = str(day)+"."+str(month_num)
            start = s.find(date)
            if (start==-1): continue
            for c in canteens:
                meals = []
                start = s[start:].find(c)+len(c)+start
                for line in s[start:].splitlines():
                    if (line=='\xa0'): 
                        break
                    l = line.strip()
                    if (l):
                        if (',' in line):
                            meals.extend([s.strip() for s in line.split(',')])
                        else:
                            meals.append(l)
                meals_of_both_canteens[c][date_num]=meals 

    return meals_of_both_canteens


if __name__=="__main__":
    meals = fetch_meals()
    print(meals["Öğle Yemeği"].keys())

