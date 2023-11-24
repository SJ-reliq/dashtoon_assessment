import io
import json

import requests
from PIL import Image

config = {
    "API_TOKEN": "VknySbLLTUjbxXAXCjyfaFIPwUTCeRXbFSOjwRiCxsxFyhbnGjSFalPKrpvvDAaPVzWEevPljilLVDBiTzfIbWFdxOkYJxnOPoHhkkVGzAknaOulWggusSFewzpqsNWM"
}
API_URL = "https://xdwvg9no7pefghrn.us-east-1.aws.endpoints.huggingface.cloud"


headers = {
    "Accept": "image/png",
    "Authorization": f"Bearer {config['API_TOKEN']}",
    "Content-Type": "application/json"
}

def query(payload):
    print("Getting image")
    response = requests.post(API_URL, headers=headers, json=payload)
    print("Got image")
    if response.status_code == 200:
        return None, response.content
    else:
        return response.content, None


from concurrent.futures import ThreadPoolExecutor

def get_image(text):

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for idx in range(10):
            # payload = {
            #     "inputs": f"Create a comic strip having different arcs. Generate the {idx+1} arc of the story. {text}",
            # }
            payload = {
                "inputs": f"Main context is: '{text}'. All the images has to be in comic book style with dialoguebox and action",
            }
            # payload = {
            #     "inputs": text,
            # }

            futures.append(executor.submit(query, payload))

        images = []
        for future in futures:
            error, image_bytes = future.result()
            if error:
                return error, None
            
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)

    # images = []
    # for idx in range(10):
    #     payload = {
    #         "inputs": f"{text}. Create a 10 panel comic strip. Generate the {idx} panel.",
    #     }
    #     error, image_bytes = query(payload)
    #     if error:
    #         return error, None
        
    #     image = Image.open(io.BytesIO(image_bytes))
    #     images.append(image)

    return None, images
