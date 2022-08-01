from PIL import Image
import glob
import os

size = 64, 64

images_path = 'static/img/'
icons_path = 'static/icon/'

for file in glob.glob(os.path.join(images_path, '*.png')):
    with Image.open(file) as im:
        path, file = os.path.split(file)
        file, ext = os.path.splitext(file)
        if not os.path.exists(icons_path):
            os.makedirs(icons_path)
        im.thumbnail(size)
        im.save(os.path.join(icons_path, file + ".ico"), "ICO")
