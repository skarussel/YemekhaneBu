import time
from datetime import date, datetime, timezone
from bs4 import BeautifulSoup
from urllib.request import urlopen
import db
import re
import texts
from translation import translate_word, translate_list
import pytz


istanbul = pytz.timezone("Europe/Istanbul")


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
    urls.append(soup.find_all(
        "li", {"class": "date-next"})[0].findChild("a")['href'])

    canteens = ["Öğle Yemeği", "Akşam Yemeği"]
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
        month_num = texts.get_month_num(month, "tr")
        s = soup.get_text()
        for day in range(1, 32):
            date = str(day)+" "+month
            next_date = str(day+1)+" "+month
            date_num = str(day)+"."+str(month_num)
            start = s.find(date)
            end = s.find(next_date)
            if (start == -1):
                continue
            for c in canteens:
                meals = []
                if (s[start:end].find(c) == -1):
                    continue
                start = s[start:end].find(c)+len(c)+start
                for line in s[start:].splitlines():
                    if (line == '\xa0'):
                        break
                    l = line.strip()
                    if (l):
                        if (',' in line):
                            meals.extend([s.strip() for s in line.split(',')])
                        else:
                            meals.append(l)
                meals_of_both_canteens[c][date_num] = meals

    return meals_of_both_canteens


def fetch_ingredients(ingredients):

    url = "https://yemekhane.boun.edu.tr/aylik-menu"

    try:
        page = urlopen(url)
    except:
        return ingredients, None
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    new_ingredients = []
    mealSet = set()
    links = soup.findAll('a')

    for link in links:
        if (link.has_attr("datatype")):
            mealSet.add(link)

    base_url = "https://yemekhane.boun.edu.tr"
    meal_names = [m.text for m in mealSet]
    links = [m["href"] for m in mealSet]
    link_dict = dict(zip(meal_names, links))

    for meal, link in link_dict.items():
        raw_ings = None
        ing = None
        translated_ings = [None, None]
        kcal = None
        translated_kcal = [None, None]
        if meal not in ingredients.keys():
            try:
                ingridient_url = base_url + link
                page = urlopen(ingridient_url)
                html = page.read().decode("utf-8")
                soup = BeautifulSoup(html, "html.parser")
                fields = soup.find_all("div", class_="field-items")
                labels = soup.find_all("div", class_="field-label")
                if fields:
                    labels = [x.text.strip() for x in labels]
                    if ("İçindekiler:" in labels and "Kalori Miktarı:" in labels):
                        kcal = fields[0].text
                        raw_ings = fields[1]
                    elif ("Kalori Miktarı:" in labels):
                        kcal = fields[0].text
                    elif ("İçindekiler:" in labels):
                        raw_ings = fields[0]

                    if (kcal and "gr" in kcal):
                        # kcal and size of portions in gram available
                        kcal = kcal[:kcal.index(
                            "-")] + kcal[kcal.index("("):].strip()
                    if (raw_ings):
                        raw_ings = [x.text for x in raw_ings.find_all("div")]
                        raw_ings = [x for x in raw_ings if x !=
                                    "İçindeki Malzemeler ( Çiğ )\n"]
                        raw_ings = [s for s in raw_ings if re.sub(
                            " *\d+ *gr\.*", "", s)]
                        raw_ings = [s for s in raw_ings if re.sub(
                            "\d|\( *Çiğ *\)|\.", "", s)]
                        raw_ings = "\n".join(raw_ings)
                        translated_ings = translate_word(raw_ings)
                    if (kcal):
                        translated_kcal = translate_word(kcal)

                    ingredients[meal] = [[kcal, raw_ings], [translated_kcal[0], translated_ings[0]], [
                        translated_kcal[1], translated_ings[1]]]
                    new_ingredients.append(meal)

            except Exception as e:
                print(
                    f"{datetime.now(istanbul)}: Error occured during fetching ingredients")
                print(meal)
                print(kcal)
                print(raw_ings)
                print(e)
                print()

    return ingredients, new_ingredients
