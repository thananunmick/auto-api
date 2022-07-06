from __future__ import unicode_literals, print_function
#from aioflask import Flask, request, jsonify
from flask import Flask, request, jsonify 
#from quart import Quart, request, jsonify
import random
from pathlib import Path
import spacy
from tqdm import tqdm
from spacy.training import Example
from bs4 import BeautifulSoup
import requests
#from requests_html import AsyncHTMLSession
#import asyncio

app = Flask(__name__)
#app = Quart(__name__)
nlp = spacy.load('ner')
#session = AsyncHTMLSession()

def generate_keywords_from_url(url):
    #r = await session.get(url)
    #await r.html.arender()
    try:
        r = requests.get(url)
    except:
        return list()
    
    if (r.status_code / 100) % 10 != 2:
        return list()
    
#     print(r.html.text)
    
    #soup = BeautifulSoup(r.html.html, 'html.parser')
    soup = BeautifulSoup(r.text, 'html.parser')
    raw_text = soup.get_text()
    
#     print(raw_text)
    
    splitting_text = ""
    splitting_texts = ["Qualifications", "Qualities", "Responsibilities", "Who You Are", "Objectives", "Skills",
                       "We want to hear from you"]
    
    for text in splitting_texts:
        if text in raw_text:
            splitting_text = text
            break
            
#    print(splitting_text)
            
    if splitting_text != "":
        l = raw_text.split(splitting_text, 1)[1].split("\n")
    else:
        l = raw_text.split("\n")
        
    l_removed_empty = list(filter(lambda a: a != '' and a != ' ', l))
    l_strip = list()

    for text in l_removed_empty:
        l_strip.append(text.strip())
        
    unique_vocabs = dict()

    for text in l_strip:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.text not in unique_vocabs:
                unique_vocabs[ent.text] = 1
            else:
                unique_vocabs[ent.text] += 1
            
    return unique_vocabs

@app.route('/')
def hello_world():
	return 'This is my first API call!'

@app.route('/generate', methods=['POST'])
def generate_keywords():
	input_json = request.get_json(force=True)
	dict_to_return = dict()
	
	for company in input_json:
		dict_to_return[company] = generate_keywords_from_url(input_json[company])
		#dict_to_return[company] = await generate_keywords_from_url(input_json[company])
		#dict_to_return[company] = 5

	#print(dict_to_return)
	return jsonify(dict_to_return)

@app.route('/post', methods=["POST"])
def testpost():
	input_json = request.get_json(force=True)
	dictToReturn = {'text': input_json['text']}
	return jsonify(dictToReturn)


#if __name__ == "__main__":
#	app.run()
