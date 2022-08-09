from deep_translator import GoogleTranslator
from yemek import fetch_meals




def translate_meal_list(unique_meals):
    
    tr_en= GoogleTranslator(source='tr', target='en')
    tr_de= GoogleTranslator(source='tr', target='de')
    
    translated_meals = {}

    for meal in unique_meals:
            en = tr_en.translate(meal)
            de = tr_de.translate(meal)
            translated_meals[meal] = [en,de]
    return translated_meals



    
def translate_word(word):
    tr_en= GoogleTranslator(source='tr', target='en')
    tr_de= GoogleTranslator(source='tr', target='de')

    en = tr_en.translate(word)
    de = tr_de.translate(word)

    return [en,de]


def translate_list(words):
    tr_en= GoogleTranslator(source='tr', target='en')
    tr_de= GoogleTranslator(source='tr', target='de')

    en = []
    de= []

    for word in words:
        en.append(tr_en.translate(word))
        de.append(tr_de.translate(word))
    
    return [en,de]
    

    


    



