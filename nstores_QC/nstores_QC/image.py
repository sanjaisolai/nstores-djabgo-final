import requests
from PIL import Image
from io import BytesIO
from . import fssai_detection
broken_links=[]
def is_hd(image_url,j):
    global broken_links
    global broken
    broken=0
    try:
        # Download the image from URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for bad response status

        # Open the image from the downloaded content
        img = Image.open(BytesIO(response.content))

        # Check image dimensions
        width, height = img.size
        if width >= 720 and height >= 380:
            return True
        else:
            return False

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        broken_links.append(j)
        broken=1
        return False
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        broken=1
        broken_links.append(j)
        return False
    except Exception as err:
        print(f"Error occurred: {err}")
        broken=1
        broken_links.append(j)
        return False

    