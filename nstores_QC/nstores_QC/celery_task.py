# myapp/tasks.py

from celery import shared_task
from . import image, fssai_detection

@shared_task
def process_images_task(stored_json_data,is_packaged):
    tup = image.hd(stored_json_data,is_packaged)
    non_hd = tup[0]
    not_fssai = tup[1]
    broken_links=tup[2]
    return (non_hd, not_fssai,broken_links)

# @shared_task
# def fssai_detection_task(good_images):
#     non_fssai = {}
#     for record, fields in good_images.items():
#         for field, url in fields.items():
#             for i in url:
#                 clas = fssai_detection.process_image(i)
#                 if clas == 'class2':
#                     if record not in non_fssai:
#                         non_fssai[record] = {}
#                     if 'image_url' not in non_fssai[record]:
#                         non_fssai[record]['image_url'] = []
#                     non_fssai[record]['image_url'].append(i)
#     return non_fssai
