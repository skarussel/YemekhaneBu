import os
import re

import pymongo

collections = ["users", "ögle", "aksam", "translations"]

is_prod = os.environ.get("IS_FLY", None)
print(f"IS_PROD: {is_prod}")

if is_prod:
    username = os.environ["username"]
    pw = os.environ["pw"]
    con_str = os.environ["con_str"]
else:
    import config

    username = config.username
    pw = config.pw
    con_str = config.connection_string


def connect():
    client = pymongo.MongoClient(
        f"mongodb+srv://{username}:{pw}@cluster0.{con_str}.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )
    # f"mongodb+srv://{username}:{pw}@cluster0.{con_str}.mongodb.net/"

    return client


# user


def update_user(user, lang="en", auto=1, rating=0):
    """
    Add user to users table. If user already exists but lang or auto parameter differ, update user
    """
    client = connect()
    db = client.cluster0
    db.users.update_one(
        {"_id": user},
        {"$set": {"lang": lang, "auto": auto, "rating": rating}},
        upsert=True,
    )
    client.close()


def delete_user(user):
    client = connect()
    db = client.cluster0
    db.users.delete_one({"_id": user})
    client.close()


def read_user(user):
    client = connect()
    db = client.cluster0
    entry = db.users.find_one({"_id": user})
    client.close()
    return entry


def read_users():
    """
    returns all entries as a dict
    """
    client = connect()
    db = client.cluster0
    users = {}
    entries = []
    if "users" in list(db.list_collection_names()):
        entries = list(db.users.find())

    for e in entries:
        users[e["_id"]] = [e["lang"], e["auto"], e["rating"]]
    return users


# meals


def update_meals(entries):
    client = connect()
    db = client.cluster0
    ögle = entries.get("Öğle Yemeği")
    aksam = entries.get("Akşam Yemeği")
    for k, d in ögle.items():
        db.ögle.update_one({"_id": k}, {"$set": {"meals": d}}, upsert=True)
    for k, d in aksam.items():
        db.aksam.update_one({"_id": k}, {"$set": {"meals": d}}, upsert=True)
    client.close()


def read_meals(months=""):
    """
    return meals of month from db
    """
    client = connect()
    db = client.cluster0

    if type(months) == list:
        ögle, aksam = [], []
        for m in months:
            pattern = re.compile(f"\.{m}", re.I)
            ögle.append(list(db.ögle.find({"_id": {"$regex": pattern}})))
            aksam.append(list(db.aksam.find({"_id": {"$regex": pattern}})))
        ögle = [item for sublist in ögle for item in sublist]
        aksam = [item for sublist in aksam for item in sublist]
    else:
        pattern = re.compile(f"\.{months}", re.I)
        ögle = list(db.ögle.find({"_id": {"$regex": pattern}}))
        aksam = list(db.aksam.find({"_id": {"$regex": pattern}}))

    client.close()
    if not ögle and not aksam:
        return None
    meals = {"Öğle Yemeği": {}, "Akşam Yemeği": {}}
    for e in ögle:
        meals["Öğle Yemeği"][e["_id"]] = e["meals"]
    for e in aksam:
        meals["Akşam Yemeği"][e["_id"]] = e["meals"]

    return meals


# translations


def read_translations():
    client = connect()
    db = client.cluster0
    entries = list(db.translations.find())
    translations = {}
    for e in entries:
        translations[e["_id"]] = e["translation"]

    return translations


def update_translations(translations):
    client = connect()
    db = client.cluster0
    for meal, translation in translations.items():
        db.translations.update_one(
            {"_id": meal}, {"$set": {"translation": translation}}, upsert=True
        )

    client.close()


# ingredients
def read_ingredients():
    client = connect()
    db = client.cluster0
    entries = list(db.ingredients.find())
    ingredients = {}
    for e in entries:
        ingredients[e["_id"]] = [e["english"], e["german"]]

    return ingredients


def update_ingredients(ingredients):
    client = connect()
    db = client.cluster0
    for meal, ingredients in ingredients.items():
        db.ingredients.update_one(
            {"_id": meal},
            {"$set": {"english": ingredients[0], "german": ingredients[1]}},
            upsert=True,
        )

    client.close()


# feedback
def insert_feedback(user, feedback):
    client = connect()
    db = client.cluster0
    entry = {"user": user, "feedback": feedback}
    db.feedback.insert_one(entry)

    client.close()


def size(total=1):
    client = connect()
    db = client.cluster0
    u_size = db.users.count_documents({})
    ö_size = db.ögle.count_documents({})
    a_size = db.aksam.count_documents({})
    client.close()
    if not total:
        return u_size, ö_size, a_size
    return u_size + ö_size + a_size
