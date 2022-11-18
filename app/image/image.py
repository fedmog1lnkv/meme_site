import requests
import base64
from PIL import Image
import os
import json


# https://fedor223.imgbb.com/

def post_image(file_image):
    file_image = f"app/image/images_from_form/{file_image}"
    optimize_image(file_image)
    with open(file_image, "rb") as image:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": "676833e8ae2349f44aa08932c359446c",
            "image": base64.b64encode(image.read()),
            "name": file_image,
        }
        res = requests.post(url, payload)
    json_res = res.text
    os.remove(file_image)
    return get_url(json_res)


def optimize_image(file_image):
    remove_metadata(file_image)
    resize_image(file_image)


def resize_image(file_image):
    image = Image.open(file_image)
    dim = image.size
    image.save(file_image, optimize=True, quality=30)


def remove_metadata(file_image):
    print(file_image)
    image = Image.open(file_image)
    data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    image_without_exif.save(file_image)


def get_url(json_res):
    json_res2 = json.loads(json_res)
    print(json_res2)
    TypeOfVar = type(json_res2)
    if "dict" in str(TypeOfVar):
        data_response = json_res2.get('data')
        url = data_response.get('url')
    return url

