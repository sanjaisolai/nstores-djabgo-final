from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import pandas as pd
import numpy as np
from django.db import connection
from . import spell, First_Letter, length20
from .celery_task import process_images_task
from celery.result import AsyncResult
import time
stored_json_data = None
long_json = None
process_task_id = None
image_flag=0
def home(request):
    return render(request, 'main.html', {'value': 'home','to_do':'upl'})

def upload(request, type):
    global stored_json_data
    global long_json
    global process_task_id
    global is_packaged
    if request.method == 'POST':
        if 'excel_file' not in request.FILES:
            return render(request, 'main.html')

        excel_file = request.FILES['excel_file']

        try:
            # Read Excel file into pandas DataFrame directly from memory
            df = pd.read_excel(excel_file)
            df = df.replace({np.nan: None})
            json_data = df.to_dict(orient='index')
            json_data = {str(key + 1): value for key, value in json_data.items()}

            if type == "raw":
                is_packaged=int(request.POST.get('packaged'))
                stored_json_data = json_data
                keys = stored_json_data['1'].keys()
                if 'Product_Name' not in keys:
                    return HttpResponse("<h1>Wrong Template Go back</h1>")

                process_task_id = process_images_task.delay(stored_json_data,is_packaged).id
                return render(request, 'main.html', {'value': 'upload','file':'long'})

            elif type == "long":
                long_json = json_data
                keys_long = long_json['1'].keys()
                if 'Description' not in keys_long:
                    return HttpResponse("<h1>Wrong Template Go back</h1>")

                return render(request, 'main.html', {'value': 'upload success'})

        except Exception as e:
            return HttpResponse(str(e))

    return render(request, 'main.html', {'value': 'upload','file':'master'})

def spellcheck(request, word):
    global stored_json_data

    if stored_json_data is None:
        return HttpResponse("<h1>NO excel file detected</h1><br><h2>PLS Go Back and upload the file to continue</h2>")

    if request.method == 'POST':
        word = word.replace("'", "''")
        # Connect to SQLite database and insert word if it doesn't exist
        query = f'''
        INSERT INTO Words (name)
        SELECT '{word}'
        WHERE NOT EXISTS (
            SELECT 1 FROM Words WHERE name = '{word}'
        );
        '''
        with connection.cursor() as cursor:
            cursor.execute(query)

    misspelled = spell.spellc(stored_json_data)
    return render(request, 'main.html', {'wrong_words': misspelled, 'value': 'spellcheck'})

def spellL(request, word):
    global long_json

    if request.method == 'POST':
        word = word.replace("'", "''")
        # Connect to SQLite database and insert word if it doesn't exist
        query = f'''
        INSERT INTO Words (name)
        SELECT '{word}'
        WHERE NOT EXISTS (
            SELECT 1 FROM Words WHERE name = '{word}'
        );
        '''
        with connection.cursor() as cursor:
            cursor.execute(query)

    misspelled_long = spell.spelllong(long_json)
    return render(request, 'longspell.html', {'wrong_words': misspelled_long, 'value': 'longsp'})

def firstLetter(request):
    global stored_json_data

    if request.method == "POST":

        not_title = First_Letter.first(stored_json_data)
        return render(request, 'First_Letter.html', {'wrong_words': not_title})
    else:
        return HttpResponse("<h2>SOME ERROR HAS OCCURRED PLEASE TRY AGAIN</h2>")

def length(request):
    global stored_json_data

    if request.method == "POST":
        
        not_length = length20.length_not_20(stored_json_data)
        return render(request, 'length.html', {'wrong_words': not_length})
    else:
        return HttpResponse("<h2>SOME ERROR HAS OCCURRED PLEASE TRY AGAIN</h2>")

def image_quality(request):
    
    global image_flag
    if request.method == "POST":
        if not process_task_id:
            return HttpResponse("<h1>No task found</h1>")
        
        
        return render(request, 'image_processing.html')
        
def progress(request):
    global stored_json_data
    global not_fssai
    global process_task_id
    if request.method=='POST':
        result = AsyncResult(process_task_id)
        if not result.ready():
            progress = round(result.info.get('progress', 0))
            return JsonResponse({'progress': progress})
        else:
            return JsonResponse({'progress': 100})
            
def display_image(request):
    global not_fssai
    result = AsyncResult(process_task_id)
    tup = result.result
    non_hd = tup[0]
    not_fssai = tup[1]
    broken_links=tup[2]
    print(broken_links)
    return render(request, 'image.html', {'wrong_words': non_hd,'wrong_urls':broken_links,'is_packaged':is_packaged})

def fssai(request):
    if request.method == "POST":
        return render(request, 'fssai.html', {'wrong_words': not_fssai})
