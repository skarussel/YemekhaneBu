import os
from datetime import datetime, timedelta, timezone, time
from collections import Counter
from importlib_metadata import entry_points
import pytz
import os

import telegram
from yemek import fetch_meals
from telegram import ForceReply, Update, InlineKeyboardMarkup,InlineKeyboardButton #upm package(python-telegram-bot)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler,CallbackQueryHandler  #upm package(python-telegram-bot)
import db
import texts
from translation import translate_meal_list
from tabulate import tabulate 
from dateutil.parser import parse
from dates import get_days_of_week, get_next_days, is_date
import tgcalendar 
import os
import time as t 


# translate to turkish


users, meals,translated_meals = {},{},{}
istanbul = pytz.timezone("Europe/Istanbul")
admin = 0 
OFFSET = 127462 - ord('A')

def flag(code):
    code = code.upper()
    return chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)


lang_keyboard  = [
    [InlineKeyboardButton(f"{flag('tr')} Türkçe" , callback_data='tr')],
    [InlineKeyboardButton(f"{flag('gb')} English", callback_data='en')],
    [InlineKeyboardButton(f"{flag('de')} Deutsch", callback_data='de')]
]

locations = {"Kuzey (North)": (41.086696336374395, 29.0451391825363), 
            "Güney (South)": (41.082743411608014, 29.05166212188869),
            "Hisar": (41.08953171397676, 29.050996098768962),
            "Kandilli": (41.062491006860824, 29.05752964421144),
            "Sarıtepe": (41.24602520569113, 29.01246661875565)
            }


def help(update: Update, context: CallbackContext) -> None:
  
  update.message.reply_text(texts.help[users[update.message.from_user.id][0]], parse_mode='markdown')


def start(update: Update, context: CallbackContext) -> None:


  reply_markup = InlineKeyboardMarkup(lang_keyboard)
  update.message.reply_text(texts.start_conv.replace('/name', update.message.from_user.first_name))
  t.sleep(1)
  update.message.reply_text(texts.ask_for_language, reply_markup=reply_markup)


def language(update: Update, context: CallbackContext) -> None:
  

  reply_markup = InlineKeyboardMarkup(lang_keyboard)
  update.message.reply_text('''Lütfen bir Dil seçin / Please choose a Language / Bitte wähle eine Sprache''', reply_markup=reply_markup)


def cmeals(update: Update, context: CallbackContext) -> None:
  
  lang_arg = [i for i in ['en', 'de', 'tr'] if i in [a.lower() for a in context.args]]
  date = is_date(context.args)
  if lang_arg:
    lang=lang_arg[0]
  else: 
    lang = users[update.message.from_user.id][0]
  if (date==-1):
    date = datetime.now(istanbul)
  
  text = meal_of_day(date,lang)
  update.message.reply_text(text, parse_mode="markdown")


def tomorrow(update: Update, context: CallbackContext) -> None:
  
  lang_arg = [i for i in ['en', 'de', 'tr'] if i in [a.lower() for a in context.args]]
  if lang_arg:
    lang=lang_arg[0]
  else: 
    lang = users[update.message.from_user.id][0]
  
  date = datetime.now(istanbul) + timedelta(days=1)
  text = meal_of_day(date,lang)
  update.message.reply_text(text, parse_mode="markdown")

def calendar_handler(update: Update, context: CallbackContext):
    update.message.reply_text("Please select a date: ",
    reply_markup=tgcalendar.create_calendar(users[update.message.from_user.id][0]))

def meal_of_day(date,lang):
  key = f"{date.day}.{date.month}"
  ögle_meals = meals["Öğle Yemeği"].get(key)
  aksam_meals = meals["Akşam Yemeği"].get(key)

  if (not ögle_meals or not aksam_meals):
    return texts.food_not_available(lang,date,datetime.now(istanbul).date())
  

  if lang=="en":
    ögle_meals = [x[0] for x in list(map(translated_meals.get, ögle_meals))]
    aksam_meals = [x[0] for x in list(map(translated_meals.get, aksam_meals))]
  elif lang=="de":
    ögle_meals = [x[1] for x in list(map(translated_meals.get, ögle_meals))]
    aksam_meals = [x[1] for x in list(map(translated_meals.get, aksam_meals))]
  
  formatted_date = texts.get_date_string(date.day,date.month,date.weekday(),lang)
  text = f"*{formatted_date}*\n*{texts.mealtimes[lang][0]}*\n{ögle_meals[0]}\n{ögle_meals[1]}\n{ögle_meals[2]}\n{ögle_meals[3]}, "\
  f"{ögle_meals[4]}\n{', '.join(ögle_meals[5:])}\n\n"\
  f"*{texts.mealtimes[lang][1]}*\n{aksam_meals[0]}\n{aksam_meals[1]}\n{aksam_meals[2]}\n{aksam_meals[3]}, "\
  f"{aksam_meals[4]}\n{', '.join(aksam_meals[5:])}"

  return text

def button(update: Update, context: CallbackContext) -> None:
  query = update.callback_query
  query.answer()
  user_id = update.effective_user.id
  if (query.message.reply_markup.inline_keyboard[0][0].text=="🇹🇷 Türkçe"):
    lang = query.data
    # Language Selection
    if user_id in users:
      # Language change (update)
      query.edit_message_text(text=texts.update[lang],parse_mode='markdown') 
      values = list(users[user_id])
      values[0]=query.data
      users[user_id] = tuple(values)
      rating = values[2]
      finish_text = texts.language_change[lang]+" /help"
      db.update_user(user_id,lang,rating)
      query.edit_message_text(text=finish_text,parse_mode='markdown')

    else:
      # registration
      query.edit_message_text(text=texts.registration[lang],parse_mode='markdown')
      users[user_id] = (lang, 1, 0)
      finish_text =texts.welcome[lang]+texts.help[lang]
      db.update_user(user_id,lang)
      query.edit_message_text(text=finish_text,parse_mode='markdown')
      context.bot.send_message(admin, text=f"New User 🎉 {update.effective_user.full_name} is our {len(users.keys())}th User")


 
  # rating 
  elif query.data in ["1","2","3"]:
    lang, auto = users[user_id][0:2]
    query.edit_message_text(text=f"{texts.processing[lang]} ☺️",parse_mode='markdown')
    db.update_user(user_id,lang,auto, query.data)

    values = list(users[user_id])
    if (len(values)==3):
      values[2]=query.data
    else:
      values.append(query.data)
    users[user_id] = tuple(values)

    query.edit_message_text(text=f"{texts.rating_sucess[lang]} ☺️",parse_mode='markdown')



  # locations
  elif (query.message.reply_markup.inline_keyboard[0][0].text == "Kuzey (North)"):
    lang = users[user_id][0]
    long, lat = locations[query.data]
    loc = telegram.Location(lat, long)
    query.bot.send_message(chat_id=user_id, text=f"*{query.data} {texts.campus[lang]}* 👇🏻", parse_mode="markdown")
    query.bot.send_location(chat_id=user_id, location=loc)
    
  # times
  elif (query.data in ["breakfast", "lunch", "diner"]):
    lang = users[user_id][0]
    query.bot.send_message(chat_id=user_id, text=texts.get_meal_times(lang,query.data), parse_mode="markdown")

  # calendar
  else:
    lang = users[user_id][0]
    selected,date = tgcalendar.process_calendar_selection(lang,update, context)
    if selected:
      text = meal_of_day(date,lang)
      query.bot.send_message(chat_id=user_id, text=text, parse_mode="markdown")


def morning_routine():
  month = datetime.now(istanbul).month
  meals = fetch_meals()
  if (meals):
    db.update_meals(meals)
    translated_meals = translate_meals(meals)
    db.update_translations(translated_meals)
  else:
    meals = db.read_meals(texts.tr_month_names[month])


def translate_meals(meals, translated_meals):
  '''
  translate all meals, that arent translated yet
  '''
  unique_meals = list(set([item for sublist in meals["Öğle Yemeği"].values() for item in sublist]+[item for sublist in meals["Akşam Yemeği"].values() for item in sublist])) 
  to_translate = [k for k in unique_meals if k not in translated_meals.keys()]
  extra = translate_meal_list(to_translate)
  translated_meals.update(extra)
  return translated_meals

def toggle_auto_msg(update: Update, context: CallbackContext) -> None:
  '''
  toggle auto messaging
  '''
  user_id = update.message.from_user.id
  user = users[user_id]
  auto = 1 - user[1]
  users[user_id] = (user[0], auto, user[2])
  m = update.message.reply_text(texts.update[user[0]], parse_mode="markdown")
  db.update_user(user_id, user[0], auto, user[2])
  if (auto):
    m.edit_text(texts.auto_change_1[user[0]])
  else:
    m.edit_text(texts.auto_change_0[user[0]])

def info(update: Update, context: CallbackContext) -> None:
  ratings = [int(x[2]) for x in users.values() if int(x[2])!=0]
  total = len(ratings)
  frequencies = Counter(ratings)
  if (total != 0):
    rel_frequencies = [frequencies.get(1,0)/total, frequencies.get(2,0)/total, frequencies.get(3,0)/total ]
  else:
    rel_frequencies = [0,0,0]
  text = texts.get_info(users[update.message.from_user.id][0], len(users.keys()), rel_frequencies)
  update.message.reply_text(text)


def rating(update: Update, context: CallbackContext):
  id = update.message.from_user.id
  lang = users[id][0]
  r_text = texts.rating[lang]

  rating_markup = [
  [InlineKeyboardButton(f"{r_text[0]} 😍" , callback_data=3)],
  [InlineKeyboardButton(f"{r_text[1]} 🙂", callback_data=2)],
  [InlineKeyboardButton(f"{r_text[2]} ☹️", callback_data=1)]
  ]

  reply_markup = InlineKeyboardMarkup(rating_markup)
  update.message.reply_text(f"{texts.ask_for_rating[lang]}", reply_markup=reply_markup)


def feedback(update: Update, context: CallbackContext) -> int:

  update.message.reply_text(texts.ask_for_feedback[users[update.message.from_user.id][0]], reply_markup=ForceReply())



def feedback_reply (update: Update, context: CallbackContext) -> None:
  
  id = update.message.from_user.id
  lang = users[id][0]
  check = False
  try:
    check = update.message.reply_to_message.text==texts.ask_for_feedback[lang]
  except:
    pass

  if (check):
    # save feedback
    m = update.message.reply_text(texts.processing[lang])
    context.bot.send_message(chat_id=admin, text=f"Feedback von User {id} \n\n"+update.message.text, parse_mode="markdown")

    db.insert_feedback(id, update.message.text)

    context.bot.edit_message_text(chat_id=update.message.chat_id,
                              message_id=m.message_id, 
                              text=texts.thx_for_feedback[lang])

def location(update: Update, context: CallbackContext):
  id = update.message.from_user.id
  lang = users[id][0]
  campus = list(locations.keys())
  location_markup = [
  [InlineKeyboardButton(f"{campus[0]}" , callback_data='Kuzey (North)'),InlineKeyboardButton(f"{campus[1]}", callback_data='Güney (South)'),InlineKeyboardButton(f"{campus[2]}", callback_data='Hisar')],
  [InlineKeyboardButton(f"{campus[3]}", callback_data='Kandilli'), InlineKeyboardButton(f"{campus[4]}", callback_data='Sarıtepe')]
  ]


  reply_markup = InlineKeyboardMarkup(location_markup)
  update.message.reply_text(f"{texts.ask_for_location[lang]} 😊👇🏻", reply_markup=reply_markup)

def times(update: Update, context: CallbackContext):
  id = update.message.from_user.id
  lang = users[id][0]
  meals_markup = [
  [InlineKeyboardButton(f"{texts.mealtimes[lang][2]}" , callback_data='breakfast'),InlineKeyboardButton(f"{texts.mealtimes[lang][0]}", callback_data='lunch'),InlineKeyboardButton(f"{texts.mealtimes[lang][1]}", callback_data='diner')],  ]
  reply_markup = InlineKeyboardMarkup(meals_markup)
  update.message.reply_text(f"{texts.ask_for_meal[lang]} 😊👇🏻", reply_markup=reply_markup)

def lastMonth(today):
  first = today.replace(day=1)
  lastMonth = (first - timedelta(days=1)).month
  return lastMonth

def forward_all(update: Update, context: CallbackContext):
  if (not str(update.message.from_user.id)==admin):
    return 
  text = update.message.text.replace("/all2705", "")
  if (text):
    for id in users.keys():
      context.bot.send_message(chat_id=id, text=text.strip(), parse_mode="markdown")
      t.sleep(0.035)

def forward_one(update: Update, context: CallbackContext):
  if (not str(update.message.from_user.id)==admin):
    return 
  content = update.message.text.replace("/one2705", "")
  try:
    id, text = content.split(";")
    context.bot.send_message(chat_id=id.strip(), text=text.strip(), parse_mode="markdown")
  except:
    pass     

def morning(context: CallbackContext):
  
  today = datetime.now(istanbul)
  # get meals from yemek webpage
  meals = fetch_meals()
  if (meals):
    # update meals in db
    db.update_meals(meals)
    last_month_meals = db.read_meals(lastMonth(today))
    for key in meals.keys() and last_month_meals.keys():
      meals[key].update(last_month_meals[key])

  else:
    # if meals cant grabbed from webpage, get it from db (to be logged)
    meals = db.read_meals([lastMonth(today), today.month])
  
  translated_meals = db.read_translations()
  translated_meals = translate_meals(meals,translated_meals)
  db.update_translations(translated_meals)
  
    
  # send message to all users
  users_to_drop = []
  for id, val in users.items():
    if (val[1]==1):
      try:
        context.bot.send_message(chat_id=id, text=meal_of_day(datetime.now(istanbul), val[0]), parse_mode="markdown")
        t.sleep(0.035)
      except Exception as e:
        if (str(e)=="Forbidden: bot was blocked by the user"):
          users_to_drop.append(id)

  # drop users who blocked the bot  
  for id in users_to_drop:
    del users[id]
    db.delete_user(id)


if __name__ == "__main__":
  
  is_prod = os.environ.get('IS_HEROKU', None)

  if is_prod:
    #here goes all your heroku config
    token =  os.environ['TOKEN']
    admin = os.environ['admin_user_id']
  else:
    import config
    token = config.token
    admin = config.admin_user_id


  # get users from db  
  users = db.read_users()

  if (is_prod):
    # get meals from yemek webpage
    meals = fetch_meals()

    if (meals):
      # update meals in db
      db.update_meals(meals)

      # get meals from last month
      last_month_meals = db.read_meals(lastMonth(datetime.now(istanbul)))
      for key in meals.keys() and last_month_meals.keys():
        meals[key].update(last_month_meals[key])
    else:
      # if meals cant grabbed from webpage, get it from db (to be logged)
      meals = db.read_meals([lastMonth(datetime.now(istanbul)),datetime.now(istanbul).month])

    translated_meals = db.read_translations()
    translated_meals = translate_meals(meals,translated_meals)
    db.update_translations(translated_meals) 
  
  else:
    # test environment
    meals = db.read_meals([datetime.now(istanbul).month])
    if (not meals):
      meals = fetch_meals()
      db.update_meals(meals)
      translated_meals = db.read_translations()
      translated_meals = translate_meals(meals,translated_meals)
      db.update_translations(translated_meals)
    else: 
      translated_meals = db.read_translations() 



  updater = Updater(token)
  dispatcher = updater.dispatcher
  dispatcher.add_handler(CommandHandler("start", start))
  dispatcher.add_handler(CommandHandler("help", help))
  dispatcher.add_handler(CallbackQueryHandler(button))
  dispatcher.add_handler(CommandHandler("language", language))
  dispatcher.add_handler(CommandHandler("meals", cmeals))
  dispatcher.add_handler(CommandHandler("tomorrow",tomorrow))
  dispatcher.add_handler(CommandHandler("locations",location))
  dispatcher.add_handler(CommandHandler("times", times))
  dispatcher.add_handler(CommandHandler("calendar",calendar_handler))
  dispatcher.add_handler(CommandHandler("info",info))
  dispatcher.add_handler(CommandHandler("auto", toggle_auto_msg))
  dispatcher.add_handler(CommandHandler("rate", rating))
  dispatcher.add_handler(CommandHandler("contact", feedback))
  dispatcher.add_handler(CommandHandler("all2705", forward_all))
  dispatcher.add_handler(CommandHandler("one2705", forward_one))
  dispatcher.add_handler(MessageHandler(Filters.text, feedback_reply))
  updater.start_polling()
  jobs = updater.job_queue
  job_daily = jobs.run_daily(morning, days=(0, 1, 2, 3, 4, 5, 6), time=time(7,59,00, tzinfo=istanbul))

    
