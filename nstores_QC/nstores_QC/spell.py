import json
import re
import sqlite3
import enchant
from django.db import connection
def clean_word(word):
    return re.sub(r'[()\-]', '', word).lower()

def clean_long(word):
   
    pattern = r'^[^\w\d_]+|[^\w\d_]+$'
    
   
    cleaned_word = re.sub(r'_x000D_', '', word)
    
    
    cleaned_word = re.sub(pattern, '', cleaned_word)
    
    return cleaned_word.lower()

def spellc(data):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Words")
        tup = cursor.fetchall()
    words_to_skip = []
    for i in tup:
        words_to_skip.append(i[0])
    
    spell_en = enchant.Dict("en_IN")
    misspelled = {}
    json_data = data
    criteria=['Product_Name','Generic_Name','Category1','Sub_Category1']
    for i in range(1,len(json_data)+1):
        for j in criteria:
            words=json_data[str(i)][j].split()
            for word in words:
                word_lower = clean_word(word)
                if word_lower=='':
                    continue
                if word_lower not in words_to_skip and not spell_en.check(word_lower):
                    if i not in misspelled:
                            misspelled[i] = {}
                    if j not in misspelled[i]:
                            misspelled[i][j] = []
                    misspelled[i][j].append(word_lower)
    return misspelled
def spelllong(json_data):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Words")
        tup = cursor.fetchall()
    words_to_skip = []
    for i in tup:
        words_to_skip.append(i[0])
    spell_en = enchant.Dict("en_IN")
    misspelled_long={}
    criteria=['Description']
    for i in range(1,len(json_data)+1):
        for j in criteria:
            words=json_data[str(i)][j].split()
            for word in words:
                word_lower = clean_long(word)
                if word_lower=='':
                    continue
                if word_lower not in words_to_skip and not spell_en.check(word_lower):
                    if i not in misspelled_long:
                            misspelled_long[i] = {}
                    if j not in misspelled_long[i]:
                            misspelled_long[i][j] = []
                    misspelled_long[i][j].append(word_lower)
    return misspelled_long

