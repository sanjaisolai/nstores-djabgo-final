from django.shortcuts import render
from urllib.parse import unquote
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
import pandas as pd
import numpy as np
from django.db import connection
from . import spell, First_Letter, length20
from .celery_task import process_images_task
from celery.result import AsyncResult
import logging
import requests
from PIL import Image
from io import BytesIO
import os

# from celery.app.control import Control
from celery import current_app
# control=Control()
stored_json_data = None
long_json = None
process_task_id = None
image_flag=0

def home(request):
    return JsonResponse({'hello':'This is the home url'})


    
@csrf_exempt
def upload(request, type, packaged):
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
                is_packaged=int(packaged)
                stored_json_data = json_data
                keys = stored_json_data['1'].keys()
                if 'Product_Name' not in keys:
                    return JsonResponse({'template':'Wrong Template pls Upload the correct one'})
                if process_task_id:
                    result = AsyncResult(process_task_id)
                    print(f"Current task state: {result.state}")
                    if result.state in ['PENDING', 'STARTED','PROGRESS']:
                        current_app.control.revoke(process_task_id, terminate=True)
                        print('dsf')

                process_task_id = process_images_task.delay(stored_json_data,is_packaged).id
                return JsonResponse({'template':'Upload Successful'})

            elif type == "long":
                long_json = json_data
                keys_long = long_json['1'].keys()
                if 'Description' not in keys_long:
                    return JsonResponse({'template':'Wrong Template pls Upload the correct one'})

                return JsonResponse({'template':'Upload Successful'})

        except Exception as e:
            return HttpResponse(str(e))



@csrf_exempt
def spellcheck(request, word):
    global stored_json_data

    if stored_json_data is None:
        return JsonResponse("<h1>NO excel file detected</h1><br><h2>PLS Go Back and upload the file to continue</h2>")

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
    print(misspelled)
    return JsonResponse(misspelled)

@csrf_exempt
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
    return JsonResponse(misspelled_long)

@csrf_exempt
def firstLetter(request):
    global stored_json_data

    if request.method == "GET":

        not_title = First_Letter.first(stored_json_data)
        return JsonResponse(not_title)
    
@csrf_exempt
def length(request):
    global stored_json_data

    if request.method == "GET":
        
        not_length = length20.length_not_20(stored_json_data)
        return JsonResponse(not_length)
    else:
        return HttpResponse("<h2>SOME ERROR HAS OCCURRED PLEASE TRY AGAIN</h2>")
@csrf_exempt
def image_quality(request):
    
    global image_flag
    if request.method == "GET":
        if not process_task_id:
            return JsonResponse({'response':0})
        else:
            return JsonResponse({'response':1})
@csrf_exempt      
def progress(request):
    
    if request.method=='GET':
        global process_task_id
        result = AsyncResult(process_task_id)
        if not result.ready():
            progress = round(result.info.get('progress', 0))
            return JsonResponse({'progress': progress})
        else:
            return JsonResponse({'progress': 100})
@csrf_exempt            
def display_image(request): #154s time taken for 50 images
    if request.method=='GET':
        global not_fssai
        result = AsyncResult(process_task_id)
        tup = result.result
        non_hd = tup[0]
        not_fssai = tup[1]
        broken_links=tup[2]
        print(non_hd)
        return JsonResponse({'wrong_image':non_hd,'wrong_urls':broken_links})
        # return render(request, 'image.html', {'wrong_words': non_hd,'wrong_urls':broken_links,'is_packaged':is_packaged})

@csrf_exempt
def fssai(request):    #354.73399999993853s time taken for 50 images
    if request.method=='GET':
        print(not_fssai)
        return JsonResponse(not_fssai)
@csrf_exempt
def add_image(request,url):
    if request.method == 'POST':
        try:
            data_dir='./nstores_QC/sample'
            decoded_url=unquote(url)
            response = requests.get(decoded_url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                img_path = os.path.join(data_dir, 'class', f'image_{hash(decoded_url)}.jpg')  
                img.save(img_path)
                print(f"Image saved to: {img_path}")
                return JsonResponse({'nothing':'nothing'})
            else:
                print(f"Failed to fetch image from URL: {url}, Status Code: {response.status_code}")
                JsonResponse({'nothing':'nothing'})
        except Exception as e:
            print(f"Error adding image from URL: {url}, Error: {str(e)}")
            JsonResponse({'nothing':'nothing'})