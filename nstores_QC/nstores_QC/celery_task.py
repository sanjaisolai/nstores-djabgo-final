# myapp/tasks.py

from celery import shared_task
from . import image, fssai_detection
from requests.exceptions import ConnectionError, Timeout, HTTPError
import logging

@shared_task(bind=True, autoretry_for=(ConnectionError, Timeout), retry_kwargs={'max_retries': 5, 'countdown': 60})
def process_images_task(self, stored_json_data, is_packaged):
    try:
        not_fssai=[]
        image_url = []
        not_hd={}
        for i in range(1,len(stored_json_data)+1):
            image_url.append(stored_json_data[str(i)]['Image_Url'])
        
        total_images=len(image_url)
        processed=0
        j=1
        if is_packaged==1:
            for i in image_url:
                fssai_flag=0
                i=i.split(',')
                for x in i:
                    if not image.is_hd(x,j):
                        if image.broken==1:
                            continue
                        if j not in not_hd:
                            not_hd[j] = {}
                        if 'image_url' not in not_hd[j]:
                            not_hd[j]['image_url'] = []
                        not_hd[j]['image_url'].append(x)
                    else:
                        if fssai_flag==1:
                            continue
                        clas = fssai_detection.process_image(x)
                        if clas=='class1':
                            fssai_flag=1
                            continue
                        elif fssai_flag!=1 and i.index(x)==len(i)-1:
                            not_fssai.append(j)
                processed+=1
                progress=(processed/total_images)*100
                self.update_state(state='PROGRESS', meta={'progress': progress})
                j+=1
        else:
            for i in image_url:
                i=i.split(',')
                for x in i:
                    if not image.is_hd(x,j):
                        if image.broken==1:
                            continue
                        if j not in not_hd:
                            not_hd[j] = {}
                        if 'image_url' not in not_hd[j]:
                            not_hd[j]['image_url'] = []
                        not_hd[j]['image_url'].append(x)
                processed+=1
                progress=(processed/total_images)*100
                self.update_state(state='PROGRESS', meta={'progress': progress})
                j+=1
        return (not_hd,not_fssai,image.broken_links)
    
    except HTTPError as e:
 
        if e.response.status_code == 403:
            logging.error(f"403 Forbidden error: {e}")

            return "403 Forbidden error occurred"
        else:

            raise
    except Exception as e:
 
        logging.error(f"Error processing images: {e}")
        
        raise self.retry(exc=e)

