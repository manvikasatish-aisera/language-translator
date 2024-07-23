import csv
import requests
from dotenv import load_dotenv
import os

def read_csv_phrases(filepath):
    with open(filepath) as file_obj: 
        reader_obj = csv.reader(file_obj)  
        for row in reader_obj:
            for phrase in row:
                # translated = translate(phrase)
                # write_into_csv(translated)
                print(phrase)

def write_into_csv(phrase, csvfile):
    csvfile = './results/results.csv'
    with open(csvfile, 'a', newline='') as file:
        writetocsv = csv.writer(file)
        writetocsv.writerow(phrase)

def translate(phrase, language):
    load_dotenv()

    api_url = "https://agw.golinguist.com/linguistnow/resources/v1/translate"
    api_key = os.getenv('GO_LINGUIST_API_KEY')

    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "sourceContent": phrase,
        "sourceLocale": "en",
        "targetLocale": "fr", # language_code(language)
        "contentTypeName": "api",
        "translationType": "machine",
        "textType": "html",
        "evaluateQuality": True
    }

    # Make the POST request
    response = requests.post(api_url, headers=headers, json=payload)

    # Check the response status
    if response.status_code == 200:
        # Parse the JSON response
        translated_data = response.json()
        print("Translated Text:", translated_data["translatedText"])
        print("Translation ID:", translated_data["translationId"])
        print("Word Count:", translated_data["wordCount"])
        print("Below Quality Target:", translated_data["belowQualityTarget"])
        return translated_data["translatedText"]
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def language_code(language):
    return "fr" # temp, language codes are 
    # https://support.languageio.com/hc/en-us/articles/18984338183949-Language-codes-in-API-requests-and-responses#AC 

translate("hello", "fr")