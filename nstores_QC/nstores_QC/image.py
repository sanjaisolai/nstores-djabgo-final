import requests
from PIL import Image
from io import BytesIO
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
        if width >= 720 and height >= 480:
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
def hd(data):
    good_images={}
    image_url = []
    not_hd={}
    for i in range(1,len(data)+1):
        image_url.append(data[str(i)]['Image_Url'])
    j=1
    for i in image_url:
        i=i.split(',')
        for x in i:
            if not is_hd(x,j):
                if broken==1:
                    continue
                if j not in not_hd:
                    not_hd[j] = {}
                if 'image_url' not in not_hd[j]:
                    not_hd[j]['image_url'] = []
                not_hd[j]['image_url'].append(x)
            else:
                if j not in good_images:
                    good_images[j] = {}
                if 'image_url' not in good_images[j]:
                    good_images[j]['image_url'] = []
                good_images[j]['image_url'].append(x)
        j+=1
    return (not_hd,good_images,broken_links)