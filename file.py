from flask.blueprints import Blueprint
from PIL import Image

import os

file_blueprint = Blueprint("file", __name__, static_folder="./file", static_url_path="/")


def make_thumbnail(filename: str, force: bool = False):
    thumbnail_file = os.path.join("file", "thumbnail_data", filename)
    image_file = os.path.join("file", "image_data", filename)
    if force or not os.path.exists(thumbnail_file):
        try:
            print(thumbnail_file)
            image_file = Image.open(image_file)
            image_file.thumbnail((40, 40))
            image_file.save(thumbnail_file)
            return "/" + thumbnail_file.replace('\\', '/')
        except Exception as e:
            print(e)
            return None


def init_file():
    for f in os.listdir(os.path.join("file", "image_data")):
        make_thumbnail(f)


init_file()
