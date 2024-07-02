# myapp/tasks.py

from celery import shared_task
from . import image, fssai_detection
from requests.exceptions import ConnectionError, Timeout, HTTPError
import logging

@shared_task(bind=True, autoretry_for=(ConnectionError, Timeout), retry_kwargs={'max_retries': 5, 'countdown': 60})
def process_images_task(self, stored_json_data, is_packaged):
    try:
        tup = image.hd(stored_json_data, is_packaged)
        non_hd = tup[0]
        not_fssai = tup[1]
        broken_links = tup[2]
        return (non_hd, not_fssai, broken_links)
    except HTTPError as e:
        # Handle specific HTTP errors like 403
        if e.response.status_code == 403:
            logging.error(f"403 Forbidden error: {e}")
            # Handle the 403 error specifically without retrying
            return "403 Forbidden error occurred"
        else:
            # Re-raise other HTTP errors to trigger retry
            raise
    except Exception as e:
        # Log the error
        logging.error(f"Error processing images: {e}")
        # Explicitly raise the exception to trigger the retry
        raise self.retry(exc=e)

