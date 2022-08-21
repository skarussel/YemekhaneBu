from calendar import week
import re 

processing = {
      'en':
      "Processing...",
      'de':
      "Processing...",
      'tr':
      "işleme..."
}

registration = {
      'en':
      "Registration in progress...",
      'de':
      "Anmeldung läuft...",
      'tr':
      "Kayıt İşlemde..."
}

success = {
      'en':
      "Registration Successful✅",
      'de':
      "Registrierung erfolgreich✅",
      'tr':
      "Kayıt başarılı✅"
}

update = {
      'en':
      "Update in progress...",
      'de':
      "Aktualisierung läuft...",
      'tr':
      "Güncelleme devam ediyor..."
}

language_change = {
      'en':
      "Language changed successful ✅",
      'de':
      "Sprache erfolgreich umgestellt ✅",
      'tr':
      "Dil başarıyla değiştirildi ✅"
}

auto_change_1 = {
      'en':
      "Update successful ✅ I am happy to inform you every morning at 8:00 about the meals of the day ☺️",
      'de':
      "Update erfolgreich ✅ Ich freue mich dich jeden Morgen um 8:00 Uhr über die Mahlzeiten des Tages informieren zu dürfen ☺️",
      'tr':
      "Güncelleme başarılı ✅ Size her sabah saat 8:00'de günün öğünleri hakkında bilgi vermekten mutluluk duyarım ☺️"
}

auto_change_0 = {
      'en':
      "Update successful ✅ You wont recieve daily messages anymore 🙂",
      'de':
      "Update erfolgreich ✅ Du erhältst keine täglichen Benachrichtigungen mehr 🙂",
      'tr':
      "Güncelleme başarılı ✅ Günlük mesaj almayacaksın 🙂"
}

start_conv =  "Hoş geldin / Welcome / Herzlich Willkommen /name 😊"

ask_for_language = "Seninle hangi dilde konuşabilirim? / In which language may I speak with you? / In welcher Sprache möchtest du angesprochen werden? ☺"
welcome = {
      'en': 
      f'''*Welcome to the Bogazici Yemekhane Chatbot*
      
Nice to welcome you 🤗 I will inform you every day at 8:00 about daily meals in the canteen.

''', 

      'de': 
      f'''*Willkommen zum Bogazici Yemekhane Chatbot*
      
Schön dich begrüßen zu dürfen 🤗! Ich werde dich jeden Tag um 8:00 Uhr über die Gerichte in der Mensa informieren.

''',
      

      'tr': f'''*Boğaziçi Yemekhane Chatbot'a Hoş Geldiniz*
Hoş geldiniz 🤗 Her gün saat 8:00'de kantindeki yemekler hakkında sizi bilgilendireceğim.

'''}

help = {
'en':
'''You can control me by sending the commands below 👇🏻

*Get Meals*
/meals - meals of today 🍽️
/tomorrow - meals of tomorrow 🍽️
/calendar - meals of any day from calendar 📅

*Canteen* 
/times - shows opening hours of the canteens ⏱
/locations - shows locations of the canteens 📍

*Settings*
/language - change language 🌐
/auto - enable or disable receiving dishes of the day 💬

*Others*
/help - overview of commands ℹ️
/info - about me 📊
/rate - rate me ❤️ 
/contact - report problems, give feedback or share your own ideas on how to improve the bot 🤗


''',

'de': '''Du kannst mich durch die folgenden Befehle kontrollieren 👇🏻

*Gerichte*
/meals - Heutige Gerichte 🍽️
/tomorrow - Morgige Gerichte 🍽️
/calendar - Gerichte eines beliebigen Tages aus dem Kalender 📅

*Kantine* 
/times - Öffnungszeiten der Kantinen ⏱
/locations - Standorte der Kantinen 📍

*Einstellungen*
/language - Ändere die Sprache 🌐
/auto - Aktiviere oder deaktiviere automatische Benachrichtigungen über tägliche Gerichte 💬

*Sonstige*
/help - Überblick über meine Funktionen ℹ️
/info - Informationen über mich 📊
/rate - Bewerte mich ❤️
/contact - Teile deine eigenen Verbesserungsvorschläge, gib mir Feedback oder melde Probleme 🤗

''',
'tr': '''

*Bot Komutları*

*Menülere Erişmek  için*
/meals - Günün menüsü 🍽️
/tomorrow - Yarınki menü 🍽️
/calendar - Tarih seçerek o gün menüde ne olduğunu öğrenmek için 📅


*Yemekhane*
/times - Yemekhane açılış saatleri ⏱
/locations - Yemekhane konumları 📍

*Ayarlar* 
/language - Dil değiştir 🌐
/auto - Otomatik olarak günün menüsü telegram'a gelir. Eğer isterseniz bu otomatik mesajı iptal edebilirsiniz 💬

*Diğer*
/help - Bot komutlarını gösterir ℹ️
/info - Bot hakkında 📊
/rate - Botu değerlendir ❤️
/contact - sorunları bildirin, geri bildirim verin veya botu nasıl geliştireceğiniz konusunda kendi fikirlerinizi paylaşın 🤗

'''
}

mealtimes = {'de': ["Mittagessen", "Abendessen", "Frühstück"],
'tr': ["Öğle Yemeği","Akşam Yemeği", "Kahvaltı"],
'en': ["Lunch", "Dinner", "Breakfast"]
}

tr_months = ['','ocak', 'şubat','mart','nisan','mayıs','haziran','temmuz','ağustos','eylül','ekim','kasım','aralık'	
]

month_names = {'tr': [t.capitalize() for t in tr_months],
'en':  ['','January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
'de': ['','Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
}

weekday_names = {'tr': ['pazartesi','salı','çarşamba','perşembe','cumā','cumartesi','pazar' ],
'en':  ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'],
'de': ['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag']
}

weekday_shorts = {'tr': ['Pt','Sa','Çar','Per','Cu','Ct','Pa'],
'de': ["Mo","Di","Mi","Do","Fr","Sa","So"],
'en' : ["Mo","Tu","We","Th","Fr","Sa","Su"]}

not_available = {"de": "Die Gerichte für den sind noch nicht bekannt",
"en": "No meal is known yet for this date", 
"tr": "Bu tarih için henüz bir yemek bilinmiyor"}

want_feedback = {
      "de":"Möchtest du mir Verbesserungsvorschläge geben?",
      "en":"Do you want to give me Feedback?",
      "tr":""
}

feedback = { "y": {
      "de": "Bitte versende dein Feedback als Antwort auf diese Nachricht.",
      "en": "Please type in your feedback. Hint: In order to detect your feedback, it is important to reply to this message.",
      "tr": "Lütfen geri bildiriminizi yazın. İpucu: Geri bildiriminizi algılamak için bu mesajı yanıtlamanız önemlidir."
},
"n": {
      "de": "Vielleicht ein anderes Mal :)",
      "en": "Do you want to give me Feedback?",
      "tr": ""
}
}

ask_for_feedback = {
      "de":"Danke dass du dich entschieden hast, mit mir Kontakt aufzunehmen 😊. Hier kannst du mir Feedback und Verbesserungsvorschläge senden oder ein Problem melden. Sende dein Anliegen bitte als Antwort auf diese Nachricht👇🏻",
      "en":"Thank you for choosing to contact me 😊. Here you can send me feedback and suggestions for improvement or report a problem. Please send your request as a reply to this message👇🏻",
      "tr":"Benimle iletişime geçmeyi seçtiğiniz için teşekkür ederim 😊. Buradan bana geri bildirim ve iyileştirme önerileri gönderebilir veya bir sorunu bildirebilirsiniz. Lütfen isteğinizi bu mesaja cevap olarak gönderin👇🏻"
}

thx_for_feedback = {
      "de":"Dein Feedback wurde erfolgreich gespeichert ✅ Danke, dass du deine Erfahrungen mit mir geteilt hast ☺️🙌🏻",
      "en":"Your Feedback was saved successfully ✅ Thank you for sharing your experience with me ☺️🙌🏻",
      "tr":"Geri bildirim başarıyla kaydedildi ✅ tecrübeni benimle paylaştığın için teşekkür ederim ☺️🙌🏻"
}

ask_for_rating = {
      "de":"Wie bewertest du mich?",
      "en":"How do you rate my service?",
      "tr":"beni nasıl değerlendirirsin?"
}

rating = {
      "de": ["Fantastisch", "Okay", "Schlecht"],
      "en": ["Awesome", "Okay", "Bad"],
      "tr": ["Mükemmel", "Peki", "Kötü"]
}

rating_sucess = {
      "de":"Deine Bewertung wurde erfolgreich gespeichert ✅ Es wird höchstens eine Stimme pro Nutzer gespeichert. Das Gesamtergebnis kannst du unter /info sehen. Mit /contact kannst du Vorschläge machen, um mich zu verbessern.",
      "en":"Your rating was successfully saved ✅ A maximum of one vote per user is saved. You can view the overall result under /info. Use /contact to send additional feedback or suggestions to improve the bot.",
      "tr":"Derecelendirmeniz başarıyla kaydedildi ✅ Kullanıcı başına maksimum bir oy kaydedilir. Genel sonucu /info altında görüntüleyebilirsiniz. Botu geliştirmek için öneriler göndermek için /contact kullanın"
}

thx_for_rating = {
      "de":"Danke für deine Bewertung",
      "en":"Thanks for rating me",
      "tr":"puanın için teşekkürler"
}

yesno = {
      "de": ["Ja", "Nein"],
      "en": ["Yes", "No"],
      "tr": ["Evet", "Hayir"]
}

ask_for_location = {
      "de":"Wähle einen Campus aus der Liste",
      "en":"Select a campus from the list",
      "tr":"Listeden bir kampüs seçin"
}

campus = {
      "de" : "Campus",
      "en" : "Campus",
      "tr" : "Kampüsü"
}

ask_for_meal = {
      "de" : "Wähle eine Mahlzeit aus der Liste",
      "en" : "Choose a meal from the list",
      "tr" : "Listeden bir yemek seçin"

}

times = {"breakfast":
"""
*Weekdays*
Kuzey Kampüs  07:30 – 09:30
Güney Kampüs  07:30 – 09:30
Kilyos Kampüs  10:30 – 10:00
Kandilli Kampüs  07:30 - 09:30
Hisar Kampüs           -

*Weekends*
Kuzey Kampüs  08:30 – 10:00
Güney Kampüs  08:30 – 10:00
Kilyos Kampüs  08:00 – 10:30
Kandilli Kampüs  08:30 – 10:00
Hisar Kampüs         -
"""
,
      "lunch":
"""
*Weekdays*
Kuzey Kampüs	11:30 - 14:30
Güney Kampüs	12:15 - 14:30
Kilyos Kampüs	12:00 - 15:00
Kandilli Kampüs	11:30 - 14:30
Hisar Kampüs	11:30 - 14:30

*Weekends*
Kuzey Kampüs	12:00 - 13:45
Güney Kampüs	12:00 - 13:45
Kilyos Kampüs	12:00 - 13:45
Kandilli Kampüs	12:00 - 13:45
Hisar Kampüs	           –
""",
      "diner":
"""
*Weekdays*
Kuzey Kampüs	17:00 - 19:15
Güney Kampüs	17:00 - 19:15
Kilyos Kampüs	17:00 - 19:15
Kandilli Kampüs	17:00 - 19:15
Hisar Kampüs	      –

*Weekends*
Kuzey Kampüs	17:30 - 19:30
Güney Kampüs	17:30 - 19:30
Kilyos Kampüs	17:30 - 19:30
Kandilli Kampüs	17:30 - 19:30
Hisar Kampüs         -
"""

}

info = {
      "de": 
"""
Wir sind zurzeit num_user Nutzer 🙌🏻😍 Danke dass du dabei bist ☺️ 

Ihr habt wie folgt abgestimmt:
❤️ p3% 
🙂 p2% 
☹️ p1% 

Folgende Features sind geplant 📝 
- Zutaten der Gerichte  

Der Bot wurde im März 2022 von Steven Kocadag entwickelt 👨🏻‍💻 Wenn du Lust hast mitzuwirken, schick mir über /contact eine kurze Nachricht 😊💪🏻
""",

"en":
"""
We are currently num_user users 🙌🏻😍 Thanks for being here ☺️ 

You voted as follows:
❤️ p3% 
🙂 p2% 
☹️ p1% 

The following features are planned 📝 
- Ingredients of the dishes 

The bot was developed by Steven Kocadag during Spring 2022 👨🏻‍💻 If you want to contribute, send me a short message via /contact 😊💪🏻
""",
"tr":
"""
Şu anda num_user kullanıcısıyız 🙌🏻😍 Orada olduğunuz için teşekkürler ☺️

Aşağıdaki şekilde oy verdiniz:
❤️ p3%
🙂 p2%
☹️ p1%

Aşağıdaki özellikler planlanmıştır 📝
- Yemeklerin malzemeleri

Bot, Steven Kocadağ tarafından Mart 2022'de geliştirildi 👨🏻‍💻 Katkıda bulunmak isterseniz /iletişim yoluyla bana kısa bir mesaj gönderin 😊💪🏻
"""

}

weekday_end = {
      "de": ["Wochentage", "Wochenende"],
      "en": ["Weekdays", "Weekend"],
      "tr": ["hafta içi", "hafta sonu"]
}

def get_info(lang, num_of_users, probs):
      text = info[lang]
      text = text.replace("num_user", str(num_of_users))
      p1,p2,p3 = probs 
      text = text.replace("p1", str(int(p1*100)))
      text = text.replace("p2", str(int(p2*100)))
      text = text.replace("p3", str(int(p3*100)))
      return text 

def get_meal_times(lang, meal):
      if meal=="breakfast":
            präfix = mealtimes[lang][2]
      elif meal=="lunch":
            präfix = mealtimes[lang][0]
      else:
            präfix = mealtimes[lang][1]
      
      main = times[meal].replace("Weekdays", weekday_end[lang][0])
      main = main.replace("Weekends",weekday_end[lang][1])
      if (lang!="tr"):
            main = main.replace("Güney","South")
            main = main.replace("Kuzey","North")

      result_string = f"""
      *{präfix}*
      {main}
      """

      return result_string

def get_month_name(num, lang):
      return month_names[lang][num]

def get_month_num(month,lang):
      return month_names[lang].index(month)

def get_date_string(day,month,weekday,lang):
      if (lang=="tr"):
            return f"{day} {month_names[lang][month]}, {weekday_names[lang][weekday].capitalize()}" 
      return f"{weekday_names[lang][weekday]} {day}.{month_names[lang][month]}"

def get_weekday_shorts(lang):
      return weekday_shorts[lang]

def food_not_available(lang, date, today, meal_keys):

      date_pattern = re.compile(f"^[0-9]+\.{date.month}")
      meals_in_same_month = [ s for s in meal_keys if date_pattern.match(s)]
     
      if (meals_in_same_month):
            if (lang=="de"):
                  return f"Es gibt kein Essen am {date.day} {get_month_name(date.month,lang)} {date.year} 😔"
            elif (lang=="tr"):
                  return f"{date.day} {get_month_name(date.month,lang)} {date.year} kantin yemek servisi yapmayacaktır 😔"
            else: 
                  return f"There is no meal at {date.day} {get_month_name(date.month,lang)} {date.year} 😔"

      
      if (date.date()<today):
            if (lang=="de"):
                  return f"Der {date.day} {get_month_name(date.month,lang)} {date.year} liegt in der Vergangenheit. Ich weiß nicht mehr, was es an diesem Tag gab."
            elif (lang=="tr"):
                  return f"{date.day} {get_month_name(date.month,lang)} {date.year} geçmişte kaldı. o gün ne vardı hatırlamıyorum"
            else: 
                  return f"The {date.day} {get_month_name(date.month,lang)} {date.year} is in the past. I do not remember what there was that day"

      else:
            if (lang=="de"):
                  return f"Die Gerichte für den {date.day} {get_month_name(date.month,lang)} {date.year} sind noch nicht bekannt"
            elif (lang=="tr"):
                  return f"{date.day} {get_month_name(date.month,lang)} {date.year}'in yemekleri henüz bilinmiyor"
            else: 
                  return f"The dishes for {date.day} {get_month_name(date.month,lang)} {date.year} are not known yet"
            

      





