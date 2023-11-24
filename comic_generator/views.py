from django.shortcuts import render
import requests

import io
import base64
from .utils import get_image

API_ENDPOINT = 'https://api.example.com/generate_comic'


def generate_comic(request):

    error, comic_images = None, []

    if request.method == 'POST':
        text_data = {}
        prompt = request.POST.get(f'prompt')
        print("Got prompt: ", prompt)
        error, comic_images = get_image(prompt)

    context = {}
    if error:
        context['error_message'] = error

    if comic_images:
        comic_image_base64 = None

        # Convert the image to base64 format
        comic_images_base64 = []
        for comic_image in comic_images:
            buffered = io.BytesIO()
            comic_image.save(buffered, format="PNG")
            comic_image_base64 = buffered.getvalue()
            comic_image_base64 = base64.b64encode(comic_image_base64).decode('utf-8')
            comic_images_base64.append(comic_image_base64)

        context['comic_images'] = comic_images_base64

    return render(request, 'comic_generator/generate_comic.html', context=context)
