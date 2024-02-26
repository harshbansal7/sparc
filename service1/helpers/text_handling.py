#text_handling.py
import os
from dotenv import load_dotenv
import requests

import spacy
from spacy.language import Language
from spacy_language_detection import LanguageDetector

import uuid

import langid

global nlp_model

def get_lang_detector(nlp, name):
    return LanguageDetector()

nlp_model = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp_model.add_pipe('language_detector', last=True)

load_dotenv()

def get_complaint_language(input):
    doc = nlp_model(str(input))
    language = doc._.language
    if language["language"] in ['hi', 'en', 'pa']:
        return language["language"]
    else:
        com_lang, conf = langid.classify(input)
        if com_lang in ['ms', 'sw']:
            return 'hi'

    return 'oth'

def translate_complaint(input, fromlang = None):
    path = 'translate?api-version=3.0'
    params = "&to=en"

    if fromlang in ['hi', 'pa']:
        params= f"&to=en&from={fromlang}"

    constructed_url = os.getenv("TRANSLATOR_TEXT_ENDPOINT") + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': os.getenv("TRANSLATOR_TEXT_SUBSCRIPTION_KEY"),
        'Ocp-Apim-Subscription-Region': os.getenv("TRANSLATOR_TEXT_REGION"),
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': str(input)
    }]

    request = requests.post(constructed_url, headers = headers, json=body)

    response = request.json()
    output = response[0]['translations'][0]['text']

    return str(output)
    