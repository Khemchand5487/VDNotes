import json
from ibm_watson import LanguageTranslatorV3 # pip install --upgrade "ibm-watson>=4.5.0"
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('DpyP_gs5jyqY5V4Y5PyuLhlMe2BK3q6Y9PVuYzDzASK_')
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator)

language_dict=  {'arabic':'en-ar','bengali':'en-bn','bulgarian':'en-bg','czech':'en-cs','danish':'en-da','german':'en-de','greek':'en-el','spanish':'en-es','estonian':'en-et','finnish':'en-fi',
                'french':'en-fr','irish':'en-ga','gujarati':'en-gu','hebrew':'en-he','hindi':'en-hi','croatian':'en-hr','hungarian':'en-hu','indonesian':'en-id','italian':'en-it',
                'japanese':'en-ja','korean':'en-ko','lithuanian':'en-lt','latvian':'en-lv','malayalam':'en-ml','malay':'en-ms','maltese':'en-mt','nepali':'en-ne','norwegian bokmal':'en-nb',
                'dutch':'en-nl','polish':'en-pl','portuguese':'en-pt','romanian':'en-ro','russian':'en-ru','sinhala':'en-si','slovak':'en-sk','slovenian':'en-sl','swedish':'en-sv','tamil':'en-ta',
                'telugu':'en-te','thai':'en-th','turkish':'en-tr','ukrainian':'en-uk','urdu':'en-ur','vietnamese':'en-vi','chinese':'en-zh','traditional chinese':'en-zh-TW'
              }

language_translator.set_service_url('https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/29e5e230-99cb-4eb2-a8a4-9c9fb48c094a')

def translate(text, language):
    if language == "" or language == " ":
        return text
    language=language.lower()
    if language == "english":
        return text
    try:
        translation = language_translator.translate(
            text=text,
            model_id=language_dict[language]).get_result()
    except:
        print("There is an error!")
        raise ValueError("There is an error!")
    try:
        return translation["translations"][0]["translation"]
    except:
        raise ValueError("There is an error!")

# text = open("recognized.txt", "r")
# textfile = open("text.txt", "w+", encoding="utf-8")
# for i in text:
#     textfile.write(translate(i, "hindi"))
# textfile.close()
#print(translate(text, "hindi"))