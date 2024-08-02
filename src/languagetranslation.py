import csv
import os
import shutil
from googletrans import Translator
import time
from datetime import datetime

def read_csv_phrases(file, unformatted_language, src_lang):
    with open(file) as file_obj:
        for line in file_obj:
            phrase = line.strip()
            if phrase:
                translated = translate(phrase, src_lang)
                print(translated)
                write_into_csv(unformatted_language, translated)

def write_into_csv(language, phrase):
    now = datetime.now()
    date = now.strftime("%Y_%m_%d_%H_%M")

    csvfile = f'./results/{date}_{language}_results.csv'
    with open(csvfile, 'a', newline='', encoding='utf-8') as file:
        writetocsv = csv.writer(file)
        writetocsv.writerow([phrase])

def translate(phrase, src_lang='auto', retries=3):
    translator = Translator(service_urls=['translate.google.com'])

    try:
        if src_lang == 'auto':
            detected_language = translator.detect(phrase)
            src_lang = detected_language.lang
            print(f"Detected language: {src_lang} with confidence {detected_language.confidence}")
        else:
            print(f"Using provided source language: {src_lang}")

        for attempt in range(retries):
            try:
                trans_phrase = translator.translate(phrase, dest='en', src=src_lang)
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(2)
                else:
                    print("All attempts failed.")

    except Exception as e:
        print(f"Error: {e}")

    return trans_phrase.text

def get_language_code(language):
    language_codes = {
        'amharic': 'am',
        'arabic': 'ar',
        'basque': 'eu',
        'bengali': 'bn',
        'english (uk)': 'en-GB',
        'portuguese (brazil)': 'pt-BR',
        'bulgarian': 'bg',
        'catalan': 'ca',
        'cherokee': 'chr',
        'croatian': 'hr',
        'czech': 'cs',
        'danish': 'da',
        'dutch': 'nl',
        'english (us)': 'en',
        'estonian': 'et',
        'filipino': 'fil',
        'finnish': 'fi',
        'french': 'fr',
        'german': 'de',
        'greek': 'el',
        'gujarati': 'gu',
        'hebrew': 'iw',
        'hindi': 'hi',
        'hungarian': 'hu',
        'icelandic': 'is',
        'indonesian': 'id',
        'italian': 'it',
        'japanese': 'ja',
        'kannada': 'kn',
        'korean': 'ko',
        'latvian': 'lv',
        'lithuanian': 'lt',
        'malay': 'ms',
        'malayalam': 'ml',
        'marathi': 'mr',
        'norwegian': 'no',
        'polish': 'pl',
        'portuguese (portugal)': 'pt-PT',
        'romanian': 'ro',
        'russian': 'ru',
        'serbian': 'sr',
        'chinese (prc)': 'zh-CN',
        'slovak': 'sk',
        'slovenian': 'sl',
        'spanish': 'es',
        'swahili': 'sw',
        'swedish': 'sv',
        'tamil': 'ta',
        'telugu': 'te',
        'thai': 'th',
        'chinese (taiwan)': 'zh-TW',
        'turkish': 'tr',
        'urdu': 'ur',
        'ukrainian': 'uk',
        'vietnamese': 'vi',
        'welsh': 'cy'
    }
    return language_codes[language]

if __name__ == "__main__":
    language = os.getenv('LANGUAGE')
    file_path = os.path.join('/logs', os.getenv('FILE_PATH'))

    print(f"Language: {language}")
    print(f"File Path: {file_path}")

    if not file_path:
        raise ValueError("No file path provided in the environment variable 'FILE_PATH'")

    language_code = get_language_code(language.lower())
    read_csv_phrases(file_path, language, src_lang=language_code)